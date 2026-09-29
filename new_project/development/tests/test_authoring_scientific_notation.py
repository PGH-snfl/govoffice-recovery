import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_equations import logical_paragraph_text
from govoffice.services.authoring_scientific_notation import display_value, scientific_parts
from govoffice.services.authoring_validation import audit_layout
from govoffice.services.document_authoring import render_draft
from test_authoring_font_flow import document, flow_manifest
from test_authoring_output_polish import p, cell, table


class ScientificNotationTests(unittest.TestCase):
    def test_conservative_power_chemical_and_area_tokens(self):
        value = '열출력 500 MW_th, 순전력 2 MWe, CO2·H2O·CH4, 10 m^2, W/m2'
        self.assertEqual('열출력 500 MWth, 순전력 2 MWe, CO2·H2O·CH4, 10 m2, W/m2',
                         display_value(value))
        self.assertIn(('sub', 'th'), scientific_parts(value))
        self.assertIn(('sub', 'e'), scientific_parts(value))
        self.assertIn(('super', '2'), scientific_parts(value))
        self.assertEqual('B2B 사업과 Q=10은 그대로, CO₂도 그대로',
                         display_value('B2B 사업과 Q=10은 그대로, CO₂도 그대로'))
        self.assertEqual('P_net=P_gross-P_aux', display_value('P_net=P_gross-P_aux'))

    def test_agent_body_and_table_use_existing_font_with_script_shapes(self):
        root = document(p('1. 제목') + p(shape='1') +
                        p(controls=table([cell(p('고정 CO2 MW_th')) + cell(p(shape='0'))])))
        manifest = flow_manifest(root, [1, 4])
        value = '500 MW_th와 2 MWe, CO2와 H2O, 10 m^2, W/m2'
        results = {'s': {'topic_id': 's', 'values': {'P0001': value, 'P0004': value},
                         'needs_review': []}}
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'source.hwpml').write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
            xml, logs = render_draft(folder, manifest, results)
        rendered = ET.fromstring(xml)
        ps = list(rendered.iter('P'))
        shapes = {s.get('Id'): s for s in rendered.iter('CHARSHAPE')}
        for log in logs:
            paragraph = ps[log['output_index']]
            self.assertEqual(display_value(value), logical_paragraph_text(paragraph))
            scripts = [(t.find('CHAR').text, shapes[t.get('CharShape')])
                       for t in paragraph.findall('TEXT') if t.find('CHAR') is not None]
            self.assertTrue(any('th' in text and shape.find('SUBSCRIPT') is not None
                                for text, shape in scripts))
            self.assertTrue(any(text == '2' and shape.find('SUPERSCRIPT') is not None
                                for text, shape in scripts))
            faces = {shape.find('FONTID').get('Hangul') for _, shape in scripts}
            self.assertEqual(1, len(faces))
        fixed = next(p for p in ps if logical_paragraph_text(p) == '고정 CO2 MW_th')
        self.assertEqual(1, len(fixed.findall('TEXT')))
        self.assertEqual([], audit_layout(xml, logs)['issues'])

    def test_user_entered_value_is_not_rewritten(self):
        root = document(p('1. 제목') + p())
        manifest = flow_manifest(root, [1])
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'source.hwpml').write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
            xml, logs = render_draft(folder, manifest, {}, local_values={'P0001': 'H2 사업'})
        paragraph = list(ET.fromstring(xml).iter('P'))[1]
        self.assertEqual('H2 사업', logical_paragraph_text(paragraph))
        self.assertEqual([], audit_layout(xml, logs)['issues'])

    def test_equation_and_unit_in_one_paragraph_stay_separate(self):
        root = document(p('1. 제목') + p())
        ET.SubElement(root.find('HEAD'), 'PAGEDEF', {'Width': '50000'})
        manifest = flow_manifest(root, [1])
        value = '순출력 P_net=P_gross-P_aux, 열출력 500 MW_th와 CO2를 비교한다.'
        result = {'s': {'topic_id': 's', 'values': {'P0001': value}, 'needs_review': []}}
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'source.hwpml').write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
            xml, logs = render_draft(folder, manifest, result)
        rendered = ET.fromstring(xml)
        paragraph = list(rendered.iter('P'))[1]
        self.assertEqual(1, len(list(paragraph.iter('EQUATION'))))
        self.assertEqual(display_value(value), logical_paragraph_text(paragraph))
        self.assertEqual([], audit_layout(xml, logs)['issues'])


if __name__ == '__main__':
    unittest.main()
