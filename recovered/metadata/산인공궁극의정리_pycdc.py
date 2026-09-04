# Source Generated with Decompyle++
# File: ���ΰ��ñ�������.marshal (Python 3.13)

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
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ [가-힣\\s]+:', 텍스트):
passif None(' ○ [가-힣\\s]+:', 텍스트):
매치 = None('  ❍ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))elif None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  - [가-힣\\s]+:', 텍스트):
passif None('  - [가-힣\\s]+:', 텍스트):
매치 = None('  - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ※ ', 텍스트):
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
매치 = None('□ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None(' ○ ', 텍스트):
passif None(' ○ ', 텍스트):
매치 = None(' ○ ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None(' ○ [가-힣\\s]+:', 텍스트):
passif None(' ○ [가-힣\\s]+:', 텍스트):
매치 = None('  ❍ [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))elif None(' ○ \\((.*?)\\) ', 텍스트):
passif None(' ○ \\((.*?)\\) ', 텍스트):
매치 = None(' ○ \\((.*?)\\) ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  - ', 텍스트):
passif None('  - ', 텍스트):
매치 = None('  - ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('  - [가-힣\\s]+:', 텍스트):
passif None('  - [가-힣\\s]+:', 텍스트):
매치 = None('  - [가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('   \\* ', 텍스트):
passif None('   \\* ', 텍스트):
매치 = None('   \\* ', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))if None('\\*[가-힣\\s]+:', 텍스트):
passif None('\\*[가-힣\\s]+:', 텍스트):
매치 = None('\\*[가-힣\\s]+:', 텍스트)self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))self.대상.HAction.Run('Select')self.대상.MovePos(7)elif None('  ※ ', 텍스트):
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
                    elif None(' ○ ', 텍스트):
                        pass
                    if None(' ○ ', 텍스트):
                        매치 = None(' ○ ', 텍스트)
                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                        if None(' ○ [가-힣\\s]+:', 텍스트):
                            pass
                        if None(' ○ [가-힣\\s]+:', 텍스트):
                            매치 = None('  ❍ [가-힣\\s]+:', 텍스트)
                            self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                        elif None(' ○ \\((.*?)\\) ', 텍스트):
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
                        if None('  - [가-힣\\s]+:', 텍스트):
                            pass
                        if None('  - [가-힣\\s]+:', 텍스트):
                            매치 = None('  - [가-힣\\s]+:', 텍스트)
                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                        self.대상.HAction.Run('Select')
                        self.대상.MovePos(7)
                    elif None('   \\* ', 텍스트):
                        pass
                    if None('   \\* ', 텍스트):
                        매치 = None('   \\* ', 텍스트)
                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end()))
                        if None('\\*[가-힣\\s]+:', 텍스트):
                            pass
                        if None('\\*[가-힣\\s]+:', 텍스트):
                            매치 = None('\\*[가-힣\\s]+:', 텍스트)
                        self.대상.SetPosBySet(self.좌표(위치.Item('List'), 위치.Item('Para'), 위치.Item('Pos') + 매치.end() + 1))
                        self.대상.HAction.Run('Select')
                        self.대상.MovePos(7)
                    elif None('  ※ ', 텍스트):
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
self.자간헌터(1)
self.기본정렬()
텍스트 = self.블록스캔()[1]
텍스트 = 텍스트.strip()
텍스트 = None('\\s*:\\s*', ': ', 텍스트)
텍스트 = None('(?<=\\d)\\s*:\\s*(?=\\d)', ':', 텍스트)
텍스트 = None('\\s*·\\s*', '\xc2\xb7', 텍스트)
텍스트 = None('\\s*\\)\\s*', ') ', 텍스트)
텍스트 = None('\\(\\s*', '(', 텍스트)
if self.방금처리 == '산인공시간계획표':
    if None('^시간계획', 텍스트):
        pass
    if not None('^시간계획', 텍스트):
        self.방금처리 = 0
