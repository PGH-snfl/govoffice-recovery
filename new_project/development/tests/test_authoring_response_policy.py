import unittest

from govoffice.services.authoring_response_policy import normalize_response,prose_field


class AuthoringResponsePolicyTests(unittest.TestCase):
    def test_prose_inside_table_keeps_written_content(self):
        topic={'fields':[{'id':'P0001','label':'최종 목표','role':'body','in_table':True}]}
        response={'values':{'P0001':'작성된 목표입니다.\n\n[확인 필요: 확정 기간]\n\n연구 방법도 작성했습니다.'},
                  'needs_review':[]}
        normalize_response(topic,response,{'P0001':29572})
        self.assertIn('작성된 목표입니다.',response['values']['P0001'])
        self.assertIn('연구 방법도 작성했습니다.',response['values']['P0001'])
        self.assertIn('[확인 필요]',response['values']['P0001'])
        self.assertNotIn('확정 기간',response['values']['P0001'])

    def test_factual_cell_discards_unverified_draft(self):
        topic={'fields':[{'id':'P0002','label':'세계 시장 규모','role':'body','in_table':True}]}
        response={'values':{'P0002':'[확인 필요: 공식 수치]\n\n임시 추정 시장 규모를 계산했다.'},
                  'needs_review':[]}
        normalize_response(topic,response,{'P0002':9809})
        self.assertEqual('확인 필요',response['values']['P0002'])

    def test_outside_table_prose_and_personal_value(self):
        topic={'fields':[{'id':'P0003','label':'기술 동향','role':'body','in_table':False},
                         {'id':'P0004','label':'기관명','role':'personal','in_table':True}]}
        response={'values':{'P0003':'실제 본문입니다.','P0004':'서울과학기술대학교'},
                  'needs_review':['P0003: 근거 확인 필요']}
        normalize_response(topic,response,{'P0004':5000})
        self.assertEqual('실제 본문입니다.\n\n[확인 필요]',response['values']['P0003'])
        self.assertEqual('서울과학기술대학교',response['values']['P0004'])

    def test_large_yearly_plan_cell_is_prose(self):
        self.assertTrue(prose_field({'label':'3차년도 / (20xx년)','role':'body','in_table':True},34608))
        self.assertFalse(prose_field({'label':'yy.mm~yy.mm','role':'body','in_table':True},4400))
