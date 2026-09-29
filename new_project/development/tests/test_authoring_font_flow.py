import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

from test_authoring_font_profiles import fixture
from test_authoring_output_polish import p, cell, table, manifest
from govoffice.services.authoring_font_profiles import flowing_font_profiles
from govoffice.services.document_authoring import render_draft
from govoffice.services.authoring_cell_budget import attach_cell_budgets
from govoffice.services.authoring_policy import prepare_new_job


def document(content):
    _,root,_=fixture()
    section=root.find('BODY/SECTION')
    section.clear()
    for child in ET.fromstring('<ROOT>'+content+'</ROOT>'):section.append(child)
    return root


def flow_manifest(root,indices,guides=()):
    m=manifest(root,indices,guides)
    m['render_policy']['flowing_content_fonts']=True
    return m


def identity(shape):
    return shape.find('FONTID').get('Hangul'),shape.get('Height')


class FontFlowTests(unittest.TestCase):
    def test_empty_table_uses_its_original_input_font(self):
        root=document(p('1. 제목',shape='3')+p('기존 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p(shape='0'))]))+p(shape='2'))
        m=flow_manifest(root,[1,3,4]);profiles=flowing_font_profiles(root,m)
        self.assertEqual([('2','1200'),('1','1000'),('2','1200')],
                         [identity(profiles['by_field'][f'P{i:04d}']) for i in [1,3,4]])

    def test_existing_table_input_font_is_used_for_all_written_cells(self):
        root=document(p('1. 제목',shape='3')+p('기존 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p('기존 값',shape='0'))+cell(p(shape='1'))])))
        m=flow_manifest(root,[1,3,4]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0003']))
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0004']))
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            output,logs=render_draft(folder,m,{},local_values={'P0003':'변경 값','P0004':'새 값'})
        rendered=ET.fromstring(output);ps=list(rendered.iter('P'))
        shapes={s.get('Id'):s for s in rendered.iter('CHARSHAPE')}
        for entry in logs:
            shape=shapes[ps[entry['output_index']].find('TEXT').get('CharShape')]
            self.assertEqual(('1','1000'),identity(shape))

    def test_explicit_table_font_wins_over_existing_input(self):
        root=document(p('표 안 글꼴: 휴먼명조 12pt')+
                      p(controls=table([cell(p('기존 값',shape='0'))+cell(p(shape='0'))])))
        profiles=flowing_font_profiles(root,flow_manifest(root,[2,3],guides=[0]))
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0002']))
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0003']))

    def test_insert_after_heading_does_not_set_table_input_font(self):
        root=document(p('기존 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p('1. 표 소제목',shape='3')+p('기존 값',shape='0'))])))
        m=flow_manifest(root,[2,3])
        m['topics'][0]['fields'][0]['insert_after']=True
        profiles=flowing_font_profiles(root,m)
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0002']))
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0003']))

    def test_real_body_change_persists_through_tables_and_empty_slots(self):
        root=document(p('1. 제목',shape='3')+p('처음 본문 내용입니다.',shape='1')+p(shape='2')+
                      p('변경된 본문 내용입니다.',shape='0')+p(shape='1')+
                      p(controls=table([cell(p(shape='2'))]))+p(shape='1'))
        m=flow_manifest(root,[1,2,3,4,6,7]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0002']))
        for i in [3,4,6,7]:self.assertEqual(('1','1000'),identity(profiles['by_field'][f'P{i:04d}']))

    def test_explicit_table_instruction_does_not_leak_to_next_table_or_body(self):
        root=document(p('1. 제목')+p('처음 본문 내용입니다.',shape='1')+p('표 안 글꼴: 돋움 10pt')+
                      p(controls=table([cell(p(shape='1'))]))+p(shape='2')+
                      p(controls=table([cell(p(shape='0'))])))
        m=flow_manifest(root,[1,4,5,7],guides=[2]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0004']))
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0005']))
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0007']))

    def test_table_prose_format_is_local_and_labels_are_ignored(self):
        root=document(p('1. 제목')+p('본문 양식 내용입니다.',shape='1')+
                      p(controls=table([cell(p('표에 들어가는 고정 항목입니다.',shape='2'))+
                                       cell(p('기존 표 내용입니다.',shape='0')+p(shape='1'))]))+p(shape='2'))
        m=flow_manifest(root,[1,4,5,6]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('1','1000'),identity(profiles['by_field']['P0005']))
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0006']))

    def test_heading_guide_and_blank_style_do_not_change_body(self):
        root=document(p('1. 제목')+p('본문의 내용입니다.',shape='1')+p('2. 소제목 변경',shape='3')+
                      p('자료를 구체적으로 작성합니다.',shape='0')+p(shape='2'))
        m=flow_manifest(root,[1,4],guides=[3]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0004']))

    def test_literal_body_directive_and_multiple_scopes_in_one_line(self):
        root=document(p('본문 글꼴: 휴먼명조 12pt; 표 안 글꼴: 돋움 9pt')+
                      p(shape='2')+p(controls=table([cell(p(shape='1'))]))+
                      p('본문 글꼴: 돋움 11pt')+p(shape='1'))
        m=flow_manifest(root,[1,3,5],guides=[0,4]);profiles=flowing_font_profiles(root,m)
        self.assertEqual(('2','1200'),identity(profiles['by_field']['P0001']))
        self.assertEqual(('1','900'),identity(profiles['by_field']['P0003']))
        self.assertEqual(('1','1100'),identity(profiles['by_field']['P0005']))

    def test_render_and_budget_resolve_per_field_not_group_cache(self):
        root=document(p('1. 제목')+p('처음 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p(shape='0'))]))+
                      p('변경된 본문 내용입니다.',shape='0')+p(shape='1'))
        m=flow_manifest(root,[1,3,4,5]);attach_cell_budgets(root,m)
        self.assertEqual(1000,m['topics'][0]['fields'][1]['table_fit']['font_height'])
        values={f['id']:'대체한 내용입니다.\n다음 문단입니다.' for f in m['topics'][0]['fields']}
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            # Offline replay preserves contents even when a small table expands.
            for f in m['topics'][0]['fields']:
                if 'table_fit' in f:f['table_fit']['offline_replay']=True
            output,log=render_draft(folder,m,{'s':{'topic_id':'s','values':values,'needs_review':[]}})
        rendered=ET.fromstring(output);ps=list(rendered.iter('P'));shapes={s.get('Id'):s for s in rendered.iter('CHARSHAPE')}
        for entry in log:
            expected=('2','1200') if entry['field_id']=='P0001' else ('1','1000')
            for i in entry['output_indices']:self.assertEqual(expected,identity(shapes[ps[i].find('TEXT').get('CharShape')]))

    def test_default_policy_uses_flow_and_turns_off_global_uniformity(self):
        m={'topics':[]};prepare_new_job(m)
        self.assertTrue(m['render_policy']['flowing_content_fonts'])
        self.assertFalse(m['render_policy']['uniform_content_fonts'])

    def test_font_name_containing_another_font_name_is_not_ambiguous(self):
        root=document(p('본문 글꼴: 함초롬돋움 11pt')+p(shape='1'))
        for face in root.iter('FONTFACE'):
            ET.SubElement(face,'FONT',{'Id':'9','Name':'함초롬돋움'})
        profiles=flowing_font_profiles(root,flow_manifest(root,[1],guides=[0]))
        self.assertEqual(('9','1100'),identity(profiles['by_field']['P0001']))

    def test_table_subheading_keeps_following_text(self):
        root=document(p('1. 제목')+p('원래 본문 내용입니다.',shape='1')+
                      p(controls=table([cell(p(shape='0'))])))
        m=flow_manifest(root,[3])
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'source.hwpml').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')
            output,log=render_draft(folder,m,{},local_values={'P0003':'4. 단계별 시험\n시험 내용입니다.'})
        rendered=ET.fromstring(output);ps=list(rendered.iter('P'));shapes={s.get('Id'):s for s in rendered.iter('PARASHAPE')}
        self.assertEqual('true',shapes[ps[log[0]['output_indices'][0]].get('ParaShape')].get('KeepWithNext'))
        self.assertEqual('false',shapes[ps[log[0]['output_indices'][1]].get('ParaShape')].get('KeepWithNext'))


if __name__=='__main__':unittest.main()
