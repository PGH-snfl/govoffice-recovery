# -*- coding: utf-8 -*-
import sys

sys.path.insert(
    0,
    r"C:\Users\skyla\.codex\visualizations\2026\08\25\01a037d3-0794-7650-8443-98349cdbf781\project_link\recovered",
)

from 한컴오피스.한컴라이브러리 import 기본한컴
from win32com.client.gencache import EnsureDispatch


hwp = 기본한컴()
hwp.대상 = EnsureDispatch("HWPFrame.HwpObject")
hwp.대상.XHwpWindows.Item(0).Visible = True
hwp.새창()
hwp.폰트("맑은 고딕")
hwp.글자크기(16)
hwp.진하게()
hwp.문장("점수 분배 실행 예시")
hwp.대상.HAction.Run("BreakPara")
hwp.대상.HAction.Run("BreakPara")
hwp.대상.HAction.Run("CharShapeNormal")
hwp.글자크기(12)
hwp.문장(
    "문항 1  [0점]\r\n"
    "문항 2  [0점]\r\n"
    "문항 3  [0점]\r\n\r\n"
    "분배할 점수"
)
hwp.대상.HAction.Run("BreakPara")
hwp.표만들기([30, 30, 30], [10])
hwp.문장("10")
hwp.표오른쪽(1)
hwp.문장("20")
hwp.표오른쪽(1)
hwp.문장("30")
hwp.대상.HAction.Run("TableCellBlock")
hwp.대상.HAction.Run("TableCellBlockExtend")
hwp.대상.HAction.Run("TableCellBlockExtend")
hwp.점수분배()
hwp.대상.SaveAs(
    r"C:\Users\skyla\.codex\visualizations\2026\08\25\01a037d3-0794-7650-8443-98349cdbf781\project_link\점수분배_예시.hwp",
    "HWP",
    "",
)
print("OK")
