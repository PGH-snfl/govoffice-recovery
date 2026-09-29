import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_output_polish import OutputPolisher, own
from govoffice.services.document_authoring import render_draft
from govoffice.services.authoring_policy import prepare_new_job
from govoffice.services.authoring_validation import audit_layout


def p(text='', controls='', shape='0'):
    return f'<P ParaShape="0" Style="0"><TEXT CharShape="{shape}"><CHAR>{text}</CHAR>{controls}</TEXT></P>'


def cell(content, height=2000):
    return f'<CELL Height="{height}" Width="24000" RowSpan="1"><PARALIST>{content}</PARALIST></CELL>'


def table(rows, height=2000):
    return (f'<TABLE><SHAPEOBJECT><SIZE Height="{height}"/><POSITION TreatAsChar="true"/></SHAPEOBJECT>'
            + ''.join('<ROW>'+row+'</ROW>' for row in rows) + '</TABLE>')


def source(body):
    return ('<HWPML><HEAD><CHARSHAPELIST Count="2">'
            '<CHARSHAPE Id="0" Height="300" TextColor="16711680"><FONTID Hangul="2"/><BOLD/><ITALIC/></CHARSHAPE>'
            '<CHARSHAPE Id="1" Height="1100" TextColor="0"><FONTID Hangul="2"/></CHARSHAPE>'
            '</CHARSHAPELIST><PARASHAPELIST Count="1"><PARASHAPE Id="0" Align="Left">'
            '<PARAMARGIN LineSpacingType="Percent" LineSpacing="160"/></PARASHAPE></PARASHAPELIST></HEAD>'
            '<BODY><SECTION>'+body+'</SECTION></BODY></HWPML>')


def manifest(root, indices=(), guides=()):
    ps=list(root.iter('P'))
    return {'paragraph_count':len(ps), 'clear_guide_indices':list(guides),
            'render_policy':{'readable_body':True,'polished_output':True,'review_memos':True},
            'topics':[{'id':'s','start':0,'title':'연구','fields':[
                {'id':f'P{i:04d}','index':i,'original':own(ps[i]),'max_chars':1000,'role':'body','multiline':True}
                for i in indices]}]}


