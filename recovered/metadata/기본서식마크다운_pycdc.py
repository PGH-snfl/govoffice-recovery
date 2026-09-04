# Source Generated with Decompyle++
# File: �⺻���ĸ�ũ�ٿ�.marshal (Python 3.13)


def 콜론처리(배열):
    결과 = []
    for 아이템 in 배열:
        if ':' not in 아이템:
            결과.append('엔터:엔터')
            continue
        결과.append(아이템)
    return 결과


def 엔터처리(배열):
    결과 = []
    for 아이템 in 배열:
        if 아이템 == [
            '']:
            결과.append([
                '엔터',
                '엔터'])
            continue
        결과.append(아이템)
    return 결과


def 키워드처리(배열):
    for None in :
        if None:
            for None in :
                if None:
                    pass
            continue
            , [], None
            return 아이템, 내부배열
        


def 특수문자제거(배열):
    패턴 = None('[^가-힣0-9\\s]')
    for None in :
        if None:
            continue
            return 아이템,


def 배열공백제거(배열):
    for None in :
        if None:
            for None in :
                if None:
                    continue
                    continue
                    None, None, 배열, , [], None
                    return 아이템, 내부배열
                

if (lambda : 블록내용 = self.블록텍스트()줄나누기 = 블록내용.split('\r\n')줄나누기 = None(줄나누기)for None in :
if None:
continue콜론처리, 줄나누기, 콜론나누기, s = None특수문자제거(키워드처리(엔터처리(None(콜론나누기))))):
    
    def 마크다운읽기():
        블록내용 = self.블록텍스트()
        줄나누기 = 블록내용.split('\r\n')
        줄나누기 = None(줄나누기)
        for None in :
            if None:
                continue
                콜론처리, 줄나누기, 콜론나누기, s = None
        return 특수문자제거(키워드처리(엔터처리(None(콜론나누기))))
        

    배열 = None()
self.대상.HAction.Run('Delete')
참고카운트 = 0
소제목카운트 = 0
소제목로마카운트 = 0
표진입 = 0
시간계획표진입 = 0
심사기준표진입 = 0
표개수 = 0
로마숫자 = [
    '',
    'Ⅰ',
    'Ⅱ',
    'Ⅲ',
    'Ⅳ',
    'Ⅴ',
    'Ⅵ',
    'Ⅶ',
    'Ⅷ',
    'Ⅸ',
    'Ⅹ',
    'Ⅺ',
    'Ⅻ']
