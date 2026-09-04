# Source Generated with Decompyle++
# File: �������̺귯��.marshal (Python 3.13)

from win32com.client import GetActiveObject
from win32com.client.gencache import EnsureDispatch
from tkinter import filedialog
import re
from decimal import Decimal
from datetime import datetime, timedelta
import os
import itertools

def 랜덤정수(최대정수):
    return os.urandom(None(4), byteorder = 'big') % 최대정수


def 랜덤셔플(리스트):
    for i in range(len(리스트) - 1, 0, -1):
        j = 랜덤정수(i)
        리스트[j], 리스트[i] = 리스트[i], 리스트[j]
    return 리스트


def 엑셀():
    '''\xec\x97\x91\xec\x85\x80'''
    __firstlineno__ = 24
    엑셀 = None
    엑셀리스트 = None
    
    def 시작(self):
        
        try:
            self.엑셀 = GetActiveObject('Excel.Application')
        except ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            self.엑셀 = EnsureDispatch('Excel.Application')
            self.엑셀.Visible = True
            워크북 = self.엑셀.Workbooks.Add()
            워크시트 = 워크북.Worksheets(1)

        return None
        if Exception:
            e = None
            print(f'''오류 : {e}''')
            self.엑셀 = EnsureDispatch('Excel.Application')
            self.엑셀.Visible = True
            워크북 = self.엑셀.Workbooks.Add()
            워크시트 = 워크북.Worksheets(1)
            e = None
            del e
            return None
            e = None
            del e

    
    def 값만붙임(self):
        self.엑셀.Selection.PasteSpecial(Paste = -4163)

    
    def 너비맞춤(self):
        self.엑셀.Selection.Columns.AutoFit()

    
    def 배경색(self, 색상코드):
        self.엑셀.Selection.Interior.Color = 색상코드

    
    def 서식붙임(self):
        self.엑셀.Selection.PasteSpecial(Paste = -4122)

    
    def 취소선(self):
        self.엑셀.Selection.Font.Strikethrough = True

    
    def 각각카운트(self):
        엑셀리스트 = []
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                엑셀리스트.append(str(선택범위.Cells(i, j).Value))
        for None in :
            if None:
                if None:
                    continue
                continue
                , [], 엑셀리스트, x = None, 엑셀리스트
                for None in :
                    if None:
                        continue
                        None, 엑셀리스트, 엑셀리스트, 아이템 = None
                        카운트리스트 = []
                        본거 = []
                        for 아이템 in 엑셀리스트:
                            if not 아이템 not in 본거:
                                continue
                            카운트 = 엑셀리스트.count(아이템)
                            카운트리스트.append([
                                아이템,
                                카운트])
                            본거.append(아이템)
                        카운트리스트 = sorted(카운트리스트, key = (lambda x: x[1]), reverse = True)
        새워크북 = self.엑셀.Workbooks.Add()
        새워크시트 = 새워크북.Sheets(1)
        for None in enumerate(카운트리스트, start = 1):
            if ():
                for None in enumerate(줄, start = 1):
                    if ():
                        continue
                        continue
                        return None
                        
                        

    
    def 겉바속촉(self):
        self.엑셀.Selection.Borders(7).LineStyle = 1
        self.엑셀.Selection.Borders(8).LineStyle = 1
        self.엑셀.Selection.Borders(9).LineStyle = 1
        self.엑셀.Selection.Borders(10).LineStyle = 1
        self.엑셀.Selection.Borders(11).LineStyle = 1
        self.엑셀.Selection.Borders(12).LineStyle = 1
        self.엑셀.Selection.Borders(7).Weight = -4138
        self.엑셀.Selection.Borders(8).Weight = -4138
        self.엑셀.Selection.Borders(9).Weight = -4138
        self.엑셀.Selection.Borders(10).Weight = -4138
        self.엑셀.Selection.Borders(11).Weight = 2
        self.엑셀.Selection.Borders(12).Weight = 2

    
    def 겉바속점(self):
        self.엑셀.Selection.Borders(7).LineStyle = 1
        self.엑셀.Selection.Borders(8).LineStyle = 1
        self.엑셀.Selection.Borders(9).LineStyle = 1
        self.엑셀.Selection.Borders(10).LineStyle = 1
        self.엑셀.Selection.Borders(11).LineStyle = -4118
        self.엑셀.Selection.Borders(12).LineStyle = -4118
        self.엑셀.Selection.Borders(7).Weight = -4138
        self.엑셀.Selection.Borders(8).Weight = -4138
        self.엑셀.Selection.Borders(9).Weight = -4138
        self.엑셀.Selection.Borders(10).Weight = -4138
        self.엑셀.Selection.Borders(11).Weight = 2
        self.엑셀.Selection.Borders(12).Weight = 2

    
    def 공백정리(self):
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                데이터 = 선택범위.Cells(i, j).Value
                if not 데이터 != None:
                    continue
                데이터 = 데이터.strip()
                데이터 = None('\\n+', '\n', 데이터)
                데이터 = None('[ \\t]+', ' ', 데이터)
                선택범위.Cells(i, j).Value = 데이터
            re.sub

    
    def 주민암호화(self):
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                데이터 = 선택범위.Cells(i, j).Value
                if not 데이터 != None:
                    continue
                데이터 = 데이터.strip()
                데이터 = None('\\D', '', 데이터)
                if len(데이터) == 13:
                    pass
                데이터 = 데이터[:6] + '-' + 데이터[6:7] + '******'
                선택범위.Cells(i, j).Value = 데이터

    
    def 대카운트(self):
        엑셀리스트 = []
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            엑셀리스트.append(선택범위.Cells(i, 1).Value)
        for None in :
            if None:
                if None:
                    continue
                continue
                , [], 엑셀리스트, x = None, 엑셀리스트
                
                def 만나이(아이템):
                    나이 = '오류'
                    if isinstance(아이템, float):
                        pass
                    if isinstance(아이템, float):
                        pass
                    아이템 = int(아이템)
                    아이템 = str(아이템)
                    if 아이템.isdigit():
                        pass
                    if 아이템.isdigit():
                        if len(아이템) == 6:
                            년 = int(아이템[:2])
                            월 = int(아이템[2:4])
                            일 = int(아이템[4:])
                            나이 = None().year - 년
                            if datetime.today > None().month:
                                나이 -= 1
                            return 나이
                        if datetime.today == None().month and datetime.today > None().day:
                            pass
                        나이 -= 1
                        return 나이
                    if None(아이템) == 8:
                        년 = int(아이템[:4])
                        월 = int(아이템[4:6])
                        일 = int(아이템[6:])
                        나이 = None().year - 년
                        if datetime.today > None().month:
                            나이 -= 1
                        return 나이
                    if datetime.today == None().month and datetime.today > None().day:
                        pass
                    나이 -= 1
                    return 나이

                for None in :
                    if None:
                        continue
                        None, 엑셀리스트, 만나이리스트, 아이템 = None
                        for None in :
                            if None:
                                continue
                                , { }, 카운트, i = None, range(10)
                                카운트['100대이상'] = 0
                                카운트['오류'] = 0
                                for 아이템 in 만나이리스트:
                                    if isinstance(아이템, int):
                                        pass
                                    if isinstance(아이템, int):
                                        그룹 = (아이템 // 10) * 10
                                        라벨 = f'''{그룹}대''' if 그룹 < 100 else '100대이상'
                                    if not 아이템 == '오류':
                                        continue
                                self.엑셀.Workbooks.Add() = None
                                새워크시트 = 새워크북.Sheets(1)
                                새워크시트.Name = '세부내용'
                                새워크시트.Cells(1, 1).Value = '원본'
                                새워크시트.Cells(1, 2).Value = '만나이'
                                행 = 2
                                for 아이템 in 엑셀리스트:
                                    새워크시트.Cells(행, 1).Value = 아이템
                                    행 += 1
                                행 = 2
                                for 아이템 in 만나이리스트:
                                    새워크시트.Cells(행, 2).Value = 아이템
                                    행 += 1
                                새워크시트 = 새워크북.Worksheets.Add()
                                새워크시트.Name = '결과'
                                새워크시트.Cells(1, 1).Value = '연령대'
                                새워크시트.Cells(1, 2).Value = '인원수'
                                행 = 2
                                for 키, 값 in 카운트.items():
                                    새워크시트.Cells(행, 1).Value = 키
                                    새워크시트.Cells(행, 2).Value = 값
                                    행 += 1
                                return None
                                
                                
                                

    
    def 투명표(self):
        self.엑셀.Selection.Borders(7).LineStyle = -4142
        self.엑셀.Selection.Borders(8).LineStyle = -4142
        self.엑셀.Selection.Borders(9).LineStyle = -4142
        self.엑셀.Selection.Borders(10).LineStyle = -4142
        self.엑셀.Selection.Borders(11).LineStyle = -4142
        self.엑셀.Selection.Borders(12).LineStyle = -4142

    
    def 점선표(self):
        self.엑셀.Selection.Borders(7).LineStyle = -4118
        self.엑셀.Selection.Borders(8).LineStyle = -4118
        self.엑셀.Selection.Borders(9).LineStyle = -4118
        self.엑셀.Selection.Borders(10).LineStyle = -4118
        self.엑셀.Selection.Borders(11).LineStyle = -4118
        self.엑셀.Selection.Borders(12).LineStyle = -4118
        self.엑셀.Selection.Borders(7).Weight = 2
        self.엑셀.Selection.Borders(8).Weight = 2
        self.엑셀.Selection.Borders(9).Weight = 2
        self.엑셀.Selection.Borders(10).Weight = 2
        self.엑셀.Selection.Borders(11).Weight = 2
        self.엑셀.Selection.Borders(12).Weight = 2

    
    def 기본표(self):
        self.엑셀.Selection.Borders(7).LineStyle = 1
        self.엑셀.Selection.Borders(8).LineStyle = 1
        self.엑셀.Selection.Borders(9).LineStyle = 1
        self.엑셀.Selection.Borders(10).LineStyle = 1
        self.엑셀.Selection.Borders(11).LineStyle = 1
        self.엑셀.Selection.Borders(12).LineStyle = 1
        self.엑셀.Selection.Borders(7).Weight = 2
        self.엑셀.Selection.Borders(8).Weight = 2
        self.엑셀.Selection.Borders(9).Weight = 2
        self.엑셀.Selection.Borders(10).Weight = 2
        self.엑셀.Selection.Borders(11).Weight = 2
        self.엑셀.Selection.Borders(12).Weight = 2
        self.엑셀.Selection.Borders(7).Color = 0
        self.엑셀.Selection.Borders(8).Color = 0
        self.엑셀.Selection.Borders(9).Color = 0
        self.엑셀.Selection.Borders(10).Color = 0
        self.엑셀.Selection.Borders(11).Color = 0
        self.엑셀.Selection.Borders(12).Color = 0

    
    def 기본테두리(self):
        self.엑셀.Selection.Borders(7).LineStyle = 1
        self.엑셀.Selection.Borders(8).LineStyle = 1
        self.엑셀.Selection.Borders(9).LineStyle = 1
        self.엑셀.Selection.Borders(10).LineStyle = 1
        self.엑셀.Selection.Borders(7).Weight = 2
        self.엑셀.Selection.Borders(8).Weight = 2
        self.엑셀.Selection.Borders(9).Weight = 2
        self.엑셀.Selection.Borders(10).Weight = 2

    
    def 진한테두리(self):
        self.엑셀.Selection.Borders(7).LineStyle = 1
        self.엑셀.Selection.Borders(8).LineStyle = 1
        self.엑셀.Selection.Borders(9).LineStyle = 1
        self.엑셀.Selection.Borders(10).LineStyle = 1
        self.엑셀.Selection.Borders(7).Weight = -4138
        self.엑셀.Selection.Borders(8).Weight = -4138
        self.엑셀.Selection.Borders(9).Weight = -4138
        self.엑셀.Selection.Borders(10).Weight = -4138

    
    def 하단이중선(self):
        self.엑셀.Selection.Borders(9).LineStyle = -4119

    
    def 기본글자(self):
        self.엑셀.Selection.Font.Size = 11
        self.엑셀.Selection.HorizontalAlignment = -4108
        self.엑셀.Selection.VerticalAlignment = -4108
        self.엑셀.Selection.Font.Name = '맑은 고딕'
        self.엑셀.Selection.Font.Color = 0
        self.엑셀.Selection.Font.Bold = False
        self.엑셀.Selection.Font.Italic = False
        self.엑셀.Selection.Font.Underline = False
        self.엑셀.Selection.Font.Strikethrough = False

    
    def 날짜변환(self):
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                
                try:
                    데이터 = 선택범위.Cells(i, j).Text
                    데이터 = 데이터.replace(' ', '')
                    데이터 = 데이터.replace('(월)', '').replace('월요일', '')
                    데이터 = 데이터.replace('일', '')
                    데이터 = 데이터.replace('년', '-')
                    데이터 = 데이터.replace('월', '-')
                    데이터 = None('[가-힣]', '', 데이터)
                    데이터 = 데이터.replace('(', '')
                    데이터 = 데이터.replace(')', '')
                    데이터 = 데이터.replace("'", '20')
                    데이터 = 데이터.replace('`', '20')
                    데이터 = 데이터.replace('ʹ', '20')
                    데이터 = 데이터.replace('’', '20')
                    데이터 = 데이터.replace('‘', '20')
                    if None('^\\d{8}$', 데이터):
                        pass
                    if None('^\\d{8}$', 데이터):
                        pass
                    데이터 = f'''{데이터[:4]}-{데이터[4:6]}-{데이터[6:]}'''
                    데이터 = 데이터.rstrip('.')
                    데이터 = None('[./-]', '-', 데이터)
                    if len(데이터) < 7:
                        pass
                    데이터 = datetime.today(None().year) + '-' + 데이터
                    데이터 = None(데이터, '%Y-%m-%d')
                    데이터 = str(데이터.year) + '-' + str(데이터.month) + '-' + str(데이터.day)
                    선택범위.Cells(i, j).NumberFormat = 'yyyy-mm-dd'
                    선택범위.Cells(i, j).Value = 데이터
                    선택범위.Cells(i, j).NumberFormat = '@'
                    기본날짜 = datetime(1900, 1, 1)
                    변환날짜 = None + timedelta(days = int(선택범위.Cells(i, j).Value) - 2)
                    선택범위.Cells(i, j).Value = 변환날짜.strftime('%Y-%m-%d')
                except ValueError:
                    e = None
                    print(f'''날짜 오류 (셀: {i}, {j}): {e}''')

        return None
        if Exception:
            e = None
            print(f'''오류 발생 (셀: {i}, {j}): {e}''')
            e = None
            del e
            continue
            e = None
            del e

    
    def 높이같게(self):
        선택범위 = self.엑셀.Selection
        첫셀높이 = 선택범위.Cells(1, 1).RowHeight
        선택범위.RowHeight = 첫셀높이

    
    def 랜덤정렬(self):
        if self.엑셀.Selection.Rows.Count > 1:
            선택범위 = self.엑셀.Selection
            데이터 = self.엑셀.Selection.Value
            섞인데이터 = list(데이터)
            섞인데이터 = 랜덤셔플(섞인데이터)
            for None in enumerate(섞인데이터):
                if ():
                    for None in enumerate(row):
                        if ():
                            continue
                            continue
                            ()
                            return None
                            return None

    if (lambda self, 종류: 선택범위 = self.엑셀.Selection행 = 선택범위.Rows.Count열 = 선택범위.Columns.Countfor i in range(1, 행 + 1):
for j in range(1, 열 + 1):
임시데이터 = 선택범위.Cells(i, j).Textif 종류 == '텍스트':
선택범위.Cells(i, j).NumberFormat = '@'else:
선택범위.Cells(i, j).NumberFormatLocal = 'G/표준'선택범위.Cells(i, j).Value = 임시데이터):
        
        def 표시변경(self, 종류):
            선택범위 = self.엑셀.Selection
            행 = 선택범위.Rows.Count
            열 = 선택범위.Columns.Count
            for i in range(1, 행 + 1):
                for j in range(1, 열 + 1):
                    임시데이터 = 선택범위.Cells(i, j).Text
                    if 종류 == '텍스트':
                        선택범위.Cells(i, j).NumberFormat = '@'
                    else:
                        선택범위.Cells(i, j).NumberFormatLocal = 'G/표준'
                    선택범위.Cells(i, j).Value = 임시데이터

    
    def 개월년개월(self):
        선택범위 = self.엑셀.Selection
        행개수 = 선택범위.Rows.Count
        년개월 = '오류'
        for i in range(1, 행개수 + 1):
            데이터 = 선택범위.Cells(i, 1).Text
            if 데이터 == None or 데이터 == '':
                pass
            데이터 = 0
            데이터 = int(데이터)
            년개월 = f'''{데이터 // 12}년 {데이터 % 12}개월'''
            선택범위.Cells(i, 2).Value = 년개월

    
    def 만나이(self):
        선택범위 = self.엑셀.Selection
        행개수 = 선택범위.Rows.Count
        나이 = 0
        for i in range(1, 행개수 + 1):
            나이 = '오류'
            데이터 = 선택범위.Cells(i, 1).Text
            년도 = None('[^0-9]', '', 데이터)
            if len(데이터) == 6:
                년 = int(년도[:2])
                월 = int(년도[2:4])
                일 = int(년도[4:])
                나이 = None().year - 년
                if datetime.today > None().month:
                    나이 -= 1
                elif datetime.today == None().month and datetime.today > None().day:
                    pass
                나이 -= 1
            elif len(년도) == 8:
                년 = int(년도[:4])
                월 = int(년도[4:6])
                일 = int(년도[6:])
                나이 = None().year - 년
                if datetime.today > None().month:
                    나이 -= 1
                elif datetime.today == None().month and datetime.today > None().day:
                    pass
            나이 -= 1
            선택범위.Cells(i, 2).Value = 나이
        월

    if (lambda self, 크기, 진하게, 색상: self.엑셀.Selection.Font.Name = '맑은 고딕'self.엑셀.Selection.Font.Bold = Falseif 크기 != 0:
self.엑셀.Selection.Font.Size = 크기if 진하게 == 1:
self.엑셀.Selection.Font.Bold = Trueself.엑셀.Selection.Font.Color = 색상):
        
        def 맑은고딕(self, 크기, 진하게, 색상):
            self.엑셀.Selection.Font.Name = '맑은 고딕'
            self.엑셀.Selection.Font.Bold = False
            if 크기 != 0:
                self.엑셀.Selection.Font.Size = 크기
            if 진하게 == 1:
                self.엑셀.Selection.Font.Bold = True
            self.엑셀.Selection.Font.Color = 색상

    
    def 병합해제(self):
        기준시트 = self.엑셀.ActiveSheet
        시작행 = self.엑셀.Selection.Row
        마지막행 = 기준시트.UsedRange.Rows.Count + 기준시트.UsedRange.Row + 3
        마지막열 = 기준시트.UsedRange.Columns.Count + 1
        기준시트.Range(기준시트.Cells(시작행, 1), 기준시트.Cells(마지막행, 마지막열)).UnMerge()

    
    def 산출근거계산(self):
        선택범위 = self.엑셀.Selection
        행개수 = 선택범위.Rows.Count
        for i in range(1, 행개수 + 1):
            패턴 = None('(?:(?<=[^\\d\\.])(?=\\d)|(?=[^\\d\\.]))')
            연산자 = ('*', '/', '+', '-', '(', ')')
            연산순위 = {
                '*': 2,
                '/': 2,
                '+': 1,
                '-': 1,
                '(': 0 }
            후위식 = []
            스택 = []
            계산자 = ('*', '/', '+', '-')
            계산식 = {
                '*': (lambda x, y: y * x),
                '/': (lambda x, y: y / x),
                '+': (lambda x, y: y + x),
                '-': (lambda x, y: y - x) }
            계산스택 = []
            데이터 = 선택범위.Cells(i, 1).Value
            데이터 = 데이터.replace('더하기', '+').replace('곱하기', '*').replace('나누기', '/').replace('빼기', '-').replace('더하기', '+').replace('x', '*').replace('X', '*')
            데이터 = None('[^\\d\\(\\)\\-\\*\\/\\+.]', '', 데이터)
            토큰덩어리 = None(패턴, ' ', 데이터).split(' ')
            for 토큰 in 토큰덩어리:
                if 토큰 not in 연산자:
                    후위식.append(토큰)
                    continue
                if 토큰 == '(':
                    스택.append(토큰)
                    continue
                if 토큰 == ')':
                    if 스택 != [] and 스택[-1] != '(':
                        후위식.append(스택.pop())
                        if 스택 != [] and 스택[-1] != '(':
                            continue
                    스택.pop()
                    continue
                if 스택 != [] and 연산순위[스택[-1]] >= 연산순위[토큰]:
                    후위식.append(스택.pop())
                    if 스택 != [] and 연산순위[스택[-1]] >= 연산순위[토큰]:
                        continue
                스택.append(토큰)
            re.sub
            if 스택:
                pass
            if 스택:
                후위식.append(스택.pop())
                if 스택:
                    pass
                if 스택:
                    continue
            for 토큰 in 후위식:
                if 토큰 not in 계산자:
                    if '.' in 토큰:
                        계산스택.append(float(토큰))
                        continue
                    계산스택.append(int(토큰))
                    continue
                x = 계산스택.pop()
                y = 계산스택.pop()
                계산식[토큰](None(x, y))
            최종값 = str(계산스택[-1])
            선택범위.Cells(i, 2).Value = 최종값
            선택범위.Cells(i, 2).NumberFormat = '#,##0'

    
    def 순번(self):
        선택범위 = self.엑셀.Selection
        self.엑셀.Selection.NumberFormatLocal = 'G/표준'
        행 = self.엑셀.Selection.Row
        기준값 = 1
        if 선택범위.Cells(1, 1).Value != None:
            if isinstance(선택범위.Cells(1, 1).Value, (int, float)):
                pass
            if isinstance(선택범위.Cells(1, 1).Value, (int, float)) and Decimal(선택범위.Cells(1, 1).Value) % 1 == 0:
                pass
        기준값 = Decimal(선택범위.Cells(1, 1).Value)
        행개수 = 선택범위.Rows.Count
        for i in range(1, 행개수 + 1):
            선택범위.Cells(i, 1).Formula = f'''=Row()-{행}+{기준값}'''

    
    def 순환복사(self):
        self.엑셀리스트 = []
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                self.엑셀리스트.append(선택범위.Cells(i, j).Value)
        for None in :
            if None:
                if None:
                    continue
                continue
                x, self.엑셀리스트 = None, self.엑셀리스트, , []
                return None
                

    
    def 순환붙임(self):
        self.엑셀리스트
        선택범위 = self.엑셀.Selection
        임시주소목록 = []
        for 셀 in 선택범위:
            임시주소 = ''
            if 셀.MergeCells:
                pass
            if 셀.MergeCells:
                임시주소 = 셀.MergeArea.Address
            else:
                임시주소 = 셀.Address
            if not 임시주소 not in 임시주소목록:
                continue
            임시주소목록.append(임시주소)
        for i in range(0, min(len(self.엑셀리스트), len(임시주소목록))):
            self.엑셀.ActiveSheet.Range(임시주소목록[i]).Value = self.엑셀리스트[i]

    if (lambda self, 종류: 선택범위 = self.엑셀.Selection행 = 선택범위.Rows.Count열 = 선택범위.Columns.Countfor i in range(1, 행 + 1):
for j in range(1, 열 + 1):
데이터 = 선택범위.Cells(i, j).Value데이터 = str(데이터)if None('\\d', 데이터):
passif None('\\d', 데이터):
여부 = None('\\d+(천|백만)', 데이터)데이터 = None('[^0-9\\.\\-]', '', 데이터)if 여부:
passif 여부 and 여부.group(1) == '천':
passelif 여부:
pass곱할값 = 1000000 if 여부 and 여부.group(1) == '백만' else 1데이터 = Decimal(데이터) if '.' in 데이터 else int(데이터)데이터 = 데이터 * 곱할값if 종류 == '천원':
pass데이터 = str(int(round(데이터 / 1000, 0))) + '천원'if 종류 == '백만원':
pass데이터 = str(int(round(데이터 / 1000000, 0))) + '백만원'선택범위.Cells(i, j).Value = str(데이터)선택범위.Cells(i, j).NumberFormat = '#,##0'continue선택범위.Cells(i, j).Font.Color = 255선택범위.Cells(i, j).Font.Bold = Truere.subre.search):
        
        def 숫자만(self, 종류):
            선택범위 = self.엑셀.Selection
            행 = 선택범위.Rows.Count
            열 = 선택범위.Columns.Count
            for i in range(1, 행 + 1):
                for j in range(1, 열 + 1):
                    데이터 = 선택범위.Cells(i, j).Value
                    데이터 = str(데이터)
                    if None('\\d', 데이터):
                        pass
                    if None('\\d', 데이터):
                        여부 = None('\\d+(천|백만)', 데이터)
                        데이터 = None('[^0-9\\.\\-]', '', 데이터)
                        if 여부:
                            pass
                        if 여부 and 여부.group(1) == '천':
                            pass
                        elif 여부:
                            pass
                        곱할값 = 1000000 if 여부 and 여부.group(1) == '백만' else 1
                        데이터 = Decimal(데이터) if '.' in 데이터 else int(데이터)
                        데이터 = 데이터 * 곱할값
                        if 종류 == '천원':
                            pass
                        데이터 = str(int(round(데이터 / 1000, 0))) + '천원'
                        if 종류 == '백만원':
                            pass
                        데이터 = str(int(round(데이터 / 1000000, 0))) + '백만원'
                        선택범위.Cells(i, j).Value = str(데이터)
                        선택범위.Cells(i, j).NumberFormat = '#,##0'
                        continue
                    선택범위.Cells(i, j).Font.Color = 255
                    선택범위.Cells(i, j).Font.Bold = True
                re.sub
            re.search

    
    def 아래전부개수세기(self):
        기준시트 = self.엑셀.ActiveSheet
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Row
        기준행수 = self.엑셀.ActiveSheet.UsedRange.Rows.Count + 선택범위.Row + 3
        열 = 선택범위.Column
        열수 = 선택범위.Columns.Count
        for i in range(1, 열수 + 1):
            선택범위.Cells(1, i).Formula = f'''=Subtotal(3,{선택범위.Cells(2, i).Address}:{선택범위.Cells(기준행수, i).Address})'''

    
    def 아래전부합치기(self):
        기준시트 = self.엑셀.ActiveSheet
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Row
        기준행수 = self.엑셀.ActiveSheet.UsedRange.Rows.Count + 선택범위.Row + 3
        열 = 선택범위.Column
        열수 = 선택범위.Columns.Count
        for i in range(1, 열수 + 1):
            선택범위.Cells(1, i).Formula = f'''=Subtotal(9,{선택범위.Cells(2, i).Address}:{선택범위.Cells(기준행수, i).Address})'''

    
    def 아래전부평균값(self):
        기준시트 = self.엑셀.ActiveSheet
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Row
        기준행수 = self.엑셀.ActiveSheet.UsedRange.Rows.Count + 선택범위.Row + 3
        열 = 선택범위.Column
        열수 = 선택범위.Columns.Count
        for i in range(1, 열수 + 1):
            선택범위.Cells(1, i).Formula = f'''=Subtotal(1,{선택범위.Cells(2, i).Address}:{선택범위.Cells(기준행수, i).Address})'''

    
    def 아래전부중위값(self):
        기준시트 = self.엑셀.ActiveSheet
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Row
        기준행수 = self.엑셀.ActiveSheet.UsedRange.Rows.Count + 선택범위.Row + 3
        열 = 선택범위.Column
        열수 = 선택범위.Columns.Count
        for i in range(1, 열수 + 1):
            선택범위.Cells(1, i).Formula = f'''=Median({선택범위.Cells(2, i).Address}:{선택범위.Cells(기준행수, i).Address})'''

    
    def 우측설명(self):
        self.엑셀.Selection.Merge()
        self.엑셀.Selection.Font.Size = 10
        self.엑셀.Selection.HorizontalAlignment = -4152
        self.엑셀.Selection.VerticalAlignment = -4108
        self.엑셀.Selection.Font.Name = '맑은 고딕'
        self.엑셀.Selection.Font.Bold = False
        self.엑셀.Selection.Font.Italic = False
        self.엑셀.Selection.Font.Underline = False

    
    def 예시글자(self):
        self.엑셀.Selection.Font.Size = 11
        self.엑셀.Selection.HorizontalAlignment = -4108
        self.엑셀.Selection.VerticalAlignment = -4108
        self.엑셀.Selection.Font.Name = '맑은 고딕'
        self.엑셀.Selection.Font.Color = 12874308
        self.엑셀.Selection.Font.Bold = False
        self.엑셀.Selection.Font.Italic = True
        self.엑셀.Selection.Font.Underline = False
        self.엑셀.Selection.Font.Strikethrough = False

    
    def 인쇄범위(self):
        기준시트 = self.엑셀.ActiveSheet
        기준열 = 기준시트.UsedRange.Column
        기준행 = 기준시트.UsedRange.Row
        기준열수 = 기준시트.UsedRange.Columns.Count
        기준행수 = 기준시트.UsedRange.Rows.Count
        기준시트.PageSetup.PrintArea = f'''{기준시트.Cells(1, 1).Address}:{기준시트.Cells(기준행 + 기준행수 - 1, 기준열 + 기준열수 - 1).Address}'''
        기준시트.PageSetup.FitToPagesWide = 1
        기준시트.PageSetup.FitToPagesTall = False
        self.엑셀.ActiveWindow.View = 2
        기준시트.DisplayPageBreaks = True

    
    def 기본화면(self):
        기준시트 = self.엑셀.ActiveSheet
        self.엑셀.ActiveWindow.View = 1
        기준시트.DisplayPageBreaks = False

    
    def 전부해제(self):
        
        try:
            self.엑셀.ActiveSheet.Unprotect()
        except ValueError:
            e = None
            print(f'''값 오류 : {e}''')

        self.엑셀.Selection.Validation.Delete()
        self.엑셀.Selection.Locked = False
        self.엑셀.Selection.FormulaHidden = False
        return None
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            continue
            e = None
            del e

    
    def 제목(self):
        self.엑셀.Selection.Merge()
        self.엑셀.Selection.Font.Size = 16
        self.엑셀.Selection.HorizontalAlignment = -4108
        self.엑셀.Selection.VerticalAlignment = -4108
        self.엑셀.Selection.Font.Name = '맑은 고딕'
        self.엑셀.Selection.Font.Bold = True
        self.엑셀.Selection.Font.Italic = False
        self.엑셀.Selection.Font.Underline = False

    
    def 지역조합(self):
        if (lambda arr, r: if r == 0:
pass[
[]]if len(arr) < r:
pass[]include_first = None(arr[1:], r - 1)exclude_first = None(arr[1:], r)for None in :
if None:
continue조합생성, include_first, include_first, combo = 조합생성include_first + exclude_first):
            
            def 조합생성(arr, r):
                if r == 0:
                    pass
                return [
                    []]
                if len(arr) < r:
                    pass
                return []
                include_first = None(arr[1:], r - 1)
                exclude_first = None(arr[1:], r)
                for None in :
                    if None:
                        continue
                        조합생성, include_first, include_first, combo = 조합생성
                        return include_first + exclude_first

            if (lambda 개수: 결과 = []for i in range(2, 9):
결과 = 조합생성 + None(list(range(개수)), i)결과):
                
                def 조합통합생성(개수):
                    결과 = []
                    for i in range(2, 9):
                        결과 = 조합생성 + None(list(range(개수)), i)
                    return 결과

                엑셀리스트 = []
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                엑셀리스트.append(선택범위.Cells(i, j).Value)
            (조합생성,)
        for None in :
            pass
        i, 엑셀리스트 = None, range(0, len(엑셀리스트), 3), , []
        조합리스트 = None(행)
        결과리스트 = []
        for 조합 in 조합리스트:
            for None in :
                pass
            '+'.join, 조합, , [](인덱스,) = 조합통합생성
            if (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][1]:
pass엑셀리스트[인덱스][1]):
                pass
            인구합산 = (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][1]:
