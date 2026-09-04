# Source Generated with Decompyle++
# File: ���Ķ��̺귯��_2.marshal (Python 3.13)

from 한컴라이브러리_기본 import 한컴기본
None(import 엑셀.엑셀라이브러리)
from decimal import Decimal
import re
from tkinter import filedialog
from win32com.client.gencache import EnsureDispatch
from datetime import datetime, timedelta

def 한컴2():
    '''\xed\x95\x9c\xec\xbb\xb42'''
    __firstlineno__ = 10
    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
10,
1,
5])self.셀여백제로()self.표전체()self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.글자크기(1)self.캔슬()self.표처음()self.가운데정렬()self.줄간격(130)self.셀여백지정(2, 2, 2, 2)self.폰트('HY헤드라인M')self.글자색(28, 61, 98)if len(내용) >= 3:
self.글자크기(18)self.문장('- ' + 내용[2] + ' -\r\n')self.글자크기(26)if len(내용) >= 1:
if len(내용[0]) >= 16:
passself.글자간격(-4)if len(내용[0]) >= 17:
passself.글자간격(-10)if len(내용[0]) >= 18:
passself.글자장평(95)if len(내용[0]) >= 19:
passself.글자장평(90)if len(내용[0]) >= 20:
passself.글자간격(-15)self.문장(내용[0])self.글자크기(22)self.문장(' (보고)')else:
self.문장('제목')self.표오른쪽(1)self.표배경그라데이션2('Linear', 90, [
[
255,
0,
51,
102],
[
0,
204,
255,
255]])self.표오른쪽(1)self.글자크기(11)self.폰트('맑은 고딕')self.오른쪽정렬()self.문장('【')self.오늘날짜무공백()self.문장(' ')if len(내용) >= 2:
self.문장(내용[1])else:
self.문장('개발팀장 범피스(1234)')self.문장('】')self.표나가기2()):
        
        def 부교공제목(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                10,
                1,
                5])
            self.셀여백제로()
            self.표전체()
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.글자크기(1)
            self.캔슬()
            self.표처음()
            self.가운데정렬()
            self.줄간격(130)
            self.셀여백지정(2, 2, 2, 2)
            self.폰트('HY헤드라인M')
            self.글자색(28, 61, 98)
            if len(내용) >= 3:
                self.글자크기(18)
            self.문장('- ' + 내용[2] + ' -\r\n')
            self.글자크기(26)
            if len(내용) >= 1:
                if len(내용[0]) >= 16:
                    pass
                self.글자간격(-4)
                if len(내용[0]) >= 17:
                    pass
                self.글자간격(-10)
                if len(내용[0]) >= 18:
                    pass
                self.글자장평(95)
                if len(내용[0]) >= 19:
                    pass
                self.글자장평(90)
                if len(내용[0]) >= 20:
                    pass
                self.글자간격(-15)
                self.문장(내용[0])
                self.글자크기(22)
                self.문장(' (보고)')
            else:
                self.문장('제목')
            self.표오른쪽(1)
            self.표배경그라데이션2('Linear', 90, [
                [
                    255,
                    0,
                    51,
                    102],
                [
                    0,
                    204,
                    255,
                    255]])
            self.표오른쪽(1)
            self.글자크기(11)
            self.폰트('맑은 고딕')
            self.오른쪽정렬()
            self.문장('【')
            self.오늘날짜무공백()
            self.문장(' ')
            if len(내용) >= 2:
                self.문장(내용[1])
            else:
                self.문장('개발팀장 범피스(1234)')
            self.문장('】')
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ㅇ ', 텍스트):
                                pass
                            if None(' ㅇ ', 텍스트):
                                매치 = None(' ㅇ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  - ', 텍스트):
                                pass
                            if None('  - ', 텍스트):
                                매치 = None('  - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   ※ ', 텍스트):
                                pass
                            if None('   ※ ', 텍스트):
                                매치 = None('   ※ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.부교공제목(분리텍스트)
                        self.백스페이스()
                    elif None('^중제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.여광항소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(15)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            None(텍스트, 위치)
            if None('□ ', 텍스트):
                pass
            if None('□ ', 텍스트):
                매치 = None('□ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.문단위(5)
            self.내어쓰기(-30)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                pass
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None(' ㅇ ', 텍스트):
                pass
            if None(' ㅇ ', 텍스트):
                매치 = None(' ㅇ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.문단위(3)
            self.내어쓰기(-42.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  - \\((.*?)\\)', 텍스트):
                pass
            if None('  - \\((.*?)\\)', 텍스트):
                매치 = None('  - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  - ', 텍스트):
                pass
            if None('  - ', 텍스트):
                매치 = None('  - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.문단위(2)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.문단위(2)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 부교공궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ㅇ ', 텍스트):
                                    pass
                                if None(' ㅇ ', 텍스트):
                                    매치 = None(' ㅇ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  - ', 텍스트):
                                    pass
                                if None('  - ', 텍스트):
                                    매치 = None('  - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   ※ ', 텍스트):
                                    pass
                                if None('   ※ ', 텍스트):
                                    매치 = None('   ※ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.부교공제목(분리텍스트)
                            self.백스페이스()
                        elif None('^중제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.여광항소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(15)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                None(텍스트, 위치)
                if None('□ ', 텍스트):
                    pass
                if None('□ ', 텍스트):
                    매치 = None('□ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.문단위(5)
                self.내어쓰기(-30)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None(' ㅇ ', 텍스트):
                    pass
                if None(' ㅇ ', 텍스트):
                    매치 = None(' ㅇ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.문단위(3)
                self.내어쓰기(-42.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  - \\((.*?)\\)', 텍스트):
                    pass
                if None('  - \\((.*?)\\)', 텍스트):
                    매치 = None('  - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  - ', 텍스트):
                    pass
                if None('  - ', 텍스트):
                    매치 = None('  - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.문단위(2)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.문단위(2)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.부교공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.부교공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 부교공궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.부교공궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.부교공궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.부교공궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.부교공궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 부교공궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.부교공궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.부교공궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 번호, 내용: self.표만들기([
6.7,
1,
193 - self.문단여백측정()], [
8.6])self.셀여백제로()self.표배경색(0, 51, 102)self.표테두리타입(0, 0, 0, 0)self.글자크기(16)self.진하게()self.가운데정렬()self.폰트('HY헤드라인M')self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표너비줄이기(2)self.표테두리타입(0, 0, 0, 0)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 6, 0, 0)self.표테두리단일선색('하', 38, 48, 86)self.글자크기(16)self.폰트('HY헤드라인M')self.문장(' ' + 내용)self.표나가기2()):
        
        def 여광항소제목(self, 번호, 내용):
            self.표만들기([
                6.7,
                1,
                193 - self.문단여백측정()], [
                8.6])
            self.셀여백제로()
            self.표배경색(0, 51, 102)
            self.표테두리타입(0, 0, 0, 0)
            self.글자크기(16)
            self.진하게()
            self.가운데정렬()
            self.폰트('HY헤드라인M')
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표너비줄이기(2)
            self.표테두리타입(0, 0, 0, 0)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(0, 6, 0, 0)
            self.표테두리단일선색('하', 38, 48, 86)
            self.글자크기(16)
            self.폰트('HY헤드라인M')
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 이미지, 제목: self.표만들기([
205.5 - self.문단여백측정()], [
0.9,
10,
1])self.셀여백제로()self.표전체()self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.글자크기(1)self.캔슬()self.표처음()self.사진넣기배경(이미지[0])self.표오른쪽(1)self.폰트('HY헤드라인M')self.셀여백지정(2, 2, 2, 2)self.글자크기(20)self.가운데정렬()self.문장(제목)self.표오른쪽(1)self.사진넣기배경(이미지[1])self.표나가기2()):
        
        def 여광항제목(self, 이미지, 제목):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                0.9,
                10,
                1])
            self.셀여백제로()
            self.표전체()
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.글자크기(1)
            self.캔슬()
            self.표처음()
            self.사진넣기배경(이미지[0])
            self.표오른쪽(1)
            self.폰트('HY헤드라인M')
            self.셀여백지정(2, 2, 2, 2)
            self.글자크기(20)
            self.가운데정렬()
            self.문장(제목)
            self.표오른쪽(1)
            self.사진넣기배경(이미지[1])
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ㅇ ', 텍스트):
                                pass
                            if None(' ㅇ ', 텍스트):
                                매치 = None(' ㅇ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  - ', 텍스트):
                                pass
                            if None('  - ', 텍스트):
                                매치 = None('  - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   ※ ', 텍스트):
                                pass
                            if None('   ※ ', 텍스트):
                                매치 = None('   ※ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.여광항제목(이미지, 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^중제목\\s*:\\s*', 텍스트):
                pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.여광항소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(15)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            None(텍스트, 위치)
            if None('□ ', 텍스트):
                pass
            if None('□ ', 텍스트):
                매치 = None('□ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.문단위(5)
            self.내어쓰기(-30)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                pass
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None(' ㅇ ', 텍스트):
                pass
            if None(' ㅇ ', 텍스트):
                매치 = None(' ㅇ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.문단위(3)
            self.내어쓰기(-42.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  - \\((.*?)\\)', 텍스트):
                pass
            if None('  - \\((.*?)\\)', 텍스트):
                매치 = None('  - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  - ', 텍스트):
                pass
            if None('  - ', 텍스트):
                매치 = None('  - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.문단위(2)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.문단위(2)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
):
        
        def 여광항궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ㅇ ', 텍스트):
                                    pass
                                if None(' ㅇ ', 텍스트):
                                    매치 = None(' ㅇ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  - ', 텍스트):
                                    pass
                                if None('  - ', 텍스트):
                                    매치 = None('  - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   ※ ', 텍스트):
                                    pass
                                if None('   ※ ', 텍스트):
                                    매치 = None('   ※ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.여광항제목(이미지, 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^중제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.여광항소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(15)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                None(텍스트, 위치)
                if None('□ ', 텍스트):
                    pass
                if None('□ ', 텍스트):
                    매치 = None('□ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.문단위(5)
                self.내어쓰기(-30)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None(' ㅇ ', 텍스트):
                    pass
                if None(' ㅇ ', 텍스트):
                    매치 = None(' ㅇ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.문단위(3)
                self.내어쓰기(-42.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  - \\((.*?)\\)', 텍스트):
                    pass
                if None('  - \\((.*?)\\)', 텍스트):
                    매치 = None('  - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  - ', 텍스트):
                    pass
                if None('  - ', 텍스트):
                    매치 = None('  - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.문단위(2)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.문단위(2)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.여광항궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.여광항궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 여광항궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.여광항궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.여광항궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.여광항궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.여광항궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 여광항궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.여광항궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.여광항궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
10])self.표테두리타입(8, 8, 0, 0)self.표테두리굵기(7, 7, 7, 7)self.자간헌터(0)self.셀여백지정(2, 2, 2, 2)self.폰트('함초롬바탕')self.내어쓰기(-22)self.글자크기(15)self.줄간격(160)입력내용 = (lambda .0: if None:
passfor part in .0:
if '◇ ' + part.strip():
pass'◇ ' + part.strip())(내용.split('엔터 ')())
        self.문장(입력내용)
        self.표나가기2()
):
        
        def 석유공요약(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                10])
            self.표테두리타입(8, 8, 0, 0)
            self.표테두리굵기(7, 7, 7, 7)
            self.자간헌터(0)
            self.셀여백지정(2, 2, 2, 2)
            self.폰트('함초롬바탕')
            self.내어쓰기(-22)
            self.글자크기(15)
            self.줄간격(160)
            입력내용 = (lambda .0: if None:
passfor part in .0:
if '◇ ' + part.strip():
pass'◇ ' + part.strip())(내용.split('엔터 ')())
            self.문장(입력내용)
            self.표나가기2()

    if (lambda self, 번호, 내용: self.문단위(15)self.표만들기([
9.1,
1,
190 - self.문단여백측정()], [
8.8])self.셀여백제로()self.표배경색(62, 88, 137)self.표테두리타입(0, 0, 0, 0)self.글자크기(18)self.진하게()self.가운데정렬()self.폰트('HY견명조')self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표너비줄이기(2)self.표테두리타입(0, 0, 0, 0)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 8, 0, 0)self.표테두리단일선색('하', 192, 192, 192)self.글자크기(18)self.폰트('HY울릉도M')self.문장(' ' + 내용)self.표나가기2()):
        
        def 석유공소제목(self, 번호, 내용):
            self.문단위(15)
            self.표만들기([
                9.1,
                1,
                190 - self.문단여백측정()], [
                8.8])
            self.셀여백제로()
            self.표배경색(62, 88, 137)
            self.표테두리타입(0, 0, 0, 0)
            self.글자크기(18)
            self.진하게()
            self.가운데정렬()
            self.폰트('HY견명조')
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표너비줄이기(2)
            self.표테두리타입(0, 0, 0, 0)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(0, 8, 0, 0)
            self.표테두리단일선색('하', 192, 192, 192)
            self.글자크기(18)
            self.폰트('HY울릉도M')
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
0.7,
10,
0.5,
7])self.셀여백제로()self.표전체()self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.글자크기(1)self.캔슬()self.표처음()self.표배경색(0, 128, 192)self.표오른쪽(1)self.폰트('HY울릉도M')self.글자크기(20)self.가운데정렬()if len(내용) >= 1:
self.문장(내용[0])else:
self.문장('제목')self.표오른쪽(1)self.표배경그라데이션2('Linear', 90, [
[
255,
0,
128,
192],
[
0,
60,
191,
255]])self.표오른쪽(1)self.오른쪽정렬()self.글자크기(12)self.폰트('맑은 고딕')self.오늘날짜축약무공백열콤마()self.문장(', ')if len(내용) >= 2:
self.문장(내용[1])else:
self.문장('부서명/팀명/기안자명(1234)')self.표나가기2()):
        
        def 석유공제목(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                0.7,
                10,
                0.5,
                7])
            self.셀여백제로()
            self.표전체()
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.글자크기(1)
            self.캔슬()
            self.표처음()
            self.표배경색(0, 128, 192)
            self.표오른쪽(1)
            self.폰트('HY울릉도M')
            self.글자크기(20)
            self.가운데정렬()
            if len(내용) >= 1:
                self.문장(내용[0])
            else:
                self.문장('제목')
            self.표오른쪽(1)
            self.표배경그라데이션2('Linear', 90, [
                [
                    255,
                    0,
                    128,
                    192],
                [
                    0,
                    60,
                    191,
                    255]])
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.글자크기(12)
            self.폰트('맑은 고딕')
            self.오늘날짜축약무공백열콤마()
            self.문장(', ')
            if len(내용) >= 2:
                self.문장(내용[1])
            else:
                self.문장('부서명/팀명/기안자명(1234)')
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ○ ', 텍스트):
                                pass
                            if None(' ○ ', 텍스트):
                                매치 = None(' ○ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  - ', 텍스트):
                                pass
                            if None('  - ', 텍스트):
                                매치 = None('  - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   ※ ', 텍스트):
                                pass
                            if None('   ※ ', 텍스트):
                                매치 = None('   ※ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.석유공제목(분리텍스트)
                        self.백스페이스()
                    elif None('^중제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.석유공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.석유공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('함초롬바탕')
            self.글자크기(15)
            self.문단위(10)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            None(텍스트, 위치)
            if None('□ \\((.*?)\\)', 텍스트):
                pass
            if None('□ \\((.*?)\\)', 텍스트):
                매치 = None('□ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.폰트('HY울릉도M')
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('□ ', 텍스트):
                pass
            if None('□ ', 텍스트):
                매치 = None('□ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('함초롬바탕')
            self.글자크기(15)
            self.문단위(5)
            self.내어쓰기(-30)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ○ \\((.*?)\\)', 텍스트):
                pass
            if None(' ○ \\((.*?)\\)', 텍스트):
                매치 = None(' ○ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.폰트('HY울릉도M')
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  ㅇ ', 텍스트):
                pass
            if None('  ㅇ ', 텍스트):
                매치 = None('  ㅇ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('함초롬바탕')
            self.글자크기(15)
            self.문단위(3)
            self.내어쓰기(-42.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  - \\((.*?)\\)', 텍스트):
                pass
            if None('  - \\((.*?)\\)', 텍스트):
                매치 = None('  - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.폰트('HY울릉도M')
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  - ', 텍스트):
                pass
            if None('  - ', 텍스트):
                매치 = None('  - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
            텍스트 = None('(?<=\\*)\\s+(?=\\*)', '', 텍스트)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(12)
            self.내어쓰기(-29.1)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(12)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 석유공궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif None('   ※ ', 텍스트):
매치 = None('   ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ○ ', 텍스트):
                                    pass
                                if None(' ○ ', 텍스트):
                                    매치 = None(' ○ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  - ', 텍스트):
                                    pass
                                if None('  - ', 텍스트):
                                    매치 = None('  - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   ※ ', 텍스트):
                                    pass
                                if None('   ※ ', 텍스트):
                                    매치 = None('   ※ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.석유공제목(분리텍스트)
                            self.백스페이스()
                        elif None('^중제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.석유공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.석유공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('함초롬바탕')
                self.글자크기(15)
                self.문단위(10)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                None(텍스트, 위치)
                if None('□ \\((.*?)\\)', 텍스트):
                    pass
                if None('□ \\((.*?)\\)', 텍스트):
                    매치 = None('□ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.폰트('HY울릉도M')
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('□ ', 텍스트):
                    pass
                if None('□ ', 텍스트):
                    매치 = None('□ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('함초롬바탕')
                self.글자크기(15)
                self.문단위(5)
                self.내어쓰기(-30)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ○ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ○ \\((.*?)\\)', 텍스트):
                    매치 = None(' ○ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.폰트('HY울릉도M')
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  ㅇ ', 텍스트):
                    pass
                if None('  ㅇ ', 텍스트):
                    매치 = None('  ㅇ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('함초롬바탕')
                self.글자크기(15)
                self.문단위(3)
                self.내어쓰기(-42.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  - \\((.*?)\\)', 텍스트):
                    pass
                if None('  - \\((.*?)\\)', 텍스트):
                    매치 = None('  - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 4))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.폰트('HY울릉도M')
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  - ', 텍스트):
                    pass
                if None('  - ', 텍스트):
                    매치 = None('  - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
                텍스트 = None('(?<=\\*)\\s+(?=\\*)', '', 텍스트)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(12)
                self.내어쓰기(-29.1)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(12)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.석유공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.석유공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 석유공궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.석유공궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.석유공궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.석유공궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.석유공궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 석유공궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.석유공궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.석유공궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
0.7,
12,
0.7,
7])self.셀여백제로()self.표전체()self.글자크기(1)self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.캔슬()self.표처음()self.표배경색(153, 153, 153)self.표오른쪽(1)self.글자크기(19)self.가운데정렬()self.폰트('HY헤드라인M')self.문장(내용[0])self.표오른쪽(1)self.표배경색(153, 153, 153)self.표오른쪽(1)self.오른쪽정렬()self.글자크기(13)self.중고딕()self.문장(내용[1])self.문장('(')self.오늘날짜축약요없열콤마()self.문장(' ☎')self.문장(내용[2])self.문장(')')self.표나가기2()):
        
        def 에스알제목(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                0.7,
                12,
                0.7,
                7])
            self.셀여백제로()
            self.표전체()
            self.글자크기(1)
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.표처음()
            self.표배경색(153, 153, 153)
            self.표오른쪽(1)
            self.글자크기(19)
            self.가운데정렬()
            self.폰트('HY헤드라인M')
            self.문장(내용[0])
            self.표오른쪽(1)
            self.표배경색(153, 153, 153)
            self.표오른쪽(1)
            self.오른쪽정렬()
            self.글자크기(13)
            self.중고딕()
            self.문장(내용[1])
            self.문장('(')
            self.오늘날짜축약요없열콤마()
            self.문장(' ☎')
            self.문장(내용[2])
            self.문장(')')
            self.표나가기2()

    if (lambda self, 번호, 내용: self.왼쪽정렬()self.표만들기([
17.5,
1.2,
181.8 - self.문단여백측정()], [
10.1])self.셀여백제로()self.표배경색(32, 58, 123)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(17)self.가운데정렬()self.글자색(255, 255, 255)self.문장('붙임' + 번호)self.표오른쪽(1)self.표테두리타입(0, 0, 1, 1)self.표너비줄이기(2)self.표오른쪽(1)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(17)self.셀여백지정(1, 1, 4, 1)self.문장(내용)self.표나가기2()):
        
        def 공항공붙임(self, 번호, 내용):
            self.왼쪽정렬()
            self.표만들기([
                17.5,
                1.2,
                181.8 - self.문단여백측정()], [
                10.1])
            self.셀여백제로()
            self.표배경색(32, 58, 123)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(17)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('붙임' + 번호)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 1)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(17)
            self.셀여백지정(1, 1, 4, 1)
            self.문장(내용)
            self.표나가기2()

    if (lambda self, 번호, 내용: self.왼쪽정렬()self.표만들기([
17.5,
1.2,
181.8 - self.문단여백측정()], [
10.1])self.셀여백제로()self.표배경색(32, 58, 123)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(17)self.가운데정렬()self.글자색(255, 255, 255)self.문장('참고' + 번호)self.표오른쪽(1)self.표테두리타입(0, 0, 1, 1)self.표너비줄이기(2)self.표오른쪽(1)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(17)self.셀여백지정(1, 1, 4, 1)self.문장(내용)self.표나가기2()):
        
        def 공항공참고(self, 번호, 내용):
            self.왼쪽정렬()
            self.표만들기([
                17.5,
                1.2,
                181.8 - self.문단여백측정()], [
                10.1])
            self.셀여백제로()
            self.표배경색(32, 58, 123)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(17)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('참고' + 번호)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 1)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(17)
            self.셀여백지정(1, 1, 4, 1)
            self.문장(내용)
            self.표나가기2()

    if (lambda self, 번호, 내용: self.문단위(10)self.표만들기([
6.9,
1,
179 - self.문단여백측정()], [
9.4])self.셀여백제로()self.표테두리굵기(5, 5, 5, 5)self.표배경색(0, 102, 153)self.가운데정렬()self.폰트('HY헤드라인M')self.글자크기(16)self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표테두리타입(0, 0, 1, 0)self.표너비줄이기(2)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 7, 0, 0)self.표테두리단일선색('하', 0, 102, 153)self.글자크기(18)self.폰트('HY헤드라인M')self.셀여백지정(1, 1, 5, 1)self.문장(내용)self.표나가기2()):
        
        def 공항공소제목(self, 번호, 내용):
            self.문단위(10)
            self.표만들기([
                6.9,
                1,
                179 - self.문단여백측정()], [
                9.4])
            self.셀여백제로()
            self.표테두리굵기(5, 5, 5, 5)
            self.표배경색(0, 102, 153)
            self.가운데정렬()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 0)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(0, 7, 0, 0)
            self.표테두리단일선색('하', 0, 102, 153)
            self.글자크기(18)
            self.폰트('HY헤드라인M')
            self.셀여백지정(1, 1, 5, 1)
            self.문장(내용)
            self.표나가기2()

    if (lambda self, 내용: if len(내용) >= 2:
self.표만들기([
165 - self.문단여백측정(),
37], [
5,
1,
15,
1])else:
self.표만들기([
165 - self.문단여백측정(),
37], [
1,
15,
1])self.셀여백제로()self.표전체()self.글자크기(1)self.폰트('맑은 고딕')self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.캔슬()self.표처음()if len(내용) >= 2:
self.글자크기(13)self.진하게()self.문장(내용[1])self.셀세로정렬(0)self.표오른쪽(1)self.글자크기(13)self.진하게()self.오른쪽정렬()self.오늘날짜점생략()self.셀세로정렬(0)self.표오른쪽(1)self.셀선택()self.표오른쪽(1)self.셀병합()self.표배경색(0, 128, 192)self.표오른쪽(1)self.셀선택()self.표오른쪽(1)self.셀병합()self.글자크기(20)self.폰트('HY헤드라인M')self.진하게()self.가운데정렬()if len(내용) >= 1:
self.문장(내용[0])else:
self.문장('한국공항공사 계획')self.표오른쪽(1)self.셀선택()self.표오른쪽(1)self.셀병합()self.표배경그라데이션2('Linear', 90, [
[
255,
0,
128,
192],
[
0,
60,
191,
255]])self.표나가기2()):
        
        def 공항공제목(self, 내용):
            if len(내용) >= 2:
                self.표만들기([
                    165 - self.문단여백측정(),
                    37], [
                    5,
                    1,
                    15,
                    1])
            else:
                self.표만들기([
                    165 - self.문단여백측정(),
                    37], [
                    1,
                    15,
                    1])
            self.셀여백제로()
            self.표전체()
            self.글자크기(1)
            self.폰트('맑은 고딕')
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.표처음()
            if len(내용) >= 2:
                self.글자크기(13)
                self.진하게()
                self.문장(내용[1])
                self.셀세로정렬(0)
                self.표오른쪽(1)
                self.글자크기(13)
                self.진하게()
                self.오른쪽정렬()
                self.오늘날짜점생략()
                self.셀세로정렬(0)
                self.표오른쪽(1)
            
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.표배경색(0, 128, 192)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.글자크기(20)
            self.폰트('HY헤드라인M')
            self.진하게()
            self.가운데정렬()
            if len(내용) >= 1:
                self.문장(내용[0])
            else:
                self.문장('한국공항공사 계획')
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.표배경그라데이션2('Linear', 90, [
                [
                    255,
                    0,
                    128,
                    192],
                [
                    0,
                    60,
                    191,
                    255]])
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ㅇ ', 텍스트):
passif None('  ㅇ ', 텍스트):
매치 = None('  ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ㅇ \\((.*?)\\) ', 텍스트):
passif None('  ㅇ \\((.*?)\\) ', 텍스트):
매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ㅇ ', 텍스트):
passif None('  ㅇ ', 텍스트):
매치 = None('  ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ㅇ \\((.*?)\\) ', 텍스트):
passif None('  ㅇ \\((.*?)\\) ', 텍스트):
매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  ㅇ ', 텍스트):
                                pass
                            if None('  ㅇ ', 텍스트):
                                매치 = None('  ㅇ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('  ㅇ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None('  ㅇ \\((.*?)\\) ', 텍스트):
                                    매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('    - ', 텍스트):
                                pass
                            if None('    - ', 텍스트):
                                매치 = None('    - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('     ※ ', 텍스트):
                                pass
                            if None('     ※ ', 텍스트):
                                매치 = None('     ※ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('     \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.공항공제목(분리텍스트)
                        self.백스페이스()
                    elif None('^중제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.공항공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.붙임카운트 = self.붙임카운트 + 1
                self.공항공붙임(str(self.붙임카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.참고카운트 = self.참고카운트 + 1
                self.공항공참고(str(self.참고카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(10)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            None(텍스트, 위치)
            if None('□ \\((.*?)\\)', 텍스트):
                pass
            if None('□ \\((.*?)\\)', 텍스트):
                매치 = None('□ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(16)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('□ ', 텍스트):
                pass
            if None('□ ', 텍스트):
                매치 = None('□ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '  ㅇ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-30)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치)
            if None('  ㅇ \\((.*?)\\)', 텍스트):
                pass
            if None('  ㅇ \\((.*?)\\)', 텍스트):
                매치 = None('  ㅇ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.글자색(0, 0, 255)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  ㅇ ', 텍스트):
                pass
            if None('  ㅇ ', 텍스트):
                매치 = None('  ㅇ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '    - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-42.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치)
            if None('    - \\((.*?)\\)', 텍스트):
                pass
            if None('    - \\((.*?)\\)', 텍스트):
                매치 = None('    - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('    - ', 텍스트):
                pass
            if None('    - ', 텍스트):
                매치 = None('    - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '     * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '     ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 공항공궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ㅇ ', 텍스트):
passif None('  ㅇ ', 텍스트):
매치 = None('  ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ㅇ \\((.*?)\\) ', 텍스트):
passif None('  ㅇ \\((.*?)\\) ', 텍스트):
매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ㅇ ', 텍스트):
passif None('  ㅇ ', 텍스트):
매치 = None('  ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ㅇ \\((.*?)\\) ', 텍스트):
passif None('  ㅇ \\((.*?)\\) ', 텍스트):
매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  ㅇ ', 텍스트):
                                    pass
                                if None('  ㅇ ', 텍스트):
                                    매치 = None('  ㅇ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('  ㅇ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None('  ㅇ \\((.*?)\\) ', 텍스트):
                                        매치 = None('  ㅇ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('    - ', 텍스트):
                                    pass
                                if None('    - ', 텍스트):
                                    매치 = None('    - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('     ※ ', 텍스트):
                                    pass
                                if None('     ※ ', 텍스트):
                                    매치 = None('     ※ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('     \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.공항공제목(분리텍스트)
                            self.백스페이스()
                        elif None('^중제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.공항공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.붙임카운트 = self.붙임카운트 + 1
                    self.공항공붙임(str(self.붙임카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.참고카운트 = self.참고카운트 + 1
                    self.공항공참고(str(self.참고카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(10)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                None(텍스트, 위치)
                if None('□ \\((.*?)\\)', 텍스트):
                    pass
                if None('□ \\((.*?)\\)', 텍스트):
                    매치 = None('□ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(16)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('□ ', 텍스트):
                    pass
                if None('□ ', 텍스트):
                    매치 = None('□ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '  ㅇ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-30)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치)
                if None('  ㅇ \\((.*?)\\)', 텍스트):
                    pass
                if None('  ㅇ \\((.*?)\\)', 텍스트):
                    매치 = None('  ㅇ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.글자색(0, 0, 255)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  ㅇ ', 텍스트):
                    pass
                if None('  ㅇ ', 텍스트):
                    매치 = None('  ㅇ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '    - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-42.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치)
                if None('    - \\((.*?)\\)', 텍스트):
                    pass
                if None('    - \\((.*?)\\)', 텍스트):
                    매치 = None('    - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('    - ', 텍스트):
                    pass
                if None('    - ', 텍스트):
                    매치 = None('    - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '     * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '     ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.참고카운트 = 0self.카운트카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.공항공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.공항공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 공항공궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.참고카운트 = 0
            self.카운트카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.공항공궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.공항공궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.공항공궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.공항공궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 공항공궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.공항공궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.공항공궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 가스공일반계획프롬프트(self):
        self.새창()
        self.문서여백(15, 15, 15, 15, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('제목: 직원 대상, AI 활용 아이디어 공모전 계획\r\n담당부서: AI디지털혁신처 AI디지털정책부\r\n추진배경: 퇴직율 증가, 업무증대로 인한 부담 증가\r\n추진내용: 공모전 개최, 사전 홍보, 우수사례 확대 전파\r\n추진일정: 2026.7.~2026.12.\r\n기대효과: 직원들의 업무 만족감 향상, 퇴직율 감소\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 한국가스공사 직원으로 #작성내용에 대한 전문적인 지식을 가진 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 \'#작성 규칙\'을 바탕으로 \'#출력 예시\'를 참고하여 문서를 작성하라. 문서의 최소 작성분량이 2페이지 내외가 되도록 작성하라.\r\n\r\n# 출력 규칙\r\n\'#출력 서식\'에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n(제목:, 소제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용" "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n5. 표 출력 규칙\r\n- 항목이 3개 이상 나열되거나 비교·목록 구조가 명확한 경우, 서술 대신 표로 출력\r\n- 표의 컬럼은 보고서 내용에 맞게 자유롭게 구성하되, 마지막 컬럼은 반드시 \'비고\'로 고정\r\n- 표 출력 형식은 아래를 따름:\r\n\r\n  표:[컬럼1]:[컬럼2]:[컬럼3]: ... :비고\r\n  표:[값1]:[값2]:[값3]: ... :\r\n  표:[값1]:[값2]:[값3]: ... :\r\n\r\n- 컬럼명 예시 (내용에 따라 선택):\r\n  · 사업·계획류 → 연번:사업명:사업내용:비고\r\n  · 일정·추진류 → 순번:추진단계:세부내용:기간:비고\r\n  · 예산류 → 연번:사업명:예산액(천원):집행액(천원):비고\r\n  · 조직·인원류 → 연번:담당부서명:담당업무:인원:비고\r\n  · 법령·근거류 → 연번:근거법령:주요내용:비고\r\n- 컬럼 수·명칭은 위 예시에 국한하지 않고 보고서 맥락에 맞게 결정\r\n- 비고값이 없는 행은 해당 셀을 공백으로 출력\r\n\r\n# 출력 예시\r\n표지: 업무효율화 프로그램 개발 계획 : 어디어디처 : 어디어디부\r\n제목: 업무효율화 프로그램 개발 계획\r\n소제목: 목적 및 배경 \r\n네모: 추진목적\r\n원: (RPA 프로그램 개발) 문서 작성 과정에서 발생하는 반복적인 업무의 업무 현장 수요를 반영한 맞춤형 RPA* 프로그램 개발 \r\n별: RPA(Robot Process Automation), 단순 반복적인 업무를 자동화 하는 것 \r\n소제목: 추진 개요 \r\n네모: 주요내용\r\n원: (설문조사) 프로그램 내 직원 의견 반영을 위한 설문조사 실시 \r\n바: 본부 및 소속기관 직원 400명 대상 온라인 설문조사 진행 \r\n당구장: 파견 및 EPS 센터 직원은 제외 \r\n원: (용역계약) 한글(HWP) 프로그램 개발 및 업무 자동화 솔루션 전문 업체와 용역심사 및 계약을 통한 1차 프로그램 개발 진행 \r\n바: 용역 계약 관련 주요 내용1 \r\n바: 용역 계약 관련 주요 내용2 \r\n원: 기타 프로그램 개발 진행 시 추가적으로 들어가야 하는 사항 \r\n바: 관련 세부 내용* \r\n별: 세부 내용 관련 참고 사항\r\n네모: 추진 사업 목록\r\n표:연번:사업명:사업내용:비고\r\n표:1:RPA 프로그램 개발:반복업무 자동화 솔루션 개발:1차 개발\r\n표:2:설문조사 실시:직원 의견 수렴 및 수요 파악:400명 대상\r\n표:3:용역계약 체결:전문업체 선정 및 계약 추진:\r\n소제목: [4~8글자 내외 작성]\r\n네모: [핵심 주제 또는 구분 제목 작성, 4~8글자 내외]\r\n원: [세부 추진 내용 또는 주요 사항 작성, 100글자 내외]\r\n바: [구체적인 실행 내용 또는 설명 작성, 100글자 내외]\r\n별: [보충 설명 또는 강조 사항 작성]\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있으며, 일부 기호는 생략 가능하다.\r\n\r\n# 강조사항\r\n\'#출력 규칙\'과 \'#출력 서식\'을 지켰는지 검토 후 답변 출력\r\n안내 된 글자수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성\r\n표를 사용할 때는 컬럼 구성이 보고서 내용과 논리적으로 일치하는지 검토 후 출력')

    if (lambda self, 내용, 이미지: self.문단위(0)self.줄간격(160)self.표만들기([
205.5 - self.문단여백측정()], [
294.5 - self.문단여백측정세로()])self.셀여백제로()self.셀세로정렬(0)self.표테두리타입(0, 0, 0, 0)self.글자크기(24)self.엔터(2)self.가운데정렬()self.표만들기([
164], [
38])self.폰트('HY헤드라인M')self.글자크기(32)self.가운데정렬()self.표테두리타입(1, 1, 0, 0)self.표테두리굵기(11, 11, 0, 0)self.표테두리색(67, 127, 193)self.줄간격(130)if len(내용) >= 1:
if len(내용[0]) >= 14:
passself.글자크기(30)if len(내용[0]) >= 15:
passself.글자크기(28)if len(내용[0]) >= 16:
passself.글자크기(26)if len(내용[0]) >= 17:
passself.글자간격(-3)if len(내용[0]) >= 18:
passself.글자간격(-6)if len(내용[0]) >= 19:
passself.글자간격(-9)if len(내용[0]) >= 20:
passself.글자장평(95)if len(내용[0]) >= 21:
passself.글자간격(-12)self.문장(내용[0])else:
self.문장('표지제목')self.표나가기2()self.엔터(6)self.가운데정렬()self.폰트('HY헤드라인M')self.진하게()self.오늘날짜년월()self.엔터(5)self.딜리트()self.딜리트()self.가운데정렬()self.표만들기([
15,
55], [
20])self.표테두리타입(0, 0, 0, 0)self.사진넣기절대값(이미지[0], 15, 19)self.표오른쪽(1)self.표테두리타입(0, 0, 0, 0)self.줄간격(130)self.가운데정렬()self.글자크기(21)self.폰트('HY헤드라인M')self.셀한줄(1)self.진하게()if len(내용) >= 2:
self.문장(내용[1] + '\r\n')else:
self.문장('어디처\r\n')if len(내용) >= 3:
self.문장(내용[2])else:
self.문장('어디부')self.표나가기2()self.딜리트()self.백스페이스()self.표나가기2()):
        
        def 가스공표지(self, 내용, 이미지):
            self.문단위(0)
            self.줄간격(160)
            self.표만들기([
                205.5 - self.문단여백측정()], [
                294.5 - self.문단여백측정세로()])
            self.셀여백제로()
            self.셀세로정렬(0)
            self.표테두리타입(0, 0, 0, 0)
            self.글자크기(24)
            self.엔터(2)
            self.가운데정렬()
            self.표만들기([
                164], [
                38])
            self.폰트('HY헤드라인M')
            self.글자크기(32)
            self.가운데정렬()
            self.표테두리타입(1, 1, 0, 0)
            self.표테두리굵기(11, 11, 0, 0)
            self.표테두리색(67, 127, 193)
            self.줄간격(130)
            if len(내용) >= 1:
                if len(내용[0]) >= 14:
                    pass
                self.글자크기(30)
                if len(내용[0]) >= 15:
                    pass
                self.글자크기(28)
                if len(내용[0]) >= 16:
                    pass
                self.글자크기(26)
                if len(내용[0]) >= 17:
                    pass
                self.글자간격(-3)
                if len(내용[0]) >= 18:
                    pass
                self.글자간격(-6)
                if len(내용[0]) >= 19:
                    pass
                self.글자간격(-9)
                if len(내용[0]) >= 20:
                    pass
                self.글자장평(95)
                if len(내용[0]) >= 21:
                    pass
                self.글자간격(-12)
                self.문장(내용[0])
            else:
                self.문장('표지제목')
            self.표나가기2()
            self.엔터(6)
            self.가운데정렬()
            self.폰트('HY헤드라인M')
            self.진하게()
            self.오늘날짜년월()
            self.엔터(5)
            self.딜리트()
            self.딜리트()
            self.가운데정렬()
            self.표만들기([
                15,
                55], [
                20])
            self.표테두리타입(0, 0, 0, 0)
            self.사진넣기절대값(이미지[0], 15, 19)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 0, 0)
            self.줄간격(130)
            self.가운데정렬()
            self.글자크기(21)
            self.폰트('HY헤드라인M')
            self.셀한줄(1)
            self.진하게()
            if len(내용) >= 2:
                self.문장(내용[1] + '\r\n')
            else:
                self.문장('어디처\r\n')
            if len(내용) >= 3:
                self.문장(내용[2])
            else:
                self.문장('어디부')
            self.표나가기2()
            self.딜리트()
            self.백스페이스()
            self.표나가기2()

    if (lambda self, 내용: if self.방금처리 == '가스공표':
self.궁극의정리위치보정 = -1self.백스페이스()self.대상.SetPosBySet(self.위치저장)셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]if str(셀위치) == 'A1':
self.표아래쪽(1)else:
self.표오른쪽(1)for None in range(len(내용)):
i = Noneif i != 0:
pass입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                if '○' in 입력내용:
                    입력내용 = 입력내용.replace('○', ' ○')
                    self.왼쪽정렬()
                elif '□' in 입력내용:
                    입력내용 = 입력내용.replace('□', ' □')
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif '▪' in 입력내용:
                    입력내용 = 입력내용.replace('▪', ' ▪')
                    self.왼쪽정렬()
                    self.내어쓰기(-15.9)
                self.진하게()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '가스공표'
            self.표나가기2()
        return None
        표개수 = len(내용)
        기본길이 = 207 - 표개수 * 3.5
        전체길이 = 기본길이 - self.문단여백측정()
        표넓이 = [
            2] * 표개수
        for None in range(표개수):
            i = None
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                표넓이[i] = 0.5
                표넓이[i] = 0.5
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                표넓이[i] = 1
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                표넓이[i] = 1.5
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                표넓이[i] = 2
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                pass
            if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                continue
            표넓이[i] = 4
        any
        표넓이합 = sum(표넓이)
        for None in range(표개수):
            i = None
            표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
        (i, 내용)
        self.표만들기(표넓이, [
            10,
            7])
        self.표전체()
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(11)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트('맑은 고딕')
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.글자크기(11)
        self.표배경색(223, 230, 247)
        self.캔슬()
        self.표처음()
        for None in range(표개수):
            i = None
            if i != 0:
                pass
            입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
            입력내용 = 입력내용.replace(';', ':')
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = '가스공표'
        self.표나가기2()
):
        
        def 가스공표(self, 내용):
            if self.방금처리 == '가스공표':
                self.궁극의정리위치보정 = -1
                self.백스페이스()
                self.대상.SetPosBySet(self.위치저장)
                셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
                if str(셀위치) == 'A1':
                    self.표아래쪽(1)
                else:
                    self.표오른쪽(1)
                for None in range(len(내용)):
                    i = None
                    if i != 0:
                        pass
                    입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                    입력내용 = 입력내용.replace(';', ':')
                    if '○' in 입력내용:
                        입력내용 = 입력내용.replace('○', ' ○')
                        self.왼쪽정렬()
                    elif '□' in 입력내용:
                        입력내용 = 입력내용.replace('□', ' □')
                        self.왼쪽정렬()
                        self.내어쓰기(-20)
                        self.진하게()
                    elif '▪' in 입력내용:
                        입력내용 = 입력내용.replace('▪', ' ▪')
                        self.왼쪽정렬()
                        self.내어쓰기(-15.9)
                    self.진하게()
                    self.문장(입력내용)
                self.표끝()
                self.위치저장 = self.대상.GetPosBySet()
                self.방금처리 = '가스공표'
                self.표나가기2()
            return None
            표개수 = len(내용)
            기본길이 = 207 - 표개수 * 3.5
            전체길이 = 기본길이 - self.문단여백측정()
            표넓이 = [
                2] * 표개수
            for None in range(표개수):
                i = None
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    표넓이[i] = 0.5
                    표넓이[i] = 0.5
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                    표넓이[i] = 1
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                    표넓이[i] = 1.5
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                    표넓이[i] = 2
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    pass
                if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    continue
                표넓이[i] = 4
            any
            표넓이합 = sum(표넓이)
            for None in range(표개수):
                i = None
                표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
            (i, 내용)
            self.표만들기(표넓이, [
                10,
                7])
            self.표전체()
            self.셀여백지정(1, 1, 0, 0)
            self.글자크기(11)
            self.글자간격(-10)
            self.가운데정렬()
            self.폰트('맑은 고딕')
            self.줄간격(130)
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽끝()
            self.진하게()
            self.글자크기(11)
            self.표배경색(223, 230, 247)
            self.캔슬()
            self.표처음()
            for None in range(표개수):
                i = None
                if i != 0:
                    pass
                입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                self.문장(입력내용)
            self.표처음()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '가스공표'
            self.표나가기2()

    if (lambda self, 내용: self.글자크기(26)self.폰트('HY헤드라인M')self.가운데정렬()self.줄간격(160)self.글자간격(-10)self.글자장평(95)self.밑줄얇굵()self.문장(' ' + 내용 + ' ')self.문단아래(10)):
        
        def 가스공제목(self, 내용):
            self.글자크기(26)
            self.폰트('HY헤드라인M')
            self.가운데정렬()
            self.줄간격(160)
            self.글자간격(-10)
            self.글자장평(95)
            self.밑줄얇굵()
            self.문장(' ' + 내용 + ' ')
            self.문단아래(10)

    if (lambda self, 번호, 내용: self.글자크기(16)self.문단위(20)self.문단아래(5)self.폰트('HY헤드라인M')self.문장(str(번호) + '. ' + 내용)):
        
        def 가스공소제목(self, 번호, 내용):
            self.글자크기(16)
            self.문단위(20)
            self.문단아래(5)
            self.폰트('HY헤드라인M')
            self.문장(str(번호) + '. ' + 내용)

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None(' □ ', 텍스트):
passif None(' □ ', 텍스트):
매치 = None(' □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ', 텍스트):
passif None('     ', 텍스트):
매치 = None('     ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None(' □ ', 텍스트):
passif None(' □ ', 텍스트):
매치 = None(' □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ', 텍스트):
passif None('     ', 텍스트):
매치 = None('     ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None(' □ ', 텍스트):
                                pass
                            if None(' □ ', 텍스트):
                                매치 = None(' □ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  ○ ', 텍스트):
                                pass
                            if None('  ○ ', 텍스트):
                                매치 = None('  ○ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('  ○ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None('  ○ \\((.*?)\\) ', 텍스트):
                                    매치 = None('  ○ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   - ', 텍스트):
                                pass
                            if None('   - ', 텍스트):
                                매치 = None('   - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('     ', 텍스트):
                                pass
                            if None('     ', 텍스트):
                                매치 = None('     ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('    \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '가스공표':
            if None('^표', 텍스트):
                pass
            if not None('^표', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.가스공제목(텍스트.split(':', 1)[1].strip())
            elif None('^표\\s*:\\s*', 텍스트):
                pass
        if not None('^표\\s*:\\s*', 텍스트):
            if None('^표\\s+', 텍스트):
                pass
            if None('^표\\s+', 텍스트):
                텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                self.백스페이스()
                텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                        self.가스공표(분리텍스트)
                        self.백스페이스()
                    elif None('^중제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.가스공표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.가스공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
            elif None('^\\d{1,2}\\.\\s*', 텍스트):
                pass
        if None('^\\d{1,2}\\.\\s*', 텍스트):
            self.백스페이스()
            self.가스공소제목(텍스트.split('.', 1)[0].strip(), 텍스트.split('.', 1)[1].strip())
        elif None('^요약\\s*:\\s*', 텍스트):
            pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', ' □ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(15)
            self.문단위(6)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            None(텍스트, 위치)
            if None(' □ \\((.*?)\\)', 텍스트):
                pass
            if None(' □ \\((.*?)\\)', 텍스트):
                매치 = None(' □ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None(' □ ', 텍스트):
                pass
            if None(' □ ', 텍스트):
                매치 = None(' □ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '  ○ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(6)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  ○ \\((.*?)\\)', 텍스트):
                pass
            if None('  ○ \\((.*?)\\)', 텍스트):
                매치 = None('  ○ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('  ○ ', 텍스트):
                pass
            if None('  ○ ', 텍스트):
                매치 = None('  ○ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-42.4)
            self.문단위(6)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('   - \\((.*?)\\)', 텍스트):
                pass
            if None('   - \\((.*?)\\)', 텍스트):
                매치 = None('   - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('   - ', 텍스트):
                pass
            if None('   - ', 텍스트):
                매치 = None('   - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('', '점 ', '점:')):
            pass
        if 텍스트.startswith(('', '점 ', '점:')):
            텍스트 = None('^(|점\\s*:|점)\\s*', '     ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-42.4)
            self.문단위(6)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('     \\((.*?)\\)', 텍스트):
                pass
            if None('     \\((.*?)\\)', 텍스트):
                매치 = None('     \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 6))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('     ', 텍스트):
                pass
            if None('     ', 텍스트):
                매치 = None('     ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.2)
            self.문단위(3)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '    ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.2)
            self.문단위(3)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 가스공궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None(' □ ', 텍스트):
passif None(' □ ', 텍스트):
매치 = None(' □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ', 텍스트):
passif None('     ', 텍스트):
매치 = None('     ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None(' □ ', 텍스트):
passif None(' □ ', 텍스트):
매치 = None(' □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ', 텍스트):
passif None('     ', 텍스트):
매치 = None('     ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None(' □ ', 텍스트):
                                    pass
                                if None(' □ ', 텍스트):
                                    매치 = None(' □ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  ○ ', 텍스트):
                                    pass
                                if None('  ○ ', 텍스트):
                                    매치 = None('  ○ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('  ○ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None('  ○ \\((.*?)\\) ', 텍스트):
                                        매치 = None('  ○ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   - ', 텍스트):
                                    pass
                                if None('   - ', 텍스트):
                                    매치 = None('   - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('     ', 텍스트):
                                    pass
                                if None('     ', 텍스트):
                                    매치 = None('     ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('    \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '가스공표':
                if None('^표', 텍스트):
                    pass
                if not None('^표', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.가스공제목(텍스트.split(':', 1)[1].strip())
                elif None('^표\\s*:\\s*', 텍스트):
                    pass
            if not None('^표\\s*:\\s*', 텍스트):
                if None('^표\\s+', 텍스트):
                    pass
                if None('^표\\s+', 텍스트):
                    텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                    self.백스페이스()
                    텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                            self.가스공표(분리텍스트)
                            self.백스페이스()
                        elif None('^중제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.가스공표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.가스공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                elif None('^\\d{1,2}\\.\\s*', 텍스트):
                    pass
            if None('^\\d{1,2}\\.\\s*', 텍스트):
                self.백스페이스()
                self.가스공소제목(텍스트.split('.', 1)[0].strip(), 텍스트.split('.', 1)[1].strip())
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', ' □ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(15)
                self.문단위(6)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                None(텍스트, 위치)
                if None(' □ \\((.*?)\\)', 텍스트):
                    pass
                if None(' □ \\((.*?)\\)', 텍스트):
                    매치 = None(' □ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None(' □ ', 텍스트):
                    pass
                if None(' □ ', 텍스트):
                    매치 = None(' □ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '  ○ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-30)
                self.문단위(6)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  ○ \\((.*?)\\)', 텍스트):
                    pass
                if None('  ○ \\((.*?)\\)', 텍스트):
                    매치 = None('  ○ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('  ○ ', 텍스트):
                    pass
                if None('  ○ ', 텍스트):
                    매치 = None('  ○ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-42.4)
                self.문단위(6)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('   - \\((.*?)\\)', 텍스트):
                    pass
                if None('   - \\((.*?)\\)', 텍스트):
                    매치 = None('   - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('   - ', 텍스트):
                    pass
                if None('   - ', 텍스트):
                    매치 = None('   - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('', '점 ', '점:')):
                pass
            if 텍스트.startswith(('', '점 ', '점:')):
                텍스트 = None('^(|점\\s*:|점)\\s*', '     ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-42.4)
                self.문단위(6)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('     \\((.*?)\\)', 텍스트):
                    pass
                if None('     \\((.*?)\\)', 텍스트):
                    매치 = None('     \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 6))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('     ', 텍스트):
                    pass
                if None('     ', 텍스트):
                    매치 = None('     ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.2)
                self.문단위(3)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '    ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.2)
                self.문단위(3)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.가스공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.가스공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '가스공표':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 가스공궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.가스공궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.가스공궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '가스공표':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.가스공궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.가스공궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 가스공궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.가스공궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.가스공궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 토주공표서식변환(self):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.캔슬()
            self.표전체()
            self.표배경색(255, 255, 255)
            self.글자크기(13)
            self.기본글자()
            self.중고딕()
            self.표테두리타입(1, 1, 0, 0)
            self.표테두리굵기(1, 1, 1, 1)
            self.표내부선굵기(1, 1)
            self.표내부선타입(1, 1)
            self.문단음영(0xFFFFFFFF)
            self.표테두리색(0, 0, 0)
            self.표내부선색(0, 0, 0)
            self.가운데정렬()
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽끝()
            self.진하게()
            self.표배경색(229, 229, 229)
            self.진하게()
            self.표테두리단일선('하', 7, 8)
            self.캔슬()
        return None

    if (lambda self, 번호, 내용: self.표만들기([
7,
90], [
8.6])self.셀여백제로()self.표테두리굵기(6, 6, 6, 6)self.표배경색(62, 87, 165)self.폰트('HY헤드라인M')self.글자크기(16)self.가운데정렬()self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표테두리굵기(6, 7, 6, 6)self.표테두리타입(0, 1, 1, 0)self.폰트('HY헤드라인M')self.글자크기(16)self.문장(' ' + 내용)self.표나가기2()):
        
        def 토주공소제목(self, 번호, 내용):
            self.표만들기([
                7,
                90], [
                8.6])
            self.셀여백제로()
            self.표테두리굵기(6, 6, 6, 6)
            self.표배경색(62, 87, 165)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표테두리굵기(6, 7, 6, 6)
            self.표테두리타입(0, 1, 1, 0)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 번호, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
10])self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 11, 0, 0)self.표테두리단일선색('하', 51, 51, 153)self.글자크기(18)self.폰트('HY헤드라인M')self.문장(번호 + '. ' + 내용)self.표나가기2()):
        
        def 토주공제목(self, 번호, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                10])
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(0, 11, 0, 0)
            self.표테두리단일선색('하', 51, 51, 153)
            self.글자크기(18)
            self.폰트('HY헤드라인M')
            self.문장(번호 + '. ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
8])self.내어쓰기(-20.8)self.표테두리타입(1, 1, 0, 0)self.표배경색(253, 254, 235)self.자간헌터(0)self.셀여백지정(2, 2, 2, 2)self.폰트('휴먼명조')self.글자크기(15)self.줄간격(150)입력내용 = (lambda .0: if None:
passfor part in .0:
if '◈ ' + part.strip():
pass'◈ ' + part.strip())(내용.split('엔터 ')())
        self.문장(입력내용)
        self.표나가기2()
):
        
        def 토주공요약(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                8])
            self.내어쓰기(-20.8)
            self.표테두리타입(1, 1, 0, 0)
            self.표배경색(253, 254, 235)
            self.자간헌터(0)
            self.셀여백지정(2, 2, 2, 2)
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.줄간격(150)
            입력내용 = (lambda .0: if None:
passfor part in .0:
if '◈ ' + part.strip():
pass'◈ ' + part.strip())(내용.split('엔터 ')())
            self.문장(입력내용)
            self.표나가기2()

    if (lambda self, 내용, 이미지: self.표만들기([
27,
100.5,
2,
25], [
6.5] * 3)self.셀여백제로()self.표전체()self.글자크기(12)self.폰트('맑은 고딕')self.가운데정렬()self.표테두리굵기(1, 7, 1, 7)self.캔슬()self.표처음()self.셀선택()self.표아래쪽(1)self.셀병합()self.사진넣기절대값(이미지[0], 28, 8)self.표오른쪽(1)self.셀선택()self.표아래쪽(2)self.셀병합()self.글자크기(20)self.폰트('HY헤드라인M')if len(내용) >= 1:
self.문장(내용[0])else:
self.문장('보고서 제목\r\n(헤드라인, 20pt)')self.표배경색(214, 214, 214)self.표오른쪽(1)self.셀선택()self.표아래쪽(2)self.셀병합()self.줄간격(180)self.문장('담\r\n당')self.표오른쪽(1)if len(내용) >= 3:
self.문장(내용[2])else:
self.문장('부장 OOO')self.표오른쪽(4)if len(내용) >= 4:
self.문장(내용[3])else:
self.문장('차장 OOO')self.표오른쪽(1)if len(내용) >= 2:
self.문장(내용[1])else:
self.문장('○○○○처')self.표오른쪽(3)self.오늘날짜숫자만무공백()self.표나가기2()):
        
        def 토주공한장제목(self, 내용, 이미지):
            self.표만들기([
                27,
                100.5,
                2,
                25], [
                6.5] * 3)
            self.셀여백제로()
            self.표전체()
            self.글자크기(12)
            self.폰트('맑은 고딕')
            self.가운데정렬()
            self.표테두리굵기(1, 7, 1, 7)
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.사진넣기절대값(이미지[0], 28, 8)
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(2)
            self.셀병합()
            self.글자크기(20)
            self.폰트('HY헤드라인M')
            if len(내용) >= 1:
                self.문장(내용[0])
            else:
                self.문장('보고서 제목\r\n(헤드라인, 20pt)')
            self.표배경색(214, 214, 214)
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(2)
            self.셀병합()
            self.줄간격(180)
            self.문장('담\r\n당')
            self.표오른쪽(1)
            if len(내용) >= 3:
                self.문장(내용[2])
            else:
                self.문장('부장 OOO')
            self.표오른쪽(4)
            if len(내용) >= 4:
                self.문장(내용[3])
            else:
                self.문장('차장 OOO')
            self.표오른쪽(1)
            if len(내용) >= 2:
                self.문장(내용[1])
            else:
                self.문장('○○○○처')
            self.표오른쪽(3)
            self.오늘날짜숫자만무공백()
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ㅇ ', 텍스트):
                                pass
                            if None(' ㅇ ', 텍스트):
                                매치 = None(' ㅇ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   - ', 텍스트):
                                pass
                            if None('   - ', 텍스트):
                                매치 = None('   - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('    \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = 0
                self.중제목카운트 = self.중제목카운트 + 1
                if self.중제목카운트 == 13:
                    self.중제목카운트 = 1
                self.토주공제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^한장제목\\s*:\\s*', 텍스트):
                pass
        if not None('^한장제목\\s*:\\s*', 텍스트):
            if None('^한장제목\\s*', 텍스트):
                pass
            if None('^한장제목\\s*', 텍스트):
                텍스트 = None('^(한장제목\\s*:|한장제목)\\s*', '한장제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.토주공한장제목(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^보고자\\s*:\\s*', 텍스트):
                        pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.토주공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.문단위(14)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            if None('□ \\((.*?)\\)', 텍스트):
                pass
            if None('□ \\((.*?)\\)', 텍스트):
                매치 = None('□ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None('□ ', 텍스트):
                pass
            if None('□ ', 텍스트):
                매치 = None('□ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(7)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                pass
            if None(' ㅇ \\((.*?)\\)', 텍스트):
                매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None(' ㅇ ', 텍스트):
                pass
            if None(' ㅇ ', 텍스트):
                매치 = None(' ㅇ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-42.4)
            self.문단위(5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('   - \\((.*?)\\)', 텍스트):
                pass
            if None('   - \\((.*?)\\)', 텍스트):
                매치 = None('   - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
            텍스트 = None('(?<=\\*)\\s+(?=\\*)', '', 텍스트)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(12)
            self.내어쓰기(-34.1)
            self.문단위(3)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '    ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.2)
            self.문단위(3)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 토주공궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ㅇ ', 텍스트):
passif None(' ㅇ ', 텍스트):
매치 = None(' ㅇ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ㅇ \\((.*?)\\) ', 텍스트):
passif None(' ㅇ \\((.*?)\\) ', 텍스트):
매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ㅇ ', 텍스트):
                                    pass
                                if None(' ㅇ ', 텍스트):
                                    매치 = None(' ㅇ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ㅇ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ㅇ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   - ', 텍스트):
                                    pass
                                if None('   - ', 텍스트):
                                    매치 = None('   - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('    \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = 0
                    self.중제목카운트 = self.중제목카운트 + 1
                    if self.중제목카운트 == 13:
                        self.중제목카운트 = 1
                    self.토주공제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^한장제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^한장제목\\s*:\\s*', 텍스트):
                if None('^한장제목\\s*', 텍스트):
                    pass
                if None('^한장제목\\s*', 텍스트):
                    텍스트 = None('^(한장제목\\s*:|한장제목)\\s*', '한장제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.토주공한장제목(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^보고자\\s*:\\s*', 텍스트):
                            pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.토주공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.문단위(14)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                if None('□ \\((.*?)\\)', 텍스트):
                    pass
                if None('□ \\((.*?)\\)', 텍스트):
                    매치 = None('□ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 2))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None('□ ', 텍스트):
                    pass
                if None('□ ', 텍스트):
                    매치 = None('□ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ㅇ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-30)
                self.문단위(7)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ㅇ \\((.*?)\\)', 텍스트):
                    매치 = None(' ㅇ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None(' ㅇ ', 텍스트):
                    pass
                if None(' ㅇ ', 텍스트):
                    매치 = None(' ㅇ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-42.4)
                self.문단위(5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('   - \\((.*?)\\)', 텍스트):
                    pass
                if None('   - \\((.*?)\\)', 텍스트):
                    매치 = None('   - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
                텍스트 = None('(?<=\\*)\\s+(?=\\*)', '', 텍스트)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(12)
                self.내어쓰기(-34.1)
                self.문단위(3)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '    ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.2)
                self.문단위(3)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.토주공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.토주공궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 토주공궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.토주공궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.토주공궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.토주공궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.토주공궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 토주공궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.토주공궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.토주공궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 전남교일반계획프롬프트(self):
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('제목: 교직원 대상, AI 활용 아이디어 공모전 계획\r\n담당부서: AI혁신과\r\n추진배경: 퇴직율 증가, 업무증대로 인한 부담 증가\r\n추진내용: 공모전 개최, 사전 홍보, 우수사례 확대 전파\r\n추진일정: 2026.7.~2026.12.\r\n기대효과: 직원들의 업무 만족감 향상, 퇴직율 감소\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 공무원으로 #작성내용에 대한 전문적인 지식을 가진 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 \'#작성 규칙\'을 바탕으로 \'#출력 예시\'를 참고하여 문서를 작성하라. 문서의 최소 작성분량이 2페이지 내외가 되도록 작성하라.\r\n\r\n# 출력 규칙\r\n\'#출력 서식\'에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n(제목:, 소제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용" "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n5. 표 출력 규칙\r\n- 항목이 3개 이상 나열되거나 비교·목록 구조가 명확한 경우, 서술 대신 표로 출력\r\n- 표의 컬럼은 보고서 내용에 맞게 자유롭게 구성하되, 마지막 컬럼은 반드시 \'비고\'로 고정\r\n- 표 출력 형식은 아래를 따름:\r\n\r\n  표:[컬럼1]:[컬럼2]:[컬럼3]: ... :비고\r\n  표:[값1]:[값2]:[값3]: ... :\r\n  표:[값1]:[값2]:[값3]: ... :\r\n\r\n- 컬럼명 예시 (내용에 따라 선택):\r\n  · 사업·계획류 → 연번:사업명:사업내용:비고\r\n  · 일정·추진류 → 순번:추진단계:세부내용:기간:비고\r\n  · 예산류 → 연번:사업명:예산액(천원):집행액(천원):비고\r\n  · 조직·인원류 → 연번:담당부서명:담당업무:인원:비고\r\n  · 법령·근거류 → 연번:근거법령:주요내용:비고\r\n- 컬럼 수·명칭은 위 예시에 국한하지 않고 보고서 맥락에 맞게 결정\r\n- 비고값이 없는 행은 해당 셀을 공백으로 출력\r\n\r\n# 출력 예시\r\n제목: 업무효율화 프로그램 개발 계획:부서명\r\n소제목: 목적 및 배경 \r\n네모: 추진목적\r\n원: (RPA 프로그램 개발) 문서 작성 과정에서 발생하는 반복적인 업무의 업무 현장 수요를 반영한 맞춤형 RPA* 프로그램 개발 \r\n별: RPA(Robot Process Automation), 단순 반복적인 업무를 자동화 하는 것 \r\n소제목: 추진 개요 \r\n네모: 주요내용\r\n원: (설문조사) 프로그램 내 직원 의견 반영을 위한 설문조사 실시 \r\n바: 본부 및 소속기관 직원 400명 대상 온라인 설문조사 진행 \r\n당구장: 파견 및 EPS 센터 직원은 제외 \r\n원: (용역계약) 한글(HWP) 프로그램 개발 및 업무 자동화 솔루션 전문 업체와 용역심사 및 계약을 통한 1차 프로그램 개발 진행 \r\n바: 용역 계약 관련 주요 내용1 \r\n바: 용역 계약 관련 주요 내용2 \r\n원: 기타 프로그램 개발 진행 시 추가적으로 들어가야 하는 사항 \r\n바: 관련 세부 내용* \r\n별: 세부 내용 관련 참고 사항\r\n네모: 추진 사업 목록\r\n표:연번:사업명:사업내용:비고\r\n표:1:RPA 프로그램 개발:반복업무 자동화 솔루션 개발:1차 개발\r\n표:2:설문조사 실시:직원 의견 수렴 및 수요 파악:400명 대상\r\n표:3:용역계약 체결:전문업체 선정 및 계약 추진:\r\n소제목: [4~8글자 내외 작성]\r\n네모: [핵심 주제 또는 구분 제목 작성, 4~8글자 내외]\r\n원: [세부 추진 내용 또는 주요 사항 작성, 100글자 내외]\r\n바: [구체적인 실행 내용 또는 설명 작성, 100글자 내외]\r\n별: [보충 설명 또는 강조 사항 작성]\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있으며, 일부 기호는 생략 가능하다.\r\n\r\n# 강조사항\r\n\'#출력 규칙\'과 \'#출력 서식\'을 지켰는지 검토 후 답변 출력\r\n안내 된 글자수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성\r\n표를 사용할 때는 컬럼 구성이 보고서 내용과 논리적으로 일치하는지 검토 후 출력')

    if (lambda self, 번호, 내용: self.표만들기([
6.5,
1,
192.3 - self.문단여백측정()], [
8.8])self.셀여백제로()self.표테두리색(49, 95, 151)self.표배경색(28, 61, 98)self.가운데정렬()self.폰트('HY신명조')self.글자크기(18)self.진하게()self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표테두리타입(0, 0, 1, 0)self.표너비줄이기(1)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 7, 0, 0)self.표테두리색(49, 95, 151)self.폰트('HY헤드라인M')self.글자크기(15)self.문장(' ' + 내용)self.표나가기2()):
        
        def 전남교소제목(self, 번호, 내용):
            self.표만들기([
                6.5,
                1,
                192.3 - self.문단여백측정()], [
                8.8])
            self.셀여백제로()
            self.표테두리색(49, 95, 151)
            self.표배경색(28, 61, 98)
            self.가운데정렬()
            self.폰트('HY신명조')
            self.글자크기(18)
            self.진하게()
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 0)
            self.표너비줄이기(1)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(0, 7, 0, 0)
            self.표테두리색(49, 95, 151)
            self.폰트('HY헤드라인M')
            self.글자크기(15)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
81,
81], [
0.3,
12,
0.3,
7])self.표전체()self.글자크기(1)self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.캔슬()self.표처음()self.표배경색(0, 153, 255)self.표오른쪽(1)self.표배경색(255, 204, 0)self.표오른쪽(1)self.셀선택()self.표오른쪽(1)self.셀병합()self.셀여백지정(2, 2, 2, 2)self.글자크기(20)self.줄간격(130)self.폰트('HY헤드라인M')self.가운데정렬()if len(내용) > 0:
if len(내용[0]) > 24:
passself.글자간격(-10)if len(내용[0]) > 27:
self.글자간격(-15)self.글자장평(95)self.문장(내용[0])else:
self.문장('제목')self.표오른쪽(1)self.표배경색(51, 153, 0)self.표오른쪽(1)self.표배경색(255, 51, 0)self.표오른쪽(1)self.셀선택()self.표오른쪽(1)self.셀병합()self.오른쪽정렬()self.글자크기(12)self.폰트('맑은 고딕')self.문장('< ')self.오늘날짜축약()self.문장(', ')if len(내용) > 1:
self.문장(내용[1])else:
self.문장('행정과')self.문장(' >')self.표나가기2()):
        
        def 전남교제목(self, 내용):
            self.표만들기([
                81,
                81], [
                0.3,
                12,
                0.3,
                7])
            self.표전체()
            self.글자크기(1)
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.표처음()
            self.표배경색(0, 153, 255)
            self.표오른쪽(1)
            self.표배경색(255, 204, 0)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.셀여백지정(2, 2, 2, 2)
            self.글자크기(20)
            self.줄간격(130)
            self.폰트('HY헤드라인M')
            self.가운데정렬()
            if len(내용) > 0:
                if len(내용[0]) > 24:
                    pass
                self.글자간격(-10)
                if len(내용[0]) > 27:
                    self.글자간격(-15)
                self.글자장평(95)
                self.문장(내용[0])
            else:
                self.문장('제목')
            self.표오른쪽(1)
            self.표배경색(51, 153, 0)
            self.표오른쪽(1)
            self.표배경색(255, 51, 0)
            self.표오른쪽(1)
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.오른쪽정렬()
            self.글자크기(12)
            self.폰트('맑은 고딕')
            self.문장('< ')
            self.오늘날짜축약()
            self.문장(', ')
            if len(내용) > 1:
                self.문장(내용[1])
            else:
                self.문장('행정과')
            self.문장(' >')
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('□ [가-힣\\s]+:', 텍스트):
passif None('□ [가-힣\\s]+:', 텍스트):
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ◦ ', 텍스트):
passif None(' ◦ ', 텍스트):
매치 = None(' ◦ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ◦ [가-힣\\s]+:', 텍스트):
passif None(' ◦ [가-힣\\s]+:', 텍스트):
매치 = None(' ◦ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      \\* ', 텍스트):
passif None('      \\* ', 텍스트):
매치 = None('      \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('□ [가-힣\\s]+:', 텍스트):
passif None('□ [가-힣\\s]+:', 텍스트):
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ◦ ', 텍스트):
passif None(' ◦ ', 텍스트):
매치 = None(' ◦ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ◦ [가-힣\\s]+:', 텍스트):
passif None(' ◦ [가-힣\\s]+:', 텍스트):
매치 = None(' ◦ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      \\* ', 텍스트):
passif None('      \\* ', 텍스트):
매치 = None('      \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('□ [가-힣\\s]+:', 텍스트):
                                    pass
                                if None('□ [가-힣\\s]+:', 텍스트):
                                    매치 = None('□ [가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ◦ ', 텍스트):
                                pass
                            if None(' ◦ ', 텍스트):
                                매치 = None(' ◦ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ◦ [가-힣\\s]+:', 텍스트):
                                    pass
                                if None(' ◦ [가-힣\\s]+:', 텍스트):
                                    매치 = None(' ◦ [가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   - ', 텍스트):
                                pass
                            if None('   - ', 텍스트):
                                매치 = None('   - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('   - [가-힣\\s]+:', 텍스트):
                                    pass
                                if None('   - [가-힣\\s]+:', 텍스트):
                                    매치 = None('   - [가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('      \\* ', 텍스트):
                                pass
                            if None('      \\* ', 텍스트):
                                매치 = None('      \\* ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('\\*[가-힣\\s]+:', 텍스트):
                                    pass
                                if None('\\*[가-힣\\s]+:', 텍스트):
                                    매치 = None('\\*[가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('      ※ ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 종류: if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
passif re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
매치 = re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.문장내어쓰기()None):
                    
                    def 콜론내어쓰기(텍스트, 위치, 종류):
                        if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
                            pass
                        if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
                            매치 = re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트)
                            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                            self.문장내어쓰기()
                        return None

                    if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                        
                        def 별찾아바꾸기(텍스트, 위치):
                            if '*' in 텍스트:
                                for None in :
                                    if ():
                                        if not 별 == '*':
                                            continue
                                        continue
                                        for None in 별, i:
                                            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                            self.대상.HAction.Run('Select')
                                            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                            self.윗첨자()
                                            self.캔슬()
                                        return None
                                        return None
                                        

                        if (lambda : self.캔슬()self.대상.MovePos(10)):
                            
                            def 다음문단():
                                self.캔슬()
                                self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(150)
        self.기본정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '우본표':
            if None('^(표\\s*:|표)\\s+', 텍스트):
                pass
            if not None('^(표\\s*:|표)\\s+', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '컨트롤엔터':
            if None('^(컨트롤엔터\\s*:|컨트롤엔터)\\s+', 텍스트):
                pass
            if not None('^(컨트롤엔터\\s*:|컨트롤엔터)\\s+', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s+', 텍스트):
                pass
            if None('^제목\\s+', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.전남교제목(분리텍스트)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s+', 텍스트):
                pass
            if None('^소제목\\s+', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.전남교소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^중제목\\s*:\\s*', 텍스트):
                pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s+', 텍스트):
                pass
            if None('^중제목\\s+', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = 0
                self.중제목카운트 = self.중제목카운트 + 1
                if self.중제목카운트 == 13:
                    self.중제목카운트 = 1
                self.우본중제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^개요\\s*:\\s*', 텍스트):
                pass
        if not None('^개요\\s*:\\s*', 텍스트):
            if None('^개요\\s+', 텍스트):
                pass
            if None('^개요\\s+', 텍스트):
                텍스트 = None('^(개요\\s*:|개요)\\s*', '개요:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.우본개요1(분리텍스트)
                        self.백스페이스()
                    elif None('^표\\s*:\\s*', 텍스트):
                        pass
        if not None('^표\\s*:\\s*', 텍스트):
            if None('^표\\s+', 텍스트):
                pass
            if None('^표\\s+', 텍스트):
                텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                self.백스페이스()
                텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                        self.우본표(분리텍스트)
                        self.백스페이스()
                    elif None('^표지\\s*:\\s*', 텍스트):
                        pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.세종교표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^목차\\s*:\\s*', 텍스트):
                        pass
        if not None('^목차\\s*:\\s*', 텍스트):
            if None('^목차\\s+', 텍스트):
                pass
            if None('^목차\\s+', 텍스트):
                텍스트 = None('^(목차\\s*:|목차)\\s*', '목차:', 텍스트, count = 1)
                self.백스페이스()
                self.우본목차2(이미지)
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s+', 텍스트):
                pass
            if None('^참고\\s+', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.우본참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s+', 텍스트):
                pass
            if None('^붙임\\s+', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.우본붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^컨트롤엔터\\s*:\\s*', 텍스트):
                pass
        if not None('^컨트롤엔터\\s*:\\s*', 텍스트):
            if None('^컨트롤엔터\\s*', 텍스트):
                pass
            if None('^컨트롤엔터\\s*', 텍스트):
                텍스트 = '컨트롤엔터'
                self.백스페이스()
                self.페이지엔터()
                self.방금처리 = '컨트롤엔터'
                self.딜리트()
                self.궁극의정리위치보정 = self.궁극의정리위치보정 - 1
                self.캔슬()
                self.대상.MovePos(11)
            elif None('^설명\\s*:\\s*', 텍스트):
                pass
        if not None('^설명\\s*:\\s*', 텍스트):
            if None('^설명\\s+', 텍스트):
                pass
            if None('^설명\\s+', 텍스트):
                텍스트 = None('^(설명\\s*:|설명|)\\s*', '', 텍스트, count = 1)
                self.문장('< ' + 텍스트.strip() + ' >')
                None()
                self.중고딕()
                self.글자크기(13)
                self.기본글자()
                self.문단위(10)
                self.가운데정렬()
                self.진하게()
                self.캔슬()
                self.대상.MovePos(6)
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(15)
            self.내어쓰기(-24)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
        elif 텍스트.startswith(('ㅇ', '○', '◦', '❍', '', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '◦', '❍', '', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ◦ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(12)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치)
            if None(' ◦ ', 텍스트):
                pass
            if None(' ◦ ', 텍스트):
                매치 = None(' ◦ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(텍스트, 위치, '◦')
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-39.6)
            self.문단위(10)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치)
            None(텍스트, 위치, '-')
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '      * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.문단위(5)
            self.내어쓰기(-50.2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, '*')
            None(10)
        elif 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
            pass
        if 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.문단위(5)
            self.내어쓰기(-58.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, '※')
        None(10)
        None()
        return None
        
        
        
        
):
        
        def 전남교궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('□ [가-힣\\s]+:', 텍스트):
passif None('□ [가-힣\\s]+:', 텍스트):
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ◦ ', 텍스트):
passif None(' ◦ ', 텍스트):
매치 = None(' ◦ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ◦ [가-힣\\s]+:', 텍스트):
passif None(' ◦ [가-힣\\s]+:', 텍스트):
매치 = None(' ◦ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      \\* ', 텍스트):
passif None('      \\* ', 텍스트):
매치 = None('      \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('□ [가-힣\\s]+:', 텍스트):
passif None('□ [가-힣\\s]+:', 텍스트):
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ◦ ', 텍스트):
passif None(' ◦ ', 텍스트):
매치 = None(' ◦ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ◦ [가-힣\\s]+:', 텍스트):
passif None(' ◦ [가-힣\\s]+:', 텍스트):
매치 = None(' ◦ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      \\* ', 텍스트):
passif None('      \\* ', 텍스트):
매치 = None('      \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('□ [가-힣\\s]+:', 텍스트):
                                        pass
                                    if None('□ [가-힣\\s]+:', 텍스트):
                                        매치 = None('□ [가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ◦ ', 텍스트):
                                    pass
                                if None(' ◦ ', 텍스트):
                                    매치 = None(' ◦ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ◦ [가-힣\\s]+:', 텍스트):
                                        pass
                                    if None(' ◦ [가-힣\\s]+:', 텍스트):
                                        매치 = None(' ◦ [가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   - ', 텍스트):
                                    pass
                                if None('   - ', 텍스트):
                                    매치 = None('   - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('   - [가-힣\\s]+:', 텍스트):
                                        pass
                                    if None('   - [가-힣\\s]+:', 텍스트):
                                        매치 = None('   - [가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('      \\* ', 텍스트):
                                    pass
                                if None('      \\* ', 텍스트):
                                    매치 = None('      \\* ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('\\*[가-힣\\s]+:', 텍스트):
                                        pass
                                    if None('\\*[가-힣\\s]+:', 텍스트):
                                        매치 = None('\\*[가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('      ※ ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 종류: if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
passif re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
매치 = re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.문장내어쓰기()None):
                        
                        def 콜론내어쓰기(텍스트, 위치, 종류):
                            if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
                                pass
                            if re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트):
                                매치 = re.escape(f'''{None(종류)}[가-힣\\(\\)0-9\\s]+: ''', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.문장내어쓰기()
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(150)
            self.기본정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '우본표':
                if None('^(표\\s*:|표)\\s+', 텍스트):
                    pass
                if not None('^(표\\s*:|표)\\s+', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '컨트롤엔터':
                if None('^(컨트롤엔터\\s*:|컨트롤엔터)\\s+', 텍스트):
                    pass
                if not None('^(컨트롤엔터\\s*:|컨트롤엔터)\\s+', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s+', 텍스트):
                    pass
                if None('^제목\\s+', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.전남교제목(분리텍스트)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s+', 텍스트):
                    pass
                if None('^소제목\\s+', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.전남교소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^중제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s+', 텍스트):
                    pass
                if None('^중제목\\s+', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = 0
                    self.중제목카운트 = self.중제목카운트 + 1
                    if self.중제목카운트 == 13:
                        self.중제목카운트 = 1
                    self.우본중제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^개요\\s*:\\s*', 텍스트):
                    pass
            if not None('^개요\\s*:\\s*', 텍스트):
                if None('^개요\\s+', 텍스트):
                    pass
                if None('^개요\\s+', 텍스트):
                    텍스트 = None('^(개요\\s*:|개요)\\s*', '개요:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.우본개요1(분리텍스트)
                            self.백스페이스()
                        elif None('^표\\s*:\\s*', 텍스트):
                            pass
            if not None('^표\\s*:\\s*', 텍스트):
                if None('^표\\s+', 텍스트):
                    pass
                if None('^표\\s+', 텍스트):
                    텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                    self.백스페이스()
                    텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                            self.우본표(분리텍스트)
                            self.백스페이스()
                        elif None('^표지\\s*:\\s*', 텍스트):
                            pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.세종교표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^목차\\s*:\\s*', 텍스트):
                            pass
            if not None('^목차\\s*:\\s*', 텍스트):
                if None('^목차\\s+', 텍스트):
                    pass
                if None('^목차\\s+', 텍스트):
                    텍스트 = None('^(목차\\s*:|목차)\\s*', '목차:', 텍스트, count = 1)
                    self.백스페이스()
                    self.우본목차2(이미지)
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s+', 텍스트):
                    pass
                if None('^참고\\s+', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.우본참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s+', 텍스트):
                    pass
                if None('^붙임\\s+', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.우본붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^컨트롤엔터\\s*:\\s*', 텍스트):
                    pass
            if not None('^컨트롤엔터\\s*:\\s*', 텍스트):
                if None('^컨트롤엔터\\s*', 텍스트):
                    pass
                if None('^컨트롤엔터\\s*', 텍스트):
                    텍스트 = '컨트롤엔터'
                    self.백스페이스()
                    self.페이지엔터()
                    self.방금처리 = '컨트롤엔터'
                    self.딜리트()
                    self.궁극의정리위치보정 = self.궁극의정리위치보정 - 1
                    self.캔슬()
                    self.대상.MovePos(11)
                elif None('^설명\\s*:\\s*', 텍스트):
                    pass
            if not None('^설명\\s*:\\s*', 텍스트):
                if None('^설명\\s+', 텍스트):
                    pass
                if None('^설명\\s+', 텍스트):
                    텍스트 = None('^(설명\\s*:|설명|)\\s*', '', 텍스트, count = 1)
                    self.문장('< ' + 텍스트.strip() + ' >')
                    None()
                    self.중고딕()
                    self.글자크기(13)
                    self.기본글자()
                    self.문단위(10)
                    self.가운데정렬()
                    self.진하게()
                    self.캔슬()
                    self.대상.MovePos(6)
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(15)
                self.내어쓰기(-24)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
            elif 텍스트.startswith(('ㅇ', '○', '◦', '❍', '', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '◦', '❍', '', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ◦ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-30)
                self.문단위(12)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치)
                if None(' ◦ ', 텍스트):
                    pass
                if None(' ◦ ', 텍스트):
                    매치 = None(' ◦ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(텍스트, 위치, '◦')
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-39.6)
                self.문단위(10)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치)
                None(텍스트, 위치, '-')
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '      * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.문단위(5)
                self.내어쓰기(-50.2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, '*')
                None(10)
            elif 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
                pass
            if 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.문단위(5)
                self.내어쓰기(-58.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, '※')
            None(10)
            None()
            return None
            
            
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.전남교궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.전남교궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '우본표':
pass임시보정값 = 1if self.방금처리 == '컨트롤엔터':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 전남교궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.전남교궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.전남교궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '우본표':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '컨트롤엔터':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: self.네모숫자카운트 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.전남교궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.전남교궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 전남교궁극의정리범위글머리(self, 특수문자, 이미지):
            self.네모숫자카운트 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.전남교궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.전남교궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 해경사진좌회전(self):
        self.그림글자취급해제()
        self.대상.HAction.Run('ShapeObjRightAngleRotaterAnticlockwise')
        높이너비 = self.그림높이너비정보()
        self.그림높이너비지정(높이너비[1], 높이너비[0])

    
    def 해경사진우회전(self):
        self.그림글자취급해제()
        self.대상.HAction.Run('ShapeObjRightAngleRotater')
        높이너비 = self.그림높이너비정보()
        self.그림높이너비지정(높이너비[1], 높이너비[0])

    
    def 해경제목(self):
        self.표만들기([
            69,
            133 - self.문단여백측정()], [
            5.5,
            18.5])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.캔슬()
        self.표처음()
        self.표배경색(70, 105, 145)
        self.글자크기(10.5)
        self.가운데정렬()
        self.글자색(255, 255, 255)
        self.글자장평(90)
        self.폰트('HY목각파임B')
        self.문장('미래를 준비하는, 강인하고 반듯한 해양경찰')
        self.표오른쪽(1)
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.오른쪽정렬()
        self.셀여백지정(0, 0, 0, 2)
        self.문장('0000계')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(9, 9, 0, 0)
        self.표테두리색(70, 105, 145)
        self.셀여백지정(2, 2, 3, 3)
        self.폰트('HY헤드라인M')
        self.글자크기(13)
        self.글자색(0, 0, 255)
        self.문장('「0000 관련 재발 방지 세부과제 관련」\r\n')
        self.글자크기(20)
        self.가운데정렬()
        self.글자색(0, 0, 0)
        self.문장('파출소 상황대응 역량향상을 위한 세부 시행 계획')
        self.표나가기2()

    
    def 해경채증사진(self):
        이름 = None(title = 'Open File', filetypes = [
            ('image files', ('.png', '.jpg', '.jpeg'))])
        재정렬이름 = sorted(이름, key = (lambda x: int(x.split('/')[-1].split(' ')[0])))
        self.새창()
        self.문서여백(20, 20, 30, 5, 5, 5)
        self.가운데정렬()
        self.폰트('HY헤드라인M')
        self.글자크기(20)
        self.진하게()
        self.밑줄()
        self.문장('00호(항계 내 불법조업) 채증사진\r\n')
        self.기본글자()
        self.글자크기(10)
        self.엔터(2)
        self.표만들기([
            21,
            90], [
            7,
            10,
            8])
        self.표전체()
        self.가운데정렬()
        self.표테두리굵기(6, 6, 6, 6)
        self.폰트('맑은 고딕')
        self.글자크기(11)
        self.캔슬()
        self.표처음()
        self.문장('채증일시')
        self.표오른쪽(1)
        self.오늘날짜숫자만()
        self.문장(' 05:00 ~ 00:00')
        self.문장오른쪽('채증장소')
        self.표오른쪽(1)
        self.줄간격(140)
        self.문장('34-46.37N, 126-20.70E\r\n(목포대교 0번부표 인근해상)')
        self.문장오른쪽('채 증 자')
        self.문장오른쪽('순경 000 (인)')
        self.표나가기2()
        self.문장('\r\n\r\n\r\n\r\n')
        for i in range(len(재정렬이름)):
            self.가운데정렬()
            self.표만들기([
                21,
                122], [
                84,
                10])
            self.표전체()
            self.표테두리굵기(6, 6, 6, 6)
            self.표내부선굵기(6, 6)
            self.글자크기(13)
            self.폰트('맑은 고딕')
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.셀여백지정(0, 0, 0, 0)
            self.사진넣기절대값(재정렬이름[i], 150, 86)
            self.표오른쪽(1)
            self.진하게()
            self.가운데정렬()
            self.문장('사진' + 재정렬이름[i].split('/')[-1].split(' ', 1)[0] + '호')
            self.표오른쪽(1)
            self.셀한줄(1)
            self.문장(재정렬이름[i].split('/')[-1].split(' ', 1)[1].replace('.png', '').replace('.jpeg', '').replace('.jpg', '').replace('.PNG', '').replace('.JPEG', '').replace('.JPG', ''))
            self.표나가기2()
            self.글자크기(10)
            self.문장('\r\n\r\n\r\n\r\n')
        filedialog.askopenfilenames

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('❏ ', 텍스트):
passif None('❏ ', 텍스트):
매치 = None('❏ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ❍ ', 텍스트):
passif None(' ❍ ', 텍스트):
매치 = None(' ❍ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ❍ \\((.*?)\\) ', 텍스트):
passif None(' ❍ \\((.*?)\\) ', 텍스트):
매치 = None(' ❍ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('❏ ', 텍스트):
passif None('❏ ', 텍스트):
매치 = None('❏ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ❍ ', 텍스트):
passif None(' ❍ ', 텍스트):
매치 = None(' ❍ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ❍ \\((.*?)\\) ', 텍스트):
passif None(' ❍ \\((.*?)\\) ', 텍스트):
매치 = None(' ❍ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('❏ ', 텍스트):
                                pass
                            if None('❏ ', 텍스트):
                                매치 = None('❏ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ❍ ', 텍스트):
                                pass
                            if None(' ❍ ', 텍스트):
                                매치 = None(' ❍ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ❍ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ❍ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ❍ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  - ', 텍스트):
                                pass
                            if None('  - ', 텍스트):
                                매치 = None('  - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   \\* ', 텍스트):
                                pass
                            if None('   \\* ', 텍스트):
                                매치 = None('   \\* ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   ※ ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda 텍스트, 위치: 대상문자 = '➊➋➌➍➎➏➐➑➒➓'for 문자 in 대상문자:
if not 문자 in 텍스트:
continuefor None in :
if ():
if not 별 == 문자:
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()continueNone):
                                
                                def 원숫자찾아바꾸기(텍스트, 위치):
                                    대상문자 = '➊➋➌➍➎➏➐➑➒➓'
                                    for 문자 in 대상문자:
                                        if not 문자 in 텍스트:
                                            continue
                                        for None in :
                                            if ():
                                                if not 별 == 문자:
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                continue
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = 0
                self.중제목카운트 = self.중제목카운트 + 1
                if self.중제목카운트 == 13:
                    self.중제목카운트 = 1
                self.토주공제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^한장제목\\s*:\\s*', 텍스트):
                pass
        if not None('^한장제목\\s*:\\s*', 텍스트):
            if None('^한장제목\\s*', 텍스트):
                pass
            if None('^한장제목\\s*', 텍스트):
                텍스트 = None('^(한장제목\\s*:|한장제목)\\s*', '한장제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.토주공한장제목(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^보고자\\s*:\\s*', 텍스트):
                        pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.토주공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.토주공요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '❏', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '❏', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||❏|네모\\s*:|네모|)\\s*', '❏ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(5)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
            if None('❏ ', 텍스트):
                pass
            if None('❏ ', 텍스트):
                매치 = None('❏ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ❍ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ❍ \\((.*?)\\)', 텍스트):
                pass
            if None(' ❍ \\((.*?)\\)', 텍스트):
                매치 = None(' ❍ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.폰트('HY울릉도M')
                self.글자색(51, 51, 153)
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            if None(' ❍ ', 텍스트):
                pass
            if None(' ❍ ', 텍스트):
                매치 = None(' ❍ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-42.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  - \\((.*?)\\)', 텍스트):
                pass
            if None('  - \\((.*?)\\)', 텍스트):
                매치 = None('  - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-29.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치)
            if None('   \\* \\((.*?)\\)', 텍스트):
                pass
            if None('   \\* \\((.*?)\\)', 텍스트):
                매치 = None('   \\* \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(13)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-37.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 해경궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('❏ ', 텍스트):
passif None('❏ ', 텍스트):
매치 = None('❏ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ❍ ', 텍스트):
passif None(' ❍ ', 텍스트):
매치 = None(' ❍ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ❍ \\((.*?)\\) ', 텍스트):
passif None(' ❍ \\((.*?)\\) ', 텍스트):
매치 = None(' ❍ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('❏ ', 텍스트):
passif None('❏ ', 텍스트):
매치 = None('❏ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ❍ ', 텍스트):
passif None(' ❍ ', 텍스트):
매치 = None(' ❍ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ❍ \\((.*?)\\) ', 텍스트):
passif None(' ❍ \\((.*?)\\) ', 텍스트):
매치 = None(' ❍ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   ※ ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('❏ ', 텍스트):
                                    pass
                                if None('❏ ', 텍스트):
                                    매치 = None('❏ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ❍ ', 텍스트):
                                    pass
                                if None(' ❍ ', 텍스트):
                                    매치 = None(' ❍ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ❍ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ❍ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ❍ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  - ', 텍스트):
                                    pass
                                if None('  - ', 텍스트):
                                    매치 = None('  - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   \\* ', 텍스트):
                                    pass
                                if None('   \\* ', 텍스트):
                                    매치 = None('   \\* ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   ※ ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda 텍스트, 위치: 대상문자 = '➊➋➌➍➎➏➐➑➒➓'for 문자 in 대상문자:
if not 문자 in 텍스트:
continuefor None in :
if ():
if not 별 == 문자:
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()continueNone):
                                    
                                    def 원숫자찾아바꾸기(텍스트, 위치):
                                        대상문자 = '➊➋➌➍➎➏➐➑➒➓'
                                        for 문자 in 대상문자:
                                            if not 문자 in 텍스트:
                                                continue
                                            for None in :
                                                if ():
                                                    if not 별 == 문자:
                                                        continue
                                                    continue
                                                    for None in 별, i:
                                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                        self.대상.HAction.Run('Select')
                                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                        self.윗첨자()
                                                        self.캔슬()
                                                    continue
                                                    return None
                                                    

                                    if (lambda : self.캔슬()self.대상.MovePos(10)):
                                        
                                        def 다음문단():
                                            self.캔슬()
                                            self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = 0
                    self.중제목카운트 = self.중제목카운트 + 1
                    if self.중제목카운트 == 13:
                        self.중제목카운트 = 1
                    self.토주공제목(self.로마숫자[self.중제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^한장제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^한장제목\\s*:\\s*', 텍스트):
                if None('^한장제목\\s*', 텍스트):
                    pass
                if None('^한장제목\\s*', 텍스트):
                    텍스트 = None('^(한장제목\\s*:|한장제목)\\s*', '한장제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.토주공한장제목(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^보고자\\s*:\\s*', 텍스트):
                            pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.토주공소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.토주공요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '❏', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '❏', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||❏|네모\\s*:|네모|)\\s*', '❏ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(5)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
                if None('❏ ', 텍스트):
                    pass
                if None('❏ ', 텍스트):
                    매치 = None('❏ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ❍ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-30)
                self.문단위(2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ❍ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ❍ \\((.*?)\\)', 텍스트):
                    매치 = None(' ❍ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.폰트('HY울릉도M')
                    self.글자색(51, 51, 153)
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                if None(' ❍ ', 텍스트):
                    pass
                if None(' ❍ ', 텍스트):
                    매치 = None(' ❍ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-42.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  - \\((.*?)\\)', 텍스트):
                    pass
                if None('  - \\((.*?)\\)', 텍스트):
                    매치 = None('  - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-29.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치)
                if None('   \\* \\((.*?)\\)', 텍스트):
                    pass
                if None('   \\* \\((.*?)\\)', 텍스트):
                    매치 = None('   \\* \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(13)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '   ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-37.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.해경궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.해경궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 해경궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.해경궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.해경궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.해경궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.해경궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 해경궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.해경궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.해경궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 한수원꼬리말(self):
        현위치 = self.현재위치()
        self.꼬리말()
        self.대상.HAction.Run('SelectAll')
        self.딜리트()
        self.문단위(5)
        self.표만들기([
            205.5 - self.문단여백측정()], [
            6])
        self.폰트('돋움')
        self.글자크기(10)
        self.글자장평(90)
        self.글자간격(-15)
        self.문장('이 문서는 회사 자산으로 대외제공시 관리등급에 따라 사전승인을 받아야 하며, 위반시 회사관련 규정에 따라 조치할 수 있습니다.')
        self.대상.SetPosBySet(현위치)

    if (lambda self, 등급, 종류, 설명, 부서: 현위치 = self.현재위치()self.바탕쪽()self.대상.HAction.Run('SelectAll')self.딜리트()self.표만들기([
13,
15,
51,
18,
54], [
4,
4])self.셀여백제로()self.표전체()self.폰트('맑은 고딕')self.글자크기(10)self.가운데정렬()self.캔슬()self.표처음()self.문장('관리등급')self.표오른쪽(1)self.글자크기(12)self.진하게()self.문장(등급)self.표오른쪽(1)self.셀선택()self.표아래쪽(1)self.셀병합()self.표테두리타입(0, 0, 1, 1)self.표오른쪽(1)self.셀선택()self.표아래쪽(1)self.셀병합()self.폰트('HY헤드라인M')self.글자색(127, 127, 127)self.글자크기(14)self.문장(종류)self.표오른쪽(1)self.셀선택()self.표아래쪽(1)self.셀병합()self.줄간격(130)self.글자크기(9)self.글자장평(90)self.글자간격(-13)self.글자색(127, 127, 127)self.문장(설명)self.표오른쪽(1)self.문장('관리부서')self.표오른쪽(1)if len(부서) >= 6:
self.글자간격(-8)self.글자장평(90)if len(부서) >= 7:
self.글자장평(85)self.글자간격(-15)self.문장(부서)self.표절대위치이동(20, 10)self.대상.SetPosBySet(현위치)):
        
        def 한수원바탕쪽(self, 등급, 종류, 설명, 부서):
            현위치 = self.현재위치()
            self.바탕쪽()
            self.대상.HAction.Run('SelectAll')
            self.딜리트()
            self.표만들기([
                13,
                15,
                51,
                18,
                54], [
                4,
                4])
            self.셀여백제로()
            self.표전체()
            self.폰트('맑은 고딕')
            self.글자크기(10)
            self.가운데정렬()
            self.캔슬()
            self.표처음()
            self.문장('관리등급')
            self.표오른쪽(1)
            self.글자크기(12)
            self.진하게()
            self.문장(등급)
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.표테두리타입(0, 0, 1, 1)
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.폰트('HY헤드라인M')
            self.글자색(127, 127, 127)
            self.글자크기(14)
            self.문장(종류)
            self.표오른쪽(1)
            self.셀선택()
            self.표아래쪽(1)
            self.셀병합()
            self.줄간격(130)
            self.글자크기(9)
            self.글자장평(90)
            self.글자간격(-13)
            self.글자색(127, 127, 127)
            self.문장(설명)
            self.표오른쪽(1)
            self.문장('관리부서')
            self.표오른쪽(1)
            if len(부서) >= 6:
                self.글자간격(-8)
            self.글자장평(90)
            if len(부서) >= 7:
                self.글자장평(85)
            self.글자간격(-15)
            self.문장(부서)
            self.표절대위치이동(20, 10)
            self.대상.SetPosBySet(현위치)

    if (lambda self, 번호, 내용: self.문단위(10)self.표만들기([
6.2,
1,
194.3 - self.문단여백측정()], [
9])self.셀여백제로()self.표테두리타입(0, 0, 0, 0)self.표배경색(19, 48, 148)self.글자색(255, 255, 255)self.가운데정렬()self.글자크기(16)self.폰트('HY헤드라인M')self.문장(str(번호))self.표오른쪽(1)self.표너비줄이기(2)self.표테두리타입(0, 0, 0, 0)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(2, 3, 2, 2)self.표테두리색(38, 48, 86)self.글자크기(16)self.폰트('HY헤드라인M')self.문장(' ' + 내용)self.표나가기2()):
        
        def 한수원소제목(self, 번호, 내용):
            self.문단위(10)
            self.표만들기([
                6.2,
                1,
                194.3 - self.문단여백측정()], [
                9])
            self.셀여백제로()
            self.표테두리타입(0, 0, 0, 0)
            self.표배경색(19, 48, 148)
            self.글자색(255, 255, 255)
            self.가운데정렬()
            self.글자크기(16)
            self.폰트('HY헤드라인M')
            self.문장(str(번호))
            self.표오른쪽(1)
            self.표너비줄이기(2)
            self.표테두리타입(0, 0, 0, 0)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리굵기(2, 3, 2, 2)
            self.표테두리색(38, 48, 86)
            self.글자크기(16)
            self.폰트('HY헤드라인M')
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: if self.방금처리 == '한수원표':
self.궁극의정리위치보정 = -1self.백스페이스()self.대상.SetPosBySet(self.위치저장)셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]if str(셀위치) == 'A1':
self.표아래쪽(1)else:
self.표오른쪽(1)셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]if str(셀위치) == 'A3':
self.셀선택()self.표오른쪽끝()self.표단일선('상', 1, 1)self.캔슬()self.표왼쪽끝()for None in range(len(내용)):
i = Noneif i != 0:
pass입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                if '○' in 입력내용:
                    입력내용 = 입력내용.replace('○', ' ○')
                    self.왼쪽정렬()
                elif '□' in 입력내용:
                    입력내용 = 입력내용.replace('□', ' □')
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif '⦁' in 입력내용:
                    self.왼쪽정렬()
                self.내어쓰기(-12.6)
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '한수원표'
            self.표나가기2()
        return None
        표개수 = len(내용)
        기본길이 = 207 - 표개수 * 3.5
        전체길이 = 기본길이 - self.문단여백측정()
        표넓이 = [
            2] * 표개수
        for None in range(표개수):
            i = None
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                표넓이[i] = 0.7
                표넓이[i] = 0.7
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호',)()):
                표넓이[i] = 2
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분', '이름')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분', '이름')()):
                표넓이[i] = 1
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획', '비고', '시간')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획', '비고', '시간')()):
                표넓이[i] = 1.5
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                pass
            if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                continue
            표넓이[i] = 4
        any
        표넓이합 = sum(표넓이)
        for None in range(표개수):
            i = None
            표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
        (i, 내용)
        self.표만들기(표넓이, [
            6.5] * 2)
        self.표전체()
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(6, 6, 1, 1)
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(13)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트('휴먼명조')
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.표배경색(223, 234, 245)
        self.폰트('휴먼명조')
        self.진하게()
        self.표단일선('하', 6, 8)
        self.캔슬()
        self.표처음()
        for None in range(표개수):
            i = None
            if i != 0:
                pass
            입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
            입력내용 = 입력내용.replace(';', ':')
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = '한수원표'
        self.표나가기2()
):
        
        def 한수원표(self, 내용):
            if self.방금처리 == '한수원표':
                self.궁극의정리위치보정 = -1
                self.백스페이스()
                self.대상.SetPosBySet(self.위치저장)
                셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
                if str(셀위치) == 'A1':
                    self.표아래쪽(1)
                else:
                    self.표오른쪽(1)
                셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
                if str(셀위치) == 'A3':
                    self.셀선택()
                    self.표오른쪽끝()
                    self.표단일선('상', 1, 1)
                    self.캔슬()
                self.표왼쪽끝()
                for None in range(len(내용)):
                    i = None
                    if i != 0:
                        pass
                    입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                    입력내용 = 입력내용.replace(';', ':')
                    if '○' in 입력내용:
                        입력내용 = 입력내용.replace('○', ' ○')
                        self.왼쪽정렬()
                    elif '□' in 입력내용:
                        입력내용 = 입력내용.replace('□', ' □')
                        self.왼쪽정렬()
                        self.내어쓰기(-20)
                        self.진하게()
                    elif '⦁' in 입력내용:
                        self.왼쪽정렬()
                    self.내어쓰기(-12.6)
                    self.문장(입력내용)
                self.표끝()
                self.위치저장 = self.대상.GetPosBySet()
                self.방금처리 = '한수원표'
                self.표나가기2()
            return None
            표개수 = len(내용)
            기본길이 = 207 - 표개수 * 3.5
            전체길이 = 기본길이 - self.문단여백측정()
            표넓이 = [
                2] * 표개수
            for None in range(표개수):
                i = None
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    표넓이[i] = 0.7
                    표넓이[i] = 0.7
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호',)()):
                    표넓이[i] = 2
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분', '이름')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분', '이름')()):
                    표넓이[i] = 1
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획', '비고', '시간')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획', '비고', '시간')()):
                    표넓이[i] = 1.5
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    pass
                if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    continue
                표넓이[i] = 4
            any
            표넓이합 = sum(표넓이)
            for None in range(표개수):
                i = None
                표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
            (i, 내용)
            self.표만들기(표넓이, [
                6.5] * 2)
            self.표전체()
            self.표테두리타입(1, 1, 0, 0)
            self.표테두리굵기(6, 6, 1, 1)
            self.셀여백지정(1, 1, 0, 0)
            self.글자크기(13)
            self.글자간격(-10)
            self.가운데정렬()
            self.폰트('휴먼명조')
            self.줄간격(130)
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽끝()
            self.진하게()
            self.표배경색(223, 234, 245)
            self.폰트('휴먼명조')
            self.진하게()
            self.표단일선('하', 6, 8)
            self.캔슬()
            self.표처음()
            for None in range(표개수):
                i = None
                if i != 0:
                    pass
                입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                self.문장(입력내용)
            self.표처음()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '한수원표'
            self.표나가기2()

    
    def 한수원참고의견(self):
        self.문단위(10)
        self.표만들기([
            21,
            181 - self.문단여백측정()], [
            13])
        self.표전체()
        self.표테두리굵기(6, 6, 6, 6)
        self.캔슬()
        self.표처음()
        self.폰트('휴먼명조')
        self.글자크기(15)
        self.가운데정렬()
        self.셀여백지정(0, 0, 0, 0)
        self.글자간격(-10)
        self.글자장평(94)
        self.문장('참고 의견')
        self.표나가기2()

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
14,
5])self.표테두리타입(1, 1, 0, 0)self.표테두리굵기(10, 10, 0, 0)self.표테두리색(16, 33, 139)self.폰트('한수원 한돋움')self.글자장평(95)self.글자간격(-7)self.글자크기(21)self.가운데정렬()if len(내용) > 0:
self.문장(내용[0])else:
self.문장('네모네모 계획 보고')self.표오른쪽(1)self.표테두리타입(1, 1, 0, 0)self.오른쪽정렬()self.오늘날짜축약무공백열콤마()self.폰트('휴먼명조')self.글자크기(11)self.셀여백지정(2, 1, 0, 2)if len(내용) > 0:
self.문장(' ' + 내용[1])else:
self.문장(' 경영전략부장 ○○○ (사선 1720, H.P 010-△△△-XXXX)')self.표나가기2()):
        
        def 한수원제목(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                14,
                5])
            self.표테두리타입(1, 1, 0, 0)
            self.표테두리굵기(10, 10, 0, 0)
            self.표테두리색(16, 33, 139)
            self.폰트('한수원 한돋움')
            self.글자장평(95)
            self.글자간격(-7)
            self.글자크기(21)
            self.가운데정렬()
            if len(내용) > 0:
                self.문장(내용[0])
            else:
                self.문장('네모네모 계획 보고')
            self.표오른쪽(1)
            self.표테두리타입(1, 1, 0, 0)
            self.오른쪽정렬()
            self.오늘날짜축약무공백열콤마()
            self.폰트('휴먼명조')
            self.글자크기(11)
            self.셀여백지정(2, 1, 0, 2)
            if len(내용) > 0:
                self.문장(' ' + 내용[1])
            else:
                self.문장(' 경영전략부장 ○○○ (사선 1720, H.P 010-△△△-XXXX)')
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  □ ', 텍스트):
passif None('  □ ', 텍스트):
매치 = None('  □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      - ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  □ ', 텍스트):
passif None('  □ ', 텍스트):
매치 = None('  □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      - ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('  □ ', 텍스트):
                                pass
                            if None('  □ ', 텍스트):
                                매치 = None('  □ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('  ○ ', 텍스트):
                                pass
                            if None('  ○ ', 텍스트):
                                매치 = None('  ○ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('  ○ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None('  ○ \\((.*?)\\) ', 텍스트):
                                    매치 = None('  ○ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('      - ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '한수원표':
            if None('^표', 텍스트):
                pass
            if not None('^표', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.한수원제목(분리텍스트)
                        self.백스페이스()
                    elif None('^표\\s*:\\s*', 텍스트):
                        pass
        if not None('^표\\s*:\\s*', 텍스트):
            if None('^표\\s+', 텍스트):
                pass
            if None('^표\\s+', 텍스트):
                텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                self.백스페이스()
                텍스트 = None('(\\d{1,2}):(\\d{2})', '\\1;\\2', 텍스트)
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                        self.한수원표(분리텍스트)
                        self.백스페이스()
                    elif None('^참고의견\\s*:\\s*', 텍스트):
                        pass
        if not None('^참고의견\\s*:\\s*', 텍스트):
            if None('^참고의견\\s*', 텍스트):
                pass
            if None('^참고의견\\s*', 텍스트):
                텍스트 = None('^(참고의견\\s*:|참고의견)\\s*', '참고의견:', 텍스트, count = 1)
                self.백스페이스()
                self.한수원참고의견()
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                self.한수원소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.강원요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.강원참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.강원붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '  □ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-34)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  □ \\((.*?)\\)', 텍스트):
                pass
            if None('  □ \\((.*?)\\)', 텍스트):
                매치 = None('  □ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(5)
            if None('  □ ', 텍스트):
                pass
            if None('  □ ', 텍스트):
                매치 = None('  □ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '    ○ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(14)
            self.내어쓰기(-40.8)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 12)
            None(텍스트, 위치)
            None(텍스트, 위치, 14)
            if None('    ○ \\((.*?)\\)', 텍스트):
                pass
            if None('    ○ \\((.*?)\\)', 텍스트):
                매치 = None('    ○ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 7))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.진하게()
                self.글자크기(14)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
            if None('    ○ ', 텍스트):
                pass
            if None('    ○ ', 텍스트):
                매치 = None('    ○ ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '      - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(13)
            self.내어쓰기(-46.7)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 11)
            None(텍스트, 위치)
            None(텍스트, 위치, 13)
            if None('      - \\((.*?)\\)', 텍스트):
                pass
            if None('      - \\((.*?)\\)', 텍스트):
                매치 = None('      - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 9))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                self.진하게()
                self.글자크기(13)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
            if None('      - ', 텍스트):
                pass
            if None('      - ', 텍스트):
                매치 = None('      - ', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            self.문장내어쓰기()
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '      * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-47.6)
            self.문단위(0)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(13)
            self.내어쓰기(-51.6)
            self.문단위(0)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
        
):
        
        def 한수원궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  □ ', 텍스트):
passif None('  □ ', 텍스트):
매치 = None('  □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      - ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  □ ', 텍스트):
passif None('  □ ', 텍스트):
매치 = None('  □ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ○ ', 텍스트):
passif None('  ○ ', 텍스트):
매치 = None('  ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  ○ \\((.*?)\\) ', 텍스트):
passif None('  ○ \\((.*?)\\) ', 텍스트):
매치 = None('  ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('      - ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('  □ ', 텍스트):
                                    pass
                                if None('  □ ', 텍스트):
                                    매치 = None('  □ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('  ○ ', 텍스트):
                                    pass
                                if None('  ○ ', 텍스트):
                                    매치 = None('  ○ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('  ○ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None('  ○ \\((.*?)\\) ', 텍스트):
                                        매치 = None('  ○ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('      - ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '한수원표':
                if None('^표', 텍스트):
                    pass
                if not None('^표', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.한수원제목(분리텍스트)
                            self.백스페이스()
                        elif None('^표\\s*:\\s*', 텍스트):
                            pass
            if not None('^표\\s*:\\s*', 텍스트):
                if None('^표\\s+', 텍스트):
                    pass
                if None('^표\\s+', 텍스트):
                    텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                    self.백스페이스()
                    텍스트 = None('(\\d{1,2}):(\\d{2})', '\\1;\\2', 텍스트)
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                            self.한수원표(분리텍스트)
                            self.백스페이스()
                        elif None('^참고의견\\s*:\\s*', 텍스트):
                            pass
            if not None('^참고의견\\s*:\\s*', 텍스트):
                if None('^참고의견\\s*', 텍스트):
                    pass
                if None('^참고의견\\s*', 텍스트):
                    텍스트 = None('^(참고의견\\s*:|참고의견)\\s*', '참고의견:', 텍스트, count = 1)
                    self.백스페이스()
                    self.한수원참고의견()
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    self.한수원소제목(str(self.소제목카운트), 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '  □ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-34)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  □ \\((.*?)\\)', 텍스트):
                    pass
                if None('  □ \\((.*?)\\)', 텍스트):
                    매치 = None('  □ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 5))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(5)
                if None('  □ ', 텍스트):
                    pass
                if None('  □ ', 텍스트):
                    매치 = None('  □ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', '    ○ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(14)
                self.내어쓰기(-40.8)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 12)
                None(텍스트, 위치)
                None(텍스트, 위치, 14)
                if None('    ○ \\((.*?)\\)', 텍스트):
                    pass
                if None('    ○ \\((.*?)\\)', 텍스트):
                    매치 = None('    ○ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 7))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.진하게()
                    self.글자크기(14)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
                if None('    ○ ', 텍스트):
                    pass
                if None('    ○ ', 텍스트):
                    매치 = None('    ○ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '      - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(13)
                self.내어쓰기(-46.7)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 11)
                None(텍스트, 위치)
                None(텍스트, 위치, 13)
                if None('      - \\((.*?)\\)', 텍스트):
                    pass
                if None('      - \\((.*?)\\)', 텍스트):
                    매치 = None('      - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 9))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() - 1))
                    self.진하게()
                    self.글자크기(13)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
                if None('      - ', 텍스트):
                    pass
                if None('      - ', 텍스트):
                    매치 = None('      - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.문장내어쓰기()
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '      * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-47.6)
                self.문단위(0)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(13)
                self.내어쓰기(-51.6)
                self.문단위(0)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.한수원궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.한수원궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '한수원표':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 한수원궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.한수원궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.한수원궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '한수원표':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.한수원궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.한수원궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 한수원궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.한수원궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.한수원궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 이미지: self.새창()self.문서여백(20, 20, 10, 10, 10, 10)self.표만들기([
7.2,
1,
190 - self.문단여백측정()], [
8.5])self.표테두리타입(0, 0, 0, 0)self.표배경색(28, 61, 98)self.폰트('HY헤드라인M')self.글자크기(15)self.가운데정렬()self.글자색(255, 255, 255)self.문장('I')self.표오른쪽(1)self.표테두리타입(0, 0, 0, 1)self.표오른쪽(1)self.표테두리색(28, 61, 98)self.표테두리타입(0, 1, 1, 0)self.폰트('HY헤드라인M')self.글자크기(15)self.문장('비전 체계')self.표나가기2()self.표만들기([
16,
0.3,
142], [
10.5,
1,
69])self.셀여백제로()self.표전체()self.가운데정렬()self.폰트('HY헤드라인M')self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.캔슬()self.표처음()self.글자크기(16)self.문장('비전')self.표배경색(230, 238, 247)self.표테두리타입(3, 3, 3, 3)self.표오른쪽(2)self.글자크기(16)self.문장('비전내용')self.표테두리타입(1, 1, 1, 1)self.표오른쪽(4)self.글자크기(16)self.문장('목표')self.표배경색(206, 222, 239)self.표테두리타입(3, 3, 3, 3)self.표오른쪽(2)self.글자크기(14)self.기본정렬()self.폰트('맑은 고딕')self.표테두리타입(1, 1, 1, 1)self.줄간격(140)self.셀여백지정(2, 2, 2, 2)self.진하게()self.문장('▸ 목표 1\r\n')self.중고딕()self.기본글자()self.글자크기(13)self.문장('  * 추가\r\n')self.글자크기(14)self.폰트('맑은 고딕')self.진하게()self.문장('▸ 목표 1\r\n')self.표나가기2()self.가운데정렬()self.로고절대값(이미지[10], 95, 10)self.기본정렬()self.표만들기([
46,
0.3,
113], [
6,
1,
30,
1,
30,
1,
30,
1,
30])self.셀여백제로()self.표전체()self.글자크기(6)self.폰트('HY헤드라인M')self.가운데정렬()self.줄간격(170)self.표테두리타입(0, 0, 0, 0)self.표내부선타입(0, 0)self.캔슬()self.표처음()self.표테두리타입(1, 1, 1, 1)self.표배경색(253, 254, 235)self.글자크기(14)self.문장('추 진 전 략')self.표오른쪽(1)self.표너비줄이기(1)self.표오른쪽(1)self.표테두리타입(1, 1, 1, 1)self.표배경색(253, 254, 235)self.글자크기(14)self.문장('추 진 과 제')self.표오른쪽(4)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.표배경색(231, 244, 246)self.글자크기(15)self.문장('1.')self.표오른쪽(2)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.글자크기(14)self.폰트('맑은 고딕')self.진하게()self.기본정렬()self.문단여백(5, 2)self.문장('1.1. \r\n1.2. \r\n1.3.')self.표오른쪽(4)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.표배경색(231, 244, 246)self.글자크기(15)self.문장('2.')self.표오른쪽(2)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.글자크기(14)self.폰트('맑은 고딕')self.진하게()self.기본정렬()self.문단여백(5, 2)self.문장('2.1. \r\n2.2. \r\n2.3.')self.표오른쪽(4)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.표배경색(231, 244, 246)self.글자크기(15)self.문장('3.')self.표오른쪽(2)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.글자크기(14)self.폰트('맑은 고딕')self.진하게()self.기본정렬()self.문단여백(5, 2)self.문장('3.1. \r\n3.2. \r\n3.3.')self.표오른쪽(4)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.표배경색(231, 244, 246)self.글자크기(15)self.문장('4.')self.표오른쪽(2)self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(6, 6, 6, 6)self.표테두리색(56, 174, 205)self.글자크기(14)self.폰트('맑은 고딕')self.진하게()self.기본정렬()self.문단여백(5, 2)self.문장('4.1. \r\n4.2. \r\n4.3.')):
        
        def 울항비전(self, 이미지):
            self.새창()
            self.문서여백(20, 20, 10, 10, 10, 10)
            self.표만들기([
                7.2,
                1,
                190 - self.문단여백측정()], [
                8.5])
            self.표테두리타입(0, 0, 0, 0)
            self.표배경색(28, 61, 98)
            self.폰트('HY헤드라인M')
            self.글자크기(15)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('I')
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 0, 1)
            self.표오른쪽(1)
            self.표테두리색(28, 61, 98)
            self.표테두리타입(0, 1, 1, 0)
            self.폰트('HY헤드라인M')
            self.글자크기(15)
            self.문장('비전 체계')
            self.표나가기2()
            self.표만들기([
                16,
                0.3,
                142], [
                10.5,
                1,
                69])
            self.셀여백제로()
            self.표전체()
            self.가운데정렬()
            self.폰트('HY헤드라인M')
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.표처음()
            self.글자크기(16)
            self.문장('비전')
            self.표배경색(230, 238, 247)
            self.표테두리타입(3, 3, 3, 3)
            self.표오른쪽(2)
            self.글자크기(16)
            self.문장('비전내용')
            self.표테두리타입(1, 1, 1, 1)
            self.표오른쪽(4)
            self.글자크기(16)
            self.문장('목표')
            self.표배경색(206, 222, 239)
            self.표테두리타입(3, 3, 3, 3)
            self.표오른쪽(2)
            self.글자크기(14)
            self.기본정렬()
            self.폰트('맑은 고딕')
            self.표테두리타입(1, 1, 1, 1)
            self.줄간격(140)
            self.셀여백지정(2, 2, 2, 2)
            self.진하게()
            self.문장('▸ 목표 1\r\n')
            self.중고딕()
            self.기본글자()
            self.글자크기(13)
            self.문장('  * 추가\r\n')
            self.글자크기(14)
            self.폰트('맑은 고딕')
            self.진하게()
            self.문장('▸ 목표 1\r\n')
            self.표나가기2()
            self.가운데정렬()
            self.로고절대값(이미지[10], 95, 10)
            self.기본정렬()
            self.표만들기([
                46,
                0.3,
                113], [
                6,
                1,
                30,
                1,
                30,
                1,
                30,
                1,
                30])
            self.셀여백제로()
            self.표전체()
            self.글자크기(6)
            self.폰트('HY헤드라인M')
            self.가운데정렬()
            self.줄간격(170)
            self.표테두리타입(0, 0, 0, 0)
            self.표내부선타입(0, 0)
            self.캔슬()
            self.표처음()
            self.표테두리타입(1, 1, 1, 1)
            self.표배경색(253, 254, 235)
            self.글자크기(14)
            self.문장('추 진 전 략')
            self.표오른쪽(1)
            self.표너비줄이기(1)
            self.표오른쪽(1)
            self.표테두리타입(1, 1, 1, 1)
            self.표배경색(253, 254, 235)
            self.글자크기(14)
            self.문장('추 진 과 제')
            self.표오른쪽(4)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.표배경색(231, 244, 246)
            self.글자크기(15)
            self.문장('1.')
            self.표오른쪽(2)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.글자크기(14)
            self.폰트('맑은 고딕')
            self.진하게()
            self.기본정렬()
            self.문단여백(5, 2)
            self.문장('1.1. \r\n1.2. \r\n1.3.')
            self.표오른쪽(4)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.표배경색(231, 244, 246)
            self.글자크기(15)
            self.문장('2.')
            self.표오른쪽(2)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.글자크기(14)
            self.폰트('맑은 고딕')
            self.진하게()
            self.기본정렬()
            self.문단여백(5, 2)
            self.문장('2.1. \r\n2.2. \r\n2.3.')
            self.표오른쪽(4)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.표배경색(231, 244, 246)
            self.글자크기(15)
            self.문장('3.')
            self.표오른쪽(2)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.글자크기(14)
            self.폰트('맑은 고딕')
            self.진하게()
            self.기본정렬()
            self.문단여백(5, 2)
            self.문장('3.1. \r\n3.2. \r\n3.3.')
            self.표오른쪽(4)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.표배경색(231, 244, 246)
            self.글자크기(15)
            self.문장('4.')
            self.표오른쪽(2)
            self.표테두리타입(1, 1, 1, 1)
            self.표테두리굵기(6, 6, 6, 6)
            self.표테두리색(56, 174, 205)
            self.글자크기(14)
            self.폰트('맑은 고딕')
            self.진하게()
            self.기본정렬()
            self.문단여백(5, 2)
            self.문장('4.1. \r\n4.2. \r\n4.3.')

    
    def 울항보도자료(self, 이미지):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.표만들기([
            22.3,
            3,
            0.3,
            23,
            28,
            34.7,
            1,
            28], [
            9,
            8,
            7,
            6,
            6,
            0.7,
            20,
            15,
            0.7,
            170])
        self.셀여백제로()
        self.표전체()
        self.가운데정렬()
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(2)
        self.표아래쪽(2)
        self.셀병합()
        self.사진넣기절대값(이미지[9], 35, 23)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.글자크기(22)
        self.진하게()
        self.문장('보도자료')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.표아래쪽(2)
        self.셀병합()
        self.사진넣기절대값(이미지[8], 22, 24)
        self.표오른쪽(2)
        self.진하게()
        self.문장('배포 일시')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.기본정렬()
        self.문장(' ')
        self.오늘날짜무공백()
        self.문장(' 총 1매')
        self.표오른쪽(3)
        self.진하게()
        self.문장('보도 일시')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.기본정렬()
        self.문장(' 배포 즉시 가능합니다.')
        self.표오른쪽(2)
        self.셀선택()
        self.표아래쪽(1)
        self.셀병합()
        self.진하게()
        self.문장('제공부서')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.표아래쪽(1)
        self.셀병합()
        self.문장('부서명')
        self.표오른쪽(1)
        self.진하게()
        self.문장('책임자')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.문장('OOO 부장(052-228-0000)')
        self.표오른쪽(3)
        self.진하게()
        self.문장('담당자')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.문장('OOO 과장(052-228-0000)')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.표테두리타입(1, 3, 3, 0)
        self.표배경색(249, 146, 15)
        self.글자크기(3)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(4)
        self.셀병합()
        self.표테두리타입(1, 3, 0, 3)
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                22,
                47,
                147],
            [
                0,
                14,
                138,
                189]])
        self.글자크기(3)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(7)
        self.셀병합()
        self.표테두리타입(3, 3, 3, 3)
        self.줄간격(120)
        self.글자크기(18)
        self.진하게()
        self.문장('제목 17자이내, 간결, 쉽고, 핵심만 \r\n 국민관점에서, 임펙트있게 전달')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(7)
        self.셀병합()
        self.표테두리타입(3, 0, 3, 3)
        self.글자크기(13)
        self.기본정렬()
        self.문장(' ∙ 소제목 20자 이내, <맑은고딕 13> 권장\r\n ∙ 메인 제목을 부연 설명하는 내용 핵심 내용을 일목 요연하게 정리')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(6)
        self.셀병합()
        self.표테두리타입(0, 3, 3, 0)
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                14,
                138,
                189],
            [
                0,
                22,
                47,
                147]])
        self.글자크기(3)
        self.표오른쪽(1)
        self.표테두리타입(0, 3, 0, 3)
        self.표배경색(249, 146, 15)
        self.글자크기(3)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(7)
        self.셀병합()
        self.표테두리타입(3, 3, 3, 3)
        self.글자크기(14)
        self.폰트('휴먼명조')
        self.문단여백(3, 3)
        self.기본정렬()
        self.셀세로정렬(0)
        self.문장('\r\n\r\n\r\n본문 내용은 기사 형태로 작성, 국민들이 궁금해하는 내용 순으로 작성, 두괄식, 정책 내용을 고객(국민) 관점에서 작성, 2페이지 이내로 작성, 자료 내용이 많을 경우 붙임 형태로 첨부, <휴먼명조 14> 권장\r\n\r\n 보도자료 형태는 중요 내용을 부각하고 부가적 내용은 뒤로 배치하거나 작게')
        self.표나가기2()
        self.표만들기([
            205.5 - self.문단여백측정()], [
            294.5 - self.문단여백측정세로()])
        self.셀여백제로()
        self.문단여백(3, 3)
        self.셀세로정렬(0)
        self.글자크기(14)
        self.폰트('휴먼명조')
        self.문장('\r\n2장')
        self.표테두리타입(3, 3, 3, 3)

    
    def 충남주자실적보고서(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.표만들기([
            205.5 - self.문단여백측정()], [
            18,
            20,
            214])
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.캔슬()
        self.표처음()
        self.표오른쪽(1)
        self.가운데정렬()
        self.글자크기(24)
        self.폰트('HY헤드라인M')
        self.문장('지방보조사업 실적보고서')
        self.표오른쪽(1)
        self.폰트('돋움체')
        self.글자크기(15)
        self.자간헌터(0)
        self.줄간격(200)
        self.문장('「지방자치단체 보조금 관리에 관한 법률」제17조제1항 각 호 외의 부분 본문 및 같은 법 시행령 제10조제2항에 따라 위 사업에 대한 지방보조사업의  실적보고서를 다음과 같이 제출합니다.\r\n\r\n\r\n')
        self.줄간격(180)
        self.글자크기(12)
        self.내어쓰기(9)
        self.글자간격(-4)
        self.문장('첨부 서류: 1. 실적보고서\r\n')
        self.내어쓰기(73)
        self.문장('2. 지방보조사업 정산보고서(지방보조금법 시행규칙 별지 제3호 서식)\r\n3. 증빙자료(보조금 전용통장 사본(거래내역 포함), 지출결의서 사본 등)\r\n4. 기타 관련서류\r\n\r\n\r\n\r\n')
        self.글자간격(0)
        self.내어쓰기(0)
        self.오른쪽정렬()
        self.글자크기(13)
        self.진하게()
        self.글자간격(10)
        self.오늘날짜한글숫자만()
        self.엔터(3)
        self.가운데정렬()
        self.표만들기([
            23,
            52,
            15,
            30,
            25], [
            7,
            7])
        self.셀여백제로()
        self.표전체()
        self.셀한줄(1)
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(13)
        self.폰트('돋움체')
        self.진하게()
        self.캔슬()
        self.표처음()
        self.문장('제출자')
        self.문장오른쪽('기관·단체명')
        self.문장오른쪽('대표자')
        self.표오른쪽(2)
        self.글자크기(11)
        self.기본글자()
        self.글자색(128, 128, 128)
        self.문장('(서명 또는 인)')
        self.표오른쪽(1)
        self.문장오른쪽('지방보조사업자(개인)')
        self.문장오른쪽('성  명')
        self.표오른쪽(2)
        self.글자크기(11)
        self.기본글자()
        self.글자색(128, 128, 128)
        self.문장('(서명 또는 인)')
        self.표나가기2()
        self.엔터(3)
        self.글자크기(18)
        self.진하게()
        self.문장('  충청남도지사')
        self.기본글자()
        self.글자크기(14)
        self.문장(' 귀하')
        self.표나가기2()
        self.딜리트()

    
    def 충남주자서식(self, 숫자, 내용):
        self.표만들기([
            17,
            1,
            183.5 - self.문단여백측정()], [
            9.5])
        self.셀여백제로()
        self.표테두리굵기(6, 6, 6, 6)
        self.가운데정렬()
        self.표배경색(255, 231, 216)
        self.폰트('HY헤드라인M')
        self.글자크기(16)
        self.문장('서식' + 숫자)
        self.표오른쪽(1)
        self.표테두리타입(0, 0, 1, 1)
        self.표너비줄이기(3)
        self.표오른쪽(1)
        self.표테두리굵기(6, 6, 6, 6)
        self.폰트('HY헤드라인M')
        self.글자크기(15)
        self.문장(' ' + 내용)
        self.표나가기2()

    
    def 충남주자개인정보동의서(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.충남주자서식('4', '개인정보수집 동의서')
        self.표만들기([
            26,
            106,
            26], [
            3,
            3,
            230])
        self.표아래쪽(2)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.표처음()
        self.표테두리타입(0, 1, 0, 0)
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(1)
        self.셀병합()
        self.표테두리타입(0, 0, 0, 0)
        self.폰트('휴먼명조')
        self.가운데정렬()
        self.진하게()
        self.글자크기(14)
        self.문장('< 개인정보 수집․이용에 관한 안내 >')
        self.표오른쪽(1)
        self.표테두리타입(0, 1, 0, 0)
        self.표오른쪽(1)
        self.표테두리타입(1, 0, 1, 0)
        self.표오른쪽(2)
        self.표테두리타입(1, 0, 0, 1)
        self.표오른쪽(1)
        self.글자크기(14)
        self.폰트('휴먼명조')
        self.줄간격(140)
        self.내어쓰기(-21)
        self.셀여백지정(2, 2, 2, 2)
        self.표테두리타입(0, 1, 1, 1)
        self.진하게()
        self.문장(' ① 수집․이용 목적\r\n')
        self.기본글자()
        self.자간헌터(0)
        self.왼쪽정렬()
        None(str + datetime.today(None().year) + '년 충청남도 주민자치회 제안사업」 보조사업자 선정을 위해 신청 주민자치회 대표자(직원)의 인적사항을 수집·이용하고자 하며, 수집된 정보는 보조사업자 선정을 위한 목적 외로 사용하지 아니합니다.\r\n\r\n')
        self.진하게()
        self.문장(' ② 수집항목\r\n')
        self.기본글자()
        self.문장('  이력사항, 기관명, 성명, 직위, 전화번호, 전자우편 등\r\n\r\n')
        self.진하게()
        self.문장(' ③ 개인정보의 보유 및 이용 기간\r\n')
        self.기본글자()
        None(str + datetime.today(None().year) + '년 연말까지 보존합니다.\r\n\r\n')
        self.진하게()
        self.문장(' ④ 동의 거부권리 안내\r\n')
        self.기본글자()
        None(str + datetime.today(None().year) + '년 충청남도 주민자치회 제안사업」보조사업을 접수할 수 없습니다.\r\n\r\n')
        self.내어쓰기(0)
        self.문장(' 개인정보보호법 제15조, 제17조, 제18조, 제22조에 의거 개인정보처리에 관하여 고지를 받았으며, 본인은 위와 같이 개인정보 수집 및 이용·제공에 동의합니다.\r\n\r\n')
        self.가운데정렬()
        self.문장('□ 동의함              □ 동의하지 않음\r\n\r\n')
        self.오늘날짜숫자만()
        self.엔터(2)
        self.표만들기([
            15,
            10] * 5, [
            7])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.셀한줄(1)
        self.가운데정렬()
        self.폰트('휴먼명조')
        self.글자크기(14)
        self.캔슬()
        self.표처음()
        self.문장('ㅇㅇㅇ')
        self.표오른쪽(1)
        self.글자색(191, 191, 191)
        self.글자크기(11)
        self.문장('(서명)')
        self.표오른쪽(1)
        self.문장('ㅇㅇㅇ')
        self.표오른쪽(1)
        self.글자색(191, 191, 191)
        self.글자크기(11)
        self.문장('(서명)')
        self.표오른쪽(1)
        self.문장('ㅇㅇㅇ')
        self.표오른쪽(1)
        self.글자색(191, 191, 191)
        self.글자크기(11)
        self.문장('(서명)')
        self.표오른쪽(1)
        self.문장('ㅇㅇㅇ')
        self.표오른쪽(1)
        self.글자색(191, 191, 191)
        self.글자크기(11)
        self.문장('(서명)')
        self.표오른쪽(1)
        self.문장('ㅇㅇㅇ')
        self.표오른쪽(1)
        self.글자색(191, 191, 191)
        self.글자크기(11)
        self.문장('(서명)')
        self.표전체()
        self.복사()
        self.캔슬()
        self.표끝()
        self.아래로붙이기()
        self.아래로붙이기()
        self.아래로붙이기()
        self.아래로붙이기()
        self.캔슬()

    
    def 충남주자주민참여명부(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.충남주자서식('3', '주민참여명부')
        self.표만들기([
            9,
            26,
            9,
            16,
            24,
            24,
            16,
            16], [
            14] + [
            18.5] * 10)
        self.셀여백제로()
        self.표전체()
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.가운데정렬()
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.표배경색(242, 242, 242)
        self.진하게()
        self.캔슬()
        self.표처음()
        self.문장('연번')
        self.문장오른쪽('성명')
        self.문장오른쪽('성별')
        self.문장오른쪽('생년월일')
        self.문장오른쪽('주소')
        self.문장오른쪽('연락처')
        self.문장오른쪽('서명')
        self.문장오른쪽('개인정보\r\n취급동의')
        for None in range(10):
            if None:
                pass
        self.표처음()
        for None in range(10):
            if None:
                pass

    
    def 충남주자사업계획서(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.충남주자서식('2', '사업계획서')
        self.가운데정렬()
        self.폰트('휴먼명조')
        self.글자크기(16)
        self.진하게()
        self.문장('충청남도 주민자치회 제안사업 사업계획서\r\n\r\n')
        if (lambda 내용: self.폰트('휴먼명조')self.글자크기(14)self.진하게()self.문단위(10)self.문장(내용 + '\r\n')):
            
            def 진(내용):
                self.폰트('휴먼명조')
                self.글자크기(14)
                self.진하게()
                self.문단위(10)
                self.문장(내용 + '\r\n')

            if (lambda 내용: self.폰트('휴먼명조')self.글자크기(14)self.기본글자()self.문단위(0)self.문장(내용 + '\r\n')):
                
                def 연(내용):
                    self.폰트('휴먼명조')
                    self.글자크기(14)
                    self.기본글자()
                    self.문단위(0)
                    self.문장(내용 + '\r\n')

                if (lambda 내용: self.폰트('휴먼명조')self.글자크기(9)self.기본글자()self.문단위(0)self.문장(내용 + '\r\n')):
                    
                    def 별(내용):
                        self.폰트('휴먼명조')
                        self.글자크기(9)
                        self.기본글자()
                        self.문단위(0)
                        self.문장(내용 + '\r\n')

        self.기본정렬()
        None('Ⅰ. 일반 현황')
        None('  1. 읍·면·동 현황')
        None('   ◦ 인구/세대/면적, 지역여건·특성 등')
        None('  2. 주민자치회 기본 현황')
        None('   ◦ 결성일자, 위원수(연령별 구성), 회의 개최 등\r\n   ◦ 예산 현황(시군비, 자체예산 등), 간사 현황, 전용공간 현황 등\r\n   ◦ 주요 활동 내역')
        self.가운데정렬()
        self.표만들기([
            8,
            28,
            19,
            17,
            40,
            10], [
            6] * 4)
        self.표전체()
        self.폰트('휴먼명조')
        self.가운데정렬()
        self.글자크기(11)
        self.캔슬()
        self.표처음()
        self.문장('연번')
        self.문장오른쪽('사업명')
        self.문장오른쪽('기간')
        self.문장오른쪽('대상인원')
        self.문장오른쪽('사업내용')
        self.문장오른쪽('비고')
        self.문장오른쪽('1')
        self.표나가기2()
        None('\r\nⅡ. 사업 계획서')
        self.가운데정렬()
        self.표만들기([
            140], [
            40])
        self.표테두리타입(3, 3, 3, 3)
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.진하게()
        self.문장('[작성요령]\r\n')
        self.기본글자()
        self.문장(' 1. 사업성격 및 평가기준이 잘 드러나도록 자유롭게 작성(양식 편집 가능)\r\n 2. 사업선정 경위, 지속가능성 여부에 대한 자체 판단 등 포함 작성\r\n 3. 심사항목을 참고하여 사례의 추진배경 및 과정, 주요내용, 성과 등 기재\r\n 4. 작성 서류는 공모신청서를 포함하여 10쪽을 넘지 않도록 작성')
        self.표나가기2()
        None('  1. 사업명 : ')
        None('  2. 사업개요')
        None('   ◦ 사업기간 : \r\n   ◦ 장    소 : \r\n   ◦ 추진주체 : \r\n   ◦ 사 업 량 : ')
        None('  3. 추진배경 및 필요성')
        None('    - 지역특성 반영, 주민총회 개최 여부, 의견수렴 과정 등\r\n\r\n')
        None('  4. 추진과정 및 내용')
        None('    - 기획에서부터 실행, 의견 수렴, 평가에 대해 구체적 서술\r\n\r\n')
        None('  5. 세부추진계획')
        self.문단위(0)
        self.가운데정렬()
        self.표만들기([
            25,
            43,
            60], [
            6] * 4)
        self.표전체()
        self.폰트('휴먼명조')
        self.가운데정렬()
        self.글자크기(11)
        self.캔슬()
        self.표처음()
        self.문장('일정')
        self.문장오른쪽('추진단위')
        self.문장오른쪽('세부추진내용')
        self.표나가기2()
        None('  6. 추진배경 및 필요성')
        None('   ◦ 사회적 기여도')
        None('       * 해당 사례의 파급 효과 서술, 확산 가능성 등 내용 기술, 사회문제 해결 등 기술')
        None('\r\n\r\n\r\n   ◦ 사업수행 단체에 대한 기여도')
        None('       * 본 사업에 대한 지원으로 지방보조사업자에게 어떠한 도움을 줄 것인지 기대효과 기술')
        None('\r\n\r\n\r\n')
        None('  7. 기타')
        None('   - 사업 추진시 예상되는 장애요인 및 해결방안 등')
        self.페이지엔터()
        None('Ⅲ. 지방보조사업 재정운영 계획서')
        self.가운데정렬()
        self.표만들기([
            140], [
            28])
        self.표테두리타입(3, 3, 3, 3)
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.진하게()
        self.문장('[작성요령]\r\n')
        self.기본글자()
        self.문장(' 1. 사업예산과 경상예산 구분, 지방보조금과 자부담 구분\r\n 2. 세입예산과 세출예산 합계 일치\r\n 3. 자부담이 있는 경우 예산확보 방안 및 예산확보 증빙서 첨부')
        self.표나가기2()
        None('\r\n  1. 세입예산')
        self.표만들기([
            13,
            40,
            97], [
            7] * 9)
        self.표전체()
        self.글자크기(11)
        self.가운데정렬()
        self.폰트('휴먼명조')
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.진하게()
        self.문장('비 목')
        self.문장오른쪽('세입예산')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.진하게()
        self.문장('합 계')
        self.표오른쪽(2)
        self.셀선택()
        self.표아래쪽(2)
        self.셀병합()
        self.문장('자체\r\n수입')
        self.문장오른쪽('소 계')
        self.표오른쪽(4)
        self.문장('ㅇ 산출기초')
        self.표오른쪽(3)
        self.문장('ㅇ 산출기초')
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(3)
        self.셀병합()
        self.문장('보조금\r\n수입')
        self.문장오른쪽('소 계')
        self.표오른쪽(4)
        self.문장('ㅇ 산출기초')
        self.표오른쪽(3)
        self.문장('ㅇ 산출기초')
        self.표아래쪽(1)
        self.문장('ㅇ 산출기초')
        self.셀선택()
        self.표위쪽(7)
        self.기본정렬()
        self.캔슬()
        self.상단캡션()
        self.대상.HAction.Run('SelectAll')
        self.대상.HAction.Run('Delete')
        self.오른쪽정렬()
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.문장('(단위 : 천원)')
        self.표나가기2()
        None('\r\n  2. 세출예산')
        self.표만들기([
            21,
            21,
            21,
            21,
            60], [
            7] * 8)
        self.표전체()
        self.가운데정렬()
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.가운데정렬()
        self.캔슬()
        self.표처음()
        self.진하게()
        self.문장('구 분')
        self.표오른쪽(1)
        self.진하게()
        self.문장('단위사업')
        self.표오른쪽(1)
        self.진하게()
        self.문장('지출항목')
        self.표오른쪽(1)
        self.진하게()
        self.문장('금액')
        self.표오른쪽(1)
        self.진하게()
        self.문장('산출내역')
        self.문장오른쪽('합계')
        self.표아래쪽(1)
        self.셀선택()
        self.표아래쪽(3)
        self.셀병합()
        self.문장('보조금')
        self.표오른쪽(1)
        self.문장('소 계')
        self.표왼쪽(1)
        self.표아래쪽(1)
        self.셀선택()
        self.표아래쪽(1)
        self.셀병합()
        self.문장('기타')
        self.표오른쪽(1)
        self.문장('소 계')
        self.상단캡션()
        self.대상.HAction.Run('SelectAll')
        self.대상.HAction.Run('Delete')
        self.오른쪽정렬()
        self.글자크기(11)
        self.폰트('휴먼명조')
        self.문장('(단위 : 천원)')

    
    def 충남주자사업신청서(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.충남주자서식('1', '사업신청서')
        self.줄간격(180)
        self.표만들기([
            32.5,
            105,
            21], [
            4.5,
            8] + [
            10.5] * 3 + [
            13] + [
            10.5] * 2 + [
            96,
            40,
            7,
            5])
        self.표전체()
        self.셀여백제로()
        self.표테두리굵기(6, 6, 6, 6)
        self.가운데정렬()
        self.폰트('휴먼명조')
        self.글자크기(11)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(1)
        self.표아래쪽(1)
        self.셀병합()
        self.글자크기(13)
        self.문장('충청남도 주민자치회 제안사업 신청서')
        self.문장오른쪽('담당자 확인')
        self.표오른쪽(3)
        self.배분정렬()
        self.문장('신청기관')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('ㅇㅇ시군구 ㅇㅇ읍면동 주민자치회')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('대표자')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('김대표')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('주소')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('충청남도 홍성군 홍북읍 충남대로 21')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('연락처')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.줄간격(130)
        self.기본정렬()
        self.문장('(휴대전화) 010-1234-5678\r\n(전자우편) abc123@naver.com')
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('사업명')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('충청남도 사업')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('사업비')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('총 1,234천원(보조금 1,000천원, 자부담 234천원)')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.배분정렬()
        self.문장('사업내용')
        self.문단여백(10, 10)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.문장('내용입력')
        self.기본정렬()
        self.문단여백(3, 3)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.가운데정렬()
        self.줄간격(130)
        self.오늘날짜한글숫자만()
        self.엔터(2)
        self.기본정렬()
        self.문단여백(180, 0)
        self.문장('신청인 \r\n\r\n')
        self.문장('대표자                 (서명 또는 인)\r\n\r\n')
        self.문단여백(20, 0)
        self.글자크기(13)
        self.문장('충청남도지사 ')
        self.글자크기(11)
        self.문장('귀하')
        self.표오른쪽(1)
        self.셀선택()
        self.표아래쪽(1)
        self.표오른쪽(1)
        self.셀병합()
        self.기본정렬()
        self.문장('  첨부서류\r\n 1. 사업계획서 1부     2. 주민참여 명부 1부     3. 개인정보수집 동의서 1부')
        self.표오른쪽(1)
        self.문장('수수료')
        self.표오른쪽(2)
        self.문장('없음')

    
    def 인진프롬프트(self):
        self.새창()
        self.문서여백(20, 20, 10, 10, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('제목: KISA형 공문편집 자동화 프로그램 개발 계획\r\n작성목적: 현업으로 고생하는 직원들의 업무경감\r\n추진배경: 퇴직율 증가, 문서 편집으로 인한 시간낭비 심각\r\n추진내용: 공문서편집 자동화 프로그램 개발, 교육, 배포\r\n추진일정: 2026.7.~2026.12.\r\n기대효과: 직원들의 업무 만족감 향상, 퇴직율 감소\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 공기업 직원으로 #작성내용에 대한 전문적인 지식을 가진 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 \'#작성 규칙\'을 바탕으로 \'#출력 예시\'를 참고하여 문서를 작성하라. 문서의 최소 작성분량이 2페이지 내외가 되도록 작성하라.\r\n\r\n# 출력 규칙\r\n\'#출력 서식\'에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n(제목:, 소제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용" "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n5. 표 출력 규칙\r\n- 항목이 3개 이상 나열되거나 비교·목록 구조가 명확한 경우, 서술 대신 표로 출력\r\n- 표의 컬럼은 보고서 내용에 맞게 자유롭게 구성하되, 마지막 컬럼은 반드시 \'비고\'로 고정\r\n- 표 출력 형식은 아래를 따름:\r\n\r\n  표:[컬럼1]:[컬럼2]:[컬럼3]: ... :비고\r\n  표:[값1]:[값2]:[값3]: ... :\r\n  표:[값1]:[값2]:[값3]: ... :\r\n\r\n- 컬럼명 예시 (내용에 따라 선택):\r\n  · 사업·계획류 → 연번:사업명:사업내용:비고\r\n  · 일정·추진류 → 순번:추진단계:세부내용:기간:비고\r\n  · 예산류 → 연번:사업명:예산액(천원):집행액(천원):비고\r\n  · 조직·인원류 → 연번:부서명:담당업무:인원:비고\r\n  · 법령·근거류 → 연번:근거법령:주요내용:비고\r\n- 컬럼 수·명칭은 위 예시에 국한하지 않고 보고서 맥락에 맞게 결정\r\n- 비고값이 없는 행은 해당 셀을 공백으로 출력\r\n\r\n# 출력 예시\r\n\r\n\r\n# 출력 예시\r\n표지: 범정부오피스 업무 활용 교육 결과보고\r\n제목: 범정부오피스 업무 활용 교육 결과보고\r\n보고자:2026. 5. 28.(목) / 경영기획본부 혁신전략단 전략기획팀/팀장 : 범피스 (☎0000) / 담당 : 범피스 (☎0000)\r\n네모: 평가 개요\r\n원:  (일시/장소) 2026. 6. 8.(월) 14:00~16:00 / 민원동 대강당\r\n원:  (강    사) 범피스 주무관(범정부오피스 개발자)\r\n원:  (참 석 자) 참여 희망 직원 100명\r\n원:  (교육내용) 범정부 오피스를 활용한 문서작성\r\n네모: 시간계획\r\n표:시간:소요 엔터 시간:주요내용:비고\r\n표:14:00~14:05:5‘:·인사말씀:ㅁㅁㅁㅁ국장\r\n표:14:05~14:55:50‘:·범정부오피스를 활용한 문서작성:범피스주무관\r\n표:14:55~15:45:50‘:·생산성을 높이는 범피스 심화 활용법:범피스개발자\r\n표:15:45~16:00:15’:·질의 & 답변:교육 참석자\r\n네모:  행정사항\r\n원:  상시학습 실적등록\r\n원:  교육 참여인원 상시학습(비지정학습) 120분 인정 공문 발송  끝.\r\n\r\n네모: [핵심 주제 또는 구분 제목 작성, 4~8글자 내외]\r\n원:  [세부 추진 내용 또는 주요 사항 작성, 100글자 내외]\r\n바:  [구체적인 실행 내용 또는 설명 작성, 100글자 내외]\r\n별:  [보충 설명 또는 강조 사항 작성]\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있으며, 일부 기호는 생략 가능하다.\r\n\r\n# 강조사항\r\n\'#출력 규칙\'과 \'#출력 서식\'을 지켰는지 검토 후 답변 출력\r\n안내 된 글자수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성\r\n표를 사용할 때는 컬럼 구성이 보고서 내용과 논리적으로 일치하는지 검토 후 출력')

    
    def 인진보도자료본문서식(self):
        텍스트 = self.블록텍스트()
        텍스트 = None('(?:\\r\\n)+', 텍스트)
        for None in :
            pass
        , [], 텍스트 = re.split, 텍스트
        라인 = None
        텍스트 = '\r\n\r\n'.join(텍스트)
        self.문단위(0)
        self.문단아래(0)
        self.내어쓰기(0)
        self.문단여백(0, 0)
        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.줄간격(180)
        self.자간헌터(0)
        self.기본정렬()
        self.글자크기(15)
        self.휴먼명조()
        self.문장(텍스트)
        return None
        

    
    def 인진보도자료(self, 이미지, 내용):
        제목 = '제목'
        부제 = '부제'
        if 내용.count(':') == 1:
            제목 = 내용.split(':', 1)[0].strip()
            부제 = 내용.split(':', 1)[1].strip()
        else:
            제목 = 내용.strip()
        self.표만들기([
            19,
            28,
            56,
            51], [
            1,
            12,
            3.8,
            1,
            6,
            5,
            17,
            9])
        self.표전체()
        self.글자크기(1)
        self.가운데정렬()
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽(3)
        self.셀병합()
        self.표테두리타입(0, 1, 0, 0)
        self.왼쪽정렬()
        self.글자색(0, 33, 106)
        self.문장('[보도자료]')
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                6,
                33,
                106],
            [
                0,
                29,
                166,
                240]])
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.사진넣기절대값(이미지[2], 48, 9)
        self.표오른쪽(1)
        self.글자크기(24)
        self.폰트('HY헤드라인M')
        self.진하게()
        self.문장('보도자료')
        self.표오른쪽(1)
        self.사진넣기절대값(이미지[1], 44, 12)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(3)
        self.셀병합()
        self.글자크기(13)
        self.진하게()
        self.폰트('맑은 고딕')
        self.내일날짜분리년()
        self.글자색(255, 0, 0)
        self.내일날짜분리월일요일()
        self.문장(' 조간[온라인: ')
        self.오늘날짜분리월일요일()
        self.문장(' 12:00]')
        self.글자색(0, 0, 0)
        self.문장('부터 보도 가능합니다.')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(3)
        self.셀병합()
        self.표테두리타입(1, 1, 0, 0)
        self.표오른쪽(1)
        self.폰트('돋움체')
        self.진하게()
        self.글자크기(12)
        self.문장('담당부서')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(2)
        self.셀병합()
        self.글자크기(11)
        self.폰트('돋움체')
        self.줄간격(140)
        self.기본정렬()
        self.문장('○○○팀 ○○○ 팀장(전화: 061-820-0000, 전자우편: ○○○@kisa.or.kr)\r\n○○○팀 ○○○ 책임(전화: 061-820-0000, 전자우편: ○○○@kisa.or.kr)')
        self.표오른쪽(1)
        self.폰트('돋움체')
        self.진하게()
        self.글자크기(12)
        self.문장('참고자료')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(1)
        self.셀병합()
        self.글자크기(11)
        self.폰트('돋움체')
        self.문장('사진 있음 ▣   사진 없음 □')
        self.표오른쪽(1)
        self.글자크기(11)
        self.폰트('돋움체')
        self.문장('총 1매')
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(3)
        self.셀병합()
        self.표테두리타입(1, 0, 0, 0)
        self.폰트('HY헤드라인M')
        self.글자크기(20)
        self.문장(제목)
        self.표오른쪽(1)
        self.셀선택()
        self.표오른쪽(3)
        self.셀병합()
        self.표테두리타입(0, 0, 0, 0)
        self.폰트('HY헤드라인M')
        self.글자크기(17)
        self.문장('- ' + 부제 + ' -')
        self.표나가기2()

    if (lambda self, 번호, 내용: self.표만들기([
17.4,
0.9,
183.5 - self.문단여백측정()], [
9.2])self.셀여백제로()self.표배경색(43, 45, 99)self.표테두리색(43, 45, 99)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(16)self.가운데정렬()self.글자색(255, 255, 255)self.문장('참고' + str(번호))self.표오른쪽(1)self.표테두리타입(0, 0, 1, 0)self.표너비줄이기(3)self.표오른쪽(1)self.표테두리색(43, 45, 99)self.표테두리굵기(7, 7, 6, 6)self.표테두리타입(1, 1, 0, 0)self.폰트('HY헤드라인M')self.글자크기(16)self.문장(' ' + 내용)self.표나가기2()):
        
        def 인진참고(self, 번호, 내용):
            self.표만들기([
                17.4,
                0.9,
                183.5 - self.문단여백측정()], [
                9.2])
            self.셀여백제로()
            self.표배경색(43, 45, 99)
            self.표테두리색(43, 45, 99)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('참고' + str(번호))
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 0)
            self.표너비줄이기(3)
            self.표오른쪽(1)
            self.표테두리색(43, 45, 99)
            self.표테두리굵기(7, 7, 6, 6)
            self.표테두리타입(1, 1, 0, 0)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 번호, 내용: self.표만들기([
17.4,
0.9,
183.5 - self.문단여백측정()], [
9.2])self.셀여백제로()self.표배경색(43, 45, 99)self.표테두리색(43, 45, 99)self.표테두리굵기(6, 6, 6, 6)self.폰트('HY헤드라인M')self.글자크기(16)self.가운데정렬()self.글자색(255, 255, 255)self.문장('붙임' + str(번호))self.표오른쪽(1)self.표테두리타입(0, 0, 1, 0)self.표너비줄이기(3)self.표오른쪽(1)self.표테두리색(43, 45, 99)self.표테두리굵기(7, 7, 6, 6)self.표테두리타입(1, 1, 0, 0)self.폰트('HY헤드라인M')self.글자크기(16)self.문장(' ' + 내용)self.표나가기2()):
        
        def 인진붙임(self, 번호, 내용):
            self.표만들기([
                17.4,
                0.9,
                183.5 - self.문단여백측정()], [
                9.2])
            self.셀여백제로()
            self.표배경색(43, 45, 99)
            self.표테두리색(43, 45, 99)
            self.표테두리굵기(6, 6, 6, 6)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('붙임' + str(번호))
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 0)
            self.표너비줄이기(3)
            self.표오른쪽(1)
            self.표테두리색(43, 45, 99)
            self.표테두리굵기(7, 7, 6, 6)
            self.표테두리타입(1, 1, 0, 0)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
81,
81], [
11])self.표전체()self.표테두리타입(1, 1, 0, 0)self.표내부선타입(0, 0)self.글자크기(11)self.폰트('맑은 고딕')self.캔슬()self.표처음()if len(내용) >= 1:
self.문장(내용[0])else:
self.오늘날짜()self.엔터(1)if len(내용) >= 2:
self.문장(내용[1])else:
self.문장('경영기획본부 혁신전략단 전략기획팀')self.표오른쪽(1)self.오른쪽정렬()if len(내용) >= 3:
self.문장(내용[2] + ' : ')else:
self.문장('팀장 : ')if len(내용) >= 4:
self.문장(내용[3])else:
self.문장('범피스')self.엔터(1)if len(내용) >= 5:
self.문장(내용[4] + ' : ')else:
self.문장('담당 : ')if len(내용) >= 6:
self.문장(내용[5])else:
self.문장('범피스')self.표나가기2()):
        
        def 인진보고자(self, 내용):
            self.표만들기([
                81,
                81], [
                11])
            self.표전체()
            self.표테두리타입(1, 1, 0, 0)
            self.표내부선타입(0, 0)
            self.글자크기(11)
            self.폰트('맑은 고딕')
            self.캔슬()
            self.표처음()
            if len(내용) >= 1:
                self.문장(내용[0])
            else:
                self.오늘날짜()
            self.엔터(1)
            if len(내용) >= 2:
                self.문장(내용[1])
            else:
                self.문장('경영기획본부 혁신전략단 전략기획팀')
            self.표오른쪽(1)
            self.오른쪽정렬()
            if len(내용) >= 3:
                self.문장(내용[2] + ' : ')
            else:
                self.문장('팀장 : ')
            if len(내용) >= 4:
                self.문장(내용[3])
            else:
                self.문장('범피스')
            self.엔터(1)
            if len(내용) >= 5:
                self.문장(내용[4] + ' : ')
            else:
                self.문장('담당 : ')
            if len(내용) >= 6:
                self.문장(내용[5])
            else:
                self.문장('범피스')
            self.표나가기2()

    if (lambda self, 내용: if self.방금처리 == '인진표':
self.궁극의정리위치보정 = -1self.백스페이스()self.대상.SetPosBySet(self.위치저장)셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]if str(셀위치) == 'A1':
self.표아래쪽(1)else:
self.표오른쪽(1)for None in range(len(내용)):
i = Noneif i != 0:
pass입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                if '○' in 입력내용:
                    입력내용 = 입력내용.replace('○', ' ○')
                    self.왼쪽정렬()
                elif '□' in 입력내용:
                    입력내용 = 입력내용.replace('□', ' □')
                    self.왼쪽정렬()
                    self.내어쓰기(-20)
                    self.진하게()
                elif '󰋻' in 입력내용:
                    pass
                self.왼쪽정렬()
                self.문장(입력내용)
            self.표끝()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '인진표'
            self.표나가기2()
        return None
        표개수 = len(내용)
        기본길이 = 207 - 표개수 * 3.5
        전체길이 = 기본길이 - self.문단여백측정()
        표넓이 = [
            2] * 표개수
        for None in range(표개수):
            i = None
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                표넓이[i] = 0.5
                표넓이[i] = 0.5
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                표넓이[i] = 1
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                표넓이[i] = 1.5
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                표넓이[i] = 2
                continue
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                pass
            if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                pass
            if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                continue
            표넓이[i] = 4
        any
        표넓이합 = sum(표넓이)
        for None in range(표개수):
            i = None
            표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
        (i, 내용)
        self.표만들기(표넓이, [
            7,
            7])
        self.표전체()
        self.셀여백지정(1, 1, 0, 0)
        self.글자크기(12)
        self.글자간격(-10)
        self.가운데정렬()
        self.폰트('맑은 고딕')
        self.줄간격(130)
        self.캔슬()
        self.표처음()
        self.셀선택()
        self.표오른쪽끝()
        self.진하게()
        self.글자크기(12)
        self.표배경색(210, 235, 238)
        self.캔슬()
        self.표처음()
        for None in range(표개수):
            i = None
            if i != 0:
                pass
            입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
            입력내용 = 입력내용.replace(';', ':')
            self.문장(입력내용)
        self.표처음()
        self.위치저장 = self.대상.GetPosBySet()
        self.방금처리 = '인진표'
        self.표나가기2()
):
        
        def 인진표(self, 내용):
            if self.방금처리 == '인진표':
                self.궁극의정리위치보정 = -1
                self.백스페이스()
                self.대상.SetPosBySet(self.위치저장)
                셀위치 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
                if str(셀위치) == 'A1':
                    self.표아래쪽(1)
                else:
                    self.표오른쪽(1)
                for None in range(len(내용)):
                    i = None
                    if i != 0:
                        pass
                    입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                    입력내용 = 입력내용.replace(';', ':')
                    if '○' in 입력내용:
                        입력내용 = 입력내용.replace('○', ' ○')
                        self.왼쪽정렬()
                    elif '□' in 입력내용:
                        입력내용 = 입력내용.replace('□', ' □')
                        self.왼쪽정렬()
                        self.내어쓰기(-20)
                        self.진하게()
                    elif '󰋻' in 입력내용:
                        pass
                    self.왼쪽정렬()
                    self.문장(입력내용)
                self.표끝()
                self.위치저장 = self.대상.GetPosBySet()
                self.방금처리 = '인진표'
                self.표나가기2()
            return None
            표개수 = len(내용)
            기본길이 = 207 - 표개수 * 3.5
            전체길이 = 기본길이 - self.문단여백측정()
            표넓이 = [
                2] * 표개수
            for None in range(표개수):
                i = None
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('소요시간',)()):
                    표넓이[i] = 0.5
                    표넓이[i] = 0.5
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('연번', '순번', '번호', '구분')()):
                    표넓이[i] = 1
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('시간계획',)()):
                    표넓이[i] = 1.5
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주민번호', '비고')()):
                    표넓이[i] = 2
                    continue
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass):
                    pass
                if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    pass
                if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 내용[i].replace('엔터 ', '').replace(' ', ''):
pass)(('주소', '내용', '사항', '세부', '수집항목')()):
                    continue
                표넓이[i] = 4
            any
            표넓이합 = sum(표넓이)
            for None in range(표개수):
                i = None
                표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
            (i, 내용)
            self.표만들기(표넓이, [
                7,
                7])
            self.표전체()
            self.셀여백지정(1, 1, 0, 0)
            self.글자크기(12)
            self.글자간격(-10)
            self.가운데정렬()
            self.폰트('맑은 고딕')
            self.줄간격(130)
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽끝()
            self.진하게()
            self.글자크기(12)
            self.표배경색(210, 235, 238)
            self.캔슬()
            self.표처음()
            for None in range(표개수):
                i = None
                if i != 0:
                    pass
                입력내용 = (lambda .0: if None:
passfor None in .0:
if None:
if None.strip():
pass)(내용[i].split('엔터 ')())
                입력내용 = 입력내용.replace(';', ':')
                self.문장(입력내용)
            self.표처음()
            self.위치저장 = self.대상.GetPosBySet()
            self.방금처리 = '인진표'
            self.표나가기2()

    
    def 인진표지(self, 제목, 이미지):
        self.표만들기([
            205.5 - self.문단여백측정()], [
            45,
            1,
            66,
            1,
            91,
            28])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(1)
        self.캔슬()
        self.표처음()
        self.글자색(255, 255, 255)
        self.문장('[표지]')
        self.표오른쪽(1)
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                48,
                87,
                185],
            [
                0,
                223,
                230,
                247]])
        self.표오른쪽(1)
        self.폰트('HY헤드라인M')
        self.글자크기(25)
        self.가운데정렬()
        self.셀여백지정(1, 1, 2, 2)
        self.문장(제목)
        self.표오른쪽(1)
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                223,
                230,
                247],
            [
                0,
                48,
                87,
                185]])
        self.표오른쪽(1)
        self.폰트('맑은 고딕')
        self.글자크기(24)
        self.진하게()
        self.가운데정렬()
        self.오늘날짜년월()
        self.표오른쪽(1)
        self.사진넣기절대값(이미지[2], 71, 12)
        self.표나가기2()

    if (lambda self, 이미지: 현위치 = self.현재위치()self.머릿말()self.표만들기([
81,
81], [
11])self.셀여백제로()self.표테두리타입(0, 0, 0, 0)self.사진넣기절대값(이미지[0], 37, 6.6)self.기본정렬()self.표오른쪽(1)self.사진넣기절대값(이미지[1], 42, 12)self.표테두리타입(0, 0, 0, 0)self.오른쪽정렬()self.대상.SetPosBySet(현위치)):
        
        def 인진머리말(self, 이미지):
            현위치 = self.현재위치()
            self.머릿말()
            self.표만들기([
                81,
                81], [
                11])
            self.셀여백제로()
            self.표테두리타입(0, 0, 0, 0)
            self.사진넣기절대값(이미지[0], 37, 6.6)
            self.기본정렬()
            self.표오른쪽(1)
            self.사진넣기절대값(이미지[1], 42, 12)
            self.표테두리타입(0, 0, 0, 0)
            self.오른쪽정렬()
            self.대상.SetPosBySet(현위치)

    
    def 인진제목(self, 제목):
        self.표만들기([
            205.5 - self.문단여백측정()], [
            0.35,
            9,
            0.35])
        self.셀여백제로()
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(1)
        self.캔슬()
        self.표처음()
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                48,
                87,
                185],
            [
                0,
                223,
                230,
                247]])
        self.글자색(48, 87, 185)
        self.문장('[제목]')
        self.표오른쪽(1)
        self.폰트('HY헤드라인M')
        self.글자크기(20)
        self.가운데정렬()
        self.셀여백지정(1, 1, 2, 2)
        if len(제목) >= 23:
            pass
        self.글자간격(-3)
        if len(제목) >= 24:
            pass
        self.글자간격(-6)
        if len(제목) >= 25:
            pass
        self.글자간격(-9)
        if len(제목) >= 26:
            pass
        self.글자장평(95)
        if len(제목) >= 27:
            pass
        self.글자간격(-12)
        self.문장(제목)
        self.표오른쪽(1)
        self.표배경그라데이션2('Linear', 90, [
            [
                255,
                223,
                230,
                247],
            [
                0,
                48,
                87,
                185]])
        self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ○ ', 텍스트):
                                pass
                            if None(' ○ ', 텍스트):
                                매치 = None(' ○ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   - ', 텍스트):
                                pass
                            if None('   - ', 텍스트):
                                매치 = None('   - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('   - [가-힣\\s]+:', 텍스트):
                                    pass
                                if None('   - [가-힣\\s]+:', 텍스트):
                                    매치 = None('   - [가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('     \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '인진표':
            if None('^표', 텍스트):
                pass
            if not None('^표', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s+', 텍스트):
                pass
            if None('^제목\\s+', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.인진제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표\\s*:\\s*', 텍스트):
                pass
        if not None('^표\\s*:\\s*', 텍스트):
            if None('^표\\s+', 텍스트):
                pass
            if None('^표\\s+', 텍스트):
                텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                self.백스페이스()
                텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                        self.인진표(분리텍스트)
                        self.백스페이스()
                    elif None('^중제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s+', 텍스트):
                pass
            if None('^보고자\\s+', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.split, None('[:/]', 텍스트)[1:], 분리텍스트, x = re.sub
                        self.인진보고자(분리텍스트)
                        self.백스페이스()
                    elif None('^표지\\s*:\\s*', 텍스트):
                        pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s+', 텍스트):
                pass
            if None('^표지\\s+', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                self.인진표지(텍스트.split(':', 1)[1].strip(), 이미지)
                self.백스페이스()
            elif None('^소제목\\s*:\\s*', 텍스트):
                pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s+', 텍스트):
                pass
            if None('^소제목\\s+', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                if self.소제목카운트 > 12:
                    self.소제목카운트 = 1
                self.강원소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^설명\\s*:\\s*', 텍스트):
                pass
        if not None('^설명\\s*:\\s*', 텍스트):
            if None('^설명\\s+', 텍스트):
                pass
            if None('^설명\\s+', 텍스트):
                텍스트 = None('^(설명\\s*:|설명|)\\s*', '', 텍스트, count = 1)
                self.문장('< ' + 텍스트.strip() + ' >')
                None()
                self.중고딕()
                self.글자크기(13)
                self.기본글자()
                self.가운데정렬()
                self.진하게()
                self.캔슬()
                self.대상.MovePos(6)
            elif None('^보도자료\\s*:\\s*', 텍스트):
                pass
        if not None('^보도자료\\s*:\\s*', 텍스트):
            if None('^보도자료\\s+', 텍스트):
                pass
            if None('^보도자료\\s+', 텍스트):
                텍스트 = None('^(보도자료\\s*:|보도자료)\\s*', '보도자료:', 텍스트, count = 1)
                self.백스페이스()
                self.인진보도자료(이미지, 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^참고\\s*:\\s*', 텍스트):
                pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s+', 텍스트):
                pass
            if None('^참고\\s+', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.참고카운트 = self.참고카운트 + 1
                self.인진참고(self.참고카운트, 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s+', 텍스트):
                pass
            if None('^붙임\\s+', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.붙임카운트 = self.붙임카운트 + 1
                self.인진붙임(self.붙임카운트, 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(15)
            self.문단위(10)
            self.내어쓰기(-22.5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', 'O', 'o', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', 'O', 'o', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍|O|o||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-30)
            self.문단위(7)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ○ \\((.*?)\\)', 텍스트):
                pass
            if None(' ○ \\((.*?)\\)', 텍스트):
                매치 = None(' ○ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('휴먼명조')
            self.글자크기(15)
            self.내어쓰기(-46.7)
            self.문단위(5)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('   - \\((.*?)\\)', 텍스트):
                pass
            if None('   - \\((.*?)\\)', 텍스트):
                매치 = None('   - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '     * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.내어쓰기(-44.4)
            self.문단위(0)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '     ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.내어쓰기(-44.4)
            self.문단위(0)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 인진궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   - ', 텍스트):
passif None('   - ', 텍스트):
매치 = None('   - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('   - [가-힣\\s]+:', 텍스트):
passif None('   - [가-힣\\s]+:', 텍스트):
매치 = None('   - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ○ ', 텍스트):
                                    pass
                                if None(' ○ ', 텍스트):
                                    매치 = None(' ○ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   - ', 텍스트):
                                    pass
                                if None('   - ', 텍스트):
                                    매치 = None('   - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('   - [가-힣\\s]+:', 텍스트):
                                        pass
                                    if None('   - [가-힣\\s]+:', 텍스트):
                                        매치 = None('   - [가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('     \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '인진표':
                if None('^표', 텍스트):
                    pass
                if not None('^표', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s+', 텍스트):
                    pass
                if None('^제목\\s+', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.인진제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표\\s*:\\s*', 텍스트):
                    pass
            if not None('^표\\s*:\\s*', 텍스트):
                if None('^표\\s+', 텍스트):
                    pass
                if None('^표\\s+', 텍스트):
                    텍스트 = None('^(표\\s*:|표)\\s*', '표:', 텍스트, count = 1)
                    self.백스페이스()
                    텍스트 = None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 텍스트)
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.sub
                            self.인진표(분리텍스트)
                            self.백스페이스()
                        elif None('^중제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s+', 텍스트):
                    pass
                if None('^보고자\\s+', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.split, None('[:/]', 텍스트)[1:], 분리텍스트, x = re.sub
                            self.인진보고자(분리텍스트)
                            self.백스페이스()
                        elif None('^표지\\s*:\\s*', 텍스트):
                            pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s+', 텍스트):
                    pass
                if None('^표지\\s+', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    self.인진표지(텍스트.split(':', 1)[1].strip(), 이미지)
                    self.백스페이스()
                elif None('^소제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s+', 텍스트):
                    pass
                if None('^소제목\\s+', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    if self.소제목카운트 > 12:
                        self.소제목카운트 = 1
                    self.강원소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^설명\\s*:\\s*', 텍스트):
                    pass
            if not None('^설명\\s*:\\s*', 텍스트):
                if None('^설명\\s+', 텍스트):
                    pass
                if None('^설명\\s+', 텍스트):
                    텍스트 = None('^(설명\\s*:|설명|)\\s*', '', 텍스트, count = 1)
                    self.문장('< ' + 텍스트.strip() + ' >')
                    None()
                    self.중고딕()
                    self.글자크기(13)
                    self.기본글자()
                    self.가운데정렬()
                    self.진하게()
                    self.캔슬()
                    self.대상.MovePos(6)
                elif None('^보도자료\\s*:\\s*', 텍스트):
                    pass
            if not None('^보도자료\\s*:\\s*', 텍스트):
                if None('^보도자료\\s+', 텍스트):
                    pass
                if None('^보도자료\\s+', 텍스트):
                    텍스트 = None('^(보도자료\\s*:|보도자료)\\s*', '보도자료:', 텍스트, count = 1)
                    self.백스페이스()
                    self.인진보도자료(이미지, 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^참고\\s*:\\s*', 텍스트):
                    pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s+', 텍스트):
                    pass
                if None('^참고\\s+', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.참고카운트 = self.참고카운트 + 1
                    self.인진참고(self.참고카운트, 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s+', 텍스트):
                    pass
                if None('^붙임\\s+', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.붙임카운트 = self.붙임카운트 + 1
                    self.인진붙임(self.붙임카운트, 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(15)
                self.문단위(10)
                self.내어쓰기(-22.5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', 'O', 'o', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', 'O', 'o', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍|O|o||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-30)
                self.문단위(7)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ○ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ○ \\((.*?)\\)', 텍스트):
                    매치 = None(' ○ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '   - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('휴먼명조')
                self.글자크기(15)
                self.내어쓰기(-46.7)
                self.문단위(5)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('   - \\((.*?)\\)', 텍스트):
                    pass
                if None('   - \\((.*?)\\)', 텍스트):
                    매치 = None('   - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '     * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.내어쓰기(-44.4)
                self.문단위(0)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '     ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('맑은 고딕')
                self.글자크기(13)
                self.내어쓰기(-44.4)
                self.문단위(0)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.참고카운트 = 0self.붙임카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.인진궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.인진궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '인진표':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 인진궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.참고카운트 = 0
            self.붙임카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.인진궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.인진궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '인진표':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.인진궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.인진궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 인진궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.인진궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.인진궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    
    def 인진되돌리기(self):
        if (lambda : self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 텍스트 == '':
self.캔슬()self.문장('-')블록스캔값 = 99self.대상.ReleaseScan()결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = 결과텍스트.replace('\r\n', ' 엔터 ').replace('\n', ' 엔터 ')self.문장(결과텍스트)결과텍스트.strip()if ValueError:
e = Noneprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel e결과텍스트.strip()e = Nonedel eif Exception:
e = Noneprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel e결과텍스트.strip()e = Nonedel e):
            
            def 셀값읽기():
                self.대상.HAction.Run('Select')
                self.대상.HAction.Run('Select')
                self.대상.HAction.Run('Select')
                self.대상.HAction.Run('Select')
                self.대상.InitScan(1, 255)
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 텍스트 == '':
                    self.캔슬()
                    self.문장('-')
                    블록스캔값 = 99
                self.대상.ReleaseScan()
                결과텍스트 = ''
                
                try:
                    if 블록스캔값 == 2 or 블록스캔값 == 3:
                        결과텍스트 = 결과텍스트 + 텍스트
                        블록스캔 = self.대상.GetText()
                        블록스캔값 = 블록스캔[0]
                        텍스트 = 블록스캔[1]
                        if 블록스캔값 == 2:
                            continue
                        if 블록스캔값 == 3:
                            continue

                self.대상.ReleaseScan()
                결과텍스트 = 결과텍스트.replace('\r\n', ' 엔터 ').replace('\n', ' 엔터 ')
                self.문장(결과텍스트)
                return 결과텍스트.strip()
                if ValueError:
                    e = None
                    print(f'''값 오류 : {e}''')
                    self.대상.ReleaseScan()
                    e = None
                    del e
                    return 결과텍스트.strip()
                e = None
                del e
                if Exception:
                    e = None
                    print(f'''오류 발생 : {e}''')
                    self.대상.ReleaseScan()
                    e = None
                    del e
                    return 결과텍스트.strip()
                e = None
                del e

        self.문서처음()
        self.대상.HAction.Run('SelectAll')
        self.대상.HAction.Run('Copy')
        self.새창()
        self.문서여백(20, 20, 10, 15, 15, 10)
        self.대상.HAction.Run('Paste')
        for 컨트롤표 in self.컨트롤표목록():
            self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
            self.대상.HAction.Run('MoveRight')
            셀값읽기값 = None()
            if 셀값읽기값 == '[표지]':
                self.표오른쪽(2)
                표지내용 = None()
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                self.대상.SetMessageBoxMode(16)
                self.딜리트()
                self.대상.SetMessageBoxMode(240)
                self.문장('표지:' + 표지내용)
                continue
            if 셀값읽기값 == '[제목]':
                self.표오른쪽(1)
                제목내용 = None()
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                self.대상.SetMessageBoxMode(16)
                self.딜리트()
                self.대상.SetMessageBoxMode(240)
                self.문장('제목:' + 제목내용)
                continue
            if 셀값읽기값 == '[보도자료]':
                self.표아래쪽(6)
                제목 = None()
                self.표아래쪽(1)
                부제 = None().strip().strip('-').strip()
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                self.대상.SetMessageBoxMode(16)
                self.딜리트()
                self.대상.SetMessageBoxMode(240)
                self.문장('보도자료:' + 제목 + ':' + 부제)
                continue
            if '엔터' in 셀값읽기값:
                if None('\\d{4}\\.\\s*\\d{1,2}\\.\\s*\\d{1,2}\\.', 셀값읽기값):
                    pass
                if None('\\d{4}\\.\\s*\\d{1,2}\\.\\s*\\d{1,2}\\.', 셀값읽기값):
                    self.표오른쪽(1)
                    보고자 = None()
                    self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                    self.대상.SetMessageBoxMode(16)
                    self.딜리트()
                    self.대상.SetMessageBoxMode(240)
                    self.문장('보고자:' + 셀값읽기값.replace('엔터', '/') + '/' + 보고자.replace('엔터', '/'))
                    continue
            if 셀값읽기값.startswith('참고'):
                pass
            if 셀값읽기값.startswith('참고'):
                self.표오른쪽(2)
                제목내용 = None()
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                self.대상.SetMessageBoxMode(16)
                self.딜리트()
                self.대상.SetMessageBoxMode(240)
                self.문장('참고:' + 제목내용)
                continue
            if 셀값읽기값.startswith('붙임'):
                pass
            if 셀값읽기값.startswith('붙임'):
                self.표오른쪽(2)
                제목내용 = None()
                self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
                self.대상.SetMessageBoxMode(16)
                self.딜리트()
                self.대상.SetMessageBoxMode(240)
                self.문장('붙임:' + 제목내용)
                continue
            self.대상.SetPosBySet(컨트롤표.GetAnchorPos(0))
            self.문장('표:')
            self.대상.HAction.Run('MoveRight')
            self.표전체()
            self.셀엔터변환()
            self.표문장변환()
        셀값읽기
        self.대상.HAction.Run('SelectAll')
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        결과텍스트 = ''
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                결과텍스트 = 결과텍스트 + 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        분할데이터 = 결과텍스트.splitlines()
        for None in :
            if None:
                continue
                줄, + [
                    ''] = re.findall, 셀값읽기, 분할데이터
                정리데이터 = []
                for 순번, 줄 in enumerate(분할데이터):
                    if 줄.startswith('□'):
                        pass
                    if not 줄.startswith('□'):
                        if 줄.startswith('ㅁ'):
                            pass
                        if 줄.startswith('ㅁ'):
                            정리데이터.append(줄.replace('□', '네모: ', 1).replace('ㅁ', '네모: ', 1))
                            continue
                    if 줄.startswith('○'):
                        pass
                    if not 줄.startswith('○'):
                        if 줄.startswith('◯'):
                            pass
                        if 줄.startswith('◯'):
                            정리데이터.append(줄.replace('○', '원: ', 1).replace('◯', '원: ', 1))
                            continue
                    if 줄.startswith('-'):
                        pass
                    if 줄.startswith('-'):
                        정리데이터.append(줄.replace('-', '바: ', 1))
                        continue
                    if 줄.startswith('※'):
                        pass
                    if 줄.startswith('※'):
                        정리데이터.append(줄.replace('※', '당구: ', 1))
                        continue
                    if 줄.startswith('*'):
                        pass
                    if 줄.startswith('*'):
                        정리데이터.append(줄.replace('*', '별: ', 1))
                        continue
                    if 줄.startswith('표:◆ '):
                        pass
                    if not 줄.startswith('표:◆ '):
                        if 줄.startswith('표: ◆ '):
                            pass
                        if 줄.startswith('표: ◆ '):
                            정리데이터.append(줄.replace('표:◆ ', '요약 : ', 1).replace('표: ◆ ', '요약 : ', 1))
                            continue
                    if 줄.startswith('<'):
                        pass
                    if 줄.startswith('<'):
                        if 줄.endswith('>'):
                            pass
                        if 줄.endswith('>'):
                            정리데이터.append('설명: ' + 줄.replace('<', '').replace('>', ''))
                            continue
                    if None('^대면보고\\s*/\\s*', 줄):
                        pass
                    if None('^대면보고\\s*/\\s*', 줄):
                        re.sub(None('\\s*/.*?/\\s*', '', 줄).strip().replace('대면보고', '대면보고 : ', 1))
                        continue
                    if None('^서면보고\\s*/\\s*', 줄):
                        pass
                    if None('^서면보고\\s*/\\s*', 줄):
                        re.sub(None('\\s*/.*?/\\s*', '', 줄).strip().replace('서면보고', '서면보고 : ', 1))
                        continue
                    if None('표:\\d+\\s+', 줄):
                        pass
                    if None('표:\\d+\\s+', 줄):
                        re.sub(None('^표:\\d+', '소제목:', 줄))
                        continue
                    if None('^\\d{1,}\\.\\s{1}(.+)', 줄):
                        pass
                    if None('^\\d{1,}\\.\\s{1}(.+)', 줄):
                        re.sub(None('^\\d{1,}\\.\\s{1}(.+)', '소제목 : \\1', 줄))
                        continue
                    if None('^[가-하]\\.', 줄):
                        pass
                    if None('^[가-하]\\.', 줄):
                        re.sub(None('^[가-하]\\.', '가제목:', 줄))
                        continue
                    if 순번 > 0:
                        if 줄.startswith('표:연간일정:1월:2월:3월:4월:5월:6월:7월:8월:9월:10월:11월:12월'):
                            pass
                        if 줄.startswith('표:연간일정:1월:2월:3월:4월:5월:6월:7월:8월:9월:10월:11월:12월'):
                            분할데이터[순번] = 줄.replace('표:연간일정:1월:2월:3월:4월:5월:6월:7월:8월:9월:10월:11월:12월', '표:연간일정', 1)
                            정리데이터.append(분할데이터[순번])
                            continue
                    if 순번 > 0:
                        if 분할데이터[순번 - 1].startswith('표:'):
                            pass
                        if 분할데이터[순번 - 1].startswith('표:'):
                            if 분할데이터[순번 - 1].startswith('표:◆'):
                                pass
                            if not 분할데이터[순번 - 1].startswith('표:◆') and 줄 == '':
                                if 분할데이터[순번].startswith('표:'):
                                    pass
                                if not 분할데이터[순번].startswith('표:'):
                                    분할데이터[순번] = '표: ' + 줄
                                    정리데이터.append(분할데이터[순번])
                                    continue
                    정리데이터.append(줄)
                재정리데이터 = []
                for 순번, 줄 in enumerate(정리데이터):
                    if 순번 > 0 and 순번 < len(정리데이터) - 1:
                        if 정리데이터[순번 - 1].startswith('표:'):
                            pass
                        if not 정리데이터[순번 - 1].startswith('표:'):
                            if 정리데이터[순번 + 1].startswith('표:'):
                                pass
                            if not 정리데이터[순번 + 1].startswith('표:') and 줄 == '':
                                재정리데이터.append(줄.replace('표:', '글상자: ', 1))
                                continue
                    재정리데이터.append(줄)
                정리데이터.append
                결과텍스트 = '\r\n'.join(재정리데이터)
                결과텍스트 = 결과텍스트.replace('요약\r\n', '요약 : ')
                self.백스페이스()
                시작지점 = self.현재위치()
                self.기본정렬()
                self.기본글자()
                self.글자크기(10)
                self.폰트('맑은 고딕')
                self.줄간격(150)
                self.문단위(0)
                self.내어쓰기(0)
                self.문장(결과텍스트)
                종료지점 = self.현재위치()
                self.대상.SetPosBySet(시작지점)
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(종료지점)
                return None
                
                if ValueError:
                    줄, e = 정리데이터.append, re.match, None
                    print(f'''값 오류 : {e}''')
                    self.대상.ReleaseScan()
                    e = None
                    del e
                    return None
                    e = None
                    del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e

    
    def 인진MD변환(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        결과텍스트 = ''
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                결과텍스트 = 결과텍스트 + 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        분할데이터 = 결과텍스트.splitlines()
        for None in :
            if None:
                continue
                None, 분할데이터, 분할데이터, 줄 = None
                정리데이터 = []
                for None in enumerate(분할데이터):
                    if ():
                        if 줄.startswith('네모:'):
                            pass
                        if 줄.startswith('네모:'):
                            정리데이터.append(줄.replace('네모:', '[□]', 1))
                            continue
                        if 줄.startswith('원:'):
                            pass
                        if 줄.startswith('원:'):
                            정리데이터.append(줄.replace('원:', '  [○]', 1))
                            continue
                        if 줄.startswith('바:'):
                            pass
                    if 줄.startswith('바:'):
                        정리데이터.append(줄.replace('바:', '    [-]', 1))
                        continue
                    if 줄.startswith('별:'):
                        pass
                    if 줄.startswith('별:'):
                        정리데이터.append(줄.replace('별:', '    [*]', 1))
                        continue
                    if 줄.startswith('당구:'):
                        pass
                    if 줄.startswith('당구:'):
                        정리데이터.append(줄.replace('당구:', '    [※]', 1))
                        continue
                    if 줄.startswith('설명:'):
                        pass
                    if 줄.startswith('설명:'):
                        정리데이터.append(줄.replace('설명:', '[설명]', 1))
                        continue
                    if 줄.startswith('참고:'):
                        pass
                    if 줄.startswith('참고:'):
                        정리데이터.append(줄.replace('참고:', '[참고]', 1))
                        continue
                    if 줄.startswith('붙임:'):
                        pass
                    if 줄.startswith('붙임:'):
                        정리데이터.append(줄.replace('붙임:', '[붙임]', 1))
                        continue
                    if 줄.startswith('보도자료:'):
                        pass
                    if 줄.startswith('보도자료:'):
                        정리데이터.append(줄.replace('보도자료:', '[보도자료]', 1))
                        continue
                    if 줄.startswith('제목:'):
                        pass
                    if 줄.startswith('제목:'):
                        정리데이터.append(줄.replace('제목:', '# ', 1))
                        continue
                    if 줄.startswith('표지:'):
                        pass
                    if 줄.startswith('표지:'):
                        정리데이터.append('---')
                        정리데이터.append(줄)
                        정리데이터.append('---')
                        continue
                    if 순번 > 0:
                        if 분할데이터[순번 - 1].startswith('표:'):
                            pass
                        if 분할데이터[순번 - 1].startswith('표:'):
                            if 줄.startswith('표:'):
                                pass
                            if 줄.startswith('표:'):
                                정리데이터.append(줄.replace('표:', '|', 1).replace(':', '|').replace(';', ':') + '|')
                                continue
                    if 순번 == 0:
                        if 줄.startswith('표:'):
                            pass
                        if not 줄.startswith('표:'):
                            if 줄.startswith('표:'):
                                pass
                            if 줄.startswith('표:') and 순번 > 0:
                                if 분할데이터[순번 - 1].startswith('표:'):
                                    pass
                                if not 분할데이터[순번 - 1].startswith('표:'):
                                    None('\\b(\\d{1,2}):(\\d{2})\\s*~\\s*(\\d{1,2}):(\\d{2})\\b', '\\1;\\2~\\3;\\4', 줄) = re.sub
                                    개수 = 줄.count(':')
                                    정리데이터.append(줄.replace('표:', '|', 1).replace(':', '|').replace(';', ':') + '|')
                                    정리데이터.append('|---' * 개수 + '|')
                                    continue
                re.sub
                print(정리데이터)
                결과텍스트 = '\r\n'.join(정리데이터)
                self.문장(결과텍스트)
                return None
                
                if ValueError:
                    줄, e = None, None, ()
                    print(f'''값 오류 : {e}''')
                    self.대상.ReleaseScan()
                    e = None
                    del e
                    return None
                    e = None
                    del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e

    
    def MD중간변환(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        결과텍스트 = ''
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                결과텍스트 = 결과텍스트 + 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        분할데이터 = 결과텍스트.splitlines()
        for None in :
            if None:
                continue
                None, 분할데이터, 분할데이터, 줄 = None
                정리데이터 = []
                for None in enumerate(분할데이터):
                    if ():
                        if 줄.startswith('[□]'):
                            pass
                        if 줄.startswith('[□]'):
                            정리데이터.append(줄.replace('[□]', '네모:', 1))
                            continue
                        if 줄.startswith('[○]'):
                            pass
                        if 줄.startswith('[○]'):
                            정리데이터.append(줄.replace('[○]', '원:', 1))
                            continue
                        if 줄.startswith('[-]'):
                            pass
                    if 줄.startswith('[-]'):
                        정리데이터.append(줄.replace('[-]', '바:', 1))
                        continue
                    if 줄.startswith('[*]'):
                        pass
                    if 줄.startswith('[*]'):
                        정리데이터.append(줄.replace('[*]', '별:', 1))
                        continue
                    if 줄.startswith('[※]'):
                        pass
                    if 줄.startswith('[※]'):
                        정리데이터.append(줄.replace('[※]', '당구:', 1))
                        continue
                    if 줄.startswith('[설명]'):
                        pass
                    if 줄.startswith('[설명]'):
                        정리데이터.append(줄.replace('[설명]', '설명:', 1))
                        continue
                    if 줄.startswith('[참고]'):
                        pass
                    if 줄.startswith('[참고]'):
                        정리데이터.append(줄.replace('[참고]', '참고:', 1))
                        continue
                    if 줄.startswith('[붙임]'):
                        pass
                    if 줄.startswith('[붙임]'):
                        정리데이터.append(줄.replace('[붙임]', '붙임:', 1))
                        continue
                    if 줄.startswith('[보도자료]'):
                        pass
                    if 줄.startswith('[보도자료]'):
                        정리데이터.append(줄.replace('[보도자료]', '보도자료:', 1))
                        continue
                    if None('^#\\s', 줄):
                        pass
                    if None('^#\\s', 줄):
                        정리데이터.append(줄.replace('# ', '제목:', 1))
                        continue
                    if None('^##\\s', 줄):
                        pass
                    if None('^##\\s', 줄):
                        정리데이터.append(줄.replace('## ', '네모:', 1))
                        continue
                    if 줄.startswith('---'):
                        pass
                    if 줄.startswith('---'):
                        continue
                    if 줄.startswith('|-'):
                        pass
                    if 줄.startswith('|-'):
                        continue
                    if 줄.startswith('| -'):
                        pass
                    if 줄.startswith('| -'):
                        continue
                    if 줄.startswith('표지:'):
                        pass
                    if 줄.startswith('표지:'):
                        정리데이터.append(줄)
                        continue
                    if 줄.startswith('|'):
                        pass
                    if 줄.startswith('|'):
                        정리데이터.append('표:' + 줄.strip('|').replace('|', ':'))
                        continue
                re.match
                print(정리데이터)
                self.백스페이스()
                self.현재위치() = '\r\n'.join(정리데이터)
                self.기본정렬()
                self.기본글자()
                self.글자크기(10)
                self.폰트('맑은 고딕')
                self.줄간격(150)
                self.문단위(0)
                self.내어쓰기(0)
                self.문장(결과텍스트)
                종료지점 = self.현재위치()
                self.대상.SetPosBySet(시작지점)
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(종료지점)
                return None
                
                if ValueError:
                    줄, e = None, None, ()
                    print(f'''값 오류 : {e}''')
                    self.대상.ReleaseScan()
                    e = None
                    del e
                    return None
                    e = None
                    del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e

    if (lambda self, 내용: self.표만들기([
17.2,
1,
181.5 - self.문단여백측정()], [
9.2])self.셀여백제로()self.표배경색(174, 18, 95)self.폰트('HY헤드라인M')self.글자크기(16)self.가운데정렬()self.글자색(255, 255, 255)self.문장('붙임')self.표오른쪽(1)self.표테두리타입(0, 0, 1, 1)self.표너비줄이기(2)self.표오른쪽(1)self.폰트('HY헤드라인M')self.글자크기(16)self.문장(' ' + 내용)self.표나가기2()):
        
        def 세종붙임(self, 내용):
            self.표만들기([
                17.2,
                1,
                181.5 - self.문단여백측정()], [
                9.2])
            self.셀여백제로()
            self.표배경색(174, 18, 95)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('붙임')
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 1)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
17.2,
1,
181.5 - self.문단여백측정()], [
9.2])self.셀여백제로()self.표배경색(174, 18, 95)self.폰트('HY헤드라인M')self.글자크기(16)self.가운데정렬()self.글자색(255, 255, 255)self.문장('참고')self.표오른쪽(1)self.표테두리타입(0, 0, 1, 1)self.표너비줄이기(2)self.표오른쪽(1)self.폰트('HY헤드라인M')self.글자크기(16)self.문장(' ' + 내용)self.표나가기2()):
        
        def 세종참고(self, 내용):
            self.표만들기([
                17.2,
                1,
                181.5 - self.문단여백측정()], [
                9.2])
            self.셀여백제로()
            self.표배경색(174, 18, 95)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장('참고')
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 1, 1)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문장(' ' + 내용)
            self.표나가기2()

    
    def 세종기본계획프롬프트(self):
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('2026년 세종특별자치시 청년정책 기본계획\r\n\r\n')
        self.글자색(0, 0, 0)
        self.문장('#기초자료\r\n')
        self.글자색(0, 0, 255)
        self.문장('5개 분야(일자리, 주거, 교육, 복지·문화, 첨여·권리)\r\n\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 세종특별자치시의 직원으로 #작성내용에 대한 전문적인 지식을 지닌 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 #기초자료를 기본 자료로 사용하여 #작성 규칙을 바탕으로 #출력 서식을 참고하여 문서를 작성하라. 문서의 작성 분량에 관계없이 구체적으로 작성하라.\r\n\r\n# 작성 규칙\r\n‘#출력 예시’에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n  (제목:, 대제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용 "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n\r\n# 출력 서식\r\n제목: 작성하는 계획의 제목\r\n요약: 전체 내용의 요약을 두줄분량으로 한문장으로 작성\r\n소제목: 개요\r\n네모: 목적 및 배경\r\n원: (목적) 한줄의 세부적인 문장으로 작성\r\n원: (배경) 두줄분량을 한문장으로 작성\r\n원: (근거) 법적 근거을 찾아서 법령과 조항만 작성\r\n원: (현황) 내부환경과 외부환경 두줄분량을 한문장으로 작성\r\n소제목: 성과 및 개선\r\n네모: 경과 및 성과\r\n원: (경과) 그동안 추진 경과 작성\r\n원: (성과) 전년도 성과 작성\r\n네모: 평가 및 개선\r\n원: (평가) 전년도 성과에 대한 종합적인 평가 작성 \r\n원: (개선) 전년도 성과에 대한 미비점 개선 작성\r\n소제목: 비전 및 전략\r\n네모: (비전) 종합적 비전 작성 \r\n네모: (목표) 종합적 목표 작성\r\n네모: (전략) 기초자료 N개 분야 전략 작성\r\n원:N가지 내용\r\n네모: (추진과제) 각 전략에 대한 N가지 추진과제 작성\r\n원:N가지 내용\r\n네모: (추진방향) 전략과 과제 수행하기 위한 방향 제시\r\n네모: (추진체계) 계획 수행하기 위한 추진 체계 구체적 작성\r\n소제목: 과제별 추진계획\r\n네모: 과제별 제목\r\n원: 과제별 사업 세부적으로 작성\r\n원: 과제별 추진일정 월단위 구분하여 작성\r\n원: 과제별 필요한 사업예산 세부적으로 작성\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있다\r\n\r\n# 강조사항\r\n‘#작성 규칙’과 ‘#출력 서식’을 지켰는지 검토 후 답변 출력\r\n안내된 글자 수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성')

    
    def 세종추진계획프롬프트(self):
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('2026년 신생에너지 주택지원사업 추진계획\r\n\r\n')
        self.글자색(0, 0, 0)
        self.문장('#기초자료\r\n')
        self.글자색(0, 0, 255)
        self.문장('사업기간 2026.1.1.~12.31. / 사업예산 12억3천만원\r\n\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 세종특별자치시의 직원으로 #작성내용에 대한 전문적인 지식을 지닌 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 #기초자료를 기본 자료로 사용하여 #작성 규칙을 바탕으로 #출력 서식을 참고하여 문서를 작성하라. 문서의 최소 작성분량이 4페이지가 넘지 않도록 작성하라.\r\n\r\n# 작성 규칙\r\n‘#출력 서식’에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n  (제목:, 소제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용 "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n\r\n# 출력 서식\r\n제목: 추진계획 제목\r\n요약: 사업 추진한 원인에서 기대되는 효과에 대해 한 문장 작성\r\n소제목: 추진배경\r\n원: (배경) 사업 추진한 배경을 2줄 분량으로 이어서 간단한 문장으로 작성\r\n소제목: 사업개요\r\n원: (사 업 명) 사업명\r\n원: (사업기간) ‘XX.X.X. ~ XX.XX. (10개월)\r\n원: (사업예산) 000,000천원(금영억연천영백영십영만원)\r\n원: (사업대상) 세종시 소재 단독주택 소유자\r\n원: (주요사업)\r\n바: 첫번째 주요사업을 간결한 문장으로 작성\r\n바: 두번째 주요사업을 간결한 문장으로 작성\r\n바: 세번째 주요사업을 간결한 문장으로 작성\r\n소제목: 세부계획\r\n원: (사업목적) 사업의 목적 간단히 작성\r\n원: (사업내용)\r\n바: 세부 사업 세가지로 분류해서 자세한 문장으로 작성\r\n원: (추진일정) 사업 추진 과정을 간단하고 명료하게 작성\r\n원: (소요예산)\r\n바: 지출 과목 구분하여 소요 예산 산출식으로 작성\r\n원: (예산과목)\r\n원: (기대효과)\r\n바: 첫번째 기대효과에 대해 문장으로 작성\r\n바: 두번째 기대효과에 대해 문장으로 작성\r\n소제목: 향후 계획\r\n원: 사업 추진 시 해야 할 두 가지를 시기가 뒤에 표시되게 작성\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있으며, 일부 기호는 생략 가능하다.\r\n\r\n# 강조사항\r\n‘#작성 규칙’과 ‘#출력 서식’을 지켰는지 검토 후 답변 출력\r\n안내된 글자 수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성')

    
    def 세종검토보고프롬프트(self):
        self.새창()
        self.문서여백(20, 20, 15, 15, 10, 10)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.진하게()
        self.문장('#작성내용\r\n')
        self.글자색(0, 0, 255)
        self.문장('청년센터 운영 사업 업체 선정 방안 검토 보고\r\n\r\n')
        self.글자색(0, 0, 0)
        self.문장('#기초자료\r\n')
        self.글자색(0, 0, 255)
        self.문장('기존 직접 운영에서 민간 위탁으로 변경 검토 보고\r\n\r\n\r\n')
        self.글자크기(10)
        self.글자색(0, 0, 0)
        self.문장('너는 세종특별자치시의 직원으로 #작성내용에 대한 전문적인 지식을 지닌 전문가이며, 보고서 작성의 전문가이다. 위에 입력한 내용과 #기초자료를 기본 자료로 사용하여 #작성 규칙을 바탕으로 #출력 서식을 참고하여 문서를 작성하라. 문서의 최소 작성분량이 3페이지가 넘지 않도록 작성하라.\r\n\r\n# 작성 규칙\r\n‘#출력 서식’에 맞추어 작성\r\n2. 콜론(:)을 포함한 앞의 내용은 사용자가 설정한 마크다운 기호로 반드시 변경 없이 그대로 활용\r\n  (제목:, 소제목:, 네모:, 일시장소:, 참석대상: 등)\r\n3. 모든 내용은 개조식, 간결체로 작성\r\n4. 문장 preferred_endings: "필요" "추진" "강화" "확보" "개선" "운영" "적용 "검토" "예정" "완료" "준수" "관리" "반영" "구성" "지원" "확대" "연계" "정비" "수립" "도출" "제고" "감축" "방지" "가능" "불가" "권장" "제한" 등\r\n\r\n# 출력 서식\r\n제목: 검토 보고 제목\r\n요약: 검토한 원인에서 검토 타당성을 도출하는 문장으로 문서전체의 내용을 요약하여 작성\r\n소제목: 검토배경\r\n원: (배경) 검토 배경에 대해 명확한 문장을 두줄분량으로 엔터없이 작성\r\n원: (경과) 추진 경과 두줄분량으로 엔터없이 작성\r\n소제목: 현황 및 문제점\r\n원: (현황) 현황 두줄로 이어서 작성\r\n원: (원인 및 쟁점) 원인 및 쟁점 내용 두줄분량으로 엔터없이 작성\r\n원: (문제점) 문제점 내용 두줄분량으로 엔터없이 작성\r\n소제목: 검토의견\r\n원: (대책방향) 대책방향 두줄분량으로 엔터없이 작성\r\n원: (개선방안)\r\n바: 개선방안 내용\r\n바: 개선방안 내용\r\n바: 개선방안 내용\r\n원: (유사사례)\r\n바: 유사사례 내용\r\n바: 유사사례 내용\r\n원: (검토결과) 검토결과 내용 두줄분량으로 엔터없이 작성\r\n소제목: 향후 계획\r\n원: 향후계획 내용\r\n원: 향후계획 내용\r\n\r\n※ 각 기호는 보고서 구조를 의미하며, 해당 위치에 적절한 내용을 작성하라.\r\n※ 기호는 예시 구조일 뿐이며 반드시 모두 사용할 필요는 없다.\r\n※ 내용의 중요도와 논리 구조에 따라 필요한 기호만 선택적으로 사용하라.\r\n※ 동일한 기호를 여러 번 사용할 수 있으며, 일부 기호는 생략 가능하다.\r\n\r\n# 강조사항\r\n‘#작성 규칙’과 ‘#출력 서식’을 지켰는지 검토 후 답변 출력\r\n안내된 글자 수를 반드시 지켜서 작성\r\n보고서의 내용이 논리적이고 자연스럽도록 작성')

    if (lambda self, 번호, 내용: self.왼쪽정렬()self.문단위(15)self.표만들기([
5.3,
1,
194 - self.문단여백측정()], [
9])self.셀여백제로()self.표배경색(174, 18, 95)self.표테두리타입(0, 0, 0, 0)self.폰트('HY헤드라인M')self.진하게()self.글자크기(17)self.가운데정렬()self.글자색(255, 255, 255)self.문장(번호)self.표오른쪽(1)self.표테두리타입(0, 0, 0, 0)self.표너비줄이기(2)self.표오른쪽(1)self.표테두리타입(0, 1, 0, 0)self.표테두리색(174, 18, 95)self.폰트('HY헤드라인M')self.글자크기(17)self.문장(' ' + 내용)self.표나가기2()):
        
        def 세종소제목(self, 번호, 내용):
            self.왼쪽정렬()
            self.문단위(15)
            self.표만들기([
                5.3,
                1,
                194 - self.문단여백측정()], [
                9])
            self.셀여백제로()
            self.표배경색(174, 18, 95)
            self.표테두리타입(0, 0, 0, 0)
            self.폰트('HY헤드라인M')
            self.진하게()
            self.글자크기(17)
            self.가운데정렬()
            self.글자색(255, 255, 255)
            self.문장(번호)
            self.표오른쪽(1)
            self.표테두리타입(0, 0, 0, 0)
            self.표너비줄이기(2)
            self.표오른쪽(1)
            self.표테두리타입(0, 1, 0, 0)
            self.표테두리색(174, 18, 95)
            self.폰트('HY헤드라인M')
            self.글자크기(17)
            self.문장(' ' + 내용)
            self.표나가기2()

    if (lambda self, 내용: self.오른쪽정렬()self.표만들기([
199 - self.문단여백측정()], [
17])self.표테두리타입(3, 3, 3, 3)self.셀여백지정(3, 3, 2, 2)self.줄간격(150)self.폰트('맑은 고딕')self.글자크기(12)self.진하게()if len(내용) >= 1:
self.문장(내용[0] + '\r\n')else:
self.문장('[어진동] 제목입력\r\n')self.기본글자()self.표나가기2()):
        
        def 세종글상자(self, 내용):
            self.오른쪽정렬()
            self.표만들기([
                199 - self.문단여백측정()], [
                17])
            self.표테두리타입(3, 3, 3, 3)
            self.셀여백지정(3, 3, 2, 2)
            self.줄간격(150)
            self.폰트('맑은 고딕')
            self.글자크기(12)
            self.진하게()
            if len(내용) >= 1:
                self.문장(내용[0] + '\r\n')
            else:
                self.문장('[어진동] 제목입력\r\n')
            self.기본글자()
            self.표나가기2()

    if (lambda self, 제목, 이미지: self.표만들기([
205.5 - self.문단여백측정()], [
17])self.표테두리타입(0, 0, 0, 0)self.사진넣기배경(이미지[0])self.폰트('HY헤드라인M')self.글자크기(20)self.가운데정렬()self.문장(제목)self.표나가기2()):
        
        def 세종제목(self, 제목, 이미지):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                17])
            self.표테두리타입(0, 0, 0, 0)
            self.사진넣기배경(이미지[0])
            self.폰트('HY헤드라인M')
            self.글자크기(20)
            self.가운데정렬()
            self.문장(제목)
            self.표나가기2()

    if (lambda self, 내용: self.표만들기([
205.5 - self.문단여백측정()], [
15])self.표테두리타입(0, 0, 0, 0)self.표배경색(252, 245, 231)self.폰트('맑은 고딕')self.글자크기(14)self.셀여백지정(3, 3, 3, 3)self.글자간격(-10)self.줄간격(160)self.자간헌터(0)self.문장(내용)self.표나가기2()):
        
        def 세종요약(self, 내용):
            self.표만들기([
                205.5 - self.문단여백측정()], [
                15])
            self.표테두리타입(0, 0, 0, 0)
            self.표배경색(252, 245, 231)
            self.폰트('맑은 고딕')
            self.글자크기(14)
            self.셀여백지정(3, 3, 3, 3)
            self.글자간격(-10)
            self.줄간격(160)
            self.자간헌터(0)
            self.문장(내용)
            self.표나가기2()

    if (lambda self, 이미지: if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
            
            def 줄선택():
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)

            if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)if None('□ \\((.*?)\\) ', 텍스트):
passif None('□ \\((.*?)\\) ', 텍스트):
매치 = None('□ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('    - [가-힣\\s]+:', 텍스트):
passif None('    - [가-힣\\s]+:', 텍스트):
매치 = None('    - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)if None('□ \\((.*?)\\) ', 텍스트):
passif None('□ \\((.*?)\\) ', 텍스트):
매치 = None('□ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('    - [가-힣\\s]+:', 텍스트):
passif None('    - [가-힣\\s]+:', 텍스트):
매치 = None('    - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    
                    def 궁극자간(끝줄개수설정):
                        self.대상.MovePos(6)
                        시작줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.MovePos(7)
                        끝줄 = int(self.대상.KeyIndicator()[5])
                        self.대상.HAction.Run('Select')
                        self.대상.HAction.Run('MoveLineBegin')
                        끝줄개수 = len(self.블록스캔()[1])
                        self.캔슬()
                        if 끝줄개수 < 끝줄개수설정:
                            카운트 = 0
                            self.대상.MovePos(6)
                            위치 = self.대상.GetPosBySet()
                            self.대상.HAction.Run('Select')
                            self.대상.MovePos(7)
                            텍스트 = self.블록스캔()[1]
                            self.캔슬()
                            if None('□ ', 텍스트):
                                pass
                            if None('□ ', 텍스트):
                                매치 = None('□ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                if None('□ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None('□ \\((.*?)\\) ', 텍스트):
                                    매치 = None('□ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None(' ○ ', 텍스트):
                                pass
                            if None(' ○ ', 텍스트):
                                매치 = None(' ○ ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    pass
                                if None(' ○ \\((.*?)\\) ', 텍스트):
                                    매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('    - ', 텍스트):
                                pass
                            if None('    - ', 텍스트):
                                매치 = None('    - ', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                if None('    - [가-힣\\s]+:', 텍스트):
                                    pass
                                if None('    - [가-힣\\s]+:', 텍스트):
                                    매치 = None('    - [가-힣\\s]+:', 텍스트)
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                            elif None('   \\* ', 텍스트):
                                pass
                            if 끝줄 - 시작줄 >= 1:
                                임시끝줄 = 끝줄
                                if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                    카운트 += 1
                                    self.대상.HAction.Run('CharShapeSpacingDecrease')
                                    임시끝줄 = int(self.대상.KeyIndicator()[5])
                                    if 카운트 > 8:
                                        pass
                                    self.대상.HAction.Run('CharShapeWidthDecrease')
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        continue
                            self.캔슬()
                        return None

                if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                    
                    def 괄호찾아바꾸기(텍스트, 위치, 크기):
                        
                        def 괄호찾기(텍스트):
                            스택 = []
                            짝 = []
                            for i in enumerate(텍스트):
                                if ():
                                    if 문자 == '(':
                                        스택.append(i)
                                        continue
                                    if not 문자 == ')':
                                        continue
                                    if 스택:
                                        pass
                                    if not 스택:
                                        continue
                                짝.append([
                                    start,
                                    end + 1])
                            return 짝

                        if '(' in 텍스트:
                            if ')' in 텍스트:
                                for 짝 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                            return None
                        return None

                    if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            pass
                        if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                            for 요일 in None(텍스트):
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                self.글자크기(크기)
                                self.캔슬()
                            (텍스트,)
                        return None
):
                        
                        def 요일찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 요일찾기(텍스트):
                                짝 = []
                                패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                매치들 = None(패턴, 텍스트)
                                for None in :
                                    if None:
                                        continue
                                        return 매치,

                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None

                        if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                            
                            def 별찾아바꾸기(텍스트, 위치):
                                if '*' in 텍스트:
                                    for None in :
                                        if ():
                                            if not 별 == '*':
                                                continue
                                            continue
                                            for None in 별, i:
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                self.대상.HAction.Run('Select')
                                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                self.윗첨자()
                                                self.캔슬()
                                            return None
                                            return None
                                            

                            if (lambda : self.캔슬()self.대상.MovePos(10)):
                                
                                def 다음문단():
                                    self.캔슬()
                                    self.대상.MovePos(10)

        self.기본글자()
        self.글자간격(0)
        self.글자장평(100)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문단아래(0)
        self.줄간격(160)
        self.왼쪽정렬()
        self.자간헌터(0)
        텍스트 = self.블록스캔()[1]
        텍스트 = 텍스트.strip()
        텍스트 = None('\\s*:\\s*', ': ', 텍스트)
        텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
        텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
        텍스트 = None('\\(\\s*', '(', 텍스트)
        if self.방금처리 == '부여시간계획':
            if None('^시간계획', 텍스트):
                pass
            if not None('^시간계획', 텍스트):
                self.방금처리 = 0
        if self.방금처리 == '부여추진일정':
            if None('^추진일정', 텍스트):
                pass
            if not None('^추진일정', 텍스트):
                self.방금처리 = 0
        if None('^제목\\s*:\\s*', 텍스트):
            pass
        if not None('^제목\\s*:\\s*', 텍스트):
            if None('^제목\\s*', 텍스트):
                pass
            if None('^제목\\s*', 텍스트):
                텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                self.백스페이스()
                self.세종제목(텍스트.split(':', 1)[1].strip(), 이미지)
                self.백스페이스()
            elif None('^중제목\\s*:\\s*', 텍스트):
                pass
        if not None('^중제목\\s*:\\s*', 텍스트):
            if None('^중제목\\s*', 텍스트):
                pass
            if None('^중제목\\s*', 텍스트):
                텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                self.백스페이스()
                self.강원중제목(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^보고자\\s*:\\s*', 텍스트):
                pass
        if not None('^보고자\\s*:\\s*', 텍스트):
            if None('^보고자\\s*', 텍스트):
                pass
            if None('^보고자\\s*', 텍스트):
                텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                self.백스페이스()
                self.강원보고자(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^표지\\s*:\\s*', 텍스트):
                pass
        if not None('^표지\\s*:\\s*', 텍스트):
            if None('^표지\\s*', 텍스트):
                pass
            if None('^표지\\s*', 텍스트):
                텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.강원표지(분리텍스트, 이미지)
                        self.백스페이스()
                    elif None('^소제목\\s*:\\s*', 텍스트):
                        pass
        if not None('^소제목\\s*:\\s*', 텍스트):
            if None('^소제목\\s*', 텍스트):
                pass
            if None('^소제목\\s*', 텍스트):
                텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                self.백스페이스()
                self.소제목카운트 = self.소제목카운트 + 1
                if self.소제목카운트 > 12:
                    self.소제목카운트 = 1
                self.세종소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^요약\\s*:\\s*', 텍스트):
                pass
        if not None('^요약\\s*:\\s*', 텍스트):
            if None('^요약\\s*', 텍스트):
                pass
            if None('^요약\\s*', 텍스트):
                텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                self.백스페이스()
                self.세종요약(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^글상자\\s*:\\s*', 텍스트):
                pass
        if not None('^글상자\\s*:\\s*', 텍스트):
            if None('^글상자\\s*', 텍스트):
                pass
            if None('^글상자\\s*', 텍스트):
                텍스트 = None('^(글상자\\s*:|글상자)\\s*', '글상자:', 텍스트, count = 1)
                self.백스페이스()
                for None in :
                    if None:
                        continue
                        re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                        self.세종글상자(분리텍스트)
                        self.백스페이스()
                    elif None('^참고\\s*:\\s*', 텍스트):
                        pass
        if not None('^참고\\s*:\\s*', 텍스트):
            if None('^참고\\s*', 텍스트):
                pass
            if None('^참고\\s*', 텍스트):
                텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                self.백스페이스()
                self.세종참고(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif None('^붙임\\s*:\\s*', 텍스트):
                pass
        if not None('^붙임\\s*:\\s*', 텍스트):
            if None('^붙임\\s*', 텍스트):
                pass
            if None('^붙임\\s*', 텍스트):
                텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                self.백스페이스()
                self.세종붙임(텍스트.split(':', 1)[1].strip())
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                pass
        if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
            텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.폰트('HY헤드라인M')
            self.글자크기(16)
            self.문단위(15)
            self.내어쓰기(-24)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(5)
        elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            pass
        if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
            텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-29.1)
            self.문단위(3)
            self.문단아래(2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None(' ○ \\((.*?)\\)', 텍스트):
                pass
            if None(' ○ \\((.*?)\\)', 텍스트):
                매치 = None(' ○ \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.진하게()
                self.글자크기(15)
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('-', '바 ', '바:')):
            pass
        if 텍스트.startswith(('-', '바 ', '바:')):
            텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-27.4)
            self.문단아래(2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(텍스트, 위치, 13)
            None(텍스트, 위치)
            None(텍스트, 위치, 15)
            if None('  - \\((.*?)\\)', 텍스트):
                pass
            if None('  - \\((.*?)\\)', 텍스트):
                매치 = None('  - \\((.*?)\\)', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                self.글자크기(15)
                self.진하게()
                self.캔슬()
            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
            None(9)
        elif 텍스트.startswith(('․', '점 ', '점:')):
            pass
        if 텍스트.startswith(('․', '점 ', '점:')):
            텍스트 = None('^(․|점\\s*:|점)\\s*', '   ․', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.휴먼명조()
            self.글자크기(15)
            self.내어쓰기(-37.4)
            self.문단위(2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('*', '별 ', '별:')):
            pass
        if 텍스트.startswith(('*', '별 ', '별:')):
            텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(12)
            self.내어쓰기(-47.6)
            self.문단아래(2)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
            None(10)
        elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            pass
        if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
            텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
            self.문장(텍스트)
            None()
            self.중고딕()
            self.글자크기(12)
            self.내어쓰기(-45.4)
            self.캔슬()
            self.대상.MovePos(6)
            위치 = self.대상.GetPosBySet()
        None(10)
        None()
        return None
        
        
):
        
        def 세종궁극의정리(self, 이미지):
            if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                
                def 줄선택():
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)

                if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)if None('□ \\((.*?)\\) ', 텍스트):
passif None('□ \\((.*?)\\) ', 텍스트):
매치 = None('□ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('    - [가-힣\\s]+:', 텍스트):
passif None('    - [가-힣\\s]+:', 텍스트):
매치 = None('    - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('□ ', 텍스트):
passif None('□ ', 텍스트):
매치 = None('□ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)if None('□ \\((.*?)\\) ', 텍스트):
passif None('□ \\((.*?)\\) ', 텍스트):
매치 = None('□ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('    - ', 텍스트):
passif None('    - ', 텍스트):
매치 = None('    - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('    - [가-힣\\s]+:', 텍스트):
passif None('    - [가-힣\\s]+:', 텍스트):
매치 = None('    - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
                        
                        def 궁극자간(끝줄개수설정):
                            self.대상.MovePos(6)
                            시작줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.MovePos(7)
                            끝줄 = int(self.대상.KeyIndicator()[5])
                            self.대상.HAction.Run('Select')
                            self.대상.HAction.Run('MoveLineBegin')
                            끝줄개수 = len(self.블록스캔()[1])
                            self.캔슬()
                            if 끝줄개수 < 끝줄개수설정:
                                카운트 = 0
                                self.대상.MovePos(6)
                                위치 = self.대상.GetPosBySet()
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)
                                텍스트 = self.블록스캔()[1]
                                self.캔슬()
                                if None('□ ', 텍스트):
                                    pass
                                if None('□ ', 텍스트):
                                    매치 = None('□ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                    if None('□ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None('□ \\((.*?)\\) ', 텍스트):
                                        매치 = None('□ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None(' ○ ', 텍스트):
                                    pass
                                if None(' ○ ', 텍스트):
                                    매치 = None(' ○ ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        pass
                                    if None(' ○ \\((.*?)\\) ', 텍스트):
                                        매치 = None(' ○ \\((.*?)\\) ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('    - ', 텍스트):
                                    pass
                                if None('    - ', 텍스트):
                                    매치 = None('    - ', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                                    if None('    - [가-힣\\s]+:', 텍스트):
                                        pass
                                    if None('    - [가-힣\\s]+:', 텍스트):
                                        매치 = None('    - [가-힣\\s]+:', 텍스트)
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                                    self.대상.HAction.Run('Select')
                                    self.대상.MovePos(7)
                                elif None('   \\* ', 텍스트):
                                    pass
                                if 끝줄 - 시작줄 >= 1:
                                    임시끝줄 = 끝줄
                                    if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                        카운트 += 1
                                        self.대상.HAction.Run('CharShapeSpacingDecrease')
                                        임시끝줄 = int(self.대상.KeyIndicator()[5])
                                        if 카운트 > 8:
                                            pass
                                        self.대상.HAction.Run('CharShapeWidthDecrease')
                                        if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
                                            continue
                                self.캔슬()
                            return None

                    if (lambda 텍스트, 위치, 크기: 
def 괄호찾기(텍스트):
스택 = []짝 = []for i in enumerate(텍스트):
if ():
if 문자 == '(':
스택.append(i)continueif not 문자 == ')':
continueif 스택:
passif not 스택:
continue짝.append([
start,
end + 1])짝if '(' in 텍스트:
if ')' in 텍스트:
for 짝 in None(텍스트):
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))self.글자크기(크기)self.캔슬()NoneNone):
                        
                        def 괄호찾아바꾸기(텍스트, 위치, 크기):
                            
                            def 괄호찾기(텍스트):
                                스택 = []
                                짝 = []
                                for i in enumerate(텍스트):
                                    if ():
                                        if 문자 == '(':
                                            스택.append(i)
                                            continue
                                        if not 문자 == ')':
                                            continue
                                        if 스택:
                                            pass
                                        if not 스택:
                                            continue
                                    짝.append([
                                        start,
                                        end + 1])
                                return 짝

                            if '(' in 텍스트:
                                if ')' in 텍스트:
                                    for 짝 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                return None
                            return None

                        if (lambda 텍스트, 위치, 크기: 
def 요일찾기(텍스트):
짝 = []패턴 = '\\((월|화|수|목|금|토|일)\\)'매치들 = None(패턴, 텍스트)for None in :
if None:
continue매치,if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                pass
                            if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                for 요일 in None(텍스트):
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                    self.대상.HAction.Run('Select')
                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                    self.글자크기(크기)
                                    self.캔슬()
                                (텍스트,)
                            return None
):
                            
                            def 요일찾아바꾸기(텍스트, 위치, 크기):
                                
                                def 요일찾기(텍스트):
                                    짝 = []
                                    패턴 = '\\((월|화|수|목|금|토|일)\\)'
                                    매치들 = None(패턴, 텍스트)
                                    for None in :
                                        if None:
                                            continue
                                            return 매치,

                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    pass
                                if (lambda .0: if None:
passfor None in .0:
if None:
if None in 텍스트:
passcontinueNone)(('(월)', '(화)', '(수)', '(목)', '(금)', '(토)', '(일)')()):
                                    for 요일 in None(텍스트):
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[0]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 요일[1]))
                                        self.글자크기(크기)
                                        self.캔슬()
                                    (텍스트,)
                                return None

                            if (lambda 텍스트, 위치: if '*' in 텍스트:
for None in :
if ():
if not 별 == '*':
continuecontinuefor None in 별, i:
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))self.윗첨자()self.캔슬()NoneNone):
                                
                                def 별찾아바꾸기(텍스트, 위치):
                                    if '*' in 텍스트:
                                        for None in :
                                            if ():
                                                if not 별 == '*':
                                                    continue
                                                continue
                                                for None in 별, i:
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별))
                                                    self.대상.HAction.Run('Select')
                                                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 별 + 1))
                                                    self.윗첨자()
                                                    self.캔슬()
                                                return None
                                                return None
                                                

                                if (lambda : self.캔슬()self.대상.MovePos(10)):
                                    
                                    def 다음문단():
                                        self.캔슬()
                                        self.대상.MovePos(10)

            self.기본글자()
            self.글자간격(0)
            self.글자장평(100)
            self.문단여백(0, 0)
            self.문단위(0)
            self.문단아래(0)
            self.줄간격(160)
            self.왼쪽정렬()
            self.자간헌터(0)
            텍스트 = self.블록스캔()[1]
            텍스트 = 텍스트.strip()
            텍스트 = None('\\s*:\\s*', ': ', 텍스트)
            텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
            텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
            텍스트 = None('\\(\\s*', '(', 텍스트)
            if self.방금처리 == '부여시간계획':
                if None('^시간계획', 텍스트):
                    pass
                if not None('^시간계획', 텍스트):
                    self.방금처리 = 0
            if self.방금처리 == '부여추진일정':
                if None('^추진일정', 텍스트):
                    pass
                if not None('^추진일정', 텍스트):
                    self.방금처리 = 0
            if None('^제목\\s*:\\s*', 텍스트):
                pass
            if not None('^제목\\s*:\\s*', 텍스트):
                if None('^제목\\s*', 텍스트):
                    pass
                if None('^제목\\s*', 텍스트):
                    텍스트 = None('^(제목\\s*:|제목)\\s*', '제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.세종제목(텍스트.split(':', 1)[1].strip(), 이미지)
                    self.백스페이스()
                elif None('^중제목\\s*:\\s*', 텍스트):
                    pass
            if not None('^중제목\\s*:\\s*', 텍스트):
                if None('^중제목\\s*', 텍스트):
                    pass
                if None('^중제목\\s*', 텍스트):
                    텍스트 = None('^(중제목\\s*:|중제목)\\s*', '중제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원중제목(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^보고자\\s*:\\s*', 텍스트):
                    pass
            if not None('^보고자\\s*:\\s*', 텍스트):
                if None('^보고자\\s*', 텍스트):
                    pass
                if None('^보고자\\s*', 텍스트):
                    텍스트 = None('^(보고자\\s*:|보고자)\\s*', '보고자:', 텍스트, count = 1)
                    self.백스페이스()
                    self.강원보고자(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^표지\\s*:\\s*', 텍스트):
                    pass
            if not None('^표지\\s*:\\s*', 텍스트):
                if None('^표지\\s*', 텍스트):
                    pass
                if None('^표지\\s*', 텍스트):
                    텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.강원표지(분리텍스트, 이미지)
                            self.백스페이스()
                        elif None('^소제목\\s*:\\s*', 텍스트):
                            pass
            if not None('^소제목\\s*:\\s*', 텍스트):
                if None('^소제목\\s*', 텍스트):
                    pass
                if None('^소제목\\s*', 텍스트):
                    텍스트 = None('^(소제목\\s*:|소제목)\\s*', '소제목:', 텍스트, count = 1)
                    self.백스페이스()
                    self.소제목카운트 = self.소제목카운트 + 1
                    if self.소제목카운트 > 12:
                        self.소제목카운트 = 1
                    self.세종소제목(self.로마숫자[self.소제목카운트], 텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^요약\\s*:\\s*', 텍스트):
                    pass
            if not None('^요약\\s*:\\s*', 텍스트):
                if None('^요약\\s*', 텍스트):
                    pass
                if None('^요약\\s*', 텍스트):
                    텍스트 = None('^(요약\\s*:|요약)\\s*', '요약:', 텍스트, count = 1)
                    self.백스페이스()
                    self.세종요약(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^글상자\\s*:\\s*', 텍스트):
                    pass
            if not None('^글상자\\s*:\\s*', 텍스트):
                if None('^글상자\\s*', 텍스트):
                    pass
                if None('^글상자\\s*', 텍스트):
                    텍스트 = None('^(글상자\\s*:|글상자)\\s*', '글상자:', 텍스트, count = 1)
                    self.백스페이스()
                    for None in :
                        if None:
                            continue
                            re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                            self.세종글상자(분리텍스트)
                            self.백스페이스()
                        elif None('^참고\\s*:\\s*', 텍스트):
                            pass
            if not None('^참고\\s*:\\s*', 텍스트):
                if None('^참고\\s*', 텍스트):
                    pass
                if None('^참고\\s*', 텍스트):
                    텍스트 = None('^(참고\\s*:|참고)\\s*', '참고:', 텍스트, count = 1)
                    self.백스페이스()
                    self.세종참고(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif None('^붙임\\s*:\\s*', 텍스트):
                    pass
            if not None('^붙임\\s*:\\s*', 텍스트):
                if None('^붙임\\s*', 텍스트):
                    pass
                if None('^붙임\\s*', 텍스트):
                    텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
                    self.백스페이스()
                    self.세종붙임(텍스트.split(':', 1)[1].strip())
                    self.백스페이스()
                elif 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                    pass
            if 텍스트.startswith(('ㅁ', '□', '네모 ', '', '네모:')):
                텍스트 = None('^(ㅁ|□||네모\\s*:|네모|)\\s*', '□ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.폰트('HY헤드라인M')
                self.글자크기(16)
                self.문단위(15)
                self.내어쓰기(-24)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(5)
            elif 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                pass
            if 텍스트.startswith(('ㅇ', '○', '❍', '', '◦', '원 ', '원:')):
                텍스트 = None('^(ㅇ|○|❍||◦|원\\s*:|원)\\s*', ' ○ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-29.1)
                self.문단위(3)
                self.문단아래(2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None(' ○ \\((.*?)\\)', 텍스트):
                    pass
                if None(' ○ \\((.*?)\\)', 텍스트):
                    매치 = None(' ○ \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.진하게()
                    self.글자크기(15)
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('-', '바 ', '바:')):
                pass
            if 텍스트.startswith(('-', '바 ', '바:')):
                텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-27.4)
                self.문단아래(2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(텍스트, 위치, 13)
                None(텍스트, 위치)
                None(텍스트, 위치, 15)
                if None('  - \\((.*?)\\)', 텍스트):
                    pass
                if None('  - \\((.*?)\\)', 텍스트):
                    매치 = None('  - \\((.*?)\\)', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
                    self.대상.HAction.Run('Select')
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.글자크기(15)
                    self.진하게()
                    self.캔슬()
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                None(9)
            elif 텍스트.startswith(('․', '점 ', '점:')):
                pass
            if 텍스트.startswith(('․', '점 ', '점:')):
                텍스트 = None('^(․|점\\s*:|점)\\s*', '   ․', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.휴먼명조()
                self.글자크기(15)
                self.내어쓰기(-37.4)
                self.문단위(2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('*', '별 ', '별:')):
                pass
            if 텍스트.startswith(('*', '별 ', '별:')):
                텍스트 = None('^(\\*|별\\s*:|별)\\s*', '    * ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(12)
                self.내어쓰기(-47.6)
                self.문단아래(2)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
                None(10)
            elif 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                pass
            if 텍스트.startswith(('※', '당구장 ', '당구 ', '당구장:', '당구:')):
                텍스트 = None('^(※|당구장\\s*:|당구\\s*:|당구장|당구)\\s*', '      ※ ', 텍스트, count = 1)
                self.문장(텍스트)
                None()
                self.중고딕()
                self.글자크기(12)
                self.내어쓰기(-45.4)
                self.캔슬()
                self.대상.MovePos(6)
                위치 = self.대상.GetPosBySet()
            None(10)
            None()
            return None
            
            

    if (lambda self, 이미지: self.소제목카운트 = 0self.중제목카운트 = 0self.위치저장 = 0self.방금처리 = 0self.궁극의정리위치보정 = 0시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.세종궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0지금위치 = 아까위치임시보정값 = 0if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치 and 임시보정값 == 0:
passNoneself.세종궁극의정리(이미지)마지막위치 = 마지막위치 + self.궁극의정리위치보정self.궁극의정리위치보정 = 0임시보정값 = 0if self.방금처리 == '부여시간계획':
pass임시보정값 = 1if self.방금처리 == '부여추진일정':
pass임시보정값 = 1if 지금위치 >= 마지막위치 + 임시보정값:
self.방금처리 = 0None아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 세종궁극의정리범위(self, 이미지):
            self.소제목카운트 = 0
            self.중제목카운트 = 0
            self.위치저장 = 0
            self.방금처리 = 0
            self.궁극의정리위치보정 = 0
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.세종궁극의정리(이미지)
                마지막위치 = 마지막위치 + self.궁극의정리위치보정
                self.궁극의정리위치보정 = 0
                지금위치 = 아까위치
                임시보정값 = 0
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치 and 임시보정값 == 0:
                        pass
                    return None
                    self.세종궁극의정리(이미지)
                    마지막위치 = 마지막위치 + self.궁극의정리위치보정
                    self.궁극의정리위치보정 = 0
                    임시보정값 = 0
                    if self.방금처리 == '부여시간계획':
                        pass
                    임시보정값 = 1
                    if self.방금처리 == '부여추진일정':
                        pass
                    임시보정값 = 1
                    if 지금위치 >= 마지막위치 + 임시보정값:
                        self.방금처리 = 0
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 특수문자, 이미지: 시작지점 = self.블록첫위치()끝지점 = self.블록끝위치()if 시작지점.Item('Para') != None:
self.캔슬()self.대상.SetPosBySet(끝지점)마지막위치 = self.대상.GetPosBySet().Item('Para')self.대상.SetPosBySet(시작지점)아까위치 = self.대상.GetPosBySet().Item('Para')self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.세종궁극의정리(이미지)지금위치 = 아까위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
지금위치 = self.대상.GetPosBySet().Item('Para')if 지금위치 == 아까위치:
passNoneself.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])self.세종궁극의정리(이미지)if 지금위치 >= 마지막위치:
passNone아까위치 = 지금위치if 시작지점.Item('Para') != 끝지점.Item('Para'):
continueNoneNone):
        
        def 세종궁극의정리범위글머리(self, 특수문자, 이미지):
            시작지점 = self.블록첫위치()
            끝지점 = self.블록끝위치()
            if 시작지점.Item('Para') != None:
                self.캔슬()
                self.대상.SetPosBySet(끝지점)
                마지막위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.SetPosBySet(시작지점)
                아까위치 = self.대상.GetPosBySet().Item('Para')
                self.대상.MovePos(6)
                self.대상.HAction.Run('Select')
                self.대상.MovePos(7)
                텍스트 = self.블록스캔()[1]
                한글찾기 = None('[(가-힣0-9a-zA-Z“(]+')
                self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                self.세종궁극의정리(이미지)
                지금위치 = 아까위치
                if 시작지점.Item('Para') != 끝지점.Item('Para'):
                    지금위치 = self.대상.GetPosBySet().Item('Para')
                    if 지금위치 == 아까위치:
                        pass
                    return None
                    self.대상.MovePos(6)
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                    텍스트 = self.블록스캔()[1]
                    한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
                    self.문장(특수문자 + ' ' + 텍스트[한글찾기.search(텍스트).start():len(텍스트)])
                    self.세종궁극의정리(이미지)
                    if 지금위치 >= 마지막위치:
                        pass
                    return None
                    아까위치 = 지금위치
                    if 시작지점.Item('Para') != 끝지점.Item('Para'):
                        continue
                return None
            return None

    if (lambda self, 이미지: 데이터리스트 = []if self.대상.CellShape:
passif self.대상.CellShape:
self.캔슬()self.표전체()마지막위치 = self.대상.GetPosBySet()self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()self.대상.MovePos(201)처음위치 = self.대상.GetPosBySet()self.대상.ReleaseScan()for i in range(처음위치.Item('List'), 마지막위치.Item('List') + 1):
self.대상.SetPosBySet(self.셀위치(i))결과텍스트 = ''self.대상.InitScan(0, 85)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = 결과텍스트 + 텍스트if 블록스캔값 == 0 or 블록스캔값 == 1:
pass데이터리스트.append(결과텍스트.strip())self.대상.ReleaseScan()for None in :
if None:
continueNone, range(0, len(데이터리스트), 5), 분할리스트, i = Nonefor None in :
if None:
if not None[1].strip() != '':
continuecontinueNone, 분할리스트, 분할리스트, 줄 = Nonefor None in :
if None:
continueNone, 분할리스트, 분할리스트, 줄 = None피피티 = EnsureDispatch('PowerPoint.Application')피피티.Visible = True프레젠테이션 = 피피티.Presentations.Add()슬라이드 = 프레젠테이션.Slides.Add(1, 1)프레젠테이션.PageSetup.SlideWidth = 720프레젠테이션.PageSetup.SlideHeight = 540for 객체 in list(슬라이드.Shapes):
객체.Delete()if (lambda 포인트, 색상, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()색상 = 도형포인트.ConvertToShape()도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색if 색상 == 16777215:
도형모양.Fill.Visible = False도형모양):
                                        if (lambda 포인트, 색상, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()색상 = 도형포인트.ConvertToShape()도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색if 색상 == 16777215:
도형모양.Fill.Visible = False도형모양):
                                            
                                            def 도형(포인트, 색상, 굵기, 테두리색):
                                                도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])
                                                for None in 포인트[1:]:
                                                    if ():
                                                        continue
                                                        ()
                                                        색상 = 도형포인트.ConvertToShape()
                                                        도형모양.Line.Weight = 굵기
                                                도형모양.Line.ForeColor.RGB = 테두리색
                                                if 색상 == 16777215:
                                                    도형모양.Fill.Visible = False
                                                return 도형모양

                                    if (lambda 포인트, 색상1, 색상2, 색상3, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()True = 도형포인트.ConvertToShape()도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3도형모양.Fill.GradientStops.Insert(색상2, 0.49)도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색도형모양):
                                        if (lambda 포인트, 색상1, 색상2, 색상3, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()True = 도형포인트.ConvertToShape()도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3도형모양.Fill.GradientStops.Insert(색상2, 0.49)도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색도형모양):
                                            
                                            def 도형그라데이션(포인트, 색상1, 색상2, 색상3, 굵기, 테두리색):
                                                도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])
                                                for None in 포인트[1:]:
                                                    if ():
                                                        continue
                                                        ()
                                                        True = 도형포인트.ConvertToShape()
                                                        도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)
                                                도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1
                                                도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3
                                                도형모양.Fill.GradientStops.Insert(색상2, 0.49)
                                                도형모양.Line.Weight = 굵기
                                                도형모양.Line.ForeColor.RGB = 테두리색
                                                return 도형모양

                                        if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                            if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                
                                                def 글자(X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드):
                                                    글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)
                                                    글자박스.TextFrame.TextRange.Text = 텍스트
                                                    글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트
                                                    글자박스.TextFrame.TextRange.Font.Name = 폰트
                                                    글자박스.TextFrame.TextRange.Font.Size = 글자크기
                                                    글자박스.TextFrame.TextRange.Font.Bold = 볼드
                                                    글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러
                                                    글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬
                                                    return 글자박스

                                            if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame2.TextRange.Font.Fill.Visible = True글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame2.TextRange.Font.Fill.Visible = True글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                    
                                                    def 글자그라데이션(X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드):
                                                        글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)
                                                        글자박스.TextFrame.TextRange.Text = 텍스트
                                                        글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트
                                                        글자박스.TextFrame.TextRange.Font.Name = 폰트
                                                        글자박스.TextFrame.TextRange.Font.Size = 글자크기
                                                        글자박스.TextFrame.TextRange.Font.Bold = 볼드
                                                        글자박스.TextFrame2.TextRange.Font.Fill.Visible = True
                                                        글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)
                                                        글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248
                                                        글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868
                                                        글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬
                                                        return 글자박스

            for 순번 in range(1, len(분할리스트)):
                if 순번 != 1:
                    슬라이드 = 프레젠테이션.Slides.Add(순번, 1)
                    for 객체 in list(슬라이드.Shapes):
                        객체.Delete()
                (0, 0, 100, 22, '기본', 12, '궁서체', 5, 0, True)
                배경선 = None([
                    (338, 92),
                    (593, 92),
                    (593, 259),
                    (338, 259),
                    (338, 92)], 16777215, 1, 0)
                if len(분할리스트[순번][2]) <= 3:
                    pass
                elif len(분할리스트[순번][2]) == 4:
                    pass
                elif len(분할리스트[순번][2]) == 5:
                    pass
                
                이름크기 = 40
                이름 = None(340, 178 - 이름크기, 250, 90, 분할리스트[순번][2], 이름크기, 'HY견고딕', 2, 0, 1)
                배경선2 = None([
                    (363, 200),
                    (567, 200)], 16777215, 1, 13998939)
                소속 = None(340, 206, 250, 90, 분할리스트[순번][0], 24, '나눔고딕 ExtraBold', 2, 0, 1)
                배경선3 = None([
                    (338, 320),
                    (655, 320),
                    (655, 524),
                    (338, 524),
                    (338, 320)], 16777215, 1, 0)
                로고1 = 슬라이드.Shapes.AddPicture(FileName = 이미지[0], LinkToFile = False, SaveWithDocument = True, Left = 339, Top = 320, Width = 317, Height = 23)
                로고2 = 슬라이드.Shapes.AddPicture(FileName = 이미지[1], LinkToFile = False, SaveWithDocument = True, Left = 433, Top = 491, Width = 127, Height = 17.5)
                if len(분할리스트[순번][2]) <= 3:
                    pass
                elif len(분할리스트[순번][2]) == 4:
                    pass
                elif len(분할리스트[순번][2]) == 5:
                    pass
                
                이름크기2 = 36
                이름2 = None(335, 442 - 이름크기2, 200, 90, 분할리스트[순번][2], 이름크기2, 'HY견고딕', 2, 0, 1)
                if len(분할리스트[순번][1]) <= 2:
                    pass
                elif len(분할리스트[순번][1]) == 3:
                    pass
                elif len(분할리스트[순번][1]) == 4:
                    pass
                
                이름크기3 = 18
                이름3 = None(535, 414 - 이름크기3 / 2, 110, 90, 분할리스트[순번][1], 이름크기3, 'HY견고딕', 2, 0, 1)
                로고3 = 슬라이드.Shapes.AddPicture(FileName = 이미지[2], LinkToFile = False, SaveWithDocument = True, Left = 31, Top = 194, Width = 247, Height = 186)
                배경선4 = None([
                    (31, 194),
                    (278, 194),
                    (278, 524),
                    (31, 524),
                    (31, 194)], 16777215, 1, 0)
                로고4 = 슬라이드.Shapes.AddPicture(FileName = 이미지[1], LinkToFile = False, SaveWithDocument = True, Left = 91, Top = 491, Width = 127, Height = 17.5)
                if len(분할리스트[순번][2]) <= 3:
                    pass
                elif len(분할리스트[순번][2]) == 4:
                    pass
                elif len(분할리스트[순번][2]) == 5:
                    pass
                
                이름크기4 = 32
                이름4 = None(31, 423, 247, 90, 분할리스트[순번][2], 이름크기4, '넥슨Lv2고딕 Bold', 2, 16279883, 1)
                이름5 = None(31, 400, 247, 90, 분할리스트[순번][0], 14, '넥슨Lv2고딕 Bold', 2, 16279883, 1)
            글자
        return None
        return None
        
        
        
):
        
        def 인국공명찰(self, 이미지):
            데이터리스트 = []
            if self.대상.CellShape:
                pass
            if self.대상.CellShape:
                self.캔슬()
                self.표전체()
                마지막위치 = self.대상.GetPosBySet()
                self.대상.InitScan(1, 255)
                블록스캔 = self.대상.GetText()
                self.대상.MovePos(201)
                처음위치 = self.대상.GetPosBySet()
                self.대상.ReleaseScan()
                for i in range(처음위치.Item('List'), 마지막위치.Item('List') + 1):
                    self.대상.SetPosBySet(self.셀위치(i))
                    결과텍스트 = ''
                    self.대상.InitScan(0, 85)
                    블록스캔 = self.대상.GetText()
                    블록스캔값 = 블록스캔[0]
                    텍스트 = 블록스캔[1]
                    결과텍스트 = 결과텍스트 + 텍스트
                    if 블록스캔값 == 0 or 블록스캔값 == 1:
                        pass
                    
                    데이터리스트.append(결과텍스트.strip())
                    self.대상.ReleaseScan()
                for None in :
                    if None:
                        continue
                        None, range(0, len(데이터리스트), 5), 분할리스트, i = None
                        for None in :
                            if None:
                                if not None[1].strip() != '':
                                    continue
                                continue
                                None, 분할리스트, 분할리스트, 줄 = None
                                for None in :
                                    if None:
                                        continue
                                        None, 분할리스트, 분할리스트, 줄 = None
                                        피피티 = EnsureDispatch('PowerPoint.Application')
                                        피피티.Visible = True
                                        프레젠테이션 = 피피티.Presentations.Add()
                                        슬라이드 = 프레젠테이션.Slides.Add(1, 1)
                                        프레젠테이션.PageSetup.SlideWidth = 720
                                        프레젠테이션.PageSetup.SlideHeight = 540
                                        for 객체 in list(슬라이드.Shapes):
                                            객체.Delete()
                                        if (lambda 포인트, 색상, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()색상 = 도형포인트.ConvertToShape()도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색if 색상 == 16777215:
도형모양.Fill.Visible = False도형모양):
                                            if (lambda 포인트, 색상, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()색상 = 도형포인트.ConvertToShape()도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색if 색상 == 16777215:
도형모양.Fill.Visible = False도형모양):
                                                
                                                def 도형(포인트, 색상, 굵기, 테두리색):
                                                    도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])
                                                    for None in 포인트[1:]:
                                                        if ():
                                                            continue
                                                            ()
                                                            색상 = 도형포인트.ConvertToShape()
                                                            도형모양.Line.Weight = 굵기
                                                    도형모양.Line.ForeColor.RGB = 테두리색
                                                    if 색상 == 16777215:
                                                        도형모양.Fill.Visible = False
                                                    return 도형모양

                                        if (lambda 포인트, 색상1, 색상2, 색상3, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()True = 도형포인트.ConvertToShape()도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3도형모양.Fill.GradientStops.Insert(색상2, 0.49)도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색도형모양):
                                            if (lambda 포인트, 색상1, 색상2, 색상3, 굵기, 테두리색: 도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])for None in 포인트[1:]:
if ():
continue()True = 도형포인트.ConvertToShape()도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3도형모양.Fill.GradientStops.Insert(색상2, 0.49)도형모양.Line.Weight = 굵기도형모양.Line.ForeColor.RGB = 테두리색도형모양):
                                                
                                                def 도형그라데이션(포인트, 색상1, 색상2, 색상3, 굵기, 테두리색):
                                                    도형포인트 = 슬라이드.Shapes.BuildFreeform(EditingType = 1, X1 = 포인트[0][0], Y1 = 포인트[0][1])
                                                    for None in 포인트[1:]:
                                                        if ():
                                                            continue
                                                            ()
                                                            True = 도형포인트.ConvertToShape()
                                                            도형모양.Fill.TwoColorGradient(Style = 2, Variant = 1)
                                                    도형모양.Fill.GradientStops.Item(1).Color.RGB = 색상1
                                                    도형모양.Fill.GradientStops.Item(2).Color.RGB = 색상3
                                                    도형모양.Fill.GradientStops.Insert(색상2, 0.49)
                                                    도형모양.Line.Weight = 굵기
                                                    도형모양.Line.ForeColor.RGB = 테두리색
                                                    return 도형모양

                                            if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                    
                                                    def 글자(X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드):
                                                        글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)
                                                        글자박스.TextFrame.TextRange.Text = 텍스트
                                                        글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트
                                                        글자박스.TextFrame.TextRange.Font.Name = 폰트
                                                        글자박스.TextFrame.TextRange.Font.Size = 글자크기
                                                        글자박스.TextFrame.TextRange.Font.Bold = 볼드
                                                        글자박스.TextFrame.TextRange.Font.Color.RGB = 컬러
                                                        글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬
                                                        return 글자박스

                                                if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame2.TextRange.Font.Fill.Visible = True글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                    if (lambda X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드: 글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)글자박스.TextFrame.TextRange.Text = 텍스트글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트글자박스.TextFrame.TextRange.Font.Name = 폰트글자박스.TextFrame.TextRange.Font.Size = 글자크기글자박스.TextFrame.TextRange.Font.Bold = 볼드글자박스.TextFrame2.TextRange.Font.Fill.Visible = True글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬글자박스):
                                                        
                                                        def 글자그라데이션(X축, Y축, 너비, 높이, 텍스트, 글자크기, 폰트, 정렬, 컬러, 볼드):
                                                            글자박스 = 슬라이드.Shapes.AddTextbox(Orientation = 1, Left = X축, Top = Y축, Width = 너비, Height = 높이)
                                                            글자박스.TextFrame.TextRange.Text = 텍스트
                                                            글자박스.TextFrame.TextRange.Font.NameFarEast = 폰트
                                                            글자박스.TextFrame.TextRange.Font.Name = 폰트
                                                            글자박스.TextFrame.TextRange.Font.Size = 글자크기
                                                            글자박스.TextFrame.TextRange.Font.Bold = 볼드
                                                            글자박스.TextFrame2.TextRange.Font.Fill.Visible = True
                                                            글자박스.TextFrame2.TextRange.Font.Fill.TwoColorGradient(Style = 2, Variant = 1)
                                                            글자박스.TextFrame2.TextRange.Font.Fill.ForeColor.RGB = 10453248
                                                            글자박스.TextFrame2.TextRange.Font.Fill.BackColor.RGB = 7619868
                                                            글자박스.TextFrame.TextRange.ParagraphFormat.Alignment = 정렬
                                                            return 글자박스

                for 순번 in range(1, len(분할리스트)):
                    if 순번 != 1:
                        슬라이드 = 프레젠테이션.Slides.Add(순번, 1)
                        for 객체 in list(슬라이드.Shapes):
                            객체.Delete()
                    (0, 0, 100, 22, '기본', 12, '궁서체', 5, 0, True)
                    배경선 = None([
                        (338, 92),
                        (593, 92),
                        (593, 259),
                        (338, 259),
                        (338, 92)], 16777215, 1, 0)
                    if len(분할리스트[순번][2]) <= 3:
                        pass
                    elif len(분할리스트[순번][2]) == 4:
                        pass
                    elif len(분할리스트[순번][2]) == 5:
                        pass
                    
                    이름크기 = 40
                    이름 = None(340, 178 - 이름크기, 250, 90, 분할리스트[순번][2], 이름크기, 'HY견고딕', 2, 0, 1)
                    배경선2 = None([
                        (363, 200),
                        (567, 200)], 16777215, 1, 13998939)
                    소속 = None(340, 206, 250, 90, 분할리스트[순번][0], 24, '나눔고딕 ExtraBold', 2, 0, 1)
                    배경선3 = None([
                        (338, 320),
                        (655, 320),
                        (655, 524),
                        (338, 524),
                        (338, 320)], 16777215, 1, 0)
                    로고1 = 슬라이드.Shapes.AddPicture(FileName = 이미지[0], LinkToFile = False, SaveWithDocument = True, Left = 339, Top = 320, Width = 317, Height = 23)
                    로고2 = 슬라이드.Shapes.AddPicture(FileName = 이미지[1], LinkToFile = False, SaveWithDocument = True, Left = 433, Top = 491, Width = 127, Height = 17.5)
                    if len(분할리스트[순번][2]) <= 3:
                        pass
                    elif len(분할리스트[순번][2]) == 4:
                        pass
                    elif len(분할리스트[순번][2]) == 5:
                        pass
                    
                    이름크기2 = 36
                    이름2 = None(335, 442 - 이름크기2, 200, 90, 분할리스트[순번][2], 이름크기2, 'HY견고딕', 2, 0, 1)
                    if len(분할리스트[순번][1]) <= 2:
                        pass
                    elif len(분할리스트[순번][1]) == 3:
                        pass
                    elif len(분할리스트[순번][1]) == 4:
                        pass
                    
                    이름크기3 = 18
                    이름3 = None(535, 414 - 이름크기3 / 2, 110, 90, 분할리스트[순번][1], 이름크기3, 'HY견고딕', 2, 0, 1)
                    로고3 = 슬라이드.Shapes.AddPicture(FileName = 이미지[2], LinkToFile = False, SaveWithDocument = True, Left = 31, Top = 194, Width = 247, Height = 186)
                    배경선4 = None([
                        (31, 194),
                        (278, 194),
                        (278, 524),
                        (31, 524),
                        (31, 194)], 16777215, 1, 0)
                    로고4 = 슬라이드.Shapes.AddPicture(FileName = 이미지[1], LinkToFile = False, SaveWithDocument = True, Left = 91, Top = 491, Width = 127, Height = 17.5)
                    if len(분할리스트[순번][2]) <= 3:
                        pass
                    elif len(분할리스트[순번][2]) == 4:
                        pass
                    elif len(분할리스트[순번][2]) == 5:
                        pass
                    
                    이름크기4 = 32
                    이름4 = None(31, 423, 247, 90, 분할리스트[순번][2], 이름크기4, '넥슨Lv2고딕 Bold', 2, 16279883, 1)
                    이름5 = None(31, 400, 247, 90, 분할리스트[순번][0], 14, '넥슨Lv2고딕 Bold', 2, 16279883, 1)
                글자
            return None
            return None
            
            
            

    __static_attributes__ = ('\xea\xb6\x81\xea\xb7\xb9\xec\x9d\x98\xec\xa0\x95\xeb\xa6\xac\xec\x9c\x84\xec\xb9\x98\xeb\xb3\xb4\xec\xa0\x95', '\xeb\x84\xa4\xeb\xaa\xa8\xec\x88\xab\xec\x9e\x90\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8', '\xeb\xb0\xa9\xea\xb8\x88\xec\xb2\x98\xeb\xa6\xac', '\xeb\xb6\x99\xec\x9e\x84\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8', '\xec\x86\x8c\xec\xa0\x9c\xeb\xaa\xa9\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8', '\xec\x9c\x84\xec\xb9\x98\xec\xa0\x80\xec\x9e\xa5', '\xec\xa4\x91\xec\xa0\x9c\xeb\xaa\xa9\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8', '\xec\xb0\xb8\xea\xb3\xa0\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8', '\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8\xec\xb9\xb4\xec\x9a\xb4\xed\x8a\xb8')

한컴2 = None(한컴2, '\xed\x95\x9c\xec\xbb\xb42', 한컴기본)