self.대상.SetMessageBoxMode(16)
self.글자스타일(0)
self.대상.SetMessageBoxMode(240)
for 아이템 in 배열:
    if 아이템[0] != '표' and 표진입 == 1:
        self.대상.MovePos(105)
        self.대상.MovePos(107)
        self.대상.MovePos(23)
        self.표나가기()
    표진입 = 0
    if 아이템[0] != '시간계획표' and 시간계획표진입 == 1:
        self.대상.MovePos(105)
        self.대상.MovePos(107)
        self.대상.MovePos(23)
        self.표나가기()
    시간계획표진입 = 0
    if 아이템[0] != '심사기준표' and 심사기준표진입 == 1:
        self.대상.MovePos(105)
        self.대상.MovePos(107)
        self.대상.MovePos(23)
        self.표나가기()
    심사기준표진입 = 0
    if 아이템[0] == '소제목' and 아이템[0] == '숫자소제목' or 아이템[0] == '소제목숫자':
        소제목카운트 = 소제목카운트 + 1
    self.소제목(str(소제목카운트), ' ' + 아이템[1], 4 + 6.2 * len(아이템[1]) - 2.9 * 아이템[1].count(' '))
    if 아이템[0] == '소제목로마' or 아이템[0] == '로마소제목':
        소제목로마카운트 = 소제목로마카운트 + 1
        if 소제목로마카운트 >= 12:
            pass
        소제목로마카운트 = 12
    self.소제목(로마숫자[소제목로마카운트], ' ' + 아이템[1], 4 + 6.2 * len(아이템[1]) - 2.9 * 아이템[1].count(' '))
    if 아이템[0] == '제목':
        pass
    self.기본서식제목(아이템[1])
    if 아이템[0] == '참고':
        참고카운트 = 참고카운트 + 1
        self.다음페이지()
    self.기본서식참고(str(참고카운트), 아이템[1])
    if 아이템[0] == '상단박스' and 아이템[0] == '서론' or 아이템[0] == '배경':
        pass
    self.상단박스(아이템[1])
    if 아이템[0] == '동그라미' or 아이템[0] == '원':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-30)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.문장(' ○ ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] in ('원1', '원2', '원3', '원4', '원5', '원6', '원7', '원8', '원9', '원10'):
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-23.2)
        self.글자간격(0)
        self.기본정렬()
        self.기본글자()
        self.진하게()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        
        def 임시변환기(텍스트):
            for i in range(1, 11):
                텍스트 = 텍스트.replace(f'''원{i}''', chr(9311 + i))
            return 텍스트

        임시변환기(None(아이템[0]) + ' ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] in ('기간', '구성', '내용', '대상', '목적', '방식', '방법', '일시', '일정', '주체', '장소', '참석'):
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-72.7)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.진하게()
        self.문장(' ○ ' + 아이템[0])
        if 아이템[1] != '':
            self.문장(': ')
            self.기본글자()
            self.글자간격(-8)
        self.문장(아이템[1])
    self.엔터(1)
    if 아이템[0] in ('심사기준', '심사 기준', '심사방법', '심사 방법', '심사항목', '심사 항목', '시상규모', '시상 규모', '신청절차', '신청 절차', '응모자격', '응모 자격', '응모분야', '응모 분야', '주요내용', '조사대상', '조사내용', '조사기간', '제출방법', '제출 방법', '참석대상', '평가항목', '활동기간', '활동내용', '활동방법'):
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-30)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.진하게()
        self.문장(' ○ ' + 아이템[0][:2] + 아이템[0][-2:])
        if 아이템[1] != '':
            self.문장(': ')
            self.기본글자()
            self.글자간격(-8)
        self.문장(아이템[1])
    self.엔터(1)
    if 아이템[0] == '심사위원명단' or 아이템[0] == '심사위원 명단':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-30)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.진하게()
        self.문장(' ○ 심사위원 명단:')
        self.기본글자()
        self.문장(' ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] == '일시방식':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-30)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.진하게()
        self.문장(' ○ 일시/방식:')
        self.기본글자()
        self.글자간격(-8)
        self.문장(' ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] == '일시장소':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-30)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(3)
        self.진하게()
        self.문장(' ○ 일시/장소:')
        self.기본글자()
        self.글자간격(-8)
        self.문장(' ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] == '바':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-34.9)
        self.글자간격(0)
        self.기본정렬()
        self.휴먼명조()
        self.글자크기(15)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(5)
        self.문장('   - ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] == '네모' or 아이템[0] == '사각형':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(0)
        self.글자간격(0)
        self.진하게()
        self.기본정렬()
        self.폰트('맑은 고딕')
        self.글자크기(16)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(10)
        self.문장('□ ' + 아이템[1])
    self.엔터(1)
    if 아이템[0] == '당구' or 아이템[0] == '당구장':
        self.기본글자()
        self.자간헌터(0)
        self.내어쓰기(-39.6)
        self.글자간격(0)
        self.기본정렬()
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문장('    ※ ' + 아이템[1])
    self.대상.HAction.Run('BreakPara')
    if 아이템[0] == '주석' and 아이템[0] == '주석1' or 아이템[0] == '별':
        self.대상.HAction.Run('CharShapeNormal')
        self.자간헌터(0)
        self.내어쓰기(-41.1)
        self.글자간격(0)
        self.대상.HAction.Run('ParagraphShapeAlignJustify')
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문장('     * ' + 아이템[1])
    self.대상.HAction.Run('BreakPara')
    if 아이템[0] == '주석2':
        self.대상.HAction.Run('CharShapeNormal')
        self.자간헌터(0)
        self.내어쓰기(-41.1)
        self.글자간격(0)
        self.대상.HAction.Run('ParagraphShapeAlignJustify')
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)
        self.문단위(0)
        self.문장('    ** ' + 아이템[1])
    self.대상.HAction.Run('BreakPara')
    if 아이템[0] == '엔터':
        pass
    self.대상.HAction.Run('BreakPara')
    if 아이템[0] == '표' and 표진입 == 1:
        if 아이템[1]:
            pass
        if 아이템[1]:
            표배열 = None(':', 아이템[1])
            if len(표배열) < 표개수:
                pass
            표배열 += [
                ''] * (표개수 - len(표배열))
            self.표오른쪽(1)
            for None in range(표개수):
                i = None
                if not i != 표개수 - 1:
                    continue
                self.표오른쪽(1)
    self.문장
    if 아이템[0] == '시간계획표' and 시간계획표진입 == 1:
        if 아이템[1]:
            pass
        if 아이템[1]:
            시간계획표배열 = None(':', 아이템[1])
            if len(시간계획표배열) < 7:
                pass
            시간계획표배열 += [
                ''] * (7 - len(시간계획표배열))
            self.표오른쪽(1)
            self.문장(시간계획표배열[0].strip())
            self.문장(':')
            self.문장(시간계획표배열[1].strip())
            self.문장('~')
            self.문장(시간계획표배열[2].strip())
            self.문장(':')
            self.문장(시간계획표배열[3].strip())
            self.표오른쪽(1)
            self.문장(시간계획표배열[4].strip())
            self.표오른쪽(1)
            self.기본정렬()
            self.기본글자()
            self.진하게()
            self.내어쓰기(-9.3)
            self.문장('· ' + 시간계획표배열[5].strip())
            self.표오른쪽(1)
            self.셀한줄(1)
    self.문장(시간계획표배열[6].strip())
    if 아이템[0] == '심사기준표' and 심사기준표진입 == 1:
        if 아이템[1]:
            pass
        if 아이템[1]:
            심사기준표배열 = None(':', 아이템[1])
            if len(심사기준표배열) < 4:
                pass
            심사기준표배열 += [
                ''] * (4 - len(심사기준표배열))
            self.표오른쪽(1)
            self.문장(심사기준표배열[0].strip())
            self.표오른쪽(1)
            self.기본글자()
            self.문장('• ' + 심사기준표배열[1].strip())
            self.엔터(1)
            self.문장('• ' + 심사기준표배열[2].strip())
            self.표오른쪽(1)
            self.가운데정렬()
    self.문장(심사기준표배열[3].strip())
    if 아이템[0] == '심사기준표' and 심사기준표진입 == 0:
        if 아이템[1]:
            pass
        if 아이템[1]:
            심사기준표진입 = 1
            심사기준표배열 = None(':', 아이템[1])
            if len(심사기준표배열) < 3:
                pass
            심사기준표배열 += [
                ''] * (3 - len(심사기준표배열))
            self.표만들기([
                28,
                120,
                10], [
                5,
                10,
                10])
            self.표전체()
            self.폰트('맑은 고딕')
            self.글자크기(11)
            self.표내부선타입(3, 3)
            self.표테두리굵기(6, 6, 0, 0)
            self.표테두리타입(1, 1, 0, 0)
            self.진하게()
            self.줄간격(110)
            self.캔슬()
            self.표처음()
            self.가운데정렬()
            self.문장('구분')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.가운데정렬()
            self.문장('주요 내용')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.가운데정렬()
            self.문장('배점')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.문장(심사기준표배열[0].strip())
            self.표오른쪽(1)
            self.기본글자()
            self.문장('• ' + 심사기준표배열[1].strip())
            self.엔터(1)
            self.문장('• ' + 심사기준표배열[2].strip())
            self.표오른쪽(1)
            self.가운데정렬()
    self.문장(심사기준표배열[3].strip())
    if 아이템[0] == '시간계획표' and 시간계획표진입 == 0:
        if 아이템[1]:
            pass
        if 아이템[1]:
            시간계획표진입 = 1
            시간계획표배열 = None(':', 아이템[1])
            if len(시간계획표배열) < 7:
                pass
            시간계획표배열 += [
                ''] * (7 - len(시간계획표배열))
            self.표만들기([
                27,
                10,
                88,
                29], [
                11,
                9,
                9])
            self.표전체()
            self.폰트('맑은 고딕')
            self.글자크기(13)
            self.가운데정렬()
            self.표내부선타입(3, 3)
            self.표테두리굵기(6, 6, 0, 0)
            self.표테두리타입(1, 1, 0, 0)
            self.캔슬()
            self.표처음()
            self.셀선택()
            self.표오른쪽(1)
            self.셀병합()
            self.진하게()
            self.문장('시 간')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.기본글자()
            self.진하게()
            self.문장('주요 내용')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.진하게()
            self.문장('비 고')
            self.표배경색(223, 230, 247)
            self.표단일선('하', 6, 8)
            self.표오른쪽(1)
            self.문장(시간계획표배열[0].strip())
            self.문장(':')
            self.문장(시간계획표배열[1].strip())
            self.문장('~')
            self.문장(시간계획표배열[2].strip())
            self.문장(':')
            self.문장(시간계획표배열[3].strip())
            self.표오른쪽(1)
            self.문장(시간계획표배열[4].strip())
            self.표오른쪽(1)
            self.기본정렬()
            self.기본글자()
            self.진하게()
            self.내어쓰기(-9.3)
            self.문장('· ' + 시간계획표배열[5].strip())
            self.표오른쪽(1)
            self.셀한줄(1)
    self.문장(시간계획표배열[6].strip())
    if not 아이템[0] == '표':
        continue
    if not 표진입 == 0:
        continue
    if 아이템[1]:
        pass
    if not 아이템[1]:
        continue
    표진입 = 1
    표배열 = None(':', 아이템[1])
    표개수 = len(표배열)
    기본길이 = 207 - 표개수 * 3.5
    if 기본길이 < 100:
        pass
    기본길이 = 100
    if 표개수 == 1:
        pass
    기본길이 = 130
    if 표개수 == 2:
        pass
    기본길이 = 150
    if 표개수 == 3:
        pass
    기본길이 = 170
    전체길이 = 기본길이 - self.문단여백측정()
    표넓이 = [
        2] * 표개수
    for 일단계단어들 in range(표개수):
        i = None
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(일단계단어들()):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(일단계단어들()):
            표넓이[i] = 표넓이[i] - 1
        이단계단어들 = [
            '주민번호']
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(이단계단어들()):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(이단계단어들()):
            표넓이[i] = 2
        사단계단어들 = [
            '주소',
            '내용',
            '사항',
            '세부']
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass):
            pass
        if (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(사단계단어들()):
            pass
        if not (lambda .0: if None:
passfor None in .0:
if None:
passif None in 표배열[i].replace(' ', ''):
pass)(사단계단어들()):
            continue
        표넓이[i] = 표넓이[i] + 2
    any
    표넓이합 = sum(표넓이)
    for None in range(표개수):
        i = None
        표넓이[i] = (표넓이[i] / 표넓이합) * 전체길이
    (i, 표배열)
    self.대상.HAction.Run('ParagraphShapeAlignCenter')
    self.표만들기(표넓이, [
        7.4,
        7.4])
    self.대상.HAction.Run('TableCellBlock')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.글자크기(12)
    self.폰트('맑은 고딕')
    self.표테두리굵기(6, 6, 6, 6)
    self.대상.HAction.Run('ParagraphShapeAlignCenter')
    self.대상.HAction.Run('Cancel')
    self.대상.MovePos(106)
    self.대상.MovePos(104)
    for None in range(표개수):
        i = None
        self.표배경색(223, 230, 247)
        self.문장(표배열[i].strip())
        if not i != 표개수 - 1:
            continue
        self.표오른쪽(1)
any
