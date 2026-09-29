import unittest
import xml.etree.ElementTree as ET
from govoffice.services.template_guide_registration import bind_local_slots,partition_guided_reviews


def p(text=''):
    return '<P><TEXT><CHAR>'+text+'</CHAR></TEXT></P>'


class LocalSlotsTests(unittest.TestCase):
    def bind(self, xml, headings, unassigned=()):
        root=ET.fromstring('<HWPML><BODY><SECTION>'+xml+'</SECTION></BODY></HWPML>')
        ps=list(root.iter('P'))
        outline={'chapters':[{'index':i,'title':''.join(ps[i].itertext()),
            'instructions':[{'index':g,'text':''.join(ps[g].itertext())} for g in guides],
            'subtopics':[]} for i,guides in headings], 'common_instructions':[], 'unassigned_indices':list(unassigned)}
        before=ET.tostring(root)
        m=bind_local_slots(root,outline)
        self.assertEqual(before,ET.tostring(root),'Local mapping changed source')
        return m

    def test_duplicate_unnumbered_titles_keep_separate_instructions(self):
        m=self.bind(p('추진 계획')+p('첫 요령')+p('____')+p('추진 계획')+p('둘째 요령')+p('____'),[(0,[1]),(3,[4])])
        self.assertEqual([0,3],[t['start'] for t in m['topics']])
        self.assertEqual([['첫 요령'],['둘째 요령']],[[r['text'] for r in t['instructions']] for t in m['topics']])
        self.assertEqual([2,5],[f['index'] for t in m['topics'] for f in t['fields']])

    def test_same_cell_heading_and_empty_body_are_supported(self):
        table='<P><TEXT><TABLE><ROW><CELL><PARALIST>'+p('추진 계획')+p('작성 안내')+p()+'</PARALIST></CELL></ROW></TABLE></TEXT></P>'
        m=self.bind(table,[(1,[2])])
        field=m['topics'][0]['fields'][0]
        self.assertEqual(3,field['index']);self.assertTrue(field['in_table'])

    def test_guide_padding_excluded_and_numeric_cells_require_facts(self):
        numeric='<P><TEXT><TABLE><ROW><CELL RowAddr="0" ColAddr="0"><PARALIST>'+p('금액')+'</PARALIST></CELL><CELL RowAddr="0" ColAddr="1"><PARALIST>'+p()+'</PARALIST></CELL></ROW></TABLE></TEXT></P>'
        guide='<P><TEXT><TABLE><ROW><CELL><PARALIST>'+p('작성 요령')+p('요령 원문')+p('____')+'</PARALIST></CELL></ROW></TABLE></TEXT></P>'
        m=self.bind(p('추진 계획')+p('____')+numeric+guide,[(0,[6,7])])
        self.assertEqual([1,4],[f['index'] for t in m['topics'] for f in t['fields']])
        self.assertEqual('factual_cell',m['topics'][0]['fields'][1]['kind'])
        self.assertEqual([6,7],m['clear_guide_indices'])

    def test_unattached_guides_are_kept_without_common_classification(self):
        m=self.bind(p('별도 안내')+p('추진 계획')+p('____'),[(1,[])],[0])
        self.assertEqual([],m['common_instructions'])
        self.assertEqual([{'index':0,'text':'별도 안내'}],m['unassigned_instructions'])
        self.assertNotIn(0,m['clear_guide_indices'])

    def test_ambiguous_spacers_need_no_user_choice_when_safe_body_anchor_exists(self):
        manifest={'topics':[{'id':'s0003','start':3,'fields':[{'index':3,'role':'body','insert_after':True}]}]}
        reviews=[{'index':4,'topic_index':3,'table_index':None},
                 {'index':5,'topic_index':3,'table_index':None},
                 {'index':6,'topic_index':3,'table_index':2}]
        actionable,covered=partition_guided_reviews(manifest,reviews)
        self.assertEqual([6],[x['index'] for x in actionable])
        self.assertEqual([4,5],covered)

    def test_parent_heading_without_own_field_is_not_reported_as_manual_topic(self):
        root=ET.fromstring('<HWPML><BODY><SECTION>'+p('1. 연구개발')+
                           p('1-1. 연구 내용')+p('____')+'</SECTION></BODY></HWPML>')
        outline={'chapters':[{'index':0,'title':'1. 연구개발','instructions':[],
            'subtopics':[{'index':1,'title':'1-1. 연구 내용','instructions':[],
                          'subtopics':[]}]}],'unassigned_indices':[]}
        manifest=bind_local_slots(root,outline)
        self.assertEqual([],manifest['manual_topics'])


if __name__=='__main__':unittest.main()
