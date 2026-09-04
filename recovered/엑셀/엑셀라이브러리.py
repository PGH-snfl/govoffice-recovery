"""한글 기능에서 사용하는 최소 Excel COM 연결 계층."""

from win32com.client import GetActiveObject
from win32com.client.gencache import EnsureDispatch


class 엑셀:
    엑셀 = None
    엑셀리스트 = None

    def 시작(self):
        try:
            self.엑셀 = GetActiveObject("Excel.Application")
        except Exception:
            self.엑셀 = EnsureDispatch("Excel.Application")
            self.엑셀.Visible = True
            워크북 = self.엑셀.Workbooks.Add()
            워크북.Worksheets(1)
        return None