pass엑셀리스트[인덱스][1])(조합())
            if (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][2]:
pass엑셀리스트[인덱스][2]):
                pass
            면적합산 = (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][2]:
pass엑셀리스트[인덱스][2])(조합())
            결과리스트.append([
                이름조합,
                인구합산,
                면적합산])
        sum
        for None in :
            if None:
                if not None[1] <= 20000:
                    continue
                continue
                None, 결과리스트, 필터리스트, 아이템 = (엑셀리스트,)
                새워크북 = self.엑셀.Workbooks.Add()
                새워크시트 = 새워크북.Sheets(1)
                for i, 데이터 in enumerate(필터리스트, start = 1):
                    새워크시트.Cells(i, 1).Value = 데이터[0]
                    새워크시트.Cells(i, 2).Value = 데이터[1]
                    새워크시트.Cells(i, 3).Value = 데이터[2]
                sum
                새워크시트.Cells(1, 4).Value = '완료' + str(len(필터리스트))
                return None
                
                
                

    
    def 지역조건조합(self, 중심, 주변):
        if (lambda arr, r: if r == 0:
pass[
[]]if len(arr) < r:
pass[]include_first = None(arr[1:], r - 1)exclude_first = None(arr[1:], r)for None in :
if None:
continue조합생성, include_first, include_first, combo = 조합생성include_first + exclude_first):
            
            def 조합생성(arr, r):
                if r == 0:
                    pass
                return [
                    []]
                if len(arr) < r:
                    pass
                return []
                include_first = None(arr[1:], r - 1)
                exclude_first = None(arr[1:], r)
                for None in :
                    if None:
                        continue
                        조합생성, include_first, include_first, combo = 조합생성
                        return include_first + exclude_first

            if (lambda 개수: 결과 = []for i in range(2, 9):
결과 = 조합생성 + None(list(range(개수)), i)결과):
                
                def 조합통합생성(개수):
                    결과 = []
                    for i in range(2, 9):
                        결과 = 조합생성 + None(list(range(개수)), i)
                    return 결과

                엑셀리스트 = []
        선택범위 = self.엑셀.Selection
        행 = 선택범위.Rows.Count
        열 = 선택범위.Columns.Count
        for i in range(1, 행 + 1):
            for j in range(1, 열 + 1):
                엑셀리스트.append(선택범위.Cells(i, j).Value)
            (조합생성,)
        for None in :
            pass
        i, 엑셀리스트 = None, range(0, len(엑셀리스트), 3), , []
        조합리스트 = None(행)
        결과리스트 = []
        for 조합 in 조합리스트:
            for None in :
                pass
            '+'.join, 조합, , [](인덱스,) = 조합통합생성
            if (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][1]:
pass엑셀리스트[인덱스][1]):
                pass
            인구합산 = (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][1]:
pass엑셀리스트[인덱스][1])(조합())
            if (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][2]:
