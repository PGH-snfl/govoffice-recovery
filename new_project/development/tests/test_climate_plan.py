import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from govoffice.institutions.packages.seoultech.climate_2026.generator import (
    ASSETS, SOURCE_SHA256, generate, own_text, render_example,
)
from govoffice.institutions.packages.seoultech.climate_2026.example_content import example_fields


class ClimatePlanTests(unittest.TestCase):
    def test_every_source_paragraph_is_in_both_markdown_references(self):
        source=ET.fromstring((ASSETS/'source.hwpml').read_text(encoding='utf-8'))
        guides=(ASSETS/'작성요령.md').read_text(encoding='utf-8')
        full=(ASSETS/'전체원문_대조본.md').read_text(encoding='utf-8')
        for i,p in enumerate(source.iter('P')):
            text=own_text(p)
            if text.strip():
                self.assertIn(f'<!-- P{i:04d} -->',guides)
                self.assertIn(text,guides)
                self.assertIn(f'### P{i:04d}',full)
                self.assertIn(text,full)

    def test_template_original_and_section_settings_are_preserved(self):
        xml,report,fields=render_example()
        self.assertEqual(SOURCE_SHA256,hashlib.sha256((ASSETS/'template.hwp').read_bytes()).hexdigest())
        root=ET.fromstring(xml)
        original=ET.fromstring((ASSETS/'source.hwpml').read_text(encoding='utf-8'))
        self.assertEqual(1,len(root.findall('BODY/SECTION')))
        self.assertIsNotNone(root.find('BODY/SECTION/P/TEXT/SECDEF'))
        self.assertEqual(ET.tostring(original.find('.//PAGEDEF')),ET.tostring(root.find('.//PAGEDEF')))
        self.assertEqual(23,report['removed_guide_tables'])
        self.assertNotIn('작성 요령(연구개발계획서 작성 후',xml)
        self.assertFalse(report['submission_ready'])
        self.assertFalse(report['ai_connected'])
        for f in fields:self.assertIn(f['value'],''.join(root.itertext()))

    def test_budget_and_metric_weights_are_consistent(self):
        f=example_fields()
        self.assertEqual('600,000',f[241])
        self.assertEqual(f[241],f[5794])
        self.assertEqual(f[241],f[6030])
        self.assertEqual(100,sum(int(f[i]) for i in (802,816,830)))
        for k in range(3):
            self.assertEqual(int(f[5789+k].replace(',','')),
                             int(f[5775+k].replace(',',''))+int(f[5782+k].replace(',','')))
        self.assertEqual('발전 예측 오차율',f[1220])

    def test_runs_never_overwrite_and_failure_does_not_claim_native_success(self):
        with tempfile.TemporaryDirectory() as temp:
            a=generate(Path(temp));b=generate(Path(temp))
            self.assertNotEqual(a['output_dir'],b['output_dir'])
            self.assertFalse(a['native_verified'])
            self.assertIsNone(a['hwp_path'])
            def fail(*args):raise RuntimeError('test conversion failed')
            with self.assertRaisesRegex(RuntimeError,'한글 파일 변환 실패'):
                generate(Path(temp),fail)
            reports=[json.loads(p.read_text(encoding='utf-8')) for p in Path(temp).glob('*/생성결과.json')]
            self.assertEqual(1,len([r for r in reports if r.get('native_error')]))
            self.assertTrue(all(not r['native_verified'] for r in reports))

    def test_live_button_reads_manifest_and_routes_to_backend(self):
        project=Path(__file__).resolve().parents[2]
        manifest=json.loads((ASSETS.parent/'manifest.json').read_text(encoding='utf-8'))
        self.assertIn('climate_plan_generate',[f['action'] for f in manifest['custom_features']])
        launcher=(project/'launch_gui.ps1').read_text(encoding='utf-8-sig')
        self.assertIn('$SeoultechManifest.custom_features',launcher)
        self.assertIn("Send-Backend @{action='climate_plan_generate'}",launcher)
        self.assertIn('return 60000',launcher)


if __name__=='__main__':unittest.main()
