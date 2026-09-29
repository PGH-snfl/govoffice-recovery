import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from govoffice.services.authoring_equations import (FORMULA, equation_script,
    equation_source, logical_paragraph_text)
from govoffice.services.authoring_validation import audit_layout
from govoffice.services.document_authoring import render_draft
from test_authoring_font_flow import document, flow_manifest
from test_authoring_output_polish import p, cell, table


class EquationTests(unittest.TestCase):
    def test_only_unambiguous_formula_spans_are_selected(self):
        value = '순출력 P_net=P_gross-P_aux와 효율 η_net=P_net/P_th×100을 관리한다. Q=10은 목표다.'
        self.assertEqual(['P_net=P_gross-P_aux', 'η_net=P_net/P_th×100'],
                         [match.group() for match in FORMULA.finditer(value)])
        self.assertEqual('P_{net}=P_{gross}-P_{aux}', equation_script('P_net=P_gross-P_aux'))
        self.assertEqual('P_net=P_gross-P_aux', equation_source('P_{net}=P_{gross}-P_{aux}'))
        self.assertEqual([], list(FORMULA.finditer('E_spec=P_input(MW)×1000/m_H2(kg/h)')))

    def test_body_and_table_equations_keep_original_logical_text(self):
        root = document(p('1. 제목') + p() +
                        p(controls=table([cell(p('고정 P_net=P_gross-P_aux')) + cell(p())])))
        ET.SubElement(root.find('HEAD'), 'PAGEDEF', {'Width': '50000'})
        manifest = flow_manifest(root, [1, 4])
        value = '순출력 P_net=P_gross-P_aux와 효율 η_net=P_net/P_th×100을 관리한다.'
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'source.hwpml').write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
            xml, logs = render_draft(folder, manifest, {},
                                     local_values={field['id']: value for field in manifest['topics'][0]['fields']})
        rendered = ET.fromstring(xml)
        paragraphs = list(rendered.iter('P'))
        self.assertEqual([2, 2], [log['equation_count'] for log in logs])
        for log in logs:
            paragraph = paragraphs[log['output_index']]
            self.assertEqual(value, logical_paragraph_text(paragraph))
            self.assertEqual(2, len(list(paragraph.iter('EQUATION'))))
            self.assertTrue(all(eq.find('SHAPEOBJECT/SIZE') is not None
                                for eq in paragraph.iter('EQUATION')))
        fixed = next(p for p in paragraphs if '고정 P_net=P_gross-P_aux' in logical_paragraph_text(p))
        self.assertEqual(0, len(list(fixed.iter('EQUATION'))))
        self.assertEqual([], audit_layout(xml, logs)['issues'])

    def test_too_wide_for_cell_remains_text(self):
        root = document(p('1. 제목') + p(controls=table([cell(p())])))
        manifest = flow_manifest(root, [2])
        value = 'P_verylongterm=P_anotherlongterm-P_thirdlongterm'
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / 'source.hwpml').write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
            xml, logs = render_draft(folder, manifest, {}, local_values={'P0002': value})
        self.assertEqual(0, logs[0]['equation_count'])
        self.assertEqual(value, logical_paragraph_text(list(ET.fromstring(xml).iter('P'))[2]))


if __name__ == '__main__':
    unittest.main()
