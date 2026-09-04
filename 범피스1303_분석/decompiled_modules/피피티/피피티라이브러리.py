# Source Generated with Decompyle++
# File: ����Ƽ���̺귯��.marshal (Python 3.13)

from win32com.client import GetActiveObject
from win32com.client.gencache import EnsureDispatch
from datetime import datetime, timedelta

def 피피티():
    '''\xed\x94\xbc\xed\x94\xbc\xed\x8b\xb0'''
    __firstlineno__ = 7
    피피티 = None
    임시요일 = [
        '월',
        '화',
        '수',
        '목',
        '금',
        '토',
        '일']
    객체높이 = 0
    
    def 시작(self):
        
        try:
            self.피피티 = GetActiveObject('PowerPoint.Application')
        except ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            self.피피티 = EnsureDispatch('PowerPoint.Application')
            self.피피티.Visible = True
            현재피피티 = self.피피티.Presentations.Add()
            현재피피티.Slides.Add(1, 12)
            현재피피티.PageSetup.SlideWidth = 960
            현재피피티.PageSetup.SlideHeight = 540

        return None
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.피피티 = EnsureDispatch('PowerPoint.Application')
            self.피피티.Visible = True
            현재피피티 = self.피피티.Presentations.Add()
            현재피피티.Slides.Add(1, 12)
            현재피피티.PageSetup.SlideWidth = 960
            현재피피티.PageSetup.SlideHeight = 540
            e = None
            del e
            return None
            e = None
            del e

    if (lambda self, 포인트, 색상, 라인, 굵기, 테두리색: 