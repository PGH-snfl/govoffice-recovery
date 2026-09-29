"""Generate a synthetic typography/table example using existing form styles."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET
from uuid import uuid4

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from govoffice.services.document_authoring import render_draft,own_text,write_json
from govoffice.adapters.hwp_form_export import export_generated_hwp
from govoffice.adapters.hwp_template_import import extract_hwp


def run(source_folder, output_parent, long_table=False, fit_table=False, paragraph_table=False):
    fit_table=fit_table or paragraph_table
    source_folder=Path(source_folder).resolve();output=Path(output_parent).resolve()/('readable_'+uuid4().hex[:8])
    output.mkdir(parents=True)
    root=ET.fromstring((source_folder/'source.hwpml').read_text(encoding='utf-8'))
    original_ps=list(root.iter('P'))
    front=deepcopy(root.find('BODY/SECTION/P'))
    tables=[t for t in root.iter('TABLE') if 2<=len(t.findall('ROW'))<=3
            and t.get('ColCount')=='2' and len(t.findall('ROW/CELL'))<=6
            and all(int(c.get('Width','0'))>=4000 for c in t.findall('ROW/CELL'))]
    table=deepcopy(min(tables,key=lambda t:len(ET.tostring(t))))
    # Two ordinary rows; the source's merged, page-high signature row is not
    # part of this synthetic text-overflow fixture.
    row_model=next(row for row in table.findall('ROW') if len(row.findall('CELL'))==2)
    rows=[deepcopy(row_model),deepcopy(row_model)]
    for row in list(table.findall('ROW')):table.remove(row)
    for n,row in enumerate(rows):
        for cell in row.findall('CELL'):
            cell.attrib.update(RowAddr=str(n),RowSpan='1',Height='2131',Header='false')
        table.append(row)
    table.attrib.update(RowCount='2',RepeatHeader='false')
    table.find('SHAPEOBJECT/SIZE').set('Height','4262')
    if fit_table:
        for n,row in enumerate(rows):
            for cell in row.findall('CELL'):cell.set('Height',('16000' if paragraph_table else '7200') if n==0 else '2500')
        table.find('SHAPEOBJECT/SIZE').set('Height','18500' if paragraph_table else '9700')
    saved=json.loads((source_folder/'manifest.json').read_text(encoding='utf-8'))
    model=next(original_ps[f['index']] for t in saved['topics'] for f in t['fields']
               if f.get('role')!='personal' and not f.get('in_table') and original_ps[f['index']].find('TEXT') is not None)
    def paragraph(value):
        p=ET.Element('P',{k:v for k,v in model.attrib.items() if k in {'ParaShape','Style'}})
        t=ET.SubElement(p,'TEXT',dict(model.find('TEXT').attrib));ET.SubElement(t,'CHAR').text=value
        return p
    body=root.find('BODY');body.clear();section=ET.SubElement(body,'SECTION',{'Id':'0'})
    section.append(front)
    heading=paragraph('1. 본문 문단 검증');section.append(heading)
    slot=paragraph('____');section.append(slot)
    section.append(paragraph('1-1. 표 입력 검증'))
    container=paragraph('');container.find('TEXT').append(table);section.append(container)
    table_slots=[]
    for n,row in enumerate(table.findall('ROW')):
        cells=row.findall('CELL')
        for col,cell in enumerate(cells):
            paralist=cell.find('PARALIST')
            for child in list(paralist):paralist.remove(child)
            p=paragraph(('실행 계획' if n==0 else '확인 금액') if col==0 else '____')
            paralist.append(p)
            if col==1:table_slots.append(p)
    added=paragraph('1-2. 양식에 없던 본문 문단');section.append(added)
    ps=list(root.iter('P'));index={id(p):i for i,p in enumerate(ps)}
    def field(p,table=False,insert=False):
        i=index[id(p)]
        return {'id':f'P{i:04d}','index':i,'original':own_text(p),'label':'금액' if table and p is table_slots[-1] else '검증 입력',
                'role':'body','context':'예제','in_table':table,'max_chars':3000,
                'multiline':True,'insert_after':insert}
    fields=[field(slot),*(field(p,True) for p in table_slots),field(added,insert=True)]
    fields[-2]['kind']='factual_cell'
    manifest={'paragraph_count':len(ps),'topics':[{'id':'test','title':'서식 검증','start':index[id(heading)],'fields':fields}],
              'render_policy':{'readable_body':True,'blue_review':True,'preserve_layout':True}}
    values={fields[0]['id']:'첫 번째 문단은 연구 목표와 추진 방향을 설명합니다.\n\n두 번째 문단은 검증 절차와 기대 효과를 설명합니다.',
            fields[-1]['id']:'원래 양식에 본문 칸이 없어 새로 만든 문단입니다.\n\n예산은 확인 필요합니다.'}
    for n,f in enumerate(fields[1:-1]):
        values[f['id']]='자료 정리 후 검증 실행' if n==0 else '1,200,000'
        if long_table and n==0:
            values[f['id']]='\n\n'.join(f'{i+1}. 자료를 정리하고 검증 절차를 실행합니다. 결과를 분석하여 실행 계획을 보완합니다. '
                                      '확정된 결과는 기록합니다. 이후 다음 절차를 진행합니다. [확인 필요: 금액 확정]' for i in range(18))
    if fit_table:
        from govoffice.services.authoring_cell_budget import attach_cell_budgets,CellContentTooLong
        from govoffice.services.document_authoring import validate_result
        attach_cell_budgets(root,manifest)
        too_long={**values,fields[1]['id']:'불필요하게 긴 설명을 반복하여 작성합니다. '*15}
        try:validate_result(manifest['topics'][0],{'topic_id':'test','values':too_long,'needs_review':[]})
        except CellContentTooLong:pass
        else:raise AssertionError('oversized table content was not rejected')
        values[fields[1]['id']]='자료 정리·검증\n(확인 필요: 협의)'
        if paragraph_table:
            values[fields[1]['id']]='자료를 수집하고 항목별로 정리합니다.\n정리한 자료를 비교하여 검증합니다.\n(확인 필요: 검증 기준 협의)\n- 결과를 대조하고 누락 항목을 확인한 뒤 검증 기록을 정리합니다.'
        write_json(output/'셀별분량.json',{f['id']:f['table_fit'] for f in fields if f.get('table_fit')})
    (output/'source.hwpml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode'),encoding='utf-8')
    xml,logs=render_draft(output,manifest,{'test':{'topic_id':'test','values':values,'needs_review':[]}})
    (output/'작성중.hml').write_text(xml,encoding='utf-8');write_json(output/'입력필드.json',logs)
    target=output/'문단_표_파란검토표시_검증.hwp'
    result=export_generated_hwp(source_folder/'template.hwp',output/'작성중.hml',target)
    extract_hwp(target,output/'저장후검증.hml')
    actual=ET.fromstring((output/'저장후검증.hml').read_text(encoding='utf-8'))
    aps=list(actual.iter('P'));expected=ET.fromstring(xml);eps=list(expected.iter('P'))
    ashapes={s.get('Id'):s for s in actual.iter('CHARSHAPE')};eshapes={s.get('Id'):s for s in expected.iter('CHARSHAPE')}
    for entry in logs:
        for i,value in zip(entry['output_indices'],entry['paragraph_values']):
            assert own_text(aps[i])==value
            def styled_chars(p,shapes):
                out=[]
                for t in p.findall('TEXT'):
                    s=shapes[t.get('CharShape')]
                    style=(s.get('TextColor'),s.get('Height'),
                           tuple(sorted(s.find('CHARSPACING').attrib.items())) if s.find('CHARSPACING') is not None else (),
                           tuple(sorted(s.find('RATIO').attrib.items())) if s.find('RATIO') is not None else ())
                    out.extend((ch,style) for c in t.findall('CHAR') for ch in ''.join(c.itertext()))
                return out
            assert styled_chars(aps[i],ashapes)==styled_chars(eps[i],eshapes),('character styles',i)
    aparas={s.get('Id'):s for s in actual.iter('PARASHAPE')};eparas={s.get('Id'):s for s in expected.iter('PARASHAPE')}
    for a,e in zip(actual.iter('CELL'),expected.iter('CELL')):
        assert a.get('Width')==e.get('Width')
        if fit_table:assert a.get('Height')==e.get('Height'),('cell grew',a.attrib,e.attrib)
        for ap,ep in zip(a.findall('PARALIST/P'),e.findall('PARALIST/P')):
            assert aparas[ap.get('ParaShape')].get('Align')==eparas[ep.get('ParaShape')].get('Align')
            am=aparas[ap.get('ParaShape')].find('PARAMARGIN');em=eparas[ep.get('ParaShape')].find('PARAMARGIN')
            for k in ('Left','Right','Indent','Prev','Next','LineSpacing','LineSpacingType'):
                assert am.get(k)==em.get(k),('paragraph margin',k,am.attrib,em.attrib)
    if long_table:
        assert result['pages']>=2,result
        # HWPML retains the authored minimum height even after visual reflow.
        assert all(t.get('PageBreak')=='Cell' for t in actual.iter('TABLE'))
    import subprocess
    pdf=target.with_suffix('.pdf')
    subprocess.run([sys.executable,'-X','utf8',__file__,'--pdf',str(target),str(pdf)],check=True,timeout=50,
                   creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    result.update(file=str(target),reopened_values_and_color_verified=True)
    if fit_table:result.update(cell_dimensions_preserved=True,oversized_body_rejected=True,summary_source='synthetic_test')
    if paragraph_table:result.update(paragraph_spacing_and_list_indent_verified=True)
    write_json(output/'검증결과.json',result)
    print(json.dumps(result,ensure_ascii=False))


def pdf_preview(source,destination):
    import tempfile
    import shutil
    from govoffice.adapters.com_worker_cache import configure_worker_cache
    with tempfile.TemporaryDirectory(prefix='govoffice_layout_pdf_') as temp:
        configure_worker_cache(Path(temp)/'gen_py')
        from govoffice.adapters.recovered_hwp import 복구한글어댑터
        copied=Path(temp)/'owned.hwp';shutil.copy2(source,copied)
        adapter=복구한글어댑터()
        try:
            adapter.관리문서열기(copied,표시=False)
            assert adapter.원본.대상.SaveAs(str(Path(destination).resolve()),'PDF','') is not False
            assert Path(destination).stat().st_size>1000
        finally:
            if adapter.문서상태().get('managed'):adapter.관리문서닫기(저장여부=False)


if __name__=='__main__':
    if sys.argv[1]=='--pdf':pdf_preview(*sys.argv[2:4])
    else:run(*sys.argv[1:3],long_table='--long-table' in sys.argv,fit_table='--fit-table' in sys.argv,paragraph_table='--paragraph-table' in sys.argv)
