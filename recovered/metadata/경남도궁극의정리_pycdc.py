# Source Generated with Decompyle++
# File: �泲���ñ�������.marshal (Python 3.13)

if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  ', 텍스트):
passif None('  ', 텍스트):
매치 = None('  ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('[가-힣\\s]+:', 텍스트):
passif None('[가-힣\\s]+:', 텍스트):
매치 = None('[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))elif None('  \\((.*?)\\) ', 텍스트):
passif None('  \\((.*?)\\) ', 텍스트):
매치 = None('  \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('-[가-힣\\s]+:', 텍스트):
passif None('-[가-힣\\s]+:', 텍스트):
매치 = None('-[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   · ', 텍스트):
passif None('   · ', 텍스트):
매치 = None('   · ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('·[가-힣\\s]+:', 텍스트):
passif None('·[가-힣\\s]+:', 텍스트):
매치 = None('·[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('※[가-힣\\s]+:', 텍스트):
passif None('※[가-힣\\s]+:', 텍스트):
매치 = None('※[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
passif 끝줄 - 시작줄 >= 1:
임시끝줄 = 끝줄if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
카운트 += 1self.대상.HAction.Run('CharShapeSpacingDecrease')임시끝줄 = int(self.대상.KeyIndicator()[5])if 카운트 > 8:
passself.대상.HAction.Run('CharShapeWidthDecrease')if 끝줄 - 임시끝줄 == 0 and 카운트 < 15:
continueself.캔슬()None):
    if (lambda 끝줄개수설정: self.대상.MovePos(6)시작줄 = int(self.대상.KeyIndicator()[5])self.대상.MovePos(7)끝줄 = int(self.대상.KeyIndicator()[5])self.대상.HAction.Run('Select')self.대상.HAction.Run('MoveLineBegin')끝줄개수 = len(self.블록스캔()[1])self.캔슬()if 끝줄개수 < 끝줄개수설정:
카운트 = 0self.대상.MovePos(6)위치 = self.대상.GetPosBySet()self.대상.HAction.Run('Select')self.대상.MovePos(7)텍스트 = self.블록스캔()[1]self.캔슬()if None('  ', 텍스트):
passif None('  ', 텍스트):
매치 = None('  ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('[가-힣\\s]+:', 텍스트):
passif None('[가-힣\\s]+:', 텍스트):
매치 = None('[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))elif None('  \\((.*?)\\) ', 텍스트):
passif None('  \\((.*?)\\) ', 텍스트):
매치 = None('  \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('-[가-힣\\s]+:', 텍스트):
passif None('-[가-힣\\s]+:', 텍스트):
매치 = None('-[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   · ', 텍스트):
passif None('   · ', 텍스트):
매치 = None('   · ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('·[가-힣\\s]+:', 텍스트):
passif None('·[가-힣\\s]+:', 텍스트):
매치 = None('·[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     ※ ', 텍스트):
passif None('     ※ ', 텍스트):
매치 = None('     ※ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('※[가-힣\\s]+:', 텍스트):
passif None('※[가-힣\\s]+:', 텍스트):
매치 = None('※[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('     \\* ', 텍스트):
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
                if None('  ', 텍스트):
                    pass
                if None('  ', 텍스트):
                    매치 = None('  ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    if None('[가-힣\\s]+:', 텍스트):
                        pass
                    if None('[가-힣\\s]+:', 텍스트):
                        매치 = None('[가-힣\\s]+:', 텍스트)
                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                    elif None('  \\((.*?)\\) ', 텍스트):
                        pass
                    if None('  \\((.*?)\\) ', 텍스트):
                        매치 = None('  \\((.*?)\\) ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                elif None('  - ', 텍스트):
                    pass
                if None('  - ', 텍스트):
                    매치 = None('  - ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    if None('-[가-힣\\s]+:', 텍스트):
                        pass
                    if None('-[가-힣\\s]+:', 텍스트):
                        매치 = None('-[가-힣\\s]+:', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                elif None('   · ', 텍스트):
                    pass
                if None('   · ', 텍스트):
                    매치 = None('   · ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    if None('·[가-힣\\s]+:', 텍스트):
                        pass
                    if None('·[가-힣\\s]+:', 텍스트):
                        매치 = None('·[가-힣\\s]+:', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                    self.대상.HAction.Run('Select')
                    self.대상.MovePos(7)
                elif None('     ※ ', 텍스트):
                    pass
                if None('     ※ ', 텍스트):
                    매치 = None('     ※ ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    if None('※[가-힣\\s]+:', 텍스트):
                        pass
                    if None('※[가-힣\\s]+:', 텍스트):
                        매치 = None('※[가-힣\\s]+:', 텍스트)
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

    if (lambda 텍스트, 위치, 종류: if re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트):
passif re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트):
매치 = re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.문장내어쓰기()None):
        
        def 콜론내어쓰기(텍스트, 위치, 종류):
            if re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트):
                pass
            if re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트):
                매치 = re.escape(f'''{None(종류)}[가-힣\\s]+:''', 텍스트)
                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                self.문장내어쓰기()
            return None

        if (lambda 텍스트, 위치: if None('  \\((.*?)\\) ', 텍스트):
passif None('  \\((.*?)\\) ', 텍스트):
매치 = None('  \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.문장내어쓰기()None):
            
            def 괄호내어쓰기(텍스트, 위치):
                if None('  \\((.*?)\\) ', 텍스트):
                    pass
                if None('  \\((.*?)\\) ', 텍스트):
                    매치 = None('  \\((.*?)\\) ', 텍스트)
                    self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                    self.문장내어쓰기()
                return None

            if (lambda 텍스트, 위치: 
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
self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0] + 9))self.대상.HAction.Run('Select')self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1] + 9))self.글자색(0, 0, 255)self.캔슬()NoneNone):
                
                def 괄호찾아파란색(텍스트, 위치):
                    
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
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[0] + 9))
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 짝[1] + 9))
                                self.글자색(0, 0, 255)
                                self.캔슬()
                        return None
                    return None

                if (lambda : self.대상.MovePos(6)self.대상.HAction.Run('Select')self.대상.MovePos(7)):
                    
                    def 줄선택():
                        self.대상.MovePos(6)
                        self.대상.HAction.Run('Select')
                        self.대상.MovePos(7)

                    if (lambda : self.캔슬()self.대상.MovePos(10)):
                        
                        def 다음문단():
                            self.캔슬()
                            self.대상.MovePos(10)

self.기본글자()
self.글자간격(0)
self.글자장평(100)
self.문단여백(0, 0)
self.문단아래(0)
self.줄간격(160)
self.자간헌터(0)
self.왼쪽정렬()
텍스트 = self.블록스캔()[1]
텍스트 = 텍스트.strip()
텍스트 = None('\\s*:\\s*', ' : ', 텍스트)
텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
텍스트 = None('\\s*\\)\\s*', ') ', 텍스트)
텍스트 = None('\\(\\s*', '(', 텍스트)
if None('^\\s*제목\\s*:\\s*', 텍스트):
    pass
if None('^\\s*제목\\s*:\\s*', 텍스트):
    self.백스페이스()
    self.경남도제목(텍스트.split(':', 1)[1].strip())
    self.백스페이스()
elif None('^\\s*진행순서표\\s*:\\s*', 텍스트):
    pass
if None('^\\s*진행순서표\\s*:\\s*', 텍스트):
    self.백스페이스()
    self.경남도진행순서표()
    self.백스페이스()
elif None('^\\s*기획제목\\s*:\\s*', 텍스트):
    pass
if None('^\\s*기획제목\\s*:\\s*', 텍스트):
    self.백스페이스()
    self.경남도기획제목()
    self.문장(텍스트.split(':', 1)[1].strip())
    None(6)
elif None('^\\s*소제목\\s*:\\s*', 텍스트):
    pass
if None('^\\s*소제목\\s*:\\s*', 텍스트):
    self.백스페이스()
    self.임시카운트 = self.임시카운트 + 1
    if self.임시카운트 == 10:
        self.임시카운트 = 1
    self.경남도소제목(self.로마숫자[self.임시카운트], 텍스트.split(':', 1)[1].strip())
    self.백스페이스()
elif None('^\\s*서론\\s*:\\s*', 텍스트):
    pass
if None('^\\s*서론\\s*:\\s*', 텍스트):
    self.백스페이스()
    self.경남도서론(' ' + 텍스트.split(':', 1)[1].strip())
    self.백스페이스()
elif 텍스트.startswith(('ㅁ', '□', '네모 ', '')):
    pass
if 텍스트.startswith(('ㅁ', '□', '네모 ', '')):
    텍스트 = None('^(ㅁ|□||네모)\\s*', '', 텍스트, count = 1)
    None()
    self.백스페이스()
    self.경남네모()
    self.문장(' ' + 텍스트)
    None()
    self.폰트('HY헤드라인M')
    self.글자크기(16)
    self.내어쓰기(-24.8)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(텍스트, 위치)
    None(4)
elif 텍스트.startswith(('ㅇ', '', '○', '원 ', '동그라미 ')):
    pass
if 텍스트.startswith(('ㅇ', '', '○', '원 ', '동그라미 ')):
    텍스트 = None('^(ㅇ||○|원|동그라미)\\s*', '  ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('휴먼명조')
    self.글자크기(15)
    self.내어쓰기(-29.2)
    self.문단위(5)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    if None('  \\((.*?)\\) ', 텍스트):
        pass
    if None('  \\((.*?)\\) ', 텍스트):
        매치 = None('  \\((.*?)\\) ', 텍스트)
        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.start() + 3))
        self.대상.HAction.Run('Select')
        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
        self.진하게()
        self.캔슬()
        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
    self.문장내어쓰기()
    None(텍스트, 위치, '')
    None(5)
elif 텍스트.startswith(('-', '바 ')):
    pass
if 텍스트.startswith(('-', '바 ')):
    텍스트 = None('^(-|바)\\s*', '  - ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('휴먼명조')
    self.기본글자()
    self.글자크기(15)
    self.내어쓰기(-42.4)
    self.문단위(5)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(텍스트, 위치, '-')
    None(5)
elif 텍스트.startswith(('\xc2\xb7', '점 ')):
    pass
if 텍스트.startswith(('\xc2\xb7', '점 ')):
    텍스트 = None('^[·점]\\s*', '   · ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('휴먼명조')
    self.기본글자()
    self.글자크기(15)
    self.내어쓰기(-34.9)
    self.문단위(5)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(텍스트, 위치, '\xc2\xb7')
    None(5)
elif 텍스트.startswith(('*', '별 ')):
    pass
if 텍스트.startswith(('*', '별 ')):
    텍스트 = None('^[\\*별]\\s*', '     * ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('맑은 고딕')
    self.글자크기(12)
    self.내어쓰기(-41.1)
    self.문단위(2)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(텍스트, 위치, '*')
    None()
elif 텍스트.startswith(('※', '당구 ', '당구장 ')):
    pass
None()
