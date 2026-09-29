import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from govoffice.adapters.hwp_form_export import export_generated_hwp


class HwpFormExportTimeoutTests(unittest.TestCase):
    def test_dispatch_timeout_reports_actionable_message(self):
        timeout = subprocess.TimeoutExpired(
            'hwp worker', 50, stderr=b'GOVOFFICE_STAGE=worker_started\nGOVOFFICE_STAGE=dispatching_hwp\n'
        )
        with patch('govoffice.adapters.hwp_form_export.subprocess.run', side_effect=timeout):
            with self.assertRaisesRegex(RuntimeError, '한글 자동화 연결이 응답하지 않아') as caught:
                export_generated_hwp(Path('template.hwp'), Path('draft.hml'), Path('result.hwp'))
        self.assertIn('작업 중인 문서를 저장한 뒤', str(caught.exception))
        self.assertIn('dispatching_hwp', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
