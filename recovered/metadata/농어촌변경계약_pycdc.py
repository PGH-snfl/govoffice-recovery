# Source Generated with Decompyle++
# File: ����̺�����.marshal (Python 3.13)

if (lambda : 총 = self.대상.CreateAction('ShapeObjDialog')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('TreatAsChar', 1)총.Execute(총알)):
    
    def 글자취급():
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)

self.대상.MovePos(3)
self.표만들기([
    1], [
    1])
None()
최종위치 = self.대상.GetPosBySet().Item('List')
self.대상.SetMessageBoxMode(16)
self.대상.HAction.Run('MoveRight')
self.대상.HAction.Run('DeleteBack')
self.대상.SetMessageBoxMode(240)
데이터리스트 = []
for i in range(3, int(최종위치)):
    self.대상.SetPosBySet(self.셀위치(i))
    self.대상.HAction.Run('Select')
    self.대상.HAction.Run('Select')
    self.대상.HAction.Run('Select')
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
    결과텍스트 = 결과텍스트.strip()
    데이터리스트.append(결과텍스트)
    self.문장(결과텍스트 + ' ')
(self,)
if (lambda 타겟: 인덱스 = 데이터리스트.index(타겟)if 인덱스 + 1 < len(데이터리스트):
pass데이터리스트[인덱스 + 1]):
    
    def 데이터(타겟):
        인덱스 = 데이터리스트.index(타겟)
        if 인덱스 + 1 < len(데이터리스트):
            pass
        return 데이터리스트[인덱스 + 1]

    if (lambda 타겟: 인덱스 = 데이터리스트.index(타겟)if 인덱스 + 2 < len(데이터리스트):
pass데이터리스트[인덱스 + 2]):
        
        def 데이터2(타겟):
            인덱스 = 데이터리스트.index(타겟)
            if 인덱스 + 2 < len(데이터리스트):
                pass
            return 데이터리스트[인덱스 + 2]

        if 데이터리스트[3] == '용역변경계약서(초안)':
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(13)
            self.신명조
            self.대상.HAction.Run('CharShapeBold')
            데이터(None('용    역    명') + ' 변경계약 체결')
            self.대상.HAction.Run('BreakPara')
            self.대상.HAction.Run('BreakPara')
            self.대상.HAction.Run('CharShaepeNormal')
            self.문장('1, 관 련: ')
            self.대상.HAction.Run('BreakPara')
            '2. '(데이터 + None('용    역    명') + ' 변경계약을 체결하겠습니다.')
            self.대상.HAction.Run('BreakPara')
            데이터 + None('상 호:') + ' ('(데이터 + None('사업자등록번호:') + ')')
            self.대상.HAction.Run('BreakPara')
            ' 나. 변경사유: '(데이터 + None('변경사유'))
            self.대상.HAction.Run('BreakPara')
            self.문장(' 다. 변경내역')
            self.대상.HAction.Run('BreakPara')
            self.표만들기([
                8,
                24,
                24,
                24,
                24,
                24,
                24], [
                5] * 4)
            self.대상.HAction.Run('TableCellBlock')
            self.대상.HAction.Run('TableCellBlockExtend')
            self.대상.HAction.Run('TableCellBlockExtend')
            self.글자크기(11)
            self.신명조()
            self.표테두리굵기(7, 7, 1, 1)
            self.표테두리타입(1, 1, 0, 0)
            self.대상.HAction.Run('ParagraphShapeAlignCenter')
            self.대상.HAction.Run('Cancel')
            self.대상.MovePos(106)
            self.대상.MovePos(104)
            self.대상.HAction.Run('TableCellBlock')
            self.대상.HAction.Run('TableCellBlockExtend')
            self.대상.MovePos(103)
            self.대상.HAction.Run('TableMergeCell')
            self.표배경색(223, 230, 247)
            self.문장('구분')
            self.표오른쪽(1)
            self.대상.HAction.Run('TableCellBlock')
            self.대상.HAction.Run('TableCellBlockExtend')
            self.표오른쪽(2)
            self.대상.HAction.Run('TableMergeCell')
            self.문장('계약금액')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.대상.HAction.Run('TableCellBlock')
            self.대상.HAction.Run('TableCellBlockExtend')
            self.표오른쪽(2)
            self.대상.HAction.Run('TableMergeCell')
            self.문장('계약기간')
            self.표배경색(223, 230, 247)
            self.표오른쪽(2)
            self.문장('당초')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('변경')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('증감')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('착공일')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('당초준공일')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('변경준공일')
            self.표배경색(223, 230, 247)
            self.표오른쪽(1)
            self.문장('총괄')
            self.표오른쪽(1)
            format(int(re.sub('[^0-9\\s]'('', 데이터, None('변경전계약금액'))), ','))
            self.표오른쪽(1)
            format(int(re.sub('[^0-9\\s]'('', 데이터, None('변경후계약금액'))), ','))
            self.표오른쪽(1)
            임시계산값 = int - re.sub('[^0-9\\s]'('', 데이터, None('변경전계약금액')))
            if 임시계산값 == 0:
                self.문장('변경없음')
            elif 임시계산값 < 0:
                self.문장('△' + format(abs(임시계산값), ','))
            else:
                self.문장(format(임시계산값, ','))
            self.표오른쪽(1)
            데이터(None('변경후착수일자').replace('년', '.').replace('월', '.').replace('일', '.'))
            self.표오른쪽(1)
            데이터(None('변경전총완수일자').replace('년', '.').replace('월', '.').replace('일', '.'))
            self.표오른쪽(1)
            self.표오른쪽(1)
            self.문장('금차')
            self.표오른쪽(1)
            format(int(re.sub('[^0-9\\s]'('', 데이터2, None('변경전계약금액'))), ','))
            self.표오른쪽(1)
            format(int(re.sub('[^0-9\\s]'('', 데이터2, None('변경후계약금액'))), ','))
            self.표오른쪽(1)
            임시계산값2 = int - re.sub('[^0-9\\s]'('', 데이터2, None('변경전계약금액')))
            if 임시계산값2 == 0:
                self.문장('변경없음')
            elif 임시계산값2 < 0:
                self.문장('△' + format(abs(임시계산값2), ','))
            else:
                self.문장(format(임시계산값2, ','))
            self.표오른쪽(1)
            데이터(None('변경후착수일자').replace('년', '.').replace('월', '.').replace('일', '.'))
            self.표오른쪽(1)
            데이터(None('변경전금차완수일자').replace('년', '.').replace('월', '.').replace('일', '.'))
            self.표오른쪽(1)
            self.대상.HAction.Run('MoveRight')
            self.대상.HAction.Run('BreakPara')
            self.대상.HAction.Run('ParagraphShapeAlignJustify')
            self.대상.HAction.Run('BreakPara')
            self.대상.HAction.Run('BreakPara')
            self.문장('붙임 :  1. 용역변경계약서(초안) 1부.')
            self.대상.HAction.Run('BreakPara')