pass엑셀리스트[인덱스][2]):
                pass
            면적합산 = (lambda .0: if None:
passfor 인덱스 in .0:
if 엑셀리스트[인덱스][2]:
pass엑셀리스트[인덱스][2])(조합())
            결과리스트.append([
                이름조합,
                인구합산,
                면적합산])
        sum
        for None in :
            if not 아이템[1] <= 20000:
                continue
        , [], 필터리스트 = None, 결과리스트
        아이템 = (엑셀리스트,)
        중심값 = 중심.replace(' ', '')
        주변리스트 = 주변.replace(' ', '')
        주변리스트 = 주변리스트.split('+')
        주변리스트.append(중심값)
        필터리스트2차 = []
        for 아이템 in 필터리스트:
            첫값 = 아이템[0]
            첫값 = 첫값.split('+')
            if 중심값 not in 첫값:
                continue
            if set(첫값).issubset(주변리스트):
                pass
            if not set(첫값).issubset(주변리스트):
                continue
            for None in :
                if not 원소 != 중심값:
                    continue
            , [], 나머지 = sum, 첫값
            원소 = None
            새로운첫값 = 중심값 + '+' + '+'.join(나머지)
            필터리스트2차.append([
                새로운첫값,
                아이템[1],
                아이템[2]])
        새워크북 = self.엑셀.Workbooks.Add()
        새워크시트 = 새워크북.Sheets(1)
        for i, 데이터 in enumerate(필터리스트2차, start = 1):
            새워크시트.Cells(i, 1).Value = 데이터[0]
            새워크시트.Cells(i, 2).Value = 데이터[1]
            새워크시트.Cells(i, 3).Value = 데이터[2]
        새워크시트.Cells(1, 4).Value = '완료' + str(len(필터리스트2차))
        return None
        
        
        
        

    
    def 직제순정렬(self):
        행 = self.엑셀.Selection.Row
        열 = self.엑셀.Selection.Column
        행개수 = self.엑셀.Selection.Rows.Count
        열개수 = self.엑셀.Selection.Columns.Count
        두번째열부터 = self.엑셀.ActiveSheet.Range(self.엑셀.ActiveSheet.Cells(행, 열 + 1), self.엑셀.ActiveSheet.Cells(행 + 행개수 - 1, 열 + 열개수 - 1))
        첫번째열 = self.엑셀.Selection.Columns(1)
        리스트 = 첫번째열.Value
        for None in :
            if None:
                for None in None:
                    if None:
                        continue
                        continue
                        None = None
                        행 = None
                for None in :
                    if None:
                        if None:
                            continue
                        continue
                        , [], 리스트, x = None, 리스트
                        self.엑셀.ActiveSheet.Sort.SortFields.Clear()
        self.엑셀.ActiveSheet.Sort.SortFields.Add(Key = 두번째열부터.Columns(1), SortOn = 0, Order = 1, CustomOrder = ','.join(리스트), DataOption = 0)
        self.엑셀.ActiveSheet.Sort.SetRange(두번째열부터)
        self.엑셀.ActiveSheet.Sort.Header = 0
        self.엑셀.ActiveSheet.Sort.MatchCase = False
        self.엑셀.ActiveSheet.Sort.Orientation = 1
        self.엑셀.ActiveSheet.Sort.Apply()
        return None
        
        

    if (lambda self, 행수: 기준시트 = self.엑셀.ActiveSheet파일들 = None(title = 'Open File', filetypes = [
('Excel Files', '*.xlsx *.xls')])기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1기준열 = 20for 파일경로 in 파일들:
임시파일 = self.엑셀.Workbooks.Open(파일경로)임시시트 = 임시파일.Sheets(1)if 임시시트.AutoFilterMode:
passif 임시시트.AutoFilterMode:
임시시트.AutoFilterMode = False임시시트.Rows.Hidden = False임시시트.Columns.Hidden = False기준열 = 임시시트.UsedRange.Columns.Count + 1마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))붙임시트.Value = 복사시트.Value임시파일.Close(SaveChanges = False)기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1filedialog.askopenfilenames):
        
        def 취합(self, 행수):
            기준시트 = self.엑셀.ActiveSheet
            파일들 = None(title = 'Open File', filetypes = [
                ('Excel Files', '*.xlsx *.xls')])
            기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            기준열 = 20
            for 파일경로 in 파일들:
                임시파일 = self.엑셀.Workbooks.Open(파일경로)
                임시시트 = 임시파일.Sheets(1)
                if 임시시트.AutoFilterMode:
                    pass
                if 임시시트.AutoFilterMode:
                    임시시트.AutoFilterMode = False
                임시시트.Rows.Hidden = False
                임시시트.Columns.Hidden = False
                기준열 = 임시시트.UsedRange.Columns.Count + 1
                마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))
                붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))
                붙임시트.Value = 복사시트.Value
                임시파일.Close(SaveChanges = False)
                기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            filedialog.askopenfilenames

    
    def 선택파일시트취합(self):
        새워크북 = self.엑셀.Workbooks.Add()
        기준시트 = 새워크북.Sheets(1)
        파일들 = None(title = 'Open File', filetypes = [
            ('Excel Files', '*.xlsx *.xls')])
        로그 = '취합내용'
        for 파일경로 in 파일들:
            임시파일 = self.엑셀.Workbooks.Open(파일경로)
            이름 = 파일경로.split('/')[-1]
            매치 = None('\\((.*?)\\)', 이름)
            if 매치:
                pass
            괄호 = 매치.group(1) if 매치 else ''
            로그 += '\r\n\r\n' + 파일경로
            for 임시시트 in 임시파일.Sheets:
                임시시트.Copy(Before = 기준시트)
                복사된시트 = self.엑셀.ActiveSheet
                새이름 = ''
                if 괄호:
                    pass
                복사된시트.Name = 새이름[:31]
                로그 += '\r\n' + 새이름
            filedialog.askopenfilenames
            임시파일.Close(SaveChanges = False)
        return 로그

    if (lambda self, 행수: 기존엑셀 = self.엑셀.ActiveWorkbook새워크북 = self.엑셀.Workbooks.Add()기존엑셀.Sheets(1).Copy(After = 새워크북.Sheets(새워크북.Sheets.Count))기준시트 = self.엑셀.ActiveSheet기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1기준열 = 20for i in range(2, 기존엑셀.Sheets.Count + 1):
임시시트 = 기존엑셀.Sheets(i)if 임시시트.AutoFilterMode:
passif 임시시트.AutoFilterMode:
임시시트.AutoFilterMode = False임시시트.Rows.Hidden = False임시시트.Columns.Hidden = False기준열 = 임시시트.UsedRange.Columns.Count + 1마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))붙임시트.Value = 복사시트.Value기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1):
        
        def 시트취합(self, 행수):
            기존엑셀 = self.엑셀.ActiveWorkbook
            새워크북 = self.엑셀.Workbooks.Add()
            기존엑셀.Sheets(1).Copy(After = 새워크북.Sheets(새워크북.Sheets.Count))
            기준시트 = self.엑셀.ActiveSheet
            기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            기준열 = 20
            for i in range(2, 기존엑셀.Sheets.Count + 1):
                임시시트 = 기존엑셀.Sheets(i)
                if 임시시트.AutoFilterMode:
                    pass
                if 임시시트.AutoFilterMode:
                    임시시트.AutoFilterMode = False
                임시시트.Rows.Hidden = False
                임시시트.Columns.Hidden = False
                기준열 = 임시시트.UsedRange.Columns.Count + 1
                마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))
                붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))
                붙임시트.Value = 복사시트.Value
                기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1

    if (lambda self, 행수: 새워크북 = self.엑셀.Workbooks.Add()기준시트 = 새워크북.Sheets(1)파일들 = None(title = 'Open File', filetypes = [
('Excel Files', '*.xlsx *.xls')])로그 = '취합내용'시트이름 = []for 파일경로 in 파일들:
임시파일 = self.엑셀.Workbooks.Open(파일경로)로그 += '\r\n\r\n' + 파일경로for 임시시트 in 임시파일.Sheets:
로그 += '\r\n' + 임시시트.Nameif 임시시트.AutoFilterMode:
passif 임시시트.AutoFilterMode:
임시시트.AutoFilterMode = False임시시트.Rows.Hidden = False임시시트.Columns.Hidden = Falseif 임시시트.Name not in 시트이름:
시트이름.append(임시시트.Name)임시시트.Copy(Before = 기준시트)continueif not 임시시트.Name in 시트이름:
continue기준시트 = 새워크북.Sheets(임시시트.Name)기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1기준열 = 20기준열 = 임시시트.UsedRange.Columns.Count + 1마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))붙임시트.Value = 복사시트.Valuefiledialog.askopenfilenames임시파일.Close(SaveChanges = False)로그):
        
        def 이름별로취합하기(self, 행수):
            새워크북 = self.엑셀.Workbooks.Add()
            기준시트 = 새워크북.Sheets(1)
            파일들 = None(title = 'Open File', filetypes = [
                ('Excel Files', '*.xlsx *.xls')])
            로그 = '취합내용'
            시트이름 = []
            for 파일경로 in 파일들:
                임시파일 = self.엑셀.Workbooks.Open(파일경로)
                로그 += '\r\n\r\n' + 파일경로
                for 임시시트 in 임시파일.Sheets:
                    로그 += '\r\n' + 임시시트.Name
                    if 임시시트.AutoFilterMode:
                        pass
                    if 임시시트.AutoFilterMode:
                        임시시트.AutoFilterMode = False
                    임시시트.Rows.Hidden = False
                    임시시트.Columns.Hidden = False
                    if 임시시트.Name not in 시트이름:
                        시트이름.append(임시시트.Name)
                        임시시트.Copy(Before = 기준시트)
                        continue
                    if not 임시시트.Name in 시트이름:
                        continue
                    기준시트 = 새워크북.Sheets(임시시트.Name)
                    기준행 = 기준시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
                    기준열 = 20
                    기준열 = 임시시트.UsedRange.Columns.Count + 1
                    마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                    복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 기준열))
                    붙임시트 = 기준시트.Range(기준시트.Cells(기준행, 1), 기준시트.Cells(기준행 + 복사시트.Rows.Count - 1, 기준열))
                    붙임시트.Value = 복사시트.Value
                filedialog.askopenfilenames
                임시파일.Close(SaveChanges = False)
            return 로그

    
    def 항목서식(self):
        self.엑셀.Selection.Font.Size = 11
        self.엑셀.Selection.HorizontalAlignment = -4108
        self.엑셀.Selection.VerticalAlignment = -4108
        self.엑셀.Selection.Font.Name = '맑은 고딕'
        self.엑셀.Selection.Font.Color = 0
        self.엑셀.Selection.Font.Bold = True
        self.엑셀.Selection.Font.Italic = False
        self.엑셀.Selection.Font.Underline = False
        self.엑셀.Selection.Interior.Color = 16247775

    if (lambda self, 열번호: 기준시트 = self.엑셀.ActiveSheet끝행 = self.엑셀.Selection.Row시작행 = 기준시트.UsedRange.Rows(기준시트.UsedRange.Rows.Count).Rowfor 행 in range(시작행, 끝행, -1):
if not 기준시트.Cells(행, 열번호).Value and str(기준시트.Cells(행, 열번호).Value).strip() == '':
continue기준시트.Rows(행).Delete()):
        
        def 행제거(self, 열번호):
            기준시트 = self.엑셀.ActiveSheet
            끝행 = self.엑셀.Selection.Row
            시작행 = 기준시트.UsedRange.Rows(기준시트.UsedRange.Rows.Count).Row
            for 행 in range(시작행, 끝행, -1):
                if not 기준시트.Cells(행, 열번호).Value and str(기준시트.Cells(행, 열번호).Value).strip() == '':
                    continue
                기준시트.Rows(행).Delete()

    
    def 공무용차량기본글자(self):
        self.엑셀.Selection.Font.Color = 0
        self.엑셀.Selection.Font.Bold = False
        self.엑셀.Selection.Font.Italic = False
        self.엑셀.Selection.Font.Underline = False
        self.엑셀.Selection.Font.Strikethrough = False

    
    def 공무용차량운행개월(self):
        선택범위 = self.엑셀.Selection
        행개수 = 선택범위.Rows.Count
        오늘날짜 = None()
        작년 = 오늘날짜.year - 1
        기준날짜 = datetime(작년, 12, 31)
        for i in range(1, 행개수 + 1):
            선택범위.Cells(i, 1).NumberFormat = '@'
            if len(선택범위.Cells(i, 1).Text) == 5:
                기본날짜 = datetime(1900, 1, 1)
                변환날짜 = None + timedelta(days = int(선택범위.Cells(i, 1).Value) - 2)
                선택범위.Cells(i, 1).Value = 변환날짜.strftime('%Y-%m-%d')
            데이터 = 선택범위.Cells(i, 1).Text
            년도 = None('[^0-9]', '', 데이터)
            년 = int(년도[:4])
            월 = int(년도[4:6])
            일 = int(년도[6:])
            시작날짜 = datetime(년, 월, 일)
            운행개월수 = (기준날짜.year - 시작날짜.year) * 12 + (기준날짜.month - 시작날짜.month)
            if 기준날짜.day < 시작날짜.day:
                pass
            운행개월수 -= 1
            선택범위.Cells(i, 2).Value = 운행개월수
        기본날짜

    
    def 공무용차량제출서식(self):
        새워크북 = self.엑셀.Workbooks.Add()
        for None in range(7):
            if None:
                continue
        새워크북.Sheets(1).Name = '기본(입력)'
        워크시트 = 새워크북.Sheets('기본(입력)')
        워크시트.Range('A1:B1').Merge()
        워크시트.Range('A1:A15').HorizontalAlignment = -4108
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 16
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '기본정보입력(셀 위치 이동금지!)'
        워크시트.Columns('A').ColumnWidth = 20
        워크시트.Columns('B').ColumnWidth = 100
        워크시트.Range('A2').Value = '중앙행정기관명'
        워크시트.Range('A3').Value = '담당부서'
        워크시트.Range('A4').Value = '사무실 전화번호'
        워크시트.Range('A5').Value = '작성자 성명'
        워크시트.Range('A6').Value = '이메일 주소'
        워크시트.Range('A7').Value = '차량현황 공개위치'
        워크시트.Range('A8').Value = '홈페이지 주소'
        워크시트.Range('A9').Value = '공개내용'
        워크시트.Range('A10').Value = '공개시기(예정)'
        워크시트.Range('A11').Value = '정수 증가사유'
        워크시트.Range('A12').Value = '정수 감소사유'
        워크시트.Range('A13').Value = '(설문)배차방법'
        워크시트.Range('B2:B15').Font.Color = 12874308
        워크시트.Range('B2:B15').Font.Italic = True
        워크시트.Range('B2').Value = '행정안전부'
        워크시트.Range('B3').Value = '행정제도과'
        워크시트.Range('B4').Value = '044-205-2250'
        워크시트.Range('B5').Value = '범피스'
        워크시트.Range('B6').Value = 'nursing0705@korea.kr'
        워크시트.Range('B7').Value = '행정안전부 홈페이지-뉴스·소식-알립니다'
        워크시트.Range('B8').Value = 'https://mois.go.kr/frt/bbs/type013/commonSelectBoardList.do?bbsId=BBSMSTR_000000000006'
        워크시트.Range('B9').Value = '공무용 차량 정수 및 운영현황'
        워크시트.Range('B10').Value = '매년 2월'
        워크시트.Range('B11').Value = '해당사항 없음 / 순찰대 신설'
        워크시트.Range('B12').Value = '해당사항 없음 / 교체차량 불용 처리'
        워크시트.Range('B13').Value = '업무용 사이트 예약관리 시스템 활용 / 수기작성'
        새워크북.Sheets(2).Name = '정수(입력)'
        워크시트 = 새워크북.Sheets('정수(입력)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 30
        워크시트.Range('A1:AA1').Merge()
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = str + datetime.today(None().year - 2) + '년말 정수는 기 제출된 통계와 일치하여야 하며, 이와 다를 경우 별도 설명서 제출'
        워크시트.Columns('A').ColumnWidth = 20
        워크시트.Columns('B').ColumnWidth = 10
        워크시트.Columns('C:AA').ColumnWidth = 5
        워크시트.Range('A2:AA100').Font.Size = 9
        워크시트.Range('A2:AA100').HorizontalAlignment = -4108
        워크시트.Range('A2:AA2').Font.Bold = True
        워크시트.Range('A2').Value = '구분'
        워크시트.Range('B2').Value = '총계'
        워크시트.Range('C2').Value = '전용\n소계'
        워크시트.Range('D2').Value = '전용\n대형'
        워크시트.Range('E2').Value = '전용\n중형'
        워크시트.Range('F2').Value = '전용\n소형'
        워크시트.Range('G2').Value = '전용\n경형'
        워크시트.Range('H2').Value = '업무용\n소계'
        워크시트.Range('I2').Value = '업무용\n대형'
        워크시트.Range('J2').Value = '업무용\n중형'
        워크시트.Range('K2').Value = '업무용\n소형'
        워크시트.Range('L2').Value = '업무용\n경형'
        워크시트.Range('M2').Value = '승합용\n소계'
        워크시트.Range('N2').Value = '승합용\n대형'
        워크시트.Range('O2').Value = '승합용\n중형'
        워크시트.Range('P2').Value = '승합용\n소형'
        워크시트.Range('Q2').Value = '승합용\n경형'
        워크시트.Range('R2').Value = '화물용\n소계'
        워크시트.Range('S2').Value = '화물용\n대형'
        워크시트.Range('T2').Value = '화물용\n중형'
        워크시트.Range('U2').Value = '화물용\n소형'
        워크시트.Range('V2').Value = '화물용\n경형'
        워크시트.Range('W2').Value = '특수용\n소계'
        워크시트.Range('X2').Value = '특수용\n대형'
        워크시트.Range('Y2').Value = '특수용\n중형'
        워크시트.Range('Z2').Value = '특수용\n소형'
        워크시트.Range('AA2').Value = '특수용\n경형'
        워크시트.Range('A3:A14').Font.Color = 12874308
        워크시트.Range('A3:A14').Font.Italic = True
        워크시트.Range('D5:G14').Font.Color = 12874308
        워크시트.Range('D5:G14').Font.Italic = True
        워크시트.Range('I5:L14').Font.Color = 12874308
        워크시트.Range('I5:L14').Font.Italic = True
        워크시트.Range('N5:Q14').Font.Color = 12874308
        워크시트.Range('N5:Q14').Font.Italic = True
        워크시트.Range('S5:V14').Font.Color = 12874308
        워크시트.Range('S5:V14').Font.Italic = True
        워크시트.Range('X5:AA14').Font.Color = 12874308
        워크시트.Range('X5:AA14').Font.Italic = True
        워크시트.Range('X5:AA14').Font.Color = 12874308
        워크시트.Range('X5:AA14').Font.Italic = True
        워크시트.Range('B3:AA4').Interior.Color = 9502719
        워크시트.Range('B3:AA4').Font.Bold = True
        워크시트.Range('B3').Formula = '=SUM(C3,H3,M3,R3,W3)'
        워크시트.Range('B4').Formula = '=SUM(C4,H4,M4,R4,W4)'
        워크시트.Range('B5').Formula = '=SUM(C5,H5,M5,R5,W5)'
        워크시트.Range('B6').Formula = '=SUM(C6,H6,M6,R6,W6)'
        워크시트.Range('B7').Formula = '=SUM(C7,H7,M7,R7,W7)'
        워크시트.Range('B8').Formula = '=SUM(C8,H8,M8,R8,W8)'
        워크시트.Range('B9').Formula = '=SUM(C9,H9,M9,R9,W9)'
        워크시트.Range('B10').Formula = '=SUM(C10,H10,M10,R10,W10)'
        워크시트.Range('C3').Formula = '=SUM(D3:G3)'
        워크시트.Range('C4').Formula = '=SUM(D4:G4)'
        워크시트.Range('C5').Formula = '=SUM(D5:G5)'
        워크시트.Range('C6').Formula = '=SUM(D6:G6)'
        워크시트.Range('C7').Formula = '=SUM(D7:G7)'
        워크시트.Range('C8').Formula = '=SUM(D8:G8)'
        워크시트.Range('C9').Formula = '=SUM(D9:G9)'
        워크시트.Range('C10').Formula = '=SUM(D10:G10)'
        워크시트.Range('D3').Formula = '=SUMPRODUCT((MOD(ROW(D5:D100),2)=1)*D5:D100)'
        워크시트.Range('D4').Formula = '=SUMPRODUCT((MOD(ROW(D6:D100),2)=0)*D6:D100)'
        워크시트.Range('E3').Formula = '=SUMPRODUCT((MOD(ROW(E5:E100),2)=1)*E5:E100)'
        워크시트.Range('E4').Formula = '=SUMPRODUCT((MOD(ROW(E6:E100),2)=0)*E6:E100)'
        워크시트.Range('F3').Formula = '=SUMPRODUCT((MOD(ROW(F5:F100),2)=1)*F5:F100)'
        워크시트.Range('F4').Formula = '=SUMPRODUCT((MOD(ROW(F6:F100),2)=0)*F6:F100)'
        워크시트.Range('G3').Formula = '=SUMPRODUCT((MOD(ROW(G5:G100),2)=1)*G5:G100)'
        워크시트.Range('G4').Formula = '=SUMPRODUCT((MOD(ROW(G6:G100),2)=0)*G6:G100)'
        워크시트.Range('H3').Formula = '=SUM(I3:L3)'
        워크시트.Range('H4').Formula = '=SUM(I4:L4)'
        워크시트.Range('H5').Formula = '=SUM(I5:L5)'
        워크시트.Range('H6').Formula = '=SUM(I6:L6)'
        워크시트.Range('H7').Formula = '=SUM(I7:L7)'
        워크시트.Range('H8').Formula = '=SUM(I8:L8)'
        워크시트.Range('H9').Formula = '=SUM(I9:L9)'
        워크시트.Range('H10').Formula = '=SUM(I10:L10)'
        워크시트.Range('I3').Formula = '=SUMPRODUCT((MOD(ROW(I5:I100),2)=1)*I5:I100)'
        워크시트.Range('I4').Formula = '=SUMPRODUCT((MOD(ROW(I6:I100),2)=0)*I6:I100)'
        워크시트.Range('J3').Formula = '=SUMPRODUCT((MOD(ROW(J5:J100),2)=1)*J5:J100)'
        워크시트.Range('J4').Formula = '=SUMPRODUCT((MOD(ROW(J6:J100),2)=0)*J6:J100)'
        워크시트.Range('K3').Formula = '=SUMPRODUCT((MOD(ROW(K5:K100),2)=1)*K5:K100)'
        워크시트.Range('K4').Formula = '=SUMPRODUCT((MOD(ROW(K6:K100),2)=0)*K6:K100)'
        워크시트.Range('L3').Formula = '=SUMPRODUCT((MOD(ROW(L5:L100),2)=1)*L5:L100)'
        워크시트.Range('L4').Formula = '=SUMPRODUCT((MOD(ROW(L6:L100),2)=0)*L6:L100)'
        워크시트.Range('M3').Formula = '=SUM(N3:Q3)'
        워크시트.Range('M4').Formula = '=SUM(N4:Q4)'
        워크시트.Range('M5').Formula = '=SUM(N5:Q5)'
        워크시트.Range('M6').Formula = '=SUM(N6:Q6)'
        워크시트.Range('M7').Formula = '=SUM(N7:Q7)'
        워크시트.Range('M8').Formula = '=SUM(N8:Q8)'
        워크시트.Range('M9').Formula = '=SUM(N9:Q9)'
        워크시트.Range('M10').Formula = '=SUM(N10:Q10)'
        워크시트.Range('N3').Formula = '=SUMPRODUCT((MOD(ROW(N5:N100),2)=1)*N5:N100)'
        워크시트.Range('N4').Formula = '=SUMPRODUCT((MOD(ROW(N6:N100),2)=0)*N6:N100)'
        워크시트.Range('O3').Formula = '=SUMPRODUCT((MOD(ROW(O5:O100),2)=1)*O5:O100)'
        워크시트.Range('O4').Formula = '=SUMPRODUCT((MOD(ROW(O6:O100),2)=0)*O6:O100)'
        워크시트.Range('P3').Formula = '=SUMPRODUCT((MOD(ROW(P5:P100),2)=1)*P5:P100)'
        워크시트.Range('P4').Formula = '=SUMPRODUCT((MOD(ROW(P6:P100),2)=0)*P6:P100)'
        워크시트.Range('Q3').Formula = '=SUMPRODUCT((MOD(ROW(Q5:Q100),2)=1)*Q5:Q100)'
        워크시트.Range('Q4').Formula = '=SUMPRODUCT((MOD(ROW(Q6:Q100),2)=0)*Q6:Q100)'
        워크시트.Range('R3').Formula = '=SUM(S3:V3)'
        워크시트.Range('R4').Formula = '=SUM(S4:V4)'
        워크시트.Range('R5').Formula = '=SUM(S5:V5)'
        워크시트.Range('R6').Formula = '=SUM(S6:V6)'
        워크시트.Range('R7').Formula = '=SUM(S7:V7)'
        워크시트.Range('R8').Formula = '=SUM(S8:V8)'
        워크시트.Range('R9').Formula = '=SUM(S9:V9)'
        워크시트.Range('R10').Formula = '=SUM(S10:V10)'
        워크시트.Range('S3').Formula = '=SUMPRODUCT((MOD(ROW(S5:S100),2)=1)*S5:S100)'
        워크시트.Range('S4').Formula = '=SUMPRODUCT((MOD(ROW(S6:S100),2)=0)*S6:S100)'
        워크시트.Range('T3').Formula = '=SUMPRODUCT((MOD(ROW(T5:T100),2)=1)*T5:T100)'
        워크시트.Range('T4').Formula = '=SUMPRODUCT((MOD(ROW(T6:T100),2)=0)*T6:T100)'
        워크시트.Range('U3').Formula = '=SUMPRODUCT((MOD(ROW(U5:U100),2)=1)*U5:U100)'
        워크시트.Range('U4').Formula = '=SUMPRODUCT((MOD(ROW(U6:U100),2)=0)*U6:U100)'
        워크시트.Range('V3').Formula = '=SUMPRODUCT((MOD(ROW(V5:V100),2)=1)*V5:V100)'
        워크시트.Range('V4').Formula = '=SUMPRODUCT((MOD(ROW(V6:V100),2)=0)*V6:V100)'
        워크시트.Range('W3').Formula = '=SUM(X3:AA3)'
        워크시트.Range('W4').Formula = '=SUM(X4:AA4)'
        워크시트.Range('W5').Formula = '=SUM(X5:AA5)'
        워크시트.Range('W6').Formula = '=SUM(X6:AA6)'
        워크시트.Range('W7').Formula = '=SUM(X7:AA7)'
        워크시트.Range('W8').Formula = '=SUM(X8:AA8)'
        워크시트.Range('W9').Formula = '=SUM(X9:AA9)'
        워크시트.Range('W10').Formula = '=SUM(X10:AA10)'
        워크시트.Range('X3').Formula = '=SUMPRODUCT((MOD(ROW(X5:X100),2)=1)*X5:X100)'
        워크시트.Range('X4').Formula = '=SUMPRODUCT((MOD(ROW(X6:X100),2)=0)*X6:X100)'
        워크시트.Range('Y3').Formula = '=SUMPRODUCT((MOD(ROW(Y5:Y100),2)=1)*Y5:Y100)'
        워크시트.Range('Y4').Formula = '=SUMPRODUCT((MOD(ROW(Y6:Y100),2)=0)*Y6:Y100)'
        워크시트.Range('Z3').Formula = '=SUMPRODUCT((MOD(ROW(Z5:Z100),2)=1)*Z5:Z100)'
        워크시트.Range('Z4').Formula = '=SUMPRODUCT((MOD(ROW(Z6:Z100),2)=0)*Z6:Z100)'
        워크시트.Range('AA3').Formula = '=SUMPRODUCT((MOD(ROW(AA5:AA100),2)=1)*AA5:AA100)'
        워크시트.Range('AA4').Formula = '=SUMPRODUCT((MOD(ROW(AA6:AA100),2)=0)*AA6:AA100)'
        for 숫자 in range(2, 12, 2):
            워크시트.Range(f'''A{숫자}:AA{숫자}''').Borders(4).LineStyle = 1
        str + datetime.today(None().year - 1) + '.12.31.기준) ※전용=승용(전용), 업무용=승용(업무용)\n'
        워크시트.Range('A3').Value = str + datetime.today(None().year - 1)
        워크시트.Range('A4').Value = str + datetime.today(None().year - 2)
        워크시트.Range('A5').Value = str + datetime.today(None().year - 1)
        워크시트.Range('A6').Value = str + datetime.today(None().year - 2)
        워크시트.Range('A7').Value = str + datetime.today(None().year - 1)
        워크시트.Range('A8').Value = str + datetime.today(None().year - 2)
        워크시트.Range('A9').Value = str + datetime.today(None().year - 1)
        워크시트.Range('A10').Value = str + datetime.today(None().year - 2)
        새워크북.Sheets(3).Name = '전체차량(입력)'
        워크시트 = 새워크북.Sheets('전체차량(입력)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 80
        워크시트.Columns('A').ColumnWidth = 5
        워크시트.Columns('B').ColumnWidth = 20
        워크시트.Columns('C').ColumnWidth = 20
        워크시트.Columns('D').ColumnWidth = 15
        워크시트.Columns('E').ColumnWidth = 6
        워크시트.Columns('F').ColumnWidth = 7
        워크시트.Columns('G').ColumnWidth = 7
        워크시트.Columns('H').ColumnWidth = 20
        워크시트.Columns('I').ColumnWidth = 7
        워크시트.Columns('J').ColumnWidth = 12
        워크시트.Columns('K').ColumnWidth = 8
        워크시트.Columns('L').ColumnWidth = 9
        워크시트.Columns('M').ColumnWidth = 8
        워크시트.Columns('N').ColumnWidth = 8
        워크시트.Columns('O').ColumnWidth = 8
        워크시트.Columns('P').ColumnWidth = 8
        워크시트.Columns('A:P').HorizontalAlignment = -4108
        워크시트.Range('A1:P1').Merge()
        워크시트.Cells(1, 1).HorizontalAlignment = 1
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = str + datetime.today(None().year - 1) + '.12.31.기준) ※전용=승용(전용), 업무용=승용(업무용)\n 반드시 상단설명에 맞춰서 데이터 입력하세요!'
        워크시트.Range('A2:P2').Font.Size = 9
        워크시트.Range('A2:P2').Font.Bold = True
        워크시트.Range('A2').Value = '[순번]'
        워크시트.Range('B2').Value = '[본부명]'
        워크시트.Range('C2').Value = '[소속기관명]'
        워크시트.Range('D2').Value = '[차종]\n전용=승용(전용)\n업무용=승용(업무용)\n승합용\n화물용\n특수용'
        워크시트.Range('E2').Value = '[차형]\n대형\n중형\n소형\n경형'
        워크시트.Range('F2').Value = '[내용연수]\n숫자만\n9=9년'
        워크시트.Range('G2').Value = '[용도]\n업무\n순찰\n자유기입'
        워크시트.Range('H2').Value = '[차명]'
        워크시트.Range('I2').Value = '[배기량]\n숫자만\n2359\n=2,359cc'
        워크시트.Range('J2').Value = '[구입/임차일자]\n2111-11-11'
        워크시트.Range('K2').Value = '[운행기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('L2').Value = '[주행거리]\nKm\n숫자만\n30000\n=30,000Km'
        워크시트.Range('M2').Value = '[임차여부]\n1 또는 0\n1=임차O\n0=임차X'
        워크시트.Range('N2').Value = '[임차]\n[계약기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('O2').Value = '[환경친화]\n[차량표시]\n전기\n수소\n하이브리드'
        워크시트.Range('P2').Value = '[블랙박스]\n[설치여부]\n1 또는 0\n1=블박있음\n0=블박없음'
        워크시트.Range('A3:P5').Font.Color = 12874308
        워크시트.Range('A3:P5').Font.Italic = True
        워크시트.Range('D3:D300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '전용,업무용,승합용,화물용,특수용')
        워크시트.Range('E3:E300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '대형,중형,소형,경형')
        워크시트.Range('M3:M300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '1,0')
        워크시트.Range('O3:O300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '전기, 수소, 하이브리드')
        워크시트.Range('P3:P300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '1,0')
        워크시트.Range('A3').Value = '1'
        워크시트.Range('B3').Value = '행정안전부'
        워크시트.Range('C3').Value = '본부'
        워크시트.Range('D3').Value = '전용'
        워크시트.Range('E3').Value = '대형'
        워크시트.Range('F3').Value = '8'
        워크시트.Range('G3').Value = '업무'
        워크시트.Range('H3').Value = 'Electrified G80'
        워크시트.Range('I3').Value = '0'
        워크시트.Range('J3').Value = '2023-1-1'
        워크시트.Range('K3').Value = '24'
        워크시트.Range('L3').Value = '31234'
        워크시트.Range('M3').Value = '1'
        워크시트.Range('N3').Value = '36'
        워크시트.Range('O3').Value = '전기'
        워크시트.Range('P3').Value = '1'
        워크시트.Range('A4').Value = '2'
        워크시트.Range('B4').Value = '행정안전부'
        워크시트.Range('C4').Value = '본부'
        워크시트.Range('D4').Value = '업무용'
        워크시트.Range('E4').Value = '중형'
        워크시트.Range('F4').Value = '8'
        워크시트.Range('G4').Value = '업무'
        워크시트.Range('H4').Value = '쏘나타'
        워크시트.Range('I4').Value = '1999'
        워크시트.Range('J4').Value = '2020-6-17'
        워크시트.Range('K4').Value = '66'
        워크시트.Range('L4').Value = '71234'
        워크시트.Range('M4').Value = ''
        워크시트.Range('N4').Value = ''
        워크시트.Range('O4').Value = ''
        워크시트.Range('P4').Value = '1'
        새워크북.Sheets(4).Name = '전용차량(입력)'
        워크시트 = 새워크북.Sheets('전용차량(입력)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 80
        워크시트.Columns('A').ColumnWidth = 5
        워크시트.Columns('B').ColumnWidth = 20
        워크시트.Columns('C').ColumnWidth = 15
        워크시트.Columns('D').ColumnWidth = 20
        워크시트.Columns('E').ColumnWidth = 45
        워크시트.Columns('F').ColumnWidth = 25
        워크시트.Columns('G').ColumnWidth = 10
        워크시트.Columns('H').ColumnWidth = 10
        워크시트.Columns('I').ColumnWidth = 10
        워크시트.Columns('A:I').HorizontalAlignment = -4108
        워크시트.Range('A1:I1').Merge()
        워크시트.Cells(1, 1).HorizontalAlignment = 1
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '전용차량 배정근거'
        워크시트.Range('A2').Value = '[순번]'
        워크시트.Range('B2').Value = '[본부명]'
        워크시트.Range('C2').Value = '[급]\n총리급, 부총리급\n장관급, 차관급'
        워크시트.Range('D2').Value = '[배정대상]'
        워크시트.Range('E2').Value = '[배정근거]'
        워크시트.Range('F2').Value = '[차명]'
        워크시트.Range('G2').Value = '[친환경]\n전기\n수소\n하이브리드'
        워크시트.Range('H2').Value = '[임차여부]\n1 또는 0\n1=임차O\n0=임차X'
        워크시트.Range('I2').Value = '[임차]\n[계약기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('A2:I2').Font.Bold = True
        워크시트.Range('A3:I8').Font.Color = 12874308
        워크시트.Range('A3:I8').Font.Italic = True
        워크시트.Range('A3').Value = '1'
        워크시트.Range('B3').Value = '행정안전부'
        워크시트.Range('C3').Value = '장관급'
        워크시트.Range('D3').Value = '장관'
        워크시트.Range('E3').Value = '행정안전부와 그 소속기관 직제 별표1'
        워크시트.Range('F3').Value = '제네시스 G90'
        워크시트.Range('G3').Value = ''
        워크시트.Range('H3').Value = '1'
        워크시트.Range('I3').Value = '36'
        워크시트.Range('A4').Value = '2'
        워크시트.Range('B4').Value = '행정안전부'
        워크시트.Range('C4').Value = '차관급'
        워크시트.Range('D4').Value = '차관'
        워크시트.Range('E4').Value = '행정안전부와 그 소속기관 직제 별표1'
        워크시트.Range('F4').Value = '제네시스 G90'
        워크시트.Range('G4').Value = ''
        워크시트.Range('H4').Value = '1'
        워크시트.Range('I4').Value = '36'
        워크시트.Range('A5').Value = '3'
        워크시트.Range('B5').Value = '행정안전부'
        워크시트.Range('C5').Value = '차관급'
        워크시트.Range('D5').Value = '본부장'
        워크시트.Range('E5').Value = '행정안전부와 그 소속기관 직제 별표1'
        워크시트.Range('F5').Value = '제네시스 GV80'
        워크시트.Range('G5').Value = ''
        워크시트.Range('H5').Value = '1'
        워크시트.Range('I5').Value = '36'
        워크시트.Range('A6').Value = '4'
        워크시트.Range('B6').Value = '행정안전부'
        워크시트.Range('C6').Value = '차관급'
        워크시트.Range('D6').Value = '이북5도 도지사'
        워크시트.Range('E6').Value = '이북5도 등에 관한 특별조치법 제5조제1항, 제2항'
        워크시트.Range('F6').Value = 'Electrified 제네시스 G80'
        워크시트.Range('G6').Value = '전기'
        워크시트.Range('H6').Value = '1'
        워크시트.Range('I6').Value = '36'
        새워크북.Sheets(5).Name = '지정차량(입력)'
        워크시트 = 새워크북.Sheets('지정차량(입력)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 80
        워크시트.Columns('A').ColumnWidth = 5
        워크시트.Columns('B').ColumnWidth = 20
        워크시트.Columns('C').ColumnWidth = 15
        워크시트.Columns('D').ColumnWidth = 20
        워크시트.Columns('E').ColumnWidth = 20
        워크시트.Columns('F').ColumnWidth = 25
        워크시트.Columns('G').ColumnWidth = 10
        워크시트.Columns('H').ColumnWidth = 10
        워크시트.Columns('I').ColumnWidth = 10
        워크시트.Columns('A:I').HorizontalAlignment = -4108
        워크시트.Range('A1:I1').Merge()
        워크시트.Cells(1, 1).HorizontalAlignment = 1
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '지정차량 보유현황'
        워크시트.Range('A2').Value = '[순번]'
        워크시트.Range('B2').Value = '[본부명]'
        워크시트.Range('C2').Value = '[소속기관명]'
        워크시트.Range('D2').Value = '[배정대상 직급]'
        워크시트.Range('E2').Value = '[배정대상 직위]'
        워크시트.Range('F2').Value = '[차명]'
        워크시트.Range('G2').Value = '[친환경]\n전기\n수소\n하이브리드'
        워크시트.Range('H2').Value = '[임차여부]\n1 또는 0\n1=임차O\n0=임차X'
        워크시트.Range('I2').Value = '[임차]\n[계약기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('A2:I2').Font.Bold = True
        워크시트.Range('A3:I8').Font.Color = 12874308
        워크시트.Range('A3:I8').Font.Italic = True
        워크시트.Range('B3').Value = '해'
        워크시트.Range('C3').Value = '당'
        워크시트.Range('D3').Value = '없'
        워크시트.Range('E3').Value = '음'
        새워크북.Sheets(6).Name = '신규차량(반자동)'
        워크시트 = 새워크북.Sheets('신규차량(반자동)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 80
        워크시트.Columns('A').ColumnWidth = 5
        워크시트.Columns('B').ColumnWidth = 20
        워크시트.Columns('C').ColumnWidth = 20
        워크시트.Columns('D').ColumnWidth = 15
        워크시트.Columns('E').ColumnWidth = 6
        워크시트.Columns('F').ColumnWidth = 7
        워크시트.Columns('G').ColumnWidth = 7
        워크시트.Columns('H').ColumnWidth = 20
        워크시트.Columns('I').ColumnWidth = 7
        워크시트.Columns('J').ColumnWidth = 12
        워크시트.Columns('K').ColumnWidth = 8
        워크시트.Columns('L').ColumnWidth = 9
        워크시트.Columns('M').ColumnWidth = 8
        워크시트.Columns('N').ColumnWidth = 8
        워크시트.Columns('O').ColumnWidth = 8
        워크시트.Columns('P').ColumnWidth = 8
        워크시트.Columns('Q').ColumnWidth = 9
        워크시트.Columns('A:Q').HorizontalAlignment = -4108
        워크시트.Range('A1:P1').Merge()
        워크시트.Cells(1, 1).HorizontalAlignment = 1
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = str + datetime.today(None().year - 1) + '.12.31.기준) ※전용=승용(전용), 업무용=승용(업무용)\n 반드시 상단설명에 맞춰서 데이터 입력하세요!'
        워크시트.Range('A2:Q2').Font.Size = 9
        워크시트.Range('A2:Q2').Font.Bold = True
        워크시트.Range('A2').Value = '[순번]'
        워크시트.Range('B2').Value = '[본부명]'
        워크시트.Range('C2').Value = '[소속기관명]'
        워크시트.Range('D2').Value = '[차종]\n전용=승용(전용)\n업무용=승용(업무용)\n승합용\n화물용\n특수용'
        워크시트.Range('E2').Value = '[차형]\n대형\n중형\n소형\n경형'
        워크시트.Range('F2').Value = '[내용연수]\n숫자만\n9=9년'
        워크시트.Range('G2').Value = '[용도]\n업무\n순찰\n자유기입'
        워크시트.Range('H2').Value = '[차명]'
        워크시트.Range('I2').Value = '[배기량]\n숫자만\n2359\n=2,359cc'
        워크시트.Range('J2').Value = '[구입/임차일자]\n2111-11-11'
        워크시트.Range('K2').Value = '[운행기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('L2').Value = '[주행거리]\nKm\n숫자만\n30000\n=30,000Km'
        워크시트.Range('M2').Value = '[임차여부]\n1 또는 0\n1=임차O\n0=임차X'
        워크시트.Range('N2').Value = '[임차]\n[계약기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('O2').Value = '[환경친화]\n[차량표시]\n전기\n수소\n하이브리드'
        워크시트.Range('P2').Value = '[블랙박스]\n[설치여부]\n1 또는 0\n1=블박있음\n0=블박없음'
        워크시트.Range('Q2').Value = '[환경친화적]\n[차량구입]\n[대상여부]\n1 또는 0\n1=대상\n0=미대상'
        새워크북.Sheets(7).Name = '처분차량(입력)'
        워크시트 = 새워크북.Sheets('처분차량(입력)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 80
        워크시트.Columns('A').ColumnWidth = 5
        워크시트.Columns('B').ColumnWidth = 20
        워크시트.Columns('C').ColumnWidth = 20
        워크시트.Columns('D').ColumnWidth = 15
        워크시트.Columns('E').ColumnWidth = 6
        워크시트.Columns('F').ColumnWidth = 7
        워크시트.Columns('G').ColumnWidth = 7
        워크시트.Columns('H').ColumnWidth = 20
        워크시트.Columns('I').ColumnWidth = 12
        워크시트.Columns('J').ColumnWidth = 12
        워크시트.Columns('K').ColumnWidth = 8
        워크시트.Columns('L').ColumnWidth = 9
        워크시트.Columns('M').ColumnWidth = 15
        워크시트.Columns('N').ColumnWidth = 20
        워크시트.Columns('A:N').HorizontalAlignment = -4108
        워크시트.Range('A1:N1').Merge()
        워크시트.Cells(1, 1).HorizontalAlignment = 1
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = str + datetime.today(None().year - 1) + '.12.31.기준) ※전용=승용(전용), 업무용=승용(업무용)\n 반드시 상단설명에 맞춰서 데이터 입력하세요!'
        워크시트.Range('A2:N2').Font.Size = 9
        워크시트.Range('A2:N2').Font.Bold = True
        워크시트.Range('A2').Value = '[순번]'
        워크시트.Range('B2').Value = '[본부명]'
        워크시트.Range('C2').Value = '[소속기관명]'
        워크시트.Range('D2').Value = '[차종]\n전용=승용(전용)\n업무용=승용(업무용)\n승합용\n화물용\n특수용'
        워크시트.Range('E2').Value = '[차형]\n대형\n중형\n소형\n경형'
        워크시트.Range('F2').Value = '[내용연수]\n숫자만\n9=9년'
        워크시트.Range('G2').Value = '[용도]\n업무\n순찰\n자유기입'
        워크시트.Range('H2').Value = '[차명]'
        워크시트.Range('I2').Value = '[구입/임차일자]\n2111-11-11'
        워크시트.Range('J2').Value = '[등록말소일]\n2111-11-11'
        워크시트.Range('K2').Value = '[운행기간]\n개월수\n숫자만\n36=3년'
        워크시트.Range('L2').Value = '[주행거리]\nKm\n숫자만\n30000\n=30,000Km'
        워크시트.Range('M2').Value = '[처분방법]\n매각\n양여\n폐기\n임차반납\n기타등등'
        워크시트.Range('N2').Value = '[미준수 사유]\n최단운행년한 및\n최단주행거리\n미준수의 경우\n미준수 사유'
        워크시트.Range('D3:D300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '전용,업무용,승합용,화물용,특수용')
        워크시트.Range('E3:E300').Validation.Add(Type = 3, AlertStyle = 1, Operator = 1, Formula1 = '대형,중형,소형,경형')
        워크시트.Range('A3:M4').Font.Color = 12874308
        워크시트.Range('A3:M4').Font.Italic = True
        워크시트.Range('A3').Value = '1'
        워크시트.Range('B3').Value = '행정안전부'
        워크시트.Range('C3').Value = '본부'
        워크시트.Range('D3').Value = '업무용'
        워크시트.Range('E3').Value = '중형'
        워크시트.Range('F3').Value = '8'
        워크시트.Range('G3').Value = '업무'
        워크시트.Range('H3').Value = '니로 하이브리드'
        워크시트.Range('I3').Value = '2020-05-01'
        워크시트.Range('J3').Value = '2024-05-01'
        워크시트.Range('K3').Formula = '=DATEDIF(I3,J3,"m")'
        워크시트.Range('L3').Value = '31234'
        워크시트.Range('M3').Value = '임차반납'
        워크시트.Range('A4').Value = '2'
        워크시트.Range('B4').Value = '행정안전부'
        워크시트.Range('C4').Value = '본부'
        워크시트.Range('D4').Value = '화물용'
        워크시트.Range('E4').Value = '소형'
        워크시트.Range('F4').Value = '9'
        워크시트.Range('G4').Value = '업무'
        워크시트.Range('H4').Value = '포터2'
        워크시트.Range('I4').Value = '2010-12-01'
        워크시트.Range('J4').Value = '2024-12-01'
        워크시트.Range('K4').Formula = '=DATEDIF(I4,J4,"m")'
        워크시트.Range('L4').Value = '123456'
        워크시트.Range('M4').Value = '폐기'
        새워크북.Sheets(8).Name = '최종계산(자동)'
        워크시트 = 새워크북.Sheets('최종계산(자동)')
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 30
        워크시트.Range('A1:AA1').Merge()
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = str + datetime.today(None().year - 1) + '.12.31.기준)'
        워크시트.Columns('A').ColumnWidth = 20
        워크시트.Columns('B').ColumnWidth = 10
        워크시트.Columns('C:AA').ColumnWidth = 5
        워크시트.Range('A2:AA100').Font.Size = 9
        워크시트.Range('A2:AA100').HorizontalAlignment = -4108
        워크시트.Range('A2:AA2').Font.Bold = True
        워크시트.Range('A2').Value = '구분'
        워크시트.Range('B2').Value = '총계'
        워크시트.Range('C2').Value = '전용\n소계'
        워크시트.Range('D2').Value = '전용\n대형'
        워크시트.Range('E2').Value = '전용\n중형'
        워크시트.Range('F2').Value = '전용\n소형'
        워크시트.Range('G2').Value = '전용\n경형'
        워크시트.Range('H2').Value = '업무용\n소계'
        워크시트.Range('I2').Value = '업무용\n대형'
        워크시트.Range('J2').Value = '업무용\n중형'
        워크시트.Range('K2').Value = '업무용\n소형'
        워크시트.Range('L2').Value = '업무용\n경형'
        워크시트.Range('M2').Value = '승합용\n소계'
        워크시트.Range('N2').Value = '승합용\n대형'
        워크시트.Range('O2').Value = '승합용\n중형'
        워크시트.Range('P2').Value = '승합용\n소형'
        워크시트.Range('Q2').Value = '승합용\n경형'
        워크시트.Range('R2').Value = '화물용\n소계'
        워크시트.Range('S2').Value = '화물용\n대형'
        워크시트.Range('T2').Value = '화물용\n중형'
        워크시트.Range('U2').Value = '화물용\n소형'
        워크시트.Range('V2').Value = '화물용\n경형'
        워크시트.Range('W2').Value = '특수용\n소계'
        워크시트.Range('X2').Value = '특수용\n대형'
        워크시트.Range('Y2').Value = '특수용\n중형'
        워크시트.Range('Z2').Value = '특수용\n소형'
        워크시트.Range('AA2').Value = '특수용\n경형'
        워크시트.Range('A3:A21').Font.Size = 11
        워크시트.Range('A3').Value = '정수-보유 차이'
        워크시트.Range('A4').Value = '[정수] 차이'
        워크시트.Range('A5').Value = str + datetime.today(None().year - 1)
        워크시트.Range('A6').Value = str + datetime.today(None().year - 2)
        워크시트.Range('A7').Value = '[보유]'
        워크시트.Range('A8').Value = '[보유] 구매'
        워크시트.Range('A9').Value = '[보유] 임차'
        워크시트.Range('A10').Value = '[신규]'
        워크시트.Range('A11').Value = '[신규] 구매'
        워크시트.Range('A12').Value = '[신규] 임차'
        워크시트.Range('A13').Value = '[처분]'
        워크시트.Range('A14').Value = '[처분] 구매'
        워크시트.Range('A15').Value = '[처분] 임차'
        워크시트.Range('B16').Value = '총계'
        워크시트.Range('C16').Value = '전용'
        워크시트.Range('D16').Value = '업무용'
        워크시트.Range('E16').Value = '승합용'
        워크시트.Range('F16').Value = '화물용'
        워크시트.Range('G16').Value = '특수용'
        워크시트.Range('A17').Value = '[처분] 구매 개월 합산'
        워크시트.Range('A18').Value = '[처분] 임차 개월 합산'
        워크시트.Range('A19').Value = '[처분] 구매 Km 합산'
        워크시트.Range('A20').Value = '[처분] 임차 Km 합산'
        워크시트.Range('A21').Value = '[블랙박스] 개수'

    
    def 공무용차량오타찾기(self):
        워크시트 = self.엑셀.Worksheets('전체차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        데이터 = 워크시트.Range(f'''D3:E{마지막행}''').Value
        변환데이터 = []
        for 줄 in 데이터:
            변환줄 = []
            for None in enumerate(줄):
                if ():
                    if isinstance(아이템, float):
                        pass
                    if isinstance(아이템, float):
                        변환줄.append(int(아이템))
                        continue
                    if 아이템:
                        continue
                    continue
                    ()
                    변환데이터.append(tuple(변환줄))
                    continue
        for None in :
            if ():
                if not 아이템[0] not in ('전용', '업무용', '승합용', '화물용', '특수용'):
                    continue
                continue
                None = , []
                아이템 = None, '[오타목록]\r\n이줄 밑으로 아무것도 없으면 정상입니다!\r\n\r\n', enumerate(변환데이터)
                if 전체차량차종이상:
                    pass
                if not 전체차량차종이상:
                    전체차량차종이상 = ''
                else:
                    전체차량차종이상 = '전체차량(입력) 시트에서 [차종] 고치세요!\r\n허용되는 입력값 [전용, 업무용, 승합용, 화물용, 특수용]\r\n오타위치 ' + ', '.join(map(str, 전체차량차종이상)) + '\r\n\r\n\r\n'
                for None in :
                    if ():
                        if not 아이템[1] not in ('대형', '중형', '소형', '경형'):
                            continue
                        continue
                        None = , []
                        아이템 = None, None, enumerate(변환데이터)
                        if 전체차량차형이상:
                            pass
                        if not 전체차량차형이상:
                            전체차량차형이상 = ''
                        else:
                            전체차량차형이상 = '전체차량(입력) 시트에서 [차형] 고치세요!\r\n허용되는 입력값 [대형, 중형, 소형, 경형]\r\n오타위치 ' + ', '.join(map(str, 전체차량차형이상)) + '\r\n\r\n\r\n'
                        데이터 = 워크시트.Range(f'''M3:P{마지막행}''').Value
                        변환데이터 = []
                        for 줄 in 데이터:
                            변환줄 = []
                            for None in enumerate(줄):
                                if ():
                                    if isinstance(아이템, float):
                                        pass
                                    if isinstance(아이템, float):
                                        변환줄.append(int(아이템))
                                        continue
                                    if 아이템:
                                        continue
                                    continue
                                    ()
                                    변환데이터.append(tuple(변환줄))
                                    continue
        for None in :
            if ():
                if not 아이템[0] not in (1, 0, ''):
                    continue
                continue
                None = , []
                아이템 = None, None, enumerate(변환데이터)
                if 전체차량임차여부이상:
                    pass
                if not 전체차량임차여부이상:
                    전체차량임차여부이상 = ''
                else:
                    전체차량임차여부이상 = '전체차량(입력) 시트에서 [임차여부] 고치세요!\r\n허용되는 입력값 [1, 0, 빈값]\r\n오타위치 ' + ', '.join(map(str, 전체차량임차여부이상)) + '\r\n\r\n\r\n'
                for None in :
                    if ():
                        if not 아이템[3] not in (1, 0, ''):
                            continue
                        continue
                        None = , []
                        아이템 = None, None, enumerate(변환데이터)
                        if 전체차량블랙박스이상:
                            pass
                        if not 전체차량블랙박스이상:
                            전체차량블랙박스이상 = ''
                        else:
                            전체차량블랙박스이상 = '전체차량(입력) 시트에서 [블랙박스] 고치세요!\r\n허용되는 입력값 [1, 0, 빈값]\r\n오타위치 ' + ', '.join(map(str, 전체차량블랙박스이상)) + '\r\n\r\n\r\n'
                        워크시트 = self.엑셀.Worksheets('처분차량(입력)')
                        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        데이터 = 워크시트.Range(f'''D3:E{마지막행}''').Value
        변환데이터 = []
        for 줄 in 데이터:
            변환줄 = []
            for None in enumerate(줄):
                if ():
                    if isinstance(아이템, float):
                        pass
                    if isinstance(아이템, float):
                        변환줄.append(int(아이템))
                        continue
                    if 아이템:
                        continue
                    continue
                    ()
                    변환데이터.append(tuple(변환줄))
                    continue
        for None in :
            if ():
                if not 아이템[0] not in ('전용', '업무용', '승합용', '화물용', '특수용'):
                    continue
                continue
                None = , []
                아이템 = None, None, enumerate(변환데이터)
                if 처분차량차종이상:
                    pass
                if not 처분차량차종이상:
                    처분차량차종이상 = ''
                else:
                    처분차량차종이상 = '처분차량(입력) 시트에서 [차종] 고치세요!\r\n허용되는 입력값 [전용, 업무용, 승합용, 화물용, 특수용]\r\n오타위치 ' + ', '.join(map(str, 처분차량차종이상)) + '\r\n\r\n\r\n'
                for None in :
                    if ():
                        if not 아이템[1] not in ('대형', '중형', '소형', '경형'):
                            continue
                        continue
                        None = , []
                        아이템 = None, None, enumerate(변환데이터)
                        if 처분차량차형이상:
                            pass
                        if not 처분차량차형이상:
                            처분차량차형이상 = ''
                        else:
                            처분차량차형이상 = '처분차량(입력) 시트에서 [차형] 고치세요!\r\n허용되는 입력값 [대형, 중형, 소형, 경형]\r\n오타위치 ' + ', '.join(map(str, 처분차량차형이상)) + '\r\n\r\n\r\n'
                        return 안내내용 + 전체차량차종이상 + 전체차량차형이상 + 전체차량임차여부이상 + 전체차량블랙박스이상 + 처분차량차종이상 + 처분차량차형이상
                    
                    
                    
                    
                    

    
    def 공무용차량신규자동(self):
        워크시트 = self.엑셀.Worksheets('전체차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        기본날짜 = datetime(1900, 1, 1)
        for 셀 in 워크시트.Range(f'''J3:J{마지막행}'''):
            셀.NumberFormat = '@'
            if not len(셀.Text) == 5:
                continue
            기본날짜 = datetime(1900, 1, 1)
            변환날짜 = None + timedelta(days = int(셀.Value) - 2)
            셀.Value = 변환날짜.strftime('%Y-%m-%d')
        데이터 = 워크시트.Range(f'''A3:P{마지막행}''').Value
        변환데이터 = []
        for 줄 in 데이터:
            변환줄 = []
            for None in enumerate(줄):
                if ():
                    if i == 9:
                        변환줄.append(str(아이템)[:10])
                        continue
                    if isinstance(아이템, float):
                        pass
                    if isinstance(아이템, float):
                        변환줄.append(int(아이템))
                        continue
                    if 아이템:
                        continue
                    continue
                    ()
                    변환데이터.append(tuple(변환줄))
                    continue
        for None in :
            if None:
                if not None[9][:4] == str(작년):
                    continue
                continue
                None().year - 1, 변환데이터, 필터데이터, 줄 = datetime.today
                워크시트 = self.엑셀.Worksheets('신규차량(반자동)')
                워크시트.Rows('4:' + str(워크시트.Rows.Count)).Delete()
                for None in enumerate(필터데이터, start = 3):
                    if ():
                        for 열, 값 in enumerate(줄, start = 1):
                            워크시트.Cells(행, 열).Value = 값
                        continue
                        return None
                        

    
    def 공무용차량정수증감분석하기(self):
        워크시트 = self.엑셀.Worksheets('정수(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 1).End(-4162).Row
        데이터 = 워크시트.Range(f'''A5:AA{마지막행}''').Value
        for None in :
            if None:
                for None in :
                    if None:
                        continue
                        continue
                        , []
                        None, None, 데이터, 데이터0처리 = None
                        줄 = None
                        x = None
                        데이터1 = 데이터0처리[::2]
                        데이터2 = 데이터0처리[1::2]
                        for None in :
                            if None:
                                continue
                                None, 데이터1, 데이터1숫자, 줄 = None
                                for None in :
                                    pass
                                , [], 데이터1숫자합 = None, zip(데이터1숫자)
                                열 = None
        데이터1합계 = [
            str + datetime.today(None().year - 1)] + 데이터1숫자합
        for None in :
            if None:
                continue
                None, 데이터2, 데이터2숫자, 줄 = '총괄 '
                for None in :
                    pass
                , [], 데이터2숫자합 = None, zip(데이터2숫자)
                열 = None
        데이터2합계 = [
            str + datetime.today(None().year - 2)] + 데이터2숫자합
        for a, b in :
            pass
        , []
        None, '총괄 ', None, [
            '총괄 증감'], zip(데이터1합계[1:], 데이터2합계[1:]) + b, a = None
        최종리스트 = []
        최종리스트.append(데이터총괄증감)
        최종리스트.append(데이터1합계)
        최종리스트.append(데이터2합계)
        개별증감 = []
        for 데이1, 데이2 in zip(데이터1, 데이터2):
            제목 = None('\\d+', '', 데이1[0]).strip()
            for a, b in :
                pass
            , []
            데이터차이 = None, re.sub, zip(데이1[1:], 데이2[1:])
            a = None
            b = None
            개별증감.append([
                제목 + ' 증감'] + 데이터차이)
        for 증감, 데이1, 데이2 in zip(개별증감, 데이터1, 데이터2):
            최종리스트.append(증감)
            최종리스트.append(데이1)
            최종리스트.append(데이2)
        새워크북 = self.엑셀.Workbooks.Add()
        워크시트 = 새워크북.Sheets(1)
        워크시트.Rows(1).RowHeight = 40
        워크시트.Rows(2).RowHeight = 30
        워크시트.Range('A1:AA1').Merge()
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 14
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '공무용차량 정수증감 분석하기'
        워크시트.Columns('A').ColumnWidth = 20
        워크시트.Columns('B').ColumnWidth = 10
        워크시트.Columns('C:AA').ColumnWidth = 5
        워크시트.Range('A2:AA100').Font.Size = 9
        워크시트.Range('A2:AA100').HorizontalAlignment = -4108
        워크시트.Range('A2:AA2').Font.Bold = True
        워크시트.Range('A2').Value = '구분'
        워크시트.Range('B2').Value = '총계'
        워크시트.Range('C2').Value = '전용\n소계'
        워크시트.Range('D2').Value = '전용\n대형'
        워크시트.Range('E2').Value = '전용\n중형'
        워크시트.Range('F2').Value = '전용\n소형'
        워크시트.Range('G2').Value = '전용\n경형'
        워크시트.Range('H2').Value = '업무용\n소계'
        워크시트.Range('I2').Value = '업무용\n대형'
        워크시트.Range('J2').Value = '업무용\n중형'
        워크시트.Range('K2').Value = '업무용\n소형'
        워크시트.Range('L2').Value = '업무용\n경형'
        워크시트.Range('M2').Value = '승합용\n소계'
        워크시트.Range('N2').Value = '승합용\n대형'
        워크시트.Range('O2').Value = '승합용\n중형'
        워크시트.Range('P2').Value = '승합용\n소형'
        워크시트.Range('Q2').Value = '승합용\n경형'
        워크시트.Range('R2').Value = '화물용\n소계'
        워크시트.Range('S2').Value = '화물용\n대형'
        워크시트.Range('T2').Value = '화물용\n중형'
        워크시트.Range('U2').Value = '화물용\n소형'
        워크시트.Range('V2').Value = '화물용\n경형'
        워크시트.Range('W2').Value = '특수용\n소계'
        워크시트.Range('X2').Value = '특수용\n대형'
        워크시트.Range('Y2').Value = '특수용\n중형'
        워크시트.Range('Z2').Value = '특수용\n소형'
        워크시트.Range('AA2').Value = '특수용\n경형'
        for 행, 줄 in enumerate(최종리스트, start = 3):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        return None
        
        
        
        
        
        
        
        

    
    def 공무용차량총괄계산(self):
        워크시트 = self.엑셀.Worksheets('정수(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 1).End(-4162).Row
        정수데이터 = 워크시트.Range(f'''A5:AA{마지막행}''').Value
        for None in :
            if None:
                for None in :
                    if None:
                        continue
                        continue
                        , []
                        None, None, 정수데이터, 정수데이터0처리 = None
                        줄 = None
                        x = None
                        정수데이터1 = 정수데이터0처리[::2]
                        정수데이터2 = 정수데이터0처리[1::2]
                        for None in :
                            if None:
                                continue
                                None, 정수데이터1, 정수데이터1숫자, 줄 = None
                                for None in :
                                    pass
                                , [], 정수데이터1숫자합 = None, zip(정수데이터1숫자)
                                열 = None
        정수데이터1합계 = [
            str + datetime.today(None().year - 1)] + 정수데이터1숫자합
        for None in :
            if None:
                continue
                None, 정수데이터2, 정수데이터2숫자, 줄 = '[정수] '
                for None in :
                    pass
                , [], 정수데이터2숫자합 = None, zip(정수데이터2숫자)
                열 = None
        정수데이터2합계 = [
            str + datetime.today(None().year - 2)] + 정수데이터2숫자합
        for a, b in :
            pass
        , []
        None, '[정수] ', None, [
            '[정수] 증감'], zip(정수데이터1합계[1:], 정수데이터2합계[1:]) + b, a = None
        정수리스트 = []
        정수리스트.append(정수데이터총괄증감)
        정수리스트.append(정수데이터1합계)
        정수리스트.append(정수데이터2합계)
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        for 행, 줄 in enumerate(정수리스트, start = 4):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        워크시트 = self.엑셀.Worksheets('전체차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        보유데이터1 = 워크시트.Range(f'''D3:E{마지막행}''').Value
        보유데이터2 = 워크시트.Range(f'''M3:M{마지막행}''').Value
        if 보유데이터2:
            보유데이터2 = [
                [
                    0]]
        elif isinstance(보유데이터2, (int, float, str)):
            pass
        if isinstance(보유데이터2, (int, float, str)):
            pass
        보유데이터2 = [
            [
                보유데이터2]]
        보유데이터 = []
        for 열1, 열2 in zip(보유데이터1, 보유데이터2):
            병합열 = list(열1) + list(열2)
            보유데이터.append(병합열)
        변환보유데이터 = []
        for 줄 in 보유데이터:
            변환줄 = []
            for i, 아이템 in enumerate(줄):
                if isinstance(아이템, float):
                    pass
                if isinstance(아이템, float):
                    변환줄.append(int(아이템))
                    continue
                if 아이템:
                    continue
                변환줄.append(아이템)
            변환보유데이터.append(tuple(변환줄))
        보유구매전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매전용소계 = 보유구매전용대형 + 보유구매전용중형 + 보유구매전용소형 + 보유구매전용경형
        보유구매업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매업무용소계 = 보유구매업무용대형 + 보유구매업무용중형 + 보유구매업무용소형 + 보유구매업무용경형
        보유구매승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매승합용소계 = 보유구매승합용대형 + 보유구매승합용중형 + 보유구매승합용소형 + 보유구매승합용경형
        보유구매화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매화물용소계 = 보유구매화물용대형 + 보유구매화물용중형 + 보유구매화물용소형 + 보유구매화물용경형
        보유구매특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 0):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유구매특수용소계 = 보유구매특수용대형 + 보유구매특수용중형 + 보유구매특수용소형 + 보유구매특수용경형
        보유구매총계 = 보유구매전용소계 + 보유구매업무용소계 + 보유구매승합용소계 + 보유구매화물용소계 + 보유구매특수용소계
        보유구매리스트 = [
            보유구매총계,
            보유구매전용소계,
            보유구매전용대형,
            보유구매전용중형,
            보유구매전용소형,
            보유구매전용경형,
            보유구매업무용소계,
            보유구매업무용대형,
            보유구매업무용중형,
            보유구매업무용소형,
            보유구매업무용경형,
            보유구매승합용소계,
            보유구매승합용대형,
            보유구매승합용중형,
            보유구매승합용소형,
            보유구매승합용경형,
            보유구매화물용소계,
            보유구매화물용대형,
            보유구매화물용중형,
            보유구매화물용소형,
            보유구매화물용경형,
            보유구매특수용소계,
            보유구매특수용대형,
            보유구매특수용중형,
            보유구매특수용소형,
            보유구매특수용경형]
        보유임차전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차전용소계 = 보유임차전용대형 + 보유임차전용중형 + 보유임차전용소형 + 보유임차전용경형
        보유임차업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차업무용소계 = 보유임차업무용대형 + 보유임차업무용중형 + 보유임차업무용소형 + 보유임차업무용경형
        보유임차승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차승합용소계 = 보유임차승합용대형 + 보유임차승합용중형 + 보유임차승합용소형 + 보유임차승합용경형
        보유임차화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차화물용소계 = 보유임차화물용대형 + 보유임차화물용중형 + 보유임차화물용소형 + 보유임차화물용경형
        보유임차특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 1):
continueif 1:
passcontinueNone)(변환보유데이터())
        보유임차특수용소계 = 보유임차특수용대형 + 보유임차특수용중형 + 보유임차특수용소형 + 보유임차특수용경형
        보유임차총계 = 보유임차전용소계 + 보유임차업무용소계 + 보유임차승합용소계 + 보유임차화물용소계 + 보유임차특수용소계
        보유임차리스트 = [
            보유임차총계,
            보유임차전용소계,
            보유임차전용대형,
            보유임차전용중형,
            보유임차전용소형,
            보유임차전용경형,
            보유임차업무용소계,
            보유임차업무용대형,
            보유임차업무용중형,
            보유임차업무용소형,
            보유임차업무용경형,
            보유임차승합용소계,
            보유임차승합용대형,
            보유임차승합용중형,
            보유임차승합용소형,
            보유임차승합용경형,
            보유임차화물용소계,
            보유임차화물용대형,
            보유임차화물용중형,
            보유임차화물용소형,
            보유임차화물용경형,
            보유임차특수용소계,
            보유임차특수용대형,
            보유임차특수용중형,
            보유임차특수용소형,
            보유임차특수용경형]
        for a, b in :
            pass
        , []
        sum, None, sum, [
            '[보유]'], zip(보유구매리스트, 보유임차리스트) + b, a = None
        보유구매리스트 = [
            '[보유] 구매'] + 보유구매리스트
        보유임차리스트 = [
            '[보유] 임차'] + 보유임차리스트
        보유리스트 = []
        보유리스트.append(보유합계리스트)
        보유리스트.append(보유구매리스트)
        보유리스트.append(보유임차리스트)
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        for 행, 줄 in enumerate(보유리스트, start = 7):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        for a, b in :
            pass
        , []
        sum, None, sum, [
            '정수-보유 차이'], zip(정수데이터1합계[1:], 보유합계리스트[1:]) + b, a = None
        for 열, 값 in enumerate(정수보유차이리스트, start = 1):
            워크시트.Cells(3, 열).Value = 값
        sum
        워크시트 = self.엑셀.Worksheets('신규차량(반자동)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        신규데이터1 = 워크시트.Range(f'''D3:E{마지막행}''').Value
        신규데이터2 = 워크시트.Range(f'''M3:M{마지막행}''').Value
        if 신규데이터2:
            신규데이터2 = [
                [
                    0]]
        elif isinstance(신규데이터2, (int, float, str)):
            pass
        if isinstance(신규데이터2, (int, float, str)):
            pass
        신규데이터2 = [
            [
                신규데이터2]]
        신규데이터 = []
        for 열1, 열2 in zip(신규데이터1, 신규데이터2):
            병합열 = list(열1) + list(열2)
            신규데이터.append(병합열)
        변환신규데이터 = []
        for 줄 in 신규데이터:
            변환줄 = []
            for i, 아이템 in enumerate(줄):
                if isinstance(아이템, float):
                    pass
                if isinstance(아이템, float):
                    변환줄.append(int(아이템))
                    continue
                if 아이템:
                    continue
                변환줄.append(아이템)
            sum
            변환신규데이터.append(tuple(변환줄))
        sum
        신규구매전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매전용소계 = 신규구매전용대형 + 신규구매전용중형 + 신규구매전용소형 + 신규구매전용경형
        신규구매업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매업무용소계 = 신규구매업무용대형 + 신규구매업무용중형 + 신규구매업무용소형 + 신규구매업무용경형
        신규구매승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매승합용소계 = 신규구매승합용대형 + 신규구매승합용중형 + 신규구매승합용소형 + 신규구매승합용경형
        신규구매화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매화물용소계 = 신규구매화물용대형 + 신규구매화물용중형 + 신규구매화물용소형 + 신규구매화물용경형
        신규구매특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 0):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규구매특수용소계 = 신규구매특수용대형 + 신규구매특수용중형 + 신규구매특수용소형 + 신규구매특수용경형
        신규구매총계 = 신규구매전용소계 + 신규구매업무용소계 + 신규구매승합용소계 + 신규구매화물용소계 + 신규구매특수용소계
        신규구매리스트 = [
            신규구매총계,
            신규구매전용소계,
            신규구매전용대형,
            신규구매전용중형,
            신규구매전용소형,
            신규구매전용경형,
            신규구매업무용소계,
            신규구매업무용대형,
            신규구매업무용중형,
            신규구매업무용소형,
            신규구매업무용경형,
            신규구매승합용소계,
            신규구매승합용대형,
            신규구매승합용중형,
            신규구매승합용소형,
            신규구매승합용경형,
            신규구매화물용소계,
            신규구매화물용대형,
            신규구매화물용중형,
            신규구매화물용소형,
            신규구매화물용경형,
            신규구매특수용소계,
            신규구매특수용대형,
            신규구매특수용중형,
            신규구매특수용소형,
            신규구매특수용경형]
        신규임차전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차전용소계 = 신규임차전용대형 + 신규임차전용중형 + 신규임차전용소형 + 신규임차전용경형
        신규임차업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차업무용소계 = 신규임차업무용대형 + 신규임차업무용중형 + 신규임차업무용소형 + 신규임차업무용경형
        신규임차승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차승합용소계 = 신규임차승합용대형 + 신규임차승합용중형 + 신규임차승합용소형 + 신규임차승합용경형
        신규임차화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차화물용소계 = 신규임차화물용대형 + 신규임차화물용중형 + 신규임차화물용소형 + 신규임차화물용경형
        신규임차특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 1):
continueif 1:
passcontinueNone)(변환신규데이터())
        신규임차특수용소계 = 신규임차특수용대형 + 신규임차특수용중형 + 신규임차특수용소형 + 신규임차특수용경형
        신규임차총계 = 신규임차전용소계 + 신규임차업무용소계 + 신규임차승합용소계 + 신규임차화물용소계 + 신규임차특수용소계
        신규임차리스트 = [
            신규임차총계,
            신규임차전용소계,
            신규임차전용대형,
            신규임차전용중형,
            신규임차전용소형,
            신규임차전용경형,
            신규임차업무용소계,
            신규임차업무용대형,
            신규임차업무용중형,
            신규임차업무용소형,
            신규임차업무용경형,
            신규임차승합용소계,
            신규임차승합용대형,
            신규임차승합용중형,
            신규임차승합용소형,
            신규임차승합용경형,
            신규임차화물용소계,
            신규임차화물용대형,
            신규임차화물용중형,
            신규임차화물용소형,
            신규임차화물용경형,
            신규임차특수용소계,
            신규임차특수용대형,
            신규임차특수용중형,
            신규임차특수용소형,
            신규임차특수용경형]
        for a, b in :
            pass
        , []
        sum, None, sum, [
            '[신규]'], zip(신규구매리스트, 신규임차리스트) + b, a = None
        신규구매리스트 = [
            '[신규] 구매'] + 신규구매리스트
        신규임차리스트 = [
            '[신규] 임차'] + 신규임차리스트
        신규리스트 = []
        신규리스트.append(신규합계리스트)
        신규리스트.append(신규구매리스트)
        신규리스트.append(신규임차리스트)
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        for 행, 줄 in enumerate(신규리스트, start = 10):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        워크시트 = self.엑셀.Worksheets('처분차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        처분데이터1 = 워크시트.Range(f'''D3:E{마지막행}''').Value
        처분데이터2 = 워크시트.Range(f'''M3:M{마지막행}''').Value
        if 처분데이터2:
            처분데이터2 = [
                [
                    '없음']]
        elif isinstance(처분데이터2, str):
            pass
        if isinstance(처분데이터2, str):
            처분데이터2 = [
                [
                    처분데이터2]]
        elif isinstance(처분데이터2, (int, float)):
            pass
        if isinstance(처분데이터2, (int, float)):
            pass
        처분데이터2 = [
            [
                '없음']]
        처분데이터 = []
        for 열1, 열2 in zip(처분데이터1, 처분데이터2):
            병합열 = list(열1) + list(열2)
            처분데이터.append(병합열)
        sum
        변환처분데이터 = []
        for 줄 in 처분데이터:
            변환줄 = []
            for i, 아이템 in enumerate(줄):
                if i == 2:
                    if 아이템:
                        아이템 = '없음'
                    elif isinstance(아이템, (int, float)):
                        pass
                    if isinstance(아이템, (int, float)):
                        pass
                    아이템 = '없음'
                    임시값 = 1 if '반납' in 아이템 else 0
                    변환줄.append(임시값)
                    continue
                if isinstance(아이템, float):
                    pass
                if isinstance(아이템, float):
                    변환줄.append(int(아이템))
                    continue
                if 아이템:
                    continue
                변환줄.append(아이템)
            아이템
            변환처분데이터.append(tuple(변환줄))
        sum
        처분구매전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매전용소계 = 처분구매전용대형 + 처분구매전용중형 + 처분구매전용소형 + 처분구매전용경형
        처분구매업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매업무용소계 = 처분구매업무용대형 + 처분구매업무용중형 + 처분구매업무용소형 + 처분구매업무용경형
        처분구매승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매승합용소계 = 처분구매승합용대형 + 처분구매승합용중형 + 처분구매승합용소형 + 처분구매승합용경형
        처분구매화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매화물용소계 = 처분구매화물용대형 + 처분구매화물용중형 + 처분구매화물용소형 + 처분구매화물용경형
        처분구매특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 0):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분구매특수용소계 = 처분구매특수용대형 + 처분구매특수용중형 + 처분구매특수용소형 + 처분구매특수용경형
        처분구매총계 = 처분구매전용소계 + 처분구매업무용소계 + 처분구매승합용소계 + 처분구매화물용소계 + 처분구매특수용소계
        처분구매리스트 = [
            처분구매총계,
            처분구매전용소계,
            처분구매전용대형,
            처분구매전용중형,
            처분구매전용소형,
            처분구매전용경형,
            처분구매업무용소계,
            처분구매업무용대형,
            처분구매업무용중형,
            처분구매업무용소형,
            처분구매업무용경형,
            처분구매승합용소계,
            처분구매승합용대형,
            처분구매승합용중형,
            처분구매승합용소형,
            처분구매승합용경형,
            처분구매화물용소계,
            처분구매화물용대형,
            처분구매화물용중형,
            처분구매화물용소형,
            처분구매화물용경형,
            처분구매특수용소계,
            처분구매특수용대형,
            처분구매특수용중형,
            처분구매특수용소형,
            처분구매특수용경형]
        처분임차전용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '대형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차전용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '중형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차전용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '소형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차전용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('전용', '경형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차전용소계 = 처분임차전용대형 + 처분임차전용중형 + 처분임차전용소형 + 처분임차전용경형
        처분임차업무용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '대형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차업무용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '중형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차업무용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '소형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차업무용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('업무용', '경형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차업무용소계 = 처분임차업무용대형 + 처분임차업무용중형 + 처분임차업무용소형 + 처분임차업무용경형
        처분임차승합용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '대형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차승합용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '중형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차승합용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '소형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차승합용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('승합용', '경형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차승합용소계 = 처분임차승합용대형 + 처분임차승합용중형 + 처분임차승합용소형 + 처분임차승합용경형
        처분임차화물용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '대형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차화물용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '중형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차화물용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '소형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차화물용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('화물용', '경형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차화물용소계 = 처분임차화물용대형 + 처분임차화물용중형 + 처분임차화물용소형 + 처분임차화물용경형
        처분임차특수용대형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '대형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차특수용중형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '중형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차특수용소형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '소형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차특수용경형 = (lambda .0: if None:
passfor None in .0:
if None:
if not None == ('특수용', '경형', 1):
continueif 1:
passcontinueNone)(변환처분데이터())
        처분임차특수용소계 = 처분임차특수용대형 + 처분임차특수용중형 + 처분임차특수용소형 + 처분임차특수용경형
        처분임차총계 = 처분임차전용소계 + 처분임차업무용소계 + 처분임차승합용소계 + 처분임차화물용소계 + 처분임차특수용소계
        처분임차리스트 = [
            처분임차총계,
            처분임차전용소계,
            처분임차전용대형,
            처분임차전용중형,
            처분임차전용소형,
            처분임차전용경형,
            처분임차업무용소계,
            처분임차업무용대형,
            처분임차업무용중형,
            처분임차업무용소형,
            처분임차업무용경형,
            처분임차승합용소계,
            처분임차승합용대형,
            처분임차승합용중형,
            처분임차승합용소형,
            처분임차승합용경형,
            처분임차화물용소계,
            처분임차화물용대형,
            처분임차화물용중형,
            처분임차화물용소형,
            처분임차화물용경형,
            처분임차특수용소계,
            처분임차특수용대형,
            처분임차특수용중형,
            처분임차특수용소형,
            처분임차특수용경형]
        for a, b in :
            pass
        , []
        sum, None, sum, [
            '[처분]'], zip(처분구매리스트, 처분임차리스트) + b, a = None
        처분구매리스트 = [
            '[처분] 구매'] + 처분구매리스트
        처분임차리스트 = [
            '[처분] 임차'] + 처분임차리스트
        처분리스트 = []
        처분리스트.append(처분합계리스트)
        처분리스트.append(처분구매리스트)
        처분리스트.append(처분임차리스트)
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        for 행, 줄 in enumerate(처분리스트, start = 13):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        워크시트 = self.엑셀.Worksheets('처분차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        처분데이터1 = 워크시트.Range(f'''D3:D{마지막행}''').Value
        처분데이터2 = 워크시트.Range(f'''K3:M{마지막행}''').Value
        if 처분데이터1:
            처분데이터1 = [
                [
                    0]]
        elif isinstance(처분데이터1, (int, float, str)):
            pass
        if isinstance(처분데이터1, (int, float, str)):
            pass
        처분데이터1 = [
            [
                처분데이터1]]
        처분데이터 = []
        for 열1, 열2 in zip(처분데이터1, 처분데이터2):
            병합열 = list(열1) + list(열2)
            처분데이터.append(병합열)
        sum
        변환처분데이터 = []
        for 줄 in 처분데이터:
            변환줄 = []
            for i, 아이템 in enumerate(줄):
                if i == 3:
                    if 아이템:
                        아이템 = '없음'
                    elif isinstance(아이템, (int, float)):
                        pass
                    if isinstance(아이템, (int, float)):
                        pass
                    아이템 = '없음'
                    임시값 = 1 if '반납' in 아이템 else 0
                    변환줄.append(임시값)
                    continue
                if isinstance(아이템, float):
                    pass
                if isinstance(아이템, float):
                    변환줄.append(int(아이템))
                    continue
                if 아이템:
                    continue
                변환줄.append(아이템)
            아이템
            변환처분데이터.append(tuple(변환줄))
        sum
        처분구매전용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '전용':
continueif not item[3] == 0:
continueif item[1]:
pass)(변환처분데이터())
        처분구매업무용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '업무용':
continueif not item[3] == 0:
continueif item[1]:
pass)(변환처분데이터())
        처분구매승합용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '승합용':
continueif not item[3] == 0:
continueif item[1]:
pass)(변환처분데이터())
        처분구매화물용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '화물용':
continueif not item[3] == 0:
continueif item[1]:
pass)(변환처분데이터())
        처분구매특수용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '특수용':
continueif not item[3] == 0:
continueif item[1]:
pass)(변환처분데이터())
        처분구매개월리스트 = [
            처분구매전용개월 + 처분구매업무용개월 + 처분구매승합용개월 + 처분구매화물용개월 + 처분구매특수용개월,
            처분구매전용개월,
            처분구매업무용개월,
            처분구매승합용개월,
            처분구매화물용개월,
            처분구매특수용개월]
        처분임차전용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '전용':
continueif not item[3] == 1:
continueif item[1]:
pass)(변환처분데이터())
        처분임차업무용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '업무용':
continueif not item[3] == 1:
continueif item[1]:
pass)(변환처분데이터())
        처분임차승합용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '승합용':
continueif not item[3] == 1:
continueif item[1]:
pass)(변환처분데이터())
        처분임차화물용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '화물용':
continueif not item[3] == 1:
continueif item[1]:
pass)(변환처분데이터())
        처분임차특수용개월 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '특수용':
continueif not item[3] == 1:
continueif item[1]:
pass)(변환처분데이터())
        처분임차개월리스트 = [
            처분임차전용개월 + 처분임차업무용개월 + 처분임차승합용개월 + 처분임차화물용개월 + 처분임차특수용개월,
            처분임차전용개월,
            처분임차업무용개월,
            처분임차승합용개월,
            처분임차화물용개월,
            처분임차특수용개월]
        처분구매전용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '전용':
continueif not item[3] == 0:
continueif item[2]:
pass)(변환처분데이터())
        처분구매업무용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '업무용':
continueif not item[3] == 0:
continueif item[2]:
pass)(변환처분데이터())
        처분구매승합용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '승합용':
continueif not item[3] == 0:
continueif item[2]:
pass)(변환처분데이터())
        처분구매화물용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '화물용':
continueif not item[3] == 0:
continueif item[2]:
pass)(변환처분데이터())
        처분구매특수용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '특수용':
continueif not item[3] == 0:
continueif item[2]:
pass)(변환처분데이터())
        처분구매거리리스트 = [
            처분구매전용거리 + 처분구매업무용거리 + 처분구매승합용거리 + 처분구매화물용거리 + 처분구매특수용거리,
            처분구매전용거리,
            처분구매업무용거리,
            처분구매승합용거리,
            처분구매화물용거리,
            처분구매특수용거리]
        처분임차전용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '전용':
continueif not item[3] == 1:
continueif item[2]:
pass)(변환처분데이터())
        처분임차업무용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '업무용':
continueif not item[3] == 1:
continueif item[2]:
pass)(변환처분데이터())
        처분임차승합용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '승합용':
continueif not item[3] == 1:
continueif item[2]:
pass)(변환처분데이터())
        처분임차화물용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '화물용':
continueif not item[3] == 1:
continueif item[2]:
pass)(변환처분데이터())
        처분임차특수용거리 = (lambda .0: if None:
passfor None in .0:
if None:
if not None[0] == '특수용':
continueif not item[3] == 1:
continueif item[2]:
pass)(변환처분데이터())
        처분임차거리리스트 = [
            처분임차전용거리 + 처분임차업무용거리 + 처분임차승합용거리 + 처분임차화물용거리 + 처분임차특수용거리,
            처분임차전용거리,
            처분임차업무용거리,
            처분임차승합용거리,
            처분임차화물용거리,
            처분임차특수용거리]
        처분구매개월리스트 = [
            '[처분] 구매 개월 합산'] + 처분구매개월리스트
        처분임차개월리스트 = [
            '[처분] 임차 개월 합산'] + 처분임차개월리스트
        처분구매거리리스트 = [
            '[처분] 구매 Km 합산'] + 처분구매거리리스트
        처분임차거리리스트 = [
            '[처분] 임차 Km 합산'] + 처분임차거리리스트
        처분리스트2 = []
        처분리스트2.append(처분구매개월리스트)
        처분리스트2.append(처분임차개월리스트)
        처분리스트2.append(처분구매거리리스트)
        처분리스트2.append(처분임차거리리스트)
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        for 행, 줄 in enumerate(처분리스트2, start = 17):
            for 열, 값 in enumerate(줄, start = 1):
                워크시트.Cells(행, 열).Value = 값
        워크시트 = self.엑셀.Worksheets('전체차량(입력)')
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        블랙박스데이터 = 워크시트.Range(f'''P3:P{마지막행}''').Value
        if 블랙박스데이터:
            블랙박스데이터 = [
                [
                    0]]
        elif isinstance(블랙박스데이터, str):
            pass
        if isinstance(블랙박스데이터, str):
            블랙박스데이터 = [
                [
                    0]]
        elif isinstance(블랙박스데이터, (int, float)):
            pass
        if isinstance(블랙박스데이터, (int, float)):
            pass
        블랙박스데이터 = [
            [
                블랙박스데이터]]
        변환블랙박스데이터 = []
        for 줄 in 블랙박스데이터:
            변환줄 = []
            for i, 아이템 in enumerate(줄):
                if isinstance(아이템, float):
                    pass
                if isinstance(아이템, float):
                    변환줄.append(int(아이템))
                    continue
                if 아이템:
                    continue
                if isinstance(아이템, str):
                    pass
                if isinstance(아이템, str):
                    변환줄.append(0)
                    continue
                변환줄.append(아이템)
            블랙박스데이터
            변환블랙박스데이터.append(tuple(변환줄))
        블랙박스개수 = sum((lambda .0: if None:
passfor None in .0:
if None:
if None[0]:
passcontinueNone)(변환블랙박스데이터()))
        워크시트 = self.엑셀.Worksheets('최종계산(자동)')
        워크시트.Cells(21, 2).Value = 블랙박스개수
        return None
        
        
        
        
        
        
        
        
        
        
        

    
    def 울항여비신청서(self):
        워크북 = self.엑셀.Workbooks.Add()
        워크시트 = 워크북.Worksheets(1)
        어제날짜 = str(어제.year) + '-' + str(어제.month) + '-' + str(어제.day)
        워크시트.Range('A1:O1,A2:O2').Merge()
        워크시트.Range('A1:O39').VerticalAlignment = -4108
        워크시트.Range('A1:O39').HorizontalAlignment = -4108
        워크시트.Range('A2:A6,H5,I3:I6').HorizontalAlignment = -4131
        워크시트.Range('M6,O6').HorizontalAlignment = -4152
        워크시트.Range('A1:O39').Font.Name = '맑은 고딕'
        워크시트.Range('A1:O39').Font.Size = 10
        워크시트.Cells(1, 1).Font.Size = 17
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '국내여비 산출내역서'
        워크시트.Columns('A:A').ColumnWidth = 9.63
        워크시트.Columns('B:B').ColumnWidth = 9.88
        워크시트.Columns('C:C').ColumnWidth = 10.38
        워크시트.Columns('D:D').ColumnWidth = 8.13
        워크시트.Columns('E:E').ColumnWidth = 7.38
        워크시트.Columns('F:F').ColumnWidth = 8.13
        워크시트.Columns('G:G').ColumnWidth = 9
        워크시트.Columns('H:H').ColumnWidth = 7.25
        워크시트.Columns('I:I').ColumnWidth = 6.88
        워크시트.Columns('J:J').ColumnWidth = 7.25
        워크시트.Columns('K:K').ColumnWidth = 7.25
        워크시트.Columns('L:L').ColumnWidth = 10.75
        워크시트.Columns('M:M').ColumnWidth = 7.25
        워크시트.Columns('N:N').ColumnWidth = 7.75
        워크시트.Columns('O:O').ColumnWidth = 10.63
        워크시트.Rows(1).RowHeight = 21
        워크시트.Rows('2:39').RowHeight = 16.5
        워크시트.Rows('8:9').RowHeight = 25.5
        워크시트.Rows(12).RowHeight = 33
        워크시트.Range('A2').Value = ' * 파란색 셀만 입력하세요'
        워크시트.Range('A2').Font.Color = 16711680
        워크시트.Range('A2').Font.Italic = True
        워크시트.Range('A3:A6,I3:I6').Interior.Color = 12379352
        워크시트.Range('B3:B6,D5,L3:L5,M6,O6').Interior.Color = 15986394
        워크시트.Range('L6,N6').Interior.Color = 14610923
        선범위 = 'A3:O6,A8:O12,E14:O14'
        워크시트.Range(선범위).Borders(7).LineStyle = 1
        워크시트.Range(선범위).Borders(8).LineStyle = 1
        워크시트.Range(선범위).Borders(9).LineStyle = 1
        워크시트.Range(선범위).Borders(10).LineStyle = 1
        워크시트.Range(선범위).Borders(11).LineStyle = 1
        워크시트.Range(선범위).Borders(12).LineStyle = 1
        워크시트.Range('B3:H3,B4:H4,B6:H6,D5:E5,F5:G5,I3:K3,I4:K4,I5:K6,L3:O3,L4:O4,L5:O5,F14:G14,I14:J14,M14:O14,A20:D21,A22:A39,I20:J20,I21:J21,I22:J22,I23:J23,K20:L20,K21:L21,K22:L22,K23:L23,E20,G20').Merge()
        워크시트.Range('A3').Value = '○ 출장목적'
        워크시트.Range('A4').Value = '○ 출 장 지'
        워크시트.Range('A5').Value = '○ 출장기간'
        워크시트.Range('A6').Value = '○  출장자'
        워크시트.Range('B5').Value = 어제날짜
        워크시트.Range('C5').Value = '~'
        워크시트.Range('D5').Value = 어제날짜
        워크시트.Range('F5').Formula = '=(DATEDIF(B5,D5,"d"))+1'
        워크시트.Range('H5').Value = '일'
        워크시트.Range('I3').Value = '○ 관용차/자가차량이용여부'
        워크시트.Range('I4').Value = '○ 전일출발 여부'
        워크시트.Range('I5').Value = '○ 출장자 식사지급 여부'
        워크시트.Range('L3').Value = 'N'
        워크시트.Range('L4').Value = 'N'
        워크시트.Range('L5').Value = 'Y'
        워크시트.Range('M6').Value = '0'
        워크시트.Range('O6').Value = '10,000'
        워크시트.Range('L6').Value = '횟수'
        워크시트.Range('N6').Value = '단가'

    
    def 산인공시외출장(self):
        워크북 = self.엑셀.Workbooks.Add()
        워크시트 = 워크북.Worksheets(1)
        워크시트.Range('A1:R1').Merge()
        워크시트.Range('A1:R1').HorizontalAlignment = -4108
        워크시트.Range('A1:R1').VerticalAlignment = -4108
        워크시트.Cells(1, 1).Font.Name = 'KoPub돋움체 Bold'
        워크시트.Cells(1, 1).Font.Size = 22
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '여비 신청(정산)서'
        워크시트.Rows(1).RowHeight = 37.5
        워크시트.Rows(2).RowHeight = 30.75
        워크시트.Rows(3).RowHeight = 26.25
        워크시트.Rows(4).RowHeight = 24.75
        워크시트.Rows(5).RowHeight = 24.75
        워크시트.Rows(6).RowHeight = 24.75
        워크시트.Rows(7).RowHeight = 45
        워크시트.Rows(8).RowHeight = 49.5
        워크시트.Rows('9:30').RowHeight = 39.75
        워크시트.Columns('A:C').ColumnWidth = 6
        워크시트.Columns('D:E').ColumnWidth = 11
        워크시트.Columns('F:F').ColumnWidth = 5.75
        워크시트.Columns('G:G').ColumnWidth = 9
        워크시트.Columns('H:I').ColumnWidth = 5
        워크시트.Columns('J:J').ColumnWidth = 6.25
        워크시트.Columns('K:K').ColumnWidth = 8.75
        워크시트.Columns('L:P').ColumnWidth = 8.5
        워크시트.Columns('Q:Q').ColumnWidth = 10.25
        워크시트.Columns('R:R').ColumnWidth = 13.5
        워크시트.PageSetup.PrintArea = 'A1:R60'
        워크시트.PageSetup.Zoom = False
        워크시트.PageSetup.FitToPagesWide = 1
        워크시트.PageSetup.FitToPagesTall = 2
        self.엑셀.ActiveWindow.View = 2
        워크시트.Range('A2:R4').Font.Size = 12
        워크시트.Range('A2:R4').Font.Name = 'KoPub돋움체 Medium'
        워크시트.Range('A2:R4').HorizontalAlignment = -4108
        워크시트.Range('A2:R4').VerticalAlignment = -4108
        워크시트.Range('A2:R2').Borders(8).LineStyle = 1
        워크시트.Range('A2:R2').Borders(8).Weight = 3
        워크시트.Range('A2:R2').Borders(9).LineStyle = 1
        워크시트.Range('A2:R2').Borders(9).Weight = 3
        워크시트.Range('A2:R2').Borders(7).LineStyle = -4142
        워크시트.Range('A2:R2').Borders(10).LineStyle = -4142
        워크시트.Range('A2:C2').Merge()
        워크시트.Range('A2:C2').Interior.Color = 11184814
        워크시트.Range('A2').Value = '소속'
        워크시트.Range('D2:F2').Merge()
        워크시트.Range('D2').Value = 'OO국 OO부'
        워크시트.Range('D2').Font.Color = 16711680
        워크시트.Range('G2:I2').Merge()
        워크시트.Range('G2:I2').Interior.Color = 11184814
        워크시트.Range('G2').Value = '직급'
        워크시트.Range('J2:M2').Merge()
        워크시트.Range('J2').Value = '일반직 0급'
        워크시트.Range('J2').Font.Color = 16711680
        워크시트.Range('N2:O2').Merge()
        워크시트.Range('N2:O2').Interior.Color = 11184814
        워크시트.Range('N2').Value = '성명'
        워크시트.Range('P2:R2').Merge()
        워크시트.Range('P2:R2').Font.Color = 16711680
        워크시트.Range('P2').Value = '김공단'
        워크시트.Range('A3:R3').Borders(8).LineStyle = 1
        워크시트.Range('A3:R3').Borders(8).Weight = 3
        워크시트.Range('A3:R3').Borders(9).LineStyle = 1
        워크시트.Range('A3:R3').Borders(9).Weight = 3
        워크시트.Range('A3:R3').Merge()
        워크시트.Range('A3:R3').Font.Color = 255
        워크시트.Range('A3').Value = '(파란색 부분만 직접 입력)'
        워크시트.Range('A4:R7').Borders(8).LineStyle = 1
        워크시트.Range('A4:R7').Borders(8).Weight = 3
        워크시트.Range('A4:R7').Borders(9).LineStyle = 1
        워크시트.Range('A4:R7').Borders(9).Weight = 3
        워크시트.Range('A4:R7').Borders(11).LineStyle = 1
        워크시트.Range('A4:R7').Borders(12).LineStyle = 1
        워크시트.Range('A4:R4').Merge()
        워크시트.Range('A4:R4').Interior.Color = 11184814
        워크시트.Range('A4').Value = '여비정산 세부내역서'
        워크시트.Range('A5:R7').Font.Size = 11
        워크시트.Range('A5:R7').Font.Name = 'KoPub돋움체 Medium'
        워크시트.Range('A5:R7').HorizontalAlignment = -4108
        워크시트.Range('A5:R7').VerticalAlignment = -4108
        워크시트.Range('A5:C5').Merge()
        워크시트.Range('A5:C5').Interior.Color = 14277081
        워크시트.Range('A5').Value = '출장지역'
        워크시트.Range('D5:E5').Merge()
        워크시트.Range('D5:E5').Interior.Color = 14277081
        워크시트.Range('D5').Value = '출장기간'
        워크시트.Range('F5:F6').Merge()
        워크시트.Range('F5:F6').Interior.Color = 14277081
        워크시트.Range('F5').Value = '일수'
        워크시트.Range('G5:G6').Merge()
        워크시트.Range('G5:G6').Interior.Color = 14277081
        워크시트.Range('G5').Value = '일비'
        워크시트.Range('H5:I5').Merge()
        워크시트.Range('H5:I5').Interior.Color = 14277081
        워크시트.Range('H5').Value = '식비'
        워크시트.Range('H6').Interior.Color = 14277081
        워크시트.Range('H6').Value = '제외'
        워크시트.Range('J5:J6').Merge()
        워크시트.Range('J5:J6').Interior.Color = 14277081
        워크시트.Range('J5').Value = '거리\n(km)'
        워크시트.Range('K5').Interior.Color = 14277081
        워크시트.Range('K5').Value = '여비'
        워크시트.Range('L5:L6').Merge()
        워크시트.Range('L5:L6').Interior.Color = 14277081
        워크시트.Range('L5').Value = '유가'
        워크시트.Range('M5:M6').Merge()
        워크시트.Range('M5:M6').Interior.Color = 14277081
        워크시트.Range('M5').Value = '유류비\n합계'
        워크시트.Range('N5:N6').Merge()
        워크시트.Range('N5:N6').Interior.Color = 14277081
        워크시트.Range('N5').Value = '통행료'
        워크시트.Range('O5:O6').Merge()
        워크시트.Range('O5:O6').Interior.Color = 14277081
        워크시트.Range('O5').Value = '교통비'
        워크시트.Range('P5:P6').Merge()
        워크시트.Range('P5:P6').Interior.Color = 14277081
        워크시트.Range('P5').Value = '주차비'
        워크시트.Range('Q5:Q6').Merge()
        워크시트.Range('Q5:Q6').Interior.Color = 14277081
        워크시트.Range('Q5').Value = '숙박비'
        워크시트.Range('R5:R6').Merge()
        워크시트.Range('R5:R6').Interior.Color = 14277081
        워크시트.Range('R5').Value = '합계'
        워크시트.Range('A6').Interior.Color = 15921906
        워크시트.Range('A6').Value = '출발'
        워크시트.Range('B6').Interior.Color = 15921906
        워크시트.Range('B6').Value = '경유'
        워크시트.Range('C6').Interior.Color = 15921906
        워크시트.Range('C6').Value = '도착'
        워크시트.Range('D6').Interior.Color = 15921906
        워크시트.Range('D6').Value = '출발'
        워크시트.Range('E6').Interior.Color = 15921906
        워크시트.Range('E6').Value = '도착'
        워크시트.Range('I6').Interior.Color = 15921906
        워크시트.Range('I6').Font.Color = 16711680
        워크시트.Range('I6').Value = '2'
        워크시트.Range('K6').Interior.Color = 15921906
        워크시트.Range('K6').Font.Color = 16711680
        워크시트.Range('K6').Value = '휘발유'
        워크시트.Range('A7').Font.Color = 16711680
        워크시트.Range('A7').Value = '부산'
        워크시트.Range('B7').Font.Color = 16711680
        워크시트.Range('B7').Value = '-'
        워크시트.Range('C7').Font.Color = 16711680
        워크시트.Range('C7').Value = '서울'
        워크시트.Range('D7').Font.Color = 16711680
        임시날짜 = str + datetime.today(None().day)
        워크시트.Range('D7').Value = 임시날짜
        워크시트.Range('E7').Font.Color = 16711680
        임시날짜 = str + datetime.today(None().day)
        워크시트.Range('E7').Value = 임시날짜
        워크시트.Range('F7').Formula = '=E7-D7+1'
        워크시트.Range('G7').Formula = '=25000*F7'
        워크시트.Range('G7').NumberFormat = '#,##0'
        워크시트.Range('H7:I7').Merge()
        워크시트.Range('H7').Formula = '=ROUNDDOWN((25000/3)*((F7*3)-I6),0)'
        워크시트.Range('H7').NumberFormat = '#,##0'
        워크시트.Range('J7').Font.Color = 16711680
        워크시트.Range('J7').Value = '100'
        워크시트.Range('K7').Formula = '=IF(K6="휘발유",10.06,IF(K6="경유",10.16,IF(K6="LPG",7.87,IF(K6="하이브리드",15.37,IF(K6="플러그인 하이브리드",10.61,IF(K6="전기",5.22,IF(K6="수소",94.9,"")))))))'
        워크시트.Range('L7').Font.Color = 16711680
        워크시트.Range('L7').Value = '1639.27'
        워크시트.Range('L7').NumberFormat = '#,##0.00'
        워크시트.Range('M7').Font.Color = 16711680
        워크시트.Range('M7').Formula = '=IFERROR((J7*L7)/K7,0)'
        워크시트.Range('M7').NumberFormat = '#,##0'
        워크시트.Range('N7').Font.Color = 16711680
        워크시트.Range('N7').Value = '2000'
        워크시트.Range('N7').NumberFormat = '#,##0'
        워크시트.Range('O7').Font.Color = 16711680
        워크시트.Range('O7').Value = '2000'
        워크시트.Range('O7').NumberFormat = '#,##0'
        워크시트.Range('P7').Font.Color = 16711680
        워크시트.Range('P7').Value = '8000'
        워크시트.Range('P7').NumberFormat = '#,##0'
        워크시트.Range('Q7').Font.Color = 16711680
        워크시트.Range('Q7').Value = '200000'
        워크시트.Range('Q7').NumberFormat = '#,##0'
        워크시트.Range('R7').Formula = '=G7+H7+M7+N7+O7+P7+Q7'
        워크시트.Range('R7').NumberFormat = '₩#,##0'
        워크시트.Range('A8:R8').Merge()
        워크시트.Range('A8').Font.Size = 12
        워크시트.Range('A8').Font.Bold = True
        워크시트.Range('A8').Font.Name = 'KoPub돋움체 Medium'
        워크시트.Range('A8').Value = '증빙자료 별도 첨부'
        워크시트.Range('A8').HorizontalAlignment = -4108
        워크시트.Range('A8').VerticalAlignment = -4108

    
    def 참석자명단(self):
        워크북 = self.엑셀.Workbooks.Add()
        워크시트 = 워크북.Worksheets(1)
        워크시트.Range('A1:g1').Merge()
        워크시트.Range('A1').HorizontalAlignment = -4108
        워크시트.Range('A1').VerticalAlignment = -4108
        워크시트.Cells(1, 1).Font.Name = '맑은 고딕'
        워크시트.Cells(1, 1).Font.Size = 16
        워크시트.Cells(1, 1).Font.Bold = True
        워크시트.Cells(1, 1).Value = '제12회 어쩌구저쩌구 참석자 명단'
        워크시트.Rows(1).RowHeight = 38
        워크시트.Rows('2:3').RowHeight = 20
        워크시트.Rows(4).RowHeight = 30
        워크시트.Rows('5:20').RowHeight = 28
        워크시트.Columns('A:A').ColumnWidth = 5
        워크시트.Columns('B:F').ColumnWidth = 15
        워크시트.Columns('G').ColumnWidth = 30
        워크시트.Range('A3:g3').Merge()
        워크시트.Range('A3').HorizontalAlignment = -4152
        워크시트.Range('A3').VerticalAlignment = -4108
        워크시트.Range('A3').Font.Size = 11
        워크시트.Range('A3').Font.Name = '맑은 고딕'
        워크시트.Range('A3').Value = '2026. 1. 1.(월) 13:00~15:00 / 청주오스코 123호'
        워크시트.Range('A4:G20').Borders(7).LineStyle = 1
        워크시트.Range('A4:G20').Borders(8).LineStyle = 1
        워크시트.Range('A4:G20').Borders(9).LineStyle = 1
        워크시트.Range('A4:G20').Borders(10).LineStyle = 1
        워크시트.Range('A4:G20').Borders(11).LineStyle = 1
        워크시트.Range('A4:G20').Borders(12).LineStyle = 1
        워크시트.Range('A4:G20').Borders(7).Weight = -4138
        워크시트.Range('A4:G20').Borders(8).Weight = -4138
        워크시트.Range('A4:G20').Borders(9).Weight = -4138
        워크시트.Range('A4:G20').Borders(10).Weight = -4138
        워크시트.Range('A4:G20').Borders(11).Weight = 2
        워크시트.Range('A4:G20').Borders(12).Weight = 2
        워크시트.Range('A4:G20').HorizontalAlignment = -4108
        워크시트.Range('A4:G20').VerticalAlignment = -4108
        워크시트.Range('A4:G20').Font.Size = 11
        워크시트.Range('A4:G20').Font.Name = '맑은 고딕'
        워크시트.Range('A4:G4').Interior.Color = 16247775
        워크시트.Range('A4:G4').Font.Bold = True
        워크시트.Range('A4').Value = '연번'
        워크시트.Range('B4').Value = '기관명'
        워크시트.Range('C4').Value = '부서명'
        워크시트.Range('D4').Value = '직급'
        워크시트.Range('E4').Value = '성명'
        워크시트.Range('F4').Value = '사무실 전화번호'
        워크시트.Range('G4').Value = '어쩌구 저쩌구 여부(O, X)'
        워크시트.Range('A5:G6').Font.Color = 12874308
        워크시트.Range('A5:G6').Font.Italic = True
        워크시트.Range('A5').Value = '1'
        워크시트.Range('B5').Value = '행정안전부'
        워크시트.Range('C5').Value = '행정제도과'
        워크시트.Range('D5').Value = '행정사무관'
        워크시트.Range('E5').Value = '김사무'
        워크시트.Range('F5').Value = '044-205-2250'
        워크시트.Range('G5').Value = 'O'
        워크시트.Range('A6').Value = '2'
        워크시트.Range('B6').Value = '행정안전부'
        워크시트.Range('C6').Value = '행정제도과'
        워크시트.Range('D6').Value = '간호주사보'
        워크시트.Range('E6').Value = '범피스'
        워크시트.Range('F6').Value = '044-205-2250'
        워크시트.Range('G6').Value = 'O'

    
    def 평가입력예시서식(self):
        워크북 = self.엑셀.Workbooks.Add()
        워크시트 = 워크북.Worksheets(1)
        워크시트.Range('A1').Value = '기준'
        워크시트.Columns('A:BB').HorizontalAlignment = -4108
        워크시트.Columns('A').ColumnWidth = 20
        워크시트.Columns('B:BB').ColumnWidth = 4
        워크시트.Range('B1').Value = '1'
        워크시트.Range('C1').Value = '1'
        워크시트.Range('D1').Value = '1'
        워크시트.Range('E1').Value = '1'
        워크시트.Range('F1').Value = '0.5'
        워크시트.Range('G1').Value = '0.5'
        워크시트.Range('H1').Value = '0.5'
        워크시트.Range('I1').Value = '0.5'
        워크시트.Range('A2').Value = 'A부'
        워크시트.Range('B2').Value = '100'
        워크시트.Range('C2').Value = '90'
        워크시트.Range('D2').Value = '90'
        워크시트.Range('E2').Value = '100'
        워크시트.Range('F2').Value = '100'
        워크시트.Range('G2').Value = '90'
        워크시트.Range('H2').Value = '90'
        워크시트.Range('I2').Value = '100'
        워크시트.Range('A3').Value = 'B부'
        워크시트.Range('B3').Value = '80'
        워크시트.Range('C3').Value = '70'
        워크시트.Range('D3').Value = '70'
        워크시트.Range('E3').Value = '80'
        워크시트.Range('F3').Value = '70'
        워크시트.Range('G3').Value = '70'
        워크시트.Range('H3').Value = '70'
        워크시트.Range('I3').Value = '70'
        워크시트.Range('A4').Value = 'C부'
        워크시트.Range('B4').Value = '100'
        워크시트.Range('C4').Value = '100'
        워크시트.Range('D4').Value = '100'
        워크시트.Range('E4').Value = '100'
        워크시트.Range('F4').Value = '100'
        워크시트.Range('G4').Value = '100'
        워크시트.Range('H4').Value = '100'
        워크시트.Range('I4').Value = '100'
        워크시트.Range('A5').Value = 'D부'
        워크시트.Range('B5').Value = '90'
        워크시트.Range('C5').Value = '100'
        워크시트.Range('D5').Value = '100'
        워크시트.Range('E5').Value = '100'
        워크시트.Range('F5').Value = '100'
        워크시트.Range('G5').Value = '100'
        워크시트.Range('H5').Value = '100'
        워크시트.Range('I5').Value = '100'

    
    def 평가입력순위산출(self):
        if self.엑셀.Selection.Rows.Count > 1:
            데이터 = self.엑셀.Selection.Value
            데이터 = list(데이터)
            비율값 = 데이터[0][1:]
            부서별데이터 = 데이터[1:]
            비율값합 = sum(비율값)
            결과 = []
            for 부서 in 부서별데이터:
                부서이름 = 부서[0]
                점수들 = 부서[1:]
                if (lambda .0: if None:
passfor None in .0:
if ():
if 점수 * 비율값[i]:
passcontinueNone):
                    pass
                합계 = (lambda .0: if None:
passfor None in .0:
if ():
if 점수 * 비율값[i]:
passcontinueNone)(enumerate(점수들)())
                평균 = round(합계 / 비율값합, 2)
                결과.append((부서이름, 합계, 평균))
            sum
            결과.sort(key = (lambda x: x[1]), reverse = True)
            print(결과)
            새워크북 = self.엑셀.Workbooks.Add()
            새워크시트 = 새워크북.Sheets(1)
            새워크시트.Columns('A:D').HorizontalAlignment = -4108
            새워크시트.Columns('A').ColumnWidth = 4
            새워크시트.Columns('B').ColumnWidth = 20
            새워크시트.Columns('C:D').ColumnWidth = 10
            새워크시트.Range('A1').Value = '순위'
            새워크시트.Range('B1').Value = '이름'
            새워크시트.Range('C1').Value = '합계'
            새워크시트.Range('D1').Value = '평균'
            for i in range(1, len(결과) + 1):
                새워크시트.Cells(i + 1, 1).Value = i
            for None in enumerate(결과, start = 2):
                if ():
                    for 열, 값 in enumerate(줄, start = 2):
                        새워크시트.Cells(행, 열).Value = 값
                    continue
                    return None
                    return None

    if (lambda self, 행수: 새워크북 = self.엑셀.Workbooks.Add()for None in range(3):
if None:
continue새워크북.Sheets(1).Name = 'A시트'새워크북.Sheets(2).Name = 'B시트'새워크북.Sheets(3).Name = 'C시트'A시트 = 새워크북.Sheets('A시트')B시트 = 새워크북.Sheets('B시트')C시트 = 새워크북.Sheets('C시트')파일들 = None(title = 'Open File', filetypes = [
('Excel Files', '*.xlsx *.xls')])A행 = A시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1B행 = B시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1C행 = C시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1for 파일경로 in 파일들:
임시파일 = self.엑셀.Workbooks.Open(파일경로)임시시트 = 임시파일.Sheets(2)마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))붙임시트 = A시트.Range(A시트.Cells(A행, 1), A시트.Cells(A행 + 복사시트.Rows.Count - 1, 14))붙임시트.Value = 복사시트.ValueA행 = A시트.Cells(A시트.Rows.Count, 2).End(-4162).Row + 1임시시트 = 임시파일.Sheets(3)마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))붙임시트 = B시트.Range(B시트.Cells(B행, 1), B시트.Cells(B행 + 복사시트.Rows.Count - 1, 14))붙임시트.Value = 복사시트.ValueB행 = B시트.Cells(B시트.Rows.Count, 2).End(-4162).Row + 1임시시트 = 임시파일.Sheets(4)마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))붙임시트 = C시트.Range(C시트.Cells(C행, 1), C시트.Cells(C행 + 복사시트.Rows.Count - 1, 14))붙임시트.Value = 복사시트.ValueC행 = C시트.Cells(C시트.Rows.Count, 2).End(-4162).Row + 1임시파일.Close(SaveChanges = False)filedialog.askopenfilenames):
        
        def 민원제도과취합(self, 행수):
            새워크북 = self.엑셀.Workbooks.Add()
            for None in range(3):
                if None:
                    continue
                    새워크북.Sheets(1).Name = 'A시트'
            새워크북.Sheets(2).Name = 'B시트'
            새워크북.Sheets(3).Name = 'C시트'
            A시트 = 새워크북.Sheets('A시트')
            B시트 = 새워크북.Sheets('B시트')
            C시트 = 새워크북.Sheets('C시트')
            파일들 = None(title = 'Open File', filetypes = [
                ('Excel Files', '*.xlsx *.xls')])
            A행 = A시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            B행 = B시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            C행 = C시트.Cells(self.엑셀.ActiveSheet.Rows.Count, 2).End(-4162).Row + 1
            for 파일경로 in 파일들:
                임시파일 = self.엑셀.Workbooks.Open(파일경로)
                임시시트 = 임시파일.Sheets(2)
                마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))
                붙임시트 = A시트.Range(A시트.Cells(A행, 1), A시트.Cells(A행 + 복사시트.Rows.Count - 1, 14))
                붙임시트.Value = 복사시트.Value
                A행 = A시트.Cells(A시트.Rows.Count, 2).End(-4162).Row + 1
                임시시트 = 임시파일.Sheets(3)
                마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))
                붙임시트 = B시트.Range(B시트.Cells(B행, 1), B시트.Cells(B행 + 복사시트.Rows.Count - 1, 14))
                붙임시트.Value = 복사시트.Value
                B행 = B시트.Cells(B시트.Rows.Count, 2).End(-4162).Row + 1
                임시시트 = 임시파일.Sheets(4)
                마지막행 = 임시시트.Cells(임시시트.Rows.Count, 2).End(-4162).Row
                복사시트 = 임시시트.Range(임시시트.Cells(행수, 1), 임시시트.Cells(마지막행, 14))
                붙임시트 = C시트.Range(C시트.Cells(C행, 1), C시트.Cells(C행 + 복사시트.Rows.Count - 1, 14))
                붙임시트.Value = 복사시트.Value
                C행 = C시트.Cells(C시트.Rows.Count, 2).End(-4162).Row + 1
                임시파일.Close(SaveChanges = False)
            filedialog.askopenfilenames

    
    def 민원제도과합계(self):
        워크시트 = self.엑셀.ActiveSheet
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        보유데이터1 = 워크시트.Range(f'''B1:C{마지막행}''').Value
        보유데이터1 = (lambda .0: if None:
passfor row in .0:
if (lambda .0: if None:
passfor None in .0:
if None:
if '' if None else x:
passcontinueNone)(row()):
                    pass
                (lambda .0: if None:
passfor None in .0:
if None:
if '' if None else x:
passcontinueNone)(row())
)(보유데이터1())
        보유데이터2 = 워크시트.Range(f'''G1:N{마지막행}''').Value
        보유데이터2 = (lambda .0: if None:
passfor row in .0:
if (lambda .0: if None:
passfor x in .0:
if isinstance(x, (int, float)):
passif x if isinstance(x, (int, float)) else 0:
passx if isinstance(x, (int, float)) else 0)(row()):
                    pass
                (lambda .0: if None:
passfor x in .0:
if isinstance(x, (int, float)):
passif x if isinstance(x, (int, float)) else 0:
passx if isinstance(x, (int, float)) else 0)(row())
)(보유데이터2())
        보유데이터 = []
        for None in zip(보유데이터1, 보유데이터2):
            if ():
                continue
                ()
                { } = None
                for 줄 in 보유데이터:
                    키 = 줄[0].strip()
                    숫자 = 줄[2:]
                    if 키 not in 결과딕:
                        결과딕[키] = [
                            0] * 8
                    for i in range(8):
                        pass
                [] = None
                for k in 결과딕:
                    결과데이터.append([
                        k] + 결과딕[k])
                새워크북 = self.엑셀.Workbooks.Add()
                새워크시트 = 새워크북.Sheets(1)
                새워크시트.Cells(1, 1).Value = '구분'
                새워크시트.Cells(1, 2).Value = '폭언'
                새워크시트.Cells(1, 3).Value = '협박'
                새워크시트.Cells(1, 4).Value = '성희롱'
                새워크시트.Cells(1, 5).Value = '폭행'
                새워크시트.Cells(1, 6).Value = '기물파손'
                새워크시트.Cells(1, 7).Value = '위험물'
                새워크시트.Cells(1, 8).Value = '신상공개'
                새워크시트.Cells(1, 9).Value = '기타'
                for 행, 줄 in enumerate(결과데이터, start = 2):
                    for 열, 값 in enumerate(줄, start = 1):
                        새워크시트.Cells(행, 열).Value = 값
                return None

    
    def 민원제도과합계2(self):
        워크시트 = self.엑셀.ActiveSheet
        마지막행 = 워크시트.Cells(워크시트.Rows.Count, 2).End(-4162).Row
        보유데이터1 = 워크시트.Range(f'''B1:C{마지막행}''').Value
        보유데이터1 = (lambda .0: if None:
passfor row in .0:
if (lambda .0: if None:
passfor None in .0:
if None:
if '' if None else x:
passcontinueNone)(row()):
                    pass
                (lambda .0: if None:
passfor None in .0:
if None:
if '' if None else x:
passcontinueNone)(row())
)(보유데이터1())
        보유데이터2 = 워크시트.Range(f'''G1:N{마지막행}''').Value
        보유데이터2 = (lambda .0: if None:
passfor row in .0:
if (lambda .0: if None:
passfor x in .0:
if isinstance(x, (int, float)):
passif x if isinstance(x, (int, float)) else 0:
passx if isinstance(x, (int, float)) else 0)(row()):
                    pass
                (lambda .0: if None:
passfor x in .0:
if isinstance(x, (int, float)):
passif x if isinstance(x, (int, float)) else 0:
passx if isinstance(x, (int, float)) else 0)(row())
)(보유데이터2())
        보유데이터 = []
        for None in zip(보유데이터1, 보유데이터2):
            if ():
                continue
                ()
                { } = None
                for 줄 in 보유데이터:
                    키 = 줄[0].strip() + ' ' + 줄[1].strip()
                    숫자 = 줄[2:]
                    if 키 not in 결과딕:
                        결과딕[키] = [
                            0] * 8
                    for i in range(8):
                        pass
                [] = None
                for k in 결과딕:
                    결과데이터.append([
                        k] + 결과딕[k])
                새워크북 = self.엑셀.Workbooks.Add()
                새워크시트 = 새워크북.Sheets(1)
                새워크시트.Cells(1, 1).Value = '구분'
                새워크시트.Cells(1, 2).Value = '폭언'
                새워크시트.Cells(1, 3).Value = '협박'
                새워크시트.Cells(1, 4).Value = '성희롱'
                새워크시트.Cells(1, 5).Value = '폭행'
                새워크시트.Cells(1, 6).Value = '기물파손'
                새워크시트.Cells(1, 7).Value = '위험물'
                새워크시트.Cells(1, 8).Value = '신상공개'
                새워크시트.Cells(1, 9).Value = '기타'
                for 행, 줄 in enumerate(결과데이터, start = 2):
                    for 열, 값 in enumerate(줄, start = 1):
                        새워크시트.Cells(행, 열).Value = 값
                return None

    
    def 공무용차량취합(self):
        새워크북 = self.엑셀.Workbooks.Add()
        for None in range(9):
            if None:
                continue
        새워크북.Sheets(1).Name = '정수'
        새워크북.Sheets(2).Name = '증감사유'
        새워크북.Sheets(3).Name = '보유'
        새워크북.Sheets(4).Name = '정수보유비교'
        새워크북.Sheets(5).Name = '도입'
        새워크북.Sheets(6).Name = '처분'
        새워크북.Sheets(7).Name = '전용차량'
        새워크북.Sheets(8).Name = '전체차량'
        정수 = 새워크북.Sheets('정수')
        증감사유 = 새워크북.Sheets('증감사유')
        보유 = 새워크북.Sheets('보유')
        정수보유비교 = 새워크북.Sheets('정수보유비교')
        도입 = 새워크북.Sheets('도입')
        처분 = 새워크북.Sheets('처분')
        전용차량 = 새워크북.Sheets('전용차량')
        전체차량 = 새워크북.Sheets('전체차량')
        파일들 = None(title = 'Open File', filetypes = [
            ('Excel Files', '*.xlsx *.xls')])
        정수행 = 정수.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        증감사유행 = 증감사유.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        보유행 = 보유.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        정수보유비교행 = 정수보유비교.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        도입행 = 도입.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        처분행 = 처분.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        전용차량행 = 전용차량.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        전체차량행 = 전체차량.Cells(self.엑셀.ActiveSheet.Rows.Count, 1).End(-4162).Row + 1
        for i, 파일경로 in enumerate(파일들):
            임시파일 = self.엑셀.Workbooks.Open(파일경로)
            if i == 0:
                정수.Cells(1, 1).Value = '정수현황'
                정수.Cells(1, 2).Value = '2년전'
                정수.Cells(1, 3).Value = '1년전'
                정수.Cells(1, 4).Value = '증감'
                정수.Cells(1, 5).Value = '업무용'
                정수.Cells(1, 6).Value = '전용'
                정수.Cells(1, 7).Value = '승합용'
                정수.Cells(1, 8).Value = '화물용'
                정수.Cells(1, 9).Value = '특수용'
            정수.Cells(정수행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
            정수.Cells(정수행, 2).Value = 임시파일.Sheets(8).Range('B6').Value
            정수.Cells(정수행, 3).Value = 임시파일.Sheets(8).Range('B5').Value
            정수.Cells(정수행, 4).Value = 임시파일.Sheets(8).Range('B4').Value
            정수.Cells(정수행, 5).Value = 임시파일.Sheets(8).Range('H5').Value
            정수.Cells(정수행, 6).Value = 임시파일.Sheets(8).Range('C5').Value
            정수.Cells(정수행, 7).Value = 임시파일.Sheets(8).Range('M5').Value
            정수.Cells(정수행, 8).Value = 임시파일.Sheets(8).Range('R5').Value
            정수.Cells(정수행, 9).Value = 임시파일.Sheets(8).Range('W5').Value
            정수행 = 정수.Cells(정수.Rows.Count, 1).End(-4162).Row + 1
            if int(임시파일.Sheets(8).Range('B4').Value) != 0:
                증감사유.Cells(1, 1).Value = '구분'
                증감사유.Cells(1, 2).Value = '대수'
                증감사유.Cells(1, 3).Value = '증감사유'
                증감사유.Cells(증감사유행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
                증감사유.Cells(증감사유행, 2).Value = 임시파일.Sheets(8).Range('B4').Value
                if int(임시파일.Sheets(8).Range('B4').Value) > 0:
                    증감사유.Cells(증감사유행, 3).Value = 임시파일.Sheets(1).Range('B11').Value
                elif int(임시파일.Sheets(8).Range('B4').Value) < 0:
                    증감사유.Cells(증감사유행, 3).Value = 임시파일.Sheets(1).Range('B12').Value
            증감사유행 = 증감사유.Cells(증감사유.Rows.Count, 1).End(-4162).Row + 1
            if i == 0:
                보유.Cells(1, 1).Value = '보유현황'
                보유.Cells(1, 2).Value = '2년전'
                보유.Cells(1, 3).Value = '1년전'
                보유.Cells(1, 4).Value = '업무용'
                보유.Cells(1, 5).Value = '전용'
                보유.Cells(1, 6).Value = '승합용'
                보유.Cells(1, 7).Value = '화물용'
                보유.Cells(1, 8).Value = '특수용'
            보유.Cells(보유행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
            보유.Cells(보유행, 3).Value = 임시파일.Sheets(8).Range('B7').Value
            보유.Cells(보유행, 4).Value = 임시파일.Sheets(8).Range('H7').Value
            보유.Cells(보유행, 5).Value = 임시파일.Sheets(8).Range('C7').Value
            보유.Cells(보유행, 6).Value = 임시파일.Sheets(8).Range('M7').Value
            보유.Cells(보유행, 7).Value = 임시파일.Sheets(8).Range('R7').Value
            보유.Cells(보유행, 8).Value = 임시파일.Sheets(8).Range('W7').Value
            보유행 = 보유.Cells(보유.Rows.Count, 1).End(-4162).Row + 1
            if i == 0:
                정수보유비교.Cells(1, 1).Value = '정수보유비교'
                정수보유비교.Cells(1, 2).Value = '정수'
                정수보유비교.Cells(1, 3).Value = '보유'
                정수보유비교.Cells(1, 4).Value = '정수-보유'
                정수보유비교.Cells(1, 5).Value = '초과보유'
            정수보유비교.Cells(정수보유비교행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
            정수보유비교.Cells(정수보유비교행, 2).Value = 임시파일.Sheets(8).Range('B5').Value
            정수보유비교.Cells(정수보유비교행, 3).Value = 임시파일.Sheets(8).Range('B7').Value
            정수보유차 = int(임시파일.Sheets(8).Range('B5').Value) - int(임시파일.Sheets(8).Range('B7').Value)
            정수보유비교.Cells(정수보유비교행, 4).Value = 정수보유차
            정수보유비교행 = 정수보유비교.Cells(정수보유비교.Rows.Count, 1).End(-4162).Row + 1
            if i == 0:
                도입.Cells(1, 1).Value = '구입'
                도입.Cells(1, 2).Value = '구입대수'
                도입.Cells(1, 3).Value = '업무용'
                도입.Cells(1, 4).Value = '전용'
                도입.Cells(1, 5).Value = '승합용'
                도입.Cells(1, 6).Value = '화물용'
                도입.Cells(1, 7).Value = '특수용'
                도입.Cells(1, 8).Value = '임대대수'
                도입.Cells(1, 9).Value = '업무용'
                도입.Cells(1, 10).Value = '전용'
                도입.Cells(1, 11).Value = '승합용'
                도입.Cells(1, 12).Value = '화물용'
                도입.Cells(1, 13).Value = '특수용'
            도입.Cells(도입행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
            도입.Cells(도입행, 2).Value = 임시파일.Sheets(8).Range('B11').Value
            도입.Cells(도입행, 3).Value = 임시파일.Sheets(8).Range('H11').Value
            도입.Cells(도입행, 4).Value = 임시파일.Sheets(8).Range('C11').Value
            도입.Cells(도입행, 5).Value = 임시파일.Sheets(8).Range('M11').Value
            도입.Cells(도입행, 6).Value = 임시파일.Sheets(8).Range('R11').Value
            도입.Cells(도입행, 7).Value = 임시파일.Sheets(8).Range('W11').Value
            도입.Cells(도입행, 8).Value = 임시파일.Sheets(8).Range('B12').Value
            도입.Cells(도입행, 9).Value = 임시파일.Sheets(8).Range('H12').Value
            도입.Cells(도입행, 10).Value = 임시파일.Sheets(8).Range('C12').Value
            도입.Cells(도입행, 11).Value = 임시파일.Sheets(8).Range('M12').Value
            도입.Cells(도입행, 12).Value = 임시파일.Sheets(8).Range('R12').Value
            도입.Cells(도입행, 13).Value = 임시파일.Sheets(8).Range('W12').Value
            도입행 = 도입.Cells(도입.Rows.Count, 1).End(-4162).Row + 1
            if i == 0:
                처분.Cells(1, 1).Value = '처분'
                처분.Cells(1, 2).Value = '구매처분'
                처분.Cells(1, 3).Value = '업무용'
                처분.Cells(1, 4).Value = '전용'
                처분.Cells(1, 5).Value = '승합용'
                처분.Cells(1, 6).Value = '화물용'
                처분.Cells(1, 7).Value = '특수용'
                처분.Cells(1, 8).Value = '임대처분'
                처분.Cells(1, 9).Value = '업무용'
                처분.Cells(1, 10).Value = '전용'
                처분.Cells(1, 11).Value = '승합용'
                처분.Cells(1, 12).Value = '화물용'
                처분.Cells(1, 13).Value = '특수용'
                처분.Cells(1, 14).Value = '구매개월'
                처분.Cells(1, 15).Value = '업무용'
                처분.Cells(1, 16).Value = '전용'
                처분.Cells(1, 17).Value = '승합용'
                처분.Cells(1, 18).Value = '화물용'
                처분.Cells(1, 19).Value = '특수용'
                처분.Cells(1, 20).Value = '임차개월'
                처분.Cells(1, 21).Value = '업무용'
                처분.Cells(1, 22).Value = '전용'
                처분.Cells(1, 23).Value = '승합용'
                처분.Cells(1, 24).Value = '화물용'
                처분.Cells(1, 25).Value = '특수용'
                처분.Cells(1, 26).Value = '구매키로'
                처분.Cells(1, 27).Value = '업무용'
                처분.Cells(1, 28).Value = '전용'
                처분.Cells(1, 29).Value = '승합용'
                처분.Cells(1, 30).Value = '화물용'
                처분.Cells(1, 31).Value = '특수용'
                처분.Cells(1, 32).Value = '임대키로'
                처분.Cells(1, 33).Value = '업무용'
                처분.Cells(1, 34).Value = '전용'
                처분.Cells(1, 35).Value = '승합용'
                처분.Cells(1, 36).Value = '화물용'
                처분.Cells(1, 37).Value = '특수용'
            처분.Cells(처분행, 1).Value = 임시파일.Sheets(1).Range('B2').Value
            처분.Cells(처분행, 2).Value = 임시파일.Sheets(8).Range('B14').Value
            처분.Cells(처분행, 3).Value = 임시파일.Sheets(8).Range('H14').Value
            처분.Cells(처분행, 4).Value = 임시파일.Sheets(8).Range('C14').Value
            처분.Cells(처분행, 5).Value = 임시파일.Sheets(8).Range('M14').Value
            처분.Cells(처분행, 6).Value = 임시파일.Sheets(8).Range('R14').Value
            처분.Cells(처분행, 7).Value = 임시파일.Sheets(8).Range('W14').Value
            처분.Cells(처분행, 8).Value = 임시파일.Sheets(8).Range('B15').Value
            처분.Cells(처분행, 9).Value = 임시파일.Sheets(8).Range('H15').Value
            처분.Cells(처분행, 10).Value = 임시파일.Sheets(8).Range('C15').Value
            처분.Cells(처분행, 11).Value = 임시파일.Sheets(8).Range('M15').Value
            처분.Cells(처분행, 12).Value = 임시파일.Sheets(8).Range('R15').Value
            처분.Cells(처분행, 13).Value = 임시파일.Sheets(8).Range('W15').Value
            처분.Cells(처분행, 15).Value = 임시파일.Sheets(8).Range('D17').Value
            처분.Cells(처분행, 16).Value = 임시파일.Sheets(8).Range('C17').Value
            처분.Cells(처분행, 17).Value = 임시파일.Sheets(8).Range('E17').Value
            처분.Cells(처분행, 18).Value = 임시파일.Sheets(8).Range('F17').Value
            처분.Cells(처분행, 19).Value = 임시파일.Sheets(8).Range('G17').Value
            처분.Cells(처분행, 21).Value = 임시파일.Sheets(8).Range('D18').Value
            처분.Cells(처분행, 22).Value = 임시파일.Sheets(8).Range('C18').Value
            처분.Cells(처분행, 23).Value = 임시파일.Sheets(8).Range('E18').Value
            처분.Cells(처분행, 24).Value = 임시파일.Sheets(8).Range('F18').Value
            처분.Cells(처분행, 25).Value = 임시파일.Sheets(8).Range('G18').Value
            처분.Cells(처분행, 27).Value = 임시파일.Sheets(8).Range('D19').Value
            처분.Cells(처분행, 28).Value = 임시파일.Sheets(8).Range('C19').Value
            처분.Cells(처분행, 29).Value = 임시파일.Sheets(8).Range('E19').Value
            처분.Cells(처분행, 30).Value = 임시파일.Sheets(8).Range('F19').Value
            처분.Cells(처분행, 31).Value = 임시파일.Sheets(8).Range('G19').Value
            처분.Cells(처분행, 33).Value = 임시파일.Sheets(8).Range('D20').Value
            처분.Cells(처분행, 34).Value = 임시파일.Sheets(8).Range('C20').Value
            처분.Cells(처분행, 35).Value = 임시파일.Sheets(8).Range('E20').Value
            처분.Cells(처분행, 36).Value = 임시파일.Sheets(8).Range('F20').Value
            처분.Cells(처분행, 37).Value = 임시파일.Sheets(8).Range('G20').Value
            처분.Cells(처분행, 39).Value = 임시파일.Sheets(8).Range('B21').Value
            처분행 = 처분.Cells(처분.Rows.Count, 1).End(-4162).Row + 1
            마지막행 = 임시파일.Sheets(4).Cells(임시파일.Sheets(4).Rows.Count, 2).End(-4162).Row
            복사시트 = 임시파일.Sheets(4).Range(임시파일.Sheets(4).Cells(3, 1), 임시파일.Sheets(4).Cells(마지막행, 9))
            붙임시트 = 전용차량.Range(전용차량.Cells(전용차량행, 1), 전용차량.Cells(전용차량행 + 복사시트.Rows.Count - 1, 9))
            붙임시트.Value = 복사시트.Value
            전용차량행 = 전용차량.Cells(전용차량.Rows.Count, 2).End(-4162).Row + 1
            마지막행 = 임시파일.Sheets(3).Cells(임시파일.Sheets(3).Rows.Count, 2).End(-4162).Row
            복사시트 = 임시파일.Sheets(3).Range(임시파일.Sheets(3).Cells(3, 1), 임시파일.Sheets(3).Cells(마지막행, 16))
            붙임시트 = 전체차량.Range(전체차량.Cells(전체차량행, 1), 전체차량.Cells(전체차량행 + 복사시트.Rows.Count - 1, 16))
            붙임시트.Value = 복사시트.Value
            전체차량행 = 전체차량.Cells(전체차량.Rows.Count, 2).End(-4162).Row + 1
            임시파일.Close(SaveChanges = False)
        None if 정수보유차 < 0 else filedialog.askopenfilenames

    __static_attributes__ = ('\xec\x97\x91\xec\x85\x80', '\xec\x97\x91\xec\x85\x80\xeb\xa6\xac\xec\x8a\xa4\xed\x8a\xb8')

엑셀 = None(엑셀, '\xec\x97\x91\xec\x85\x80')
