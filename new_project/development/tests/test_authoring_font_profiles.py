import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_font_profiles import document_font_profiles, font_group
from govoffice.services.document_authoring import render_draft
from govoffice.services.authoring_cell_budget import attach_cell_budgets
from test_authoring_output_polish import p, cell, table, manifest


def fixture():
    fonts = ('<FACENAMELIST><FONTFACE Lang="Hangul"><FONT Id="1" Name="돋움"/>'
             '<FONT Id="2" Name="휴먼명조"/></FONTFACE><FONTFACE Lang="Latin">'
             '<FONT Id="5" Name="돋움"/><FONT Id="8" Name="휴먼명조"/>'
             '<FONT Id="3" Name="Other Latin"/></FONTFACE></FACENAMELIST>')
    shapes = ''.join(f'<CHARSHAPE Id="{i}" Height="{size}" TextColor="0"><FONTID Hangul="{font}" Latin="3"/>'
                     f'<CHARSPACING Hangul="{spacing}" Latin="{spacing}"/>{extra}</CHARSHAPE>'
                     for i, size, font, spacing, extra in [
                         (0, 1000, 1, 0, ''), (1, 1200, 2, 0, ''),
                         (2, 300, 1, -9, '<BOLD/><ITALIC/>'), (3, 1500, 1, -8, '<BOLD/>')])
    xml = ('<HWPML><HEAD>'+fonts+'<CHARSHAPELIST Count="4">'+shapes+'</CHARSHAPELIST>'
           '<PARASHAPELIST Count="1"><PARASHAPE Id="0"><PARAMARGIN LineSpacingType="Percent" LineSpacing="150"/>'
           '</PARASHAPE></PARASHAPELIST></HEAD><BODY><SECTION>'+p('제목', shape='3')+
           p(shape='1')+p(shape='1')+p(shape='2')+
           p(controls=table([cell(p('표 고정 항목', shape='3'))+cell(p(shape='0')),
                            cell(p(shape='0'))+cell(p(shape='2'))]))+'</SECTION></BODY></HWPML>')
    root=ET.fromstring(xml);ps=list(root.iter('P'))
    indices=[i for i,x in enumerate(ps) if i in (1,2,3) or (i>4 and not ''.join(x.itertext()).strip())]
    m=manifest(root,indices);m['render_policy']['uniform_content_fonts']=True
    m['topics'][0]['fields'][-1]['role']='personal'
    return xml,root,m


class FontProfileTests(unittest.TestCase):
    def test_separate_profiles_and_language_specific_ids(self):
        _,root,m=fixture();profiles=document_font_profiles(root,m)
        self.assertEqual('2',profiles['body'].find('FONTID').get('Hangul'))
        self.assertEqual('8',profiles['body'].find('FONTID').get('Latin'))
        self.assertEqual('1',profiles['table'].find('FONTID').get('Hangul'))
        self.assertEqual('5',profiles['table'].find('FONTID').get('Latin'))
        self.assertEqual('1200',profiles['body'].get('Height'))
        self.assertEqual('1000',profiles['table'].get('Height'))

    def test_render_uniform_including_personal_cells_but_not_fixed_labels(self):
        xml,root,m=fixture();before=ET.tostring(root)
        fields=m['topics'][0]['fields']
        results={'s':{'topic_id':'s','values':{f['id']:'본문 ABC 123\n둘째 문단' for f in fields},'needs_review':[]}}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(xml,encoding='utf-8')
            output,log=render_draft(folder,m,results)
        rendered=ET.fromstring(output);ps=list(rendered.iter('P'));parents={id(c):p for p in rendered.iter() for c in p}
        shapes={s.get('Id'):s for s in rendered.iter('CHARSHAPE')};signatures={'table':set(),'body':set()}
        for e in log:
            for index in e['output_indices']:
                para=ps[index];group=font_group(para,parents)
                for run in para.findall('TEXT'):
                    s=shapes[run.get('CharShape')]
                    signatures[group].add((s.get('Height'),ET.tostring(s.find('FONTID')),ET.tostring(s.find('CHARSPACING'))))
                    self.assertIsNone(s.find('BOLD'));self.assertIsNone(s.find('ITALIC'))
        self.assertEqual({'table':1,'body':1},{k:len(v) for k,v in signatures.items()})
        fixed=[x for x in ps if ''.join(x.itertext()) in ('제목','표 고정 항목')]
        self.assertEqual(2,len(fixed))
        self.assertTrue(all(x.find('TEXT').get('CharShape')=='3' for x in fixed))
        self.assertEqual(before,ET.tostring(root))

    def test_profile_choice_does_not_depend_on_partial_response(self):
        xml,_,m=fixture();f=m['topics'][0]['fields'][2]
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(xml,encoding='utf-8')
            output,log=render_draft(folder,m,{},local_values={f['id']:'사용자 본문'})
        r=ET.fromstring(output);ps=list(r.iter('P'));s=next(s for s in r.iter('CHARSHAPE')
            if s.get('Id')==ps[log[0]['output_index']].find('TEXT').get('CharShape'))
        self.assertEqual('2',s.find('FONTID').get('Hangul'))
        self.assertEqual('1200',s.get('Height'))

    def test_cell_budget_uses_same_font_height_as_output(self):
        _,root,m=fixture();attach_cell_budgets(root,m)
        budgets=[f['table_fit'] for t in m['topics'] for f in t['fields'] if f.get('table_fit')]
        self.assertTrue(budgets)
        self.assertTrue(all(x['font_height']==1000 for x in budgets))

    def test_empty_document_and_missing_face_list_are_safe(self):
        self.assertEqual({},document_font_profiles(ET.fromstring('<HWPML/>'),{'topics':[]}))
        _,root,m=fixture();root.find('HEAD').remove(root.find('.//FACENAMELIST'))
        self.assertEqual('2',document_font_profiles(root,m)['body'].find('FONTID').get('Hangul'))

    def test_generated_subheading_stays_with_prose_after_font_change(self):
        xml,_,m=fixture();field=m['topics'][0]['fields'][0]
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(xml,encoding='utf-8')
            output,log=render_draft(folder,m,{},local_values={field['id']:'5. 위험 대응 및 확장 필요사항\n설명 본문'})
        root=ET.fromstring(output);ps=list(root.iter('P'));shapes={s.get('Id'):s for s in root.iter('PARASHAPE')}
        self.assertEqual('true',shapes[ps[log[0]['output_indices'][0]].get('ParaShape')].get('KeepWithNext'))
        self.assertEqual('false',shapes[ps[log[0]['output_indices'][1]].get('ParaShape')].get('KeepWithNext'))


if __name__=='__main__':unittest.main()