class PolishTests(unittest.TestCase):
    def test_generated_body_normalized_without_mutating_heading_or_source_font(self):
        xml=source(p('1. 목표')+p(''))
        root=ET.fromstring(xml);m=manifest(root,[1])
        result={'s':{'topic_id':'s','values':{'P0001':'본문 첫 문단\n본문 둘째 문단'},'needs_review':[]}}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(xml,encoding='utf-8')
            output,log=render_draft(folder,m,result)
            self.assertEqual(xml,(folder/'source.hwpml').read_text(encoding='utf-8'))
        r=ET.fromstring(output);ps=list(r.iter('P'));shapes={s.get('Id'):s for s in r.iter('CHARSHAPE')}
        self.assertEqual('0',ps[0].find('TEXT').get('CharShape'))
        for i in log[0]['output_indices']:
            s=shapes[ps[i].find('TEXT').get('CharShape')]
            self.assertEqual('1100',s.get('Height'));self.assertEqual('0',s.get('TextColor'))
            self.assertIsNone(s.find('BOLD'));self.assertIsNone(s.find('ITALIC'))
            self.assertEqual('2',s.find('FONTID').get('Hangul'))
        self.assertEqual([],audit_layout(output,log)['issues'])
        paras={s.get('Id'):s for s in r.iter('PARASHAPE')}
        self.assertEqual('true',paras[ps[0].get('ParaShape')].get('KeepWithNext'))

    def test_removes_whole_explicit_guide_but_preserves_bound_guide_table(self):
        for bound in (False,True):
            r=ET.fromstring(source(p(controls=table([cell(p('작성 요령')+p('설명'))]))))
            ps=list(r.iter('P'));m=manifest(r,[2] if bound else [],[1,2])
            polisher=OutputPolisher(r,ps,m)
            for i in m['clear_guide_indices']:
                ps[i].find('TEXT/CHAR').text=''
            polisher.finish([],{})
            self.assertEqual(1 if bound else 0,len(list(r.iter('TABLE'))))

    def test_removes_guide_table_when_label_follows_header_paragraphs(self):
        guide=table([cell(p('구분')+p('내용'))+cell(p('작성요령')+p('작성 기준'))])
        r=ET.fromstring(source(p(controls=guide)+p('1. 본문')+p()))
        ps=list(r.iter('P'));m=manifest(r,guides=[4])
        polisher=OutputPolisher(r,ps,m)
        ps[4].find('TEXT/CHAR').text=''
        polisher.finish([],{})
        self.assertEqual([],list(r.iter('TABLE')))
        self.assertEqual(0,audit_layout(ET.tostring(r,encoding='unicode'),[])['remaining_guide_tables'])

    def test_removes_nested_example_not_a_real_input_table(self):
        nested=table([cell(p('알고리즘 인식률'))])
        r=ET.fromstring(source(p(controls=table([cell(p('(예) 성능 예시')+p(controls=nested))]))))
        ps=list(r.iter('P'));m=manifest(r,guides=[1])
        o=OutputPolisher(r,ps,m);o.finish([],{})
        self.assertEqual(1,len(list(r.iter('TABLE'))))
        self.assertNotIn('알고리즘 인식률',''.join(r.itertext()))

    def test_example_drawing_removed_and_row_height_released(self):
        drawing='<CONTAINER><DRAWTEXT>'+p('Wibro 모듈 설치')+'</DRAWTEXT></CONTAINER>'
        r=ET.fromstring(source(p('※ 다음 예시 (예 : Wibro)')+p(controls=table([
            cell(p('1차년도'),33000)+cell(p(controls=drawing),33000)],33000))))
        ps=list(r.iter('P'));o=OutputPolisher(r,ps,manifest(r,guides=[0]));o.finish([],{})
        self.assertIsNone(r.find('.//CONTAINER'))
        self.assertTrue(all(int(c.get('Height'))<=4000 for c in r.iter('CELL')))
        self.assertIn('1차년도',''.join(r.itertext()))

    def test_oversized_wrapper_unwrapped_and_table_can_flow(self):
        inner=table([cell(p('내용'),70000)],70000)
        r=ET.fromstring(source(p(controls='<SECDEF/>'+table([cell(p(controls=inner))],72000))))
        ps=list(r.iter('P'));o=OutputPolisher(r,ps,manifest(r));o.finish([],{})
        self.assertIsNotNone(r.find('.//SECDEF'))
        self.assertEqual(1,len(list(r.iter('TABLE'))))
        self.assertEqual('false',r.find('.//TABLE/SHAPEOBJECT/POSITION').get('TreatAsChar'))
        self.assertEqual('Cell',r.find('.//TABLE').get('PageBreak'))

    def test_mirror_summary_title_even_with_same_label_in_research_history(self):
        cover=table([cell(p('연구개발과제명'))+cell(p('국문'))+cell(p()),
                     cell(p('사업명'))+cell(p('사업명'))+cell(p('기존 다른 사업'))])
        summary=table([cell(p('요 약 문')),cell(p('연구개발과제명'))+cell(p()),
                       cell(p('사업명'))+cell(p())])
        r=ET.fromstring(source(p(controls=cover)+p(controls=summary)+p('경력 과제')))
        ps=list(r.iter('P'));text=[own(x) for x in ps]
        title_idx=text.index('연구개발과제명',4)+1;business_idx=text.index('사업명',9)+1
        m=manifest(r,[title_idx,business_idx,len(ps)-1])
        for f,label in zip(m['topics'][0]['fields'],['연구개발과제명','사업명','연구개발과제명']):f['label']=label
        o=OutputPolisher(r,ps,m)
        refs=[];fields={}
        for index,value in [(title_idx,'새 과제'),(business_idx,'')]:
            field_id=f'P{index:04d}'
            refs.append(({'field_id':field_id,'value':value},[ps[index]],[value]))
        o.finish(refs,fields)
        self.assertEqual('새 과제',own(ps[3]))
        self.assertEqual('사업명',own(ps[5]))
        self.assertEqual('',own(ps[6]))
        self.assertEqual('경력 과제',own(ps[-1]))

    def test_policy_enables_polishing_for_new_jobs(self):
        m={'topics':[]};prepare_new_job(m)
        self.assertTrue(m['render_policy']['polished_output'])

    def test_removing_guides_reindexes_later_values(self):
        xml=source(p(controls=table([cell(p('작성 요령')+p('안내 내용'))]))+p('1. 본문')+p())
        root=ET.fromstring(xml);m=manifest(root,[4],[1,2])
        result={'s':{'topic_id':'s','values':{'P0004':'저장된 본문'},'needs_review':[]}}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(xml,encoding='utf-8')
            output,log=render_draft(folder,m,result)
        self.assertEqual([],audit_layout(output,log)['issues'])
        self.assertLess(log[0]['output_index'],4)
        self.assertNotIn('<TABLE',output)

    def test_design_protected_guide_is_not_removed(self):
        r=ET.fromstring(source(p(controls=table([cell(p('작성 요령')+p('제목 디자인'))]))))
        ps=list(r.iter('P'));m=manifest(r,guides=[1,2]);m['protected_design_indices']=[2]
        o=OutputPolisher(r,ps,m);o.finish([],{})
        self.assertEqual(1,len(list(r.iter('TABLE'))))
        self.assertEqual('제목 디자인',own(ps[2]))


if __name__=='__main__':unittest.main()