self.문장('       2. 관련문서 각 1부.  끝.')
if 데이터리스트[3] == '공사변경계약서(초안)':
    self.새창()
    self.문서여백(20, 20, 15, 15, 10, 10)
    self.글자크기(13)
    self.신명조
    self.대상.HAction.Run('CharShapeBold')
    데이터(None('공    사    명') + ' 변경계약 체결')
    self.대상.HAction.Run('BreakPara')
    self.대상.HAction.Run('BreakPara')
    self.대상.HAction.Run('CharShaepeNormal')
    self.문장('1, 관 련: ')
    self.대상.HAction.Run('BreakPara')
    '2. '(데이터 + None('공    사    명') + ' 변경계약을 체결하겠습니다.')
    self.대상.HAction.Run('BreakPara')
    데이터 + None('상 호:') + ' ('(데이터 + None('사업자등록번호:') + ')')
    self.대상.HAction.Run('BreakPara')
    ' 나. 변경사유: '(데이터 + None('변경사유'))
    self.대상.HAction.Run('BreakPara')
    self.문장(' 다. 변경내역')
    self.대상.HAction.Run('BreakPara')
    self.표만들기([
        8,
        24,
        24,
        24,
        24,
        24,
        24], [
        5] * 4)
    self.대상.HAction.Run('TableCellBlock')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.글자크기(11)
    self.신명조()
    self.표테두리굵기(7, 7, 1, 1)
    self.표테두리타입(1, 1, 0, 0)
    self.대상.HAction.Run('ParagraphShapeAlignCenter')
    self.대상.HAction.Run('Cancel')
    self.대상.MovePos(106)
    self.대상.MovePos(104)
    self.대상.HAction.Run('TableCellBlock')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.대상.MovePos(103)
    self.대상.HAction.Run('TableMergeCell')
    self.표배경색(223, 230, 247)
    self.문장('구분')
    self.표오른쪽(1)
    self.대상.HAction.Run('TableCellBlock')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.표오른쪽(2)
    self.대상.HAction.Run('TableMergeCell')
    self.문장('계약금액')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.대상.HAction.Run('TableCellBlock')
    self.대상.HAction.Run('TableCellBlockExtend')
    self.표오른쪽(2)
    self.대상.HAction.Run('TableMergeCell')
    self.문장('계약기간')
    self.표배경색(223, 230, 247)
    self.표오른쪽(2)
    self.문장('당초')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('변경')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('증감')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('착공일')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('당초준공일')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('변경준공일')
    self.표배경색(223, 230, 247)
    self.표오른쪽(1)
    self.문장('총괄')
    self.표오른쪽(1)
    format(int(re.sub('[^0-9\\s]'('', 데이터, None('변경전계약금액'))), ','))
    self.표오른쪽(1)
    format(int(re.sub('[^0-9\\s]'('', 데이터, None('변경후계약금액'))), ','))
    self.표오른쪽(1)
    임시계산값 = int - re.sub('[^0-9\\s]'('', 데이터, None('변경전계약금액')))
    if 임시계산값 == 0:
        self.문장('변경없음')
    elif 임시계산값 < 0:
        self.문장('△' + format(abs(임시계산값), ','))
    else:
        self.문장(format(임시계산값, ','))
    self.표오른쪽(1)
    데이터(None('변경후착공일자').replace('년', '.').replace('월', '.').replace('일', '.'))
    self.표오른쪽(1)
    데이터(None('변경전총공사기한').replace('년', '.').replace('월', '.').replace('일', '.'))
    self.표오른쪽(1)
    self.표오른쪽(1)
    self.문장('금차')
    self.표오른쪽(1)
    format(int(re.sub('[^0-9\\s]'('', 데이터2, None('변경전계약금액'))), ','))
    self.표오른쪽(1)
    format(int(re.sub('[^0-9\\s]'('', 데이터2, None('변경후계약금액'))), ','))
    self.표오른쪽(1)
    임시계산값2 = int - re.sub('[^0-9\\s]'('', 데이터2, None('변경전계약금액')))
    if 임시계산값2 == 0:
        self.문장('변경없음')
    elif 임시계산값2 < 0:
        self.문장('△' + format(abs(임시계산값2), ','))
    else:
        self.문장(format(임시계산값2, ','))
    self.표오른쪽(1)
    데이터(None('변경후착공일자').replace('년', '.').replace('월', '.').replace('일', '.'))
    self.표오른쪽(1)
    데이터(None('변경전금차준공기한').replace('년', '.').replace('월', '.').replace('일', '.'))
    self.표오른쪽(1)
    self.대상.HAction.Run('MoveRight')
    self.대상.HAction.Run('BreakPara')
    self.대상.HAction.Run('ParagraphShapeAlignJustify')
    self.대상.HAction.Run('BreakPara')
    self.대상.HAction.Run('BreakPara')
    self.대상.HAction.Run('BreakPara')
    self.문장('붙임 :  1. 공사변경계약서(초안) 1부.')
    self.대상.HAction.Run('BreakPara')
    self.문장('       2. 관련문서 각 1부.  끝.')
return None
return None
if ValueError:
    e = self.문장 if re.sub('[^0-9\\s]'('', 데이터, None('국민주택채권\r\n  추가매입액'))) == 0 else ' 라. 추가국민주택채권: '
    print(f'''값 오류 : {e}''')
    self.대상.ReleaseScan()
    e = None
    del e
    continue
    e = None
    del e
if Exception:
    e = None
    print(f'''오류 발생 : {e}''')
    self.대상.ReleaseScan()
    e = None
    del e
    continue
    e = None
    del e
