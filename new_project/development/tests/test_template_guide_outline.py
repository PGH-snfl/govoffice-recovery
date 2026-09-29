import json
import unittest

import test_template_topic_analysis as topic_tests
from govoffice.services.document_authoring import make_prompt,topic_guide_text
from govoffice.services.authoring_research import make_research_prompt
from govoffice.services.authoring_commands import AuthoringCommands


def paragraph(text):return '<P><TEXT><CHAR>'+text+'</CHAR></TEXT></P>'


FORM='<HWPML><BODY><SECTION>'+''.join(paragraph(t) for t in [
    '1. 첫 대주제','1-1. 같은 이름','____','1-2. 같은 이름','____','2. 다른 대주제','2-1. 같은 이름','____'])+\
    '<P><TEXT><TABLE><ROW><CELL><PARALIST>'+''.join(paragraph(t) for t in [
    '작성 요령','전체 공통 규칙','첫 대주제 규칙','소주제 A 전용','소주제 B 전용','다른 대주제 전용'])+\
    '</PARALIST></CELL></ROW></TABLE></TEXT></P></SECTION></BODY></HWPML>'


class OutlineTests(unittest.TestCase):
    setUp=topic_tests.TopicAnalysisTests.setUp
    register=topic_tests.TopicAnalysisTests.register

    def prepare(self):
        original=self.agent.generate
        def mapping(prompt,schema,cancel):
            data=json.loads(prompt.split('\n',1)[1]);response=original(prompt,schema,cancel)
            if data['mode']=='headings':
                for row,target in zip(response['items'],data['targets']):
                    row.update(accepted=True,chapter_anchor=0 if target['text'].startswith('1') else 5)
            else:
                links={'첫 대주제 규칙':[0],'소주제 A 전용':[1],'소주제 B 전용':[3],'다른 대주제 전용':[6]}
                for row,block in zip(response['items'],data['targets']):
                    row.update(scope='common',topic_anchors=[],assignments=[dict(paragraph_indices=[p['index']],
                        topic_anchors=links[p['text']],scope='topic') for p in block['paragraphs'] if p['text'] in links])
            return response
        self.agent.generate=mapping
        return self.register(FORM)

    def test_result_contains_only_hierarchy_and_original_instructions(self):
        m=self.prepare();tree=m['guide_outline']
        self.assertEqual([0,5],[c['index'] for c in tree['chapters']])
        self.assertEqual([1,3],[c['index'] for c in tree['chapters'][0]['subtopics']])
        self.assertEqual([6],[c['index'] for c in tree['chapters'][1]['subtopics']])
        self.assertEqual([],tree['unassigned_indices'])
        encoded=json.dumps(tree,ensure_ascii=False)
        for forbidden in ('fields','reason','writable','body','personal','____'):
            self.assertNotIn(forbidden,encoded)
        self.assertEqual(3,sum(len(t['fields']) for t in m['topics']))

    def test_writer_gets_current_child_parent_rules_and_common_only(self):
        m=self.prepare();folder=self.registry.path(m['id'])
        for index,wanted,unwanted in [(1,'소주제 A 전용','소주제 B 전용'),(3,'소주제 B 전용','소주제 A 전용')]:
            topic=next(t for t in m['topics'] if t['start']==index)
            prompt=make_prompt(folder,m,topic,{'title':'가상 주제','description':'설명'}, {})
            self.assertIn(wanted,prompt);self.assertNotIn(unwanted,prompt)
            self.assertIn('첫 대주제 규칙',prompt);self.assertNotIn('다른 대주제 전용',prompt)
            self.assertEqual(1,prompt.count('전체 공통 규칙'))
        other=next(t for t in m['topics'] if t['start']==6)
        prompt=make_prompt(folder,m,other,{}, {})
        self.assertNotIn('첫 대주제 규칙',prompt);self.assertIn('다른 대주제 전용',prompt)

    def test_research_also_uses_same_current_topic_rules(self):
        m=self.prepare();folder=self.registry.path(m['id']);topic=next(t for t in m['topics'] if t['start']==1)
        prompt=make_research_prompt(folder,m,topic,{},[])
        self.assertIn('소주제 A 전용',prompt);self.assertNotIn('소주제 B 전용',prompt)
        self.assertNotIn('다른 대주제 전용',prompt);self.assertEqual(1,prompt.count('전체 공통 규칙'))

    def test_common_is_not_duplicated_in_topic_payload(self):
        m=self.prepare()
        for topic in m['topics']:
            self.assertNotIn('전체 공통 규칙',topic_guide_text(self.registry.path(m['id']),topic))
        first=m['guide_outline']['chapters'][0]
        self.assertNotIn('소주제 A 전용',json.dumps(first['instructions'],ensure_ascii=False))

    def test_outline_read_endpoint_and_overview_are_read_only(self):
        m=self.prepare();commands=AuthoringCommands(self.folder/'app');self.addCleanup(commands.close)
        commands.service.registry=self.registry
        before=(self.registry.path(m['id'])/'manifest.json').read_bytes()
        result=commands.handle({'action':'authoring_guide_outline','template_id':m['id']})
        self.assertEqual(m['guide_outline'],result['outline'])
        listing=commands.handle({'action':'authoring_overview'})['templates'][0]
        self.assertTrue(listing['has_guide_outline']);self.assertNotIn('guide_outline',listing)
        self.assertEqual(before,(self.registry.path(m['id'])/'manifest.json').read_bytes())


if __name__=='__main__':unittest.main()