if self.방금처리 == '부여추진일정':
    if None('^추진일정', 텍스트):
        pass
    if not None('^추진일정', 텍스트):
        self.방금처리 = 0
if None('^표지제목\\s*:\\s*', 텍스트):
    pass
if not None('^표지제목\\s*:\\s*', 텍스트):
    if None('표지제목\\s*', 텍스트):
        pass
    if None('표지제목\\s*', 텍스트):
        텍스트 = None('^(표지제목\\s*:|표지제목)\\s*', '표지제목:', 텍스트, count = 1)
        self.백스페이스()
        self.부여표지제목(텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^제목\\s*:\\s*', 텍스트):
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
                self.산인공기본보고서제목(분리텍스트)
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
                re.sub, 텍스트.split(':')[1:][:3], 분리텍스트, x = re.match
                self.산인공표지마크다운(분리텍스트, 이미지)
                self.백스페이스()
            elif None('^목차\\s*:\\s*', 텍스트):
                pass
if not None('^목차\\s*:\\s*', 텍스트):
    if None('^목차\\s*', 텍스트):
        pass
    if None('^목차\\s*', 텍스트):
        텍스트 = None('^(목차\\s*:|목차)\\s*', '목차:', 텍스트, count = 1)
        self.백스페이스()
        self.산인공목차마크다운(이미지)
        self.백스페이스()
    elif None('^사진\\s*:\\s*', 텍스트):
        pass
if not None('^사진\\s*:\\s*', 텍스트):
    if None('^사진\\s*', 텍스트):
        pass
    if None('^사진\\s*', 텍스트):
        텍스트 = None('^(사진\\s*:|사진)\\s*', '사진:', 텍스트, count = 1)
        self.백스페이스()
        self.산인공사진2단마크다운()
        self.백스페이스()
    elif None('^구매표\\s*:\\s*', 텍스트):
        pass
if not None('^구매표\\s*:\\s*', 텍스트):
    if None('^구매표\\s*', 텍스트):
        pass
    if None('^구매표\\s*', 텍스트):
        텍스트 = None('^(구매표\\s*:|구매표)\\s*', '구매표:', 텍스트, count = 1)
        self.백스페이스()
        self.산인공구매표()
        self.백스페이스()
    elif None('^참석자명단\\s*:\\s*', 텍스트):
        pass
if not None('^참석자명단\\s*:\\s*', 텍스트):
    if None('^참석자명단\\s*', 텍스트):
        pass
    if not None('^참석자명단\\s*', 텍스트):
        if None('^참석자 명단\\s*:\\s*', 텍스트):
            pass
        if not None('^참석자 명단\\s*:\\s*', 텍스트):
            if None('^참석자 명단\\s*', 텍스트):
                pass
            if None('^참석자 명단\\s*', 텍스트):
                텍스트 = None('^(참석자명단\\s*:|참석자명단|참석자 명단\\s*:|참석자 명단)\\s*', '참석자명단:', 텍스트, count = 1)
                self.백스페이스()
                self.산인공참석자명단마크다운()
                self.백스페이스()
            elif None('^관리대장\\s*:\\s*', 텍스트):
                pass
if not None('^관리대장\\s*:\\s*', 텍스트):
    if None('^관리대장\\s*', 텍스트):
        pass
    if None('^관리대장\\s*', 텍스트):
        텍스트 = None('^(관리대장\\s*:|관리대장)\\s*', '관리대장:', 텍스트, count = 1)
        self.백스페이스()
        self.산인공관리대장()
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
        self.산인공약식보고서소제목(str(self.소제목카운트), ' ' + 텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^점선박스\\s*:\\s*', 텍스트):
        pass
if not None('^점선박스\\s*:\\s*', 텍스트):
    if None('^점선박스\\s*', 텍스트):
        pass
    if None('^점선박스\\s*', 텍스트):
        텍스트 = None('^(점선박스\\s*:|점선박스)\\s*', '점선박스:', 텍스트, count = 1)
        self.백스페이스()
        self.부여점선박스(텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^참고박스\\s*:\\s*', 텍스트):
        pass
if not None('^참고박스\\s*:\\s*', 텍스트):
    if None('^참고박스\\s*', 텍스트):
        pass
    if None('^참고박스\\s*', 텍스트):
        텍스트 = None('^(참고박스\\s*:|참고박스)\\s*', '참고박스:', 텍스트, count = 1)
        self.백스페이스()
        self.부여참고박스(텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^표지\\s*:\\s*', 텍스트):
        pass
if not None('^표지\\s*:\\s*', 텍스트):
    if None('^표지\\s*', 텍스트):
        pass
    if None('^표지\\s*', 텍스트):
        텍스트 = None('^(표지\\s*:|표지)\\s*', '표지:', 텍스트, count = 1)
        self.백스페이스()
        self.부여표지(텍스트.split(':', 1)[1].strip(), 이미지[0:3])
        self.백스페이스()
    elif None('^서론\\s*:\\s*', 텍스트):
        pass
if not None('^서론\\s*:\\s*', 텍스트):
    if None('^서론\\s*', 텍스트):
        pass
    if None('^서론\\s*', 텍스트):
        텍스트 = None('^(서론\\s*:|서론)\\s*', '서론:', 텍스트, count = 1)
        self.백스페이스()
        self.부여서론(텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^붙임\\s*:\\s*', 텍스트):
        pass
if not None('^붙임\\s*:\\s*', 텍스트):
    if None('^붙임\\s*', 텍스트):
        pass
    if None('^붙임\\s*', 텍스트):
        텍스트 = None('^(붙임\\s*:|붙임)\\s*', '붙임:', 텍스트, count = 1)
        self.백스페이스()
        self.부여붙임(텍스트.split(':', 1)[1].strip())
        self.백스페이스()
    elif None('^한줄일정\\s*:\\s*', 텍스트):
        pass
if not None('^한줄일정\\s*:\\s*', 텍스트):
    if None('^한줄일정\\s*', 텍스트):
        pass
    if None('^한줄일정\\s*', 텍스트):
        텍스트 = None('^(한줄일정\\s*:|한줄일정)\\s*', '한줄일정:', 텍스트, count = 1)
        self.백스페이스()
        for None in :
            if None:
                continue
                re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                self.부여한줄일정(분리텍스트)
                self.백스페이스()
            elif None('^시간계획표\\s*:\\s*', 텍스트):
                pass
if not None('^시간계획표\\s*:\\s*', 텍스트):
    if None('^시간계획표\\s*', 텍스트):
        pass
    if None('^시간계획표\\s*', 텍스트):
        텍스트 = None('^(시간계획표\\s*:|시간계획표)\\s*', '시간계획표:', 텍스트, count = 1)
        self.백스페이스()
        for None in :
            if None:
                continue
                re.split, None('[:~]', 텍스트)[1:], 분리텍스트, x = re.sub
                self.산인공시간계획표(분리텍스트)
                self.백스페이스()
            elif None('^추진일정\\s*:\\s*', 텍스트):
                pass
if not None('^추진일정\\s*:\\s*', 텍스트):
    if None('^추진일정\\s*', 텍스트):
        pass
    if None('^추진일정\\s*', 텍스트):
        텍스트 = None('^(추진일정\\s*:|추진일정)\\s*', '추진일정:', 텍스트, count = 1)
        self.백스페이스()
        for None in :
            if None:
                continue
                re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                self.부여추진일정(분리텍스트)
                self.백스페이스()
            elif None('^동향제목\\s*:\\s*', 텍스트):
                pass
if not None('^동향제목\\s*:\\s*', 텍스트):
    if None('^동향제목\\s*', 텍스트):
        pass
    if None('^동향제목\\s*', 텍스트):
        텍스트 = None('^(동향제목\\s*:|동향제목)\\s*', '동향제목:', 텍스트, count = 1)
        self.백스페이스()
        for None in :
            if None:
                continue
                re.sub, 텍스트.split(':')[1:], 분리텍스트, x = re.match
                self.부여동향제목(이미지[3], 분리텍스트)
                self.백스페이스()
            elif 텍스트.startswith(('ㅁ', '□', '네모 ', '네모:')):
                pass
if 텍스트.startswith(('ㅁ', '□', '네모 ', '네모:')):
    텍스트 = None('^(ㅁ|□|네모\\s*:|네모)\\s*', '', 텍스트, count = 1)
    self.문장('□ ' + 텍스트)
    None()
    self.휴먼명조()
    self.글자크기(15)
    self.내어쓰기(-22.5)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(4)
elif 텍스트.startswith(('', '입체네모 ', '입체네모:')):
    pass
if 텍스트.startswith(('', '입체네모 ', '입체네모:')):
    텍스트 = None('^(|입체네모\\s*:|입체네모)\\s*', '', 텍스트, count = 1)
    self.문장(' ' + 텍스트)
    None()
    self.휴먼명조()
    self.글자크기(15)
    self.내어쓰기(-22.5)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(4)
elif 텍스트.startswith(('ㅇ', '○', '원 ', '동그라미 ', '원:', '참석대상', '주요내용', '일시장소')):
    pass
if 텍스트.startswith(('ㅇ', '○', '원 ', '동그라미 ', '원:', '참석대상', '주요내용', '일시장소')):
    텍스트 = None('^(일시장소\\s*:|일시장소)\\s*', ' ○ (일시·장소) ', 텍스트, count = 1)
    텍스트 = None('^(참석대상\\s*:|참석대상)\\s*', ' ○ (참석 대상) ', 텍스트, count = 1)
    텍스트 = None('^(주요내용\\s*:|주요내용)\\s*', ' ○ (주요 내용) ', 텍스트, count = 1)
    텍스트 = None('^(ㅇ|○|원\\s*:|원|동그라미\\s*:|동그라미)\\s*', ' ○ ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.휴먼명조()
    self.글자크기(15)
    self.내어쓰기(-31.9)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
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
    None(5)
elif 텍스트.startswith(('', '입체원 ', '입체원:')):
    pass
if 텍스트.startswith(('', '입체원 ', '입체원:')):
    텍스트 = None('^(|입체원\\s*:|입체원)\\s*', '  ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.휴먼명조()
    self.글자크기(15)
    self.내어쓰기(-31.9)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(5)
elif 텍스트.startswith(('-', '바 ', '바:')):
    pass
if 텍스트.startswith(('-', '바 ', '바:')):
    텍스트 = None('^(-|바\\s*:|바)\\s*', '  - ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('휴먼명조')
    self.기본글자()
    self.글자크기(15)
    self.내어쓰기(-34.9)
    self.문단위(10)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None(5)
elif 텍스트.startswith(('*', '별 ', '별:')):
    pass
if 텍스트.startswith(('*', '별 ', '별:')):
    텍스트 = None('^(\\*|별\\s*:|별)\\s*', '   * ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('맑은 고딕')
    self.글자크기(12)
    self.내어쓰기(-29.4)
    self.문단위(5)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
    None()
elif 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
    pass
if 텍스트.startswith(('※', '당구 ', '당구장 ', '당구:', '당구장:')):
    텍스트 = None('^(※|당구장\\s*:|당구장|당구\\s*:|당구)\\s*', '  ※ ', 텍스트, count = 1)
    self.문장(텍스트)
    None()
    self.폰트('맑은 고딕')
    self.글자크기(12)
    self.내어쓰기(-27.6)
    self.문단위(0)
    self.캔슬()
    self.대상.MovePos(6)
    위치 = self.대상.GetPosBySet()
None()
None()
return None






