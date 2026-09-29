import unittest

from govoffice.services.authoring_validation import audit_results, audit_layout, number
from govoffice.services.document_authoring import validate_result, response_schema


class ValidationTests(unittest.TestCase):
    def audit(self, values):
        return audit_results({'render_policy': {'profile': 'climate_2026_v2'}},
                             {'topic': {'values': values}})

    def test_budget_sum_mismatch_is_not_hidden(self):
        result = self.audit({'P0234':'1,000','P0235':'200','P0237':'300','P0239':'1,499'})
        self.assertEqual('failed', result['numeric_checks'][0]['status'])
        self.assertIn('1,500', result['issues'][0])
        self.assertFalse(result['submission_ready'])

    def test_exact_decimal_sum(self):
        result = self.audit({'P0234':'0.1','P0235':'0.2','P0237':'0','P0239':'0.3'})
        self.assertEqual('passed', result['numeric_checks'][0]['status'])

    def test_unknown_is_not_treated_as_zero(self):
        result = self.audit({'P0234':'확인 필요'})
        self.assertEqual('not_enough_data', result['numeric_checks'][0]['status'])
        self.assertEqual(['P0234'], result['unresolved_fields'])
        self.assertIsNone(number('100만원'))

    def test_cross_table_inconsistent_totals(self):
        result = self.audit({'P0241':'100','P5794':'110'})
        self.assertTrue(any('총액이 다릅니다' in x for x in result['issues']))

    def test_shifted_field_position_is_checked(self):
        xml = '<HWPML><P><TEXT><CHAR>first</CHAR></TEXT></P><P><TEXT><CHAR>value</CHAR></TEXT></P></HWPML>'
        field = {'field_id':'P0042','output_index':1,'value':'value'}
        self.assertEqual([], audit_layout(xml,[field])['issues'])
        field['output_index'] = 0
        self.assertIn('출력 위치 불일치', audit_layout(xml,[field])['issues'][0])

    def test_timeline_marker_schema_and_validation(self):
        topic = {'id':'topic','fields':[{'id':'P0001','kind':'schedule_marker','allow_empty':True,'max_chars':1}]}
        schema = response_schema(topic)
        self.assertEqual(['','■','?'], schema['properties']['values']['properties']['P0001']['enum'])
        for text in ('','■','?'):
            validate_result(topic, {'topic_id':'topic','values':{'P0001':text},'needs_review':[]})
        with self.assertRaises(ValueError):
            validate_result(topic, {'topic_id':'topic','values':{'P0001':'X'},'needs_review':[]})


if __name__ == '__main__':
    unittest.main()
