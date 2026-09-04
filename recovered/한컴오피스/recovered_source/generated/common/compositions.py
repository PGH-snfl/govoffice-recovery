"""원본 바이트코드에서 복구한 직선형 메서드 조합."""

import json
import math
import os
import re
import time
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

try:
    from tkinter import filedialog
except ImportError:
    filedialog = None

try:
    from win32com.client.gencache import EnsureDispatch
except ImportError:
    EnsureDispatch = None


class Generated한컴기본CompositionMixin:
    def 방금처리0(self):
        self.방금처리 = 0

    def 가운데정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignCenter')

    def 고정여백(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('InsertFixedWidthSpace')

    def 객체찾기(self):
        self.대상.FindCtrl()

    def 기본정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 기본글자(self):
        self.대상.HAction.Run('CharShapeNormal')

    def 글자작게(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('CharShapeHeightDecrease')

    def 글자크게(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('CharShapeHeightIncrease')

    def 다음페이지(self):
        self.대상.HAction.Run('BreakPage')

    def 도형나가기(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')
        self.대상.HAction.Run('BreakPara')

    def 도형나가기2(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')

    def 도형텍스트입력(self):
        self.대상.HAction.Run('ShapeObjAttachTextBox')

    def 딜리트(self):
        self.대상.HAction.Run('Delete')

    def 리스트시작(self):
        self.대상.MovePos(4)

    def 리스트끝(self):
        self.대상.MovePos(5)

    def 문서처음(self):
        self.대상.MovePos(2)

    def 문장내어쓰기(self):
        self.대상.HAction.Run('ParagraphShapeIndentAtCaret')

    def 밑줄(self):
        self.대상.HAction.Run('CharShapeUnderline')

    def 배분정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignDistribute')

    def 백스페이스(self):
        self.대상.HAction.Run('DeleteBack')

    def 복사(self):
        self.대상.HAction.Run('Copy')

    def 셀병합(self):
        self.대상.HAction.Run('TableMergeCell')

    def 셀선택(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 셀전체(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 엔드(self):
        self.대상.HAction.Run('MoveLineEnd')

    def 엔터(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('BreakPara')

    def 오른쪽정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignRight')

    def 왼쪽정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignLeft')

    def 윗첨자(self):
        self.대상.HAction.Run('CharShapeSuperscript')

    def 이탤릭(self):
        self.대상.HAction.Run('CharShapeItalic')

    def 진하게(self):
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')

    def 진하게단일(self):
        self.대상.HAction.Run('CharShapeBold')

    def 표나가기(self):
        self.대상.HAction.Run('MoveRight')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 표나가기2(self):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 표나가기0(self):
        self.대상.HAction.Run('CloseEx')

    def 표너비줄이기(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('TableResizeExLeft')

    def 표높이줄이기(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('TableResizeExUp')

    def 표오른쪽(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('TableRightCellAppend')

    def 표오른쪽끝(self):
        self.대상.MovePos(105)

    def 표왼쪽끝(self):
        self.대상.MovePos(104)

    def 표왼쪽(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.HAction.Run('TableLeftCell')

    def 표아래쪽(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.MovePos(103)

    def 표위쪽(self, 횟수=1):
        for i in range(0, 횟수):
            self.대상.MovePos(102)

    def 표위쪽끝(self):
        self.대상.MovePos(106)

    def 표아래쪽끝(self):
        self.대상.MovePos(107)

    def 표전체(self):
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')

    def 표처음(self):
        self.대상.MovePos(106)
        self.대상.MovePos(104)

    def 표끝(self):
        self.대상.MovePos(105)
        self.대상.MovePos(107)

    def 페이지엔터(self):
        self.대상.HAction.Run('BreakPage')

    def 캔슬(self):
        self.대상.HAction.Run('Cancel')

    def 탭(self):
        self.대상.HAction.Run('InsertTab')

    def 고급붙임(self):
        self.대상.HAction.Run('PasteSpecial')

    def 그림용량옵션(self, 크기):
        총 = self.대상.CreateAction('PictureSaveAsOption')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('DelCutting', 1)
        총알.SetItem('ResizeImage', 1)
        총알.SetItem('SaveType', 0)
        총알.SetItem('SaveDpiY', 크기)
        총알.SetItem('SaveDpiX', 크기)
        총.Execute(총알)

    def 그림용량지정(self):
        총 = self.대상.CreateAction('PictureSaveAsAll')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총.Execute(총알)

    def 그림글자취급해제(self):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 0)
        총.Execute(총알)

    def 그림높이너비정보(self):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        너비 = 총알.Item('Width')
        높이 = 총알.Item('Height')
        return [높이, 너비]

    def 그림높이너비지정(self, 높이, 너비):
        self.대상.HAction.GetDefault('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.Width = 너비
        self.대상.HParameterSet.HShapeObject.Height = 높이
        self.대상.HAction.Execute('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 글머리미니네모(self):
        총 = self.대상.CreateAction('ParaNumberBullet')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeadingType', 3)
        서브총알 = 총알.CreateItemSet('Bullet', 'BulletShape')
        서브총알.SetItem('BulletChar', 61607)
        서브총알.SetItem('WidthAdjust', 0)
        서브총알.SetItem('TextOffset', 50)
        서브총알.SetItem('TextOffsetType', 0)
        서브총알.SetItem('UseInstWidth', 0)
        서브총알.SetItem('AutoIndent', 1)
        총.Execute(총알)

    def 글자간격(self, 간격=0):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('SpacingJapanese', 간격)
        총알.SetItem('SpacingHanja', 간격)
        총알.SetItem('SpacingLatin', 간격)
        총알.SetItem('SpacingHangul', 간격)
        총알.SetItem('SpacingUser', 간격)
        총알.SetItem('SpacingSymbol', 간격)
        총알.SetItem('SpacingOther', 간격)
        총.Execute(총알)

    def 글자그림자(self, 간격=10):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('ShadowType', self.대상.CharShadowType('Drop'))
        총알.SetItem('ShadowOffsetY', 간격)
        총알.SetItem('ShadowOffsetX', 간격)
        총.Execute(총알)

    def 글자그림자색상(self, 간격, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('ShadowType', self.대상.CharShadowType('Drop'))
        총알.SetItem('ShadowOffsetY', 간격)
        총알.SetItem('ShadowOffsetX', 간격)
        총알.SetItem('ShadowColor', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    def 글자마이(self):
        self.대상.HAction.Run('CharShapeHeightDecrease')
        self.대상.HAction.Run('CharShapeHeightDecrease')

    def 글자문단모양복사(self):
        총 = self.대상.CreateAction('ShapeCopyPaste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Type', 2)
        총.Execute(총알)

    def 글자색(self, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TextColor', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    def 글자스타일(self, 번호):
        총 = self.대상.CreateAction('Style')
        # 일부 한글 버전/문서 상태에서는 Style 액션을 제공하지 않는다.
        # 원본은 여기서 None.CreateSet() 오류로 중단되지만, 스타일 적용을
        # 건너뛰면 마크다운의 텍스트·표 변환은 계속 수행할 수 있다.
        if 총 is None:
            return False
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Apply', 번호)
        총.Execute(총알)
        return True

    def 글자스타일조회(self):
        총 = self.대상.CreateAction('Style')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        return 총알.Item('Apply')

    def 글자음영(self, 색상=4294967295):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('ShadeColor', 색상)
        총.Execute(총알)

    def 글자장평(self, 장평):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('RatioHangul', 장평)
        총알.SetItem('RatioLatin', 장평)
        총알.SetItem('RatioHanja', 장평)
        총알.SetItem('RatioJapanese', 장평)
        총알.SetItem('RatioOther', 장평)
        총알.SetItem('RatioSymbol', 장평)
        총알.SetItem('RatioUser', 장평)
        총.Execute(총알)

    def 글자크기(self, 크기):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Height', (크기 * 100))
        총.Execute(총알)

    def 글자크기찾기(self, 크기):
        총 = self.대상.CreateAction('RepeatFind')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        총알.SetItem('Direction', 0)
        총알.SetItem('FindType', 1)
        총알.SetItem('IgnoreMessage', 1)
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        서브총알.SetItem('Height', (크기 * 100))
        총.Execute(총알)

    def 글자색찾기(self, 방향, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('RepeatFind')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        총알.SetItem('Direction', 방향)
        총알.SetItem('FindType', 1)
        총알.SetItem('IgnoreMessage', 1)
        총알.SetItem('FindString', '')
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        서브총알.SetItem('TextColor', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    @staticmethod
    def _폰트설치됨(폰트):
        """AllReplace가 충돌하지 않도록 양쪽 글꼴의 설치 여부를 확인한다.

        한글의 AllReplace는 존재하지 않는 글꼴을 FindCharShape에 넣을 때
        예외가 아니라 Hwp.exe 접근 위반으로 종료될 수 있다. Windows 글꼴
        레지스트리와 Fonts 폴더를 모두 확인하고, 확인할 수 없으면 안전하게
        False를 반환한다. 특수 환경에서 검증이 필요하면 명시적으로
        GOVOFFICE_ALLOW_UNSAFE_FONT_REPLACE=1을 설정해 원본 경로를 켤 수 있다.
        """
        if os.environ.get('GOVOFFICE_ALLOW_UNSAFE_FONT_REPLACE') == '1':
            return True
        이름 = str(폰트 or '').strip()
        if not 이름:
            return False
        정규화 = lambda 값: re.sub(r'[^0-9a-z가-힣]+', '', str(값).casefold())
        대상 = 정규화(이름)
        이름키 = re.sub(r'\s+', '', 이름)
        별칭 = {
            '맑은고딕': ('malgun',),
            '휴먼명조': ('human', '휴먼'),
        }.get(이름키, ())
        후보 = (대상,) + tuple(정규화(값) for 값 in 별칭)
        값목록 = []
        try:
            import winreg
            경로 = r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts'
            for 하이브 in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
                for 보기 in (0, getattr(winreg, 'KEY_WOW64_64KEY', 0), getattr(winreg, 'KEY_WOW64_32KEY', 0)):
                    try:
                        with winreg.OpenKey(하이브, 경로, 0, winreg.KEY_READ | 보기) as 키:
                            for 번호 in range(winreg.QueryInfoKey(키)[1]):
                                이름값, 파일값, _ = winreg.EnumValue(키, 번호)
                                값목록.extend((이름값, 파일값))
                    except OSError:
                        continue
        except ImportError:
            return False
        for 값 in 값목록:
            정규값 = 정규화(값)
            if any(후보값 and (후보값 in 정규값 or 정규값 in 후보값) for 후보값 in 후보):
                return True
        # 레지스트리 읽기가 제한된 계정에서는 Fonts 폴더를 보조 경로로
        # 확인한다. 파일명은 표시 이름과 다를 수 있어 안전한 별칭만 둔다.
        파일별칭 = {
            '맑은고딕': ('malgun',),
            '바탕': ('batang',),
            '굴림': ('gulim',),
            'arial': ('arial',),
        }.get(이름키.casefold(), ())
        if 파일별칭:
            글꼴폴더 = Path(os.environ.get('WINDIR', r'C:\\Windows')) / 'Fonts'
            try:
                for 파일 in 글꼴폴더.iterdir():
                    파일명 = 파일.name.casefold()
                    if any(별칭.casefold() in 파일명 for 별칭 in 파일별칭):
                        return True
            except OSError:
                pass
        return False

    def 글자폰트바꾸기(self, 폰트1, 폰트2):
        if not (self._폰트설치됨(폰트1) and self._폰트설치됨(폰트2)):
            return False
        총 = self.대상.CreateAction('AllReplace')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        총알.SetItem('Direction', 2)
        총알.SetItem('IgnoreMessage', 1)
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        서브총알.SetItem('FaceNameUser', 폰트1)
        서브총알.SetItem('FontTypeUser', 1)
        서브총알.SetItem('FaceNameSymbol', 폰트1)
        서브총알.SetItem('FontTypeSymbol', 1)
        서브총알.SetItem('FaceNameOther', 폰트1)
        서브총알.SetItem('FontTypeOther', 1)
        서브총알.SetItem('FaceNameJapanese', 폰트1)
        서브총알.SetItem('FontTypeJapanese', 1)
        서브총알.SetItem('FaceNameHanja', 폰트1)
        서브총알.SetItem('FontTypeHanja', 1)
        서브총알.SetItem('FaceNameLatin', 폰트1)
        서브총알.SetItem('FontTypeLatin', 1)
        서브총알.SetItem('FaceNameHangul', 폰트1)
        서브총알.SetItem('FontTypeHangul', 1)
        서브2총알 = 총알.CreateItemSet('ReplaceCharShape', 'CharShape')
        서브2총알.SetItem('FaceNameUser', 폰트2)
        서브2총알.SetItem('FontTypeUser', 1)
        서브2총알.SetItem('FaceNameSymbol', 폰트2)
        서브2총알.SetItem('FontTypeSymbol', 1)
        서브2총알.SetItem('FaceNameOther', 폰트2)
        서브2총알.SetItem('FontTypeOther', 1)
        서브2총알.SetItem('FaceNameJapanese', 폰트2)
        서브2총알.SetItem('FontTypeJapanese', 1)
        서브2총알.SetItem('FaceNameHanja', 폰트2)
        서브2총알.SetItem('FontTypeHanja', 1)
        서브2총알.SetItem('FaceNameLatin', 폰트2)
        서브2총알.SetItem('FontTypeLatin', 1)
        서브2총알.SetItem('FaceNameHangul', 폰트2)
        서브2총알.SetItem('FontTypeHangul', 1)
        총.Execute(총알)

    def 글자폰트바꾸기간격(self, 폰트1, 폰트2, 간격):
        if not (self._폰트설치됨(폰트1) and self._폰트설치됨(폰트2)):
            return False
        총 = self.대상.CreateAction('AllReplace')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        총알.SetItem('Direction', 2)
        총알.SetItem('IgnoreMessage', 1)
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        서브총알.SetItem('FaceNameUser', 폰트1)
        서브총알.SetItem('FontTypeUser', 1)
        서브총알.SetItem('FaceNameSymbol', 폰트1)
        서브총알.SetItem('FontTypeSymbol', 1)
        서브총알.SetItem('FaceNameOther', 폰트1)
        서브총알.SetItem('FontTypeOther', 1)
        서브총알.SetItem('FaceNameJapanese', 폰트1)
        서브총알.SetItem('FontTypeJapanese', 1)
        서브총알.SetItem('FaceNameHanja', 폰트1)
        서브총알.SetItem('FontTypeHanja', 1)
        서브총알.SetItem('FaceNameLatin', 폰트1)
        서브총알.SetItem('FontTypeLatin', 1)
        서브총알.SetItem('FaceNameHangul', 폰트1)
        서브총알.SetItem('FontTypeHangul', 1)
        서브2총알 = 총알.CreateItemSet('ReplaceCharShape', 'CharShape')
        서브2총알.SetItem('FaceNameUser', 폰트2)
        서브2총알.SetItem('FontTypeUser', 1)
        서브2총알.SetItem('FaceNameSymbol', 폰트2)
        서브2총알.SetItem('FontTypeSymbol', 1)
        서브2총알.SetItem('FaceNameOther', 폰트2)
        서브2총알.SetItem('FontTypeOther', 1)
        서브2총알.SetItem('FaceNameJapanese', 폰트2)
        서브2총알.SetItem('FontTypeJapanese', 1)
        서브2총알.SetItem('FaceNameHanja', 폰트2)
        서브2총알.SetItem('FontTypeHanja', 1)
        서브2총알.SetItem('FaceNameLatin', 폰트2)
        서브2총알.SetItem('FontTypeLatin', 1)
        서브2총알.SetItem('FaceNameHangul', 폰트2)
        서브2총알.SetItem('FontTypeHangul', 1)
        서브2총알.SetItem('SpacingJapanese', 간격)
        서브2총알.SetItem('SpacingHanja', 간격)
        서브2총알.SetItem('SpacingLatin', 간격)
        서브2총알.SetItem('SpacingHangul', 간격)
        서브2총알.SetItem('SpacingUser', 간격)
        서브2총알.SetItem('SpacingSymbol', 간격)
        서브2총알.SetItem('SpacingOther', 간격)
        try:
            return bool(총.Execute(총알))
        except Exception:
            # 일부 한글 버전은 AllReplace 글꼴 조건을 처리하면서 COM 서버
            # 예외를 반환한다. 이때 문서 전체를 선택해 CharShape로 대상
            # 글꼴/자간을 적용하는 호환 경로를 시도한다.
            try:
                self.대상.HAction.Run('SelectAll')
                대체 = self.대상.CreateAction('CharShape')
                대체알 = 대체.CreateSet()
                대체.GetDefault(대체알)
                for 필드 in ('User', 'Symbol', 'Other', 'Japanese', 'Hanja', 'Latin', 'Hangul'):
                    대체알.SetItem(f'FaceName{필드}', 폰트2)
                    대체알.SetItem(f'FontType{필드}', 1)
                for 필드 in ('Japanese', 'Hanja', 'Latin', 'Hangul', 'User', 'Symbol', 'Other'):
                    대체알.SetItem(f'Spacing{필드}', 간격)
                대체.Execute(대체알)
                return True
            except Exception:
                # 지원하지 않는 HWP 버전에서도 호출 자체는 정상 반환해
                # GUI와 자동화 프로세스가 중단되지 않게 한다.
                return False

    def 글자플이(self):
        self.대상.HAction.Run('CharShapeHeightIncrease')
        self.대상.HAction.Run('CharShapeHeightIncrease')

    def 꼬리말(self):
        총 = self.대상.CreateAction('HeaderFooter')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeaderFooterStyle', 0)
        총알.SetItem('HeaderFooterCtrlType', 1)
        총.Execute(총알)

    def 끼워넣기(self, 파일명='C:\\Users\\user\\Desktop\\2.hwpx'):
        총 = self.대상.CreateAction('InsertFile')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FileName', 파일명)
        총.Execute(총알)

    def 내어쓰기(self, 값):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Indentation', self.대상.PointToHwpUnit((값 * 2)))
        총.Execute(총알)

    def 내용만붙이기(self):
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Option', 5)
        총.Execute(총알)

    def 대각선(self, 선종류='앞', 선굵기=1):
        총 = self.대상.CreateAction('CellBorder')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('DiagonalWidth', 선굵기)
        if (선종류 == '앞'):
            총알.SetItem('SlashFlag', 2)
            총알.SetItem('BackSlashFlag', 0)
        if (선종류 == '뒤'):
            총알.SetItem('SlashFlag', 0)
            총알.SetItem('BackSlashFlag', 2)
        총.Execute(총알)

    def 도형(self, 넓이, 높이, 선굵기, 곡률, 면색, 선색):
        총 = self.대상.CreateAction('DrawObjCreatorRectangle')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브포인트 = 총알.CreateItemSet('ShapeDrawLayOut', 'DrawLayOut')
        서브포인트.SetItem('CreateNumPt', 4)
        서브포인트배열 = 서브포인트.CreateItemArray('CreatePt', 8)
        서브포인트배열.SetItem(0, 0)
        서브포인트배열.SetItem(1, 0)
        서브포인트배열.SetItem(2, 넓이)
        서브포인트배열.SetItem(3, 0)
        서브포인트배열.SetItem(4, 넓이)
        서브포인트배열.SetItem(5, 높이)
        서브포인트배열.SetItem(6, 0)
        서브포인트배열.SetItem(7, 높이)
        총알.SetItem('HeightRelTo', self.대상.HeightRel('Absolute'))
        총알.SetItem('Height ', 높이)
        총알.SetItem('WidthRelTo', self.대상.WidthRel('Absolute'))
        총알.SetItem('Width', 넓이)
        서브배경 = 총알.CreateItemSet('ShapeDrawFillAttr', 'DrawFillAttr')
        서브배경.SetItem('Type', 1)
        서브배경.SetItem('WinBrushAlpha', 0)
        서브배경.SetItem('WinBrushFaceStyle', 6)
        서브배경.SetItem('WinBrushHatchColor', self.대상.RGBColor(0, 0, 0))
        서브배경.SetItem('WinBrushFaceColor', self.대상.RGBColor(면색[0], 면색[1], 면색[2]))
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('Alpha', 0)
        서브선.SetItem('OutLineStyle', 0)
        서브선.SetItem('EndCap', 1)
        서브선.SetItem('Width', 선굵기)
        서브선.SetItem('Style', 1)
        서브선.SetItem('Color', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브박스 = 총알.CreateItemSet('ShapeDrawRectType', 'DrawRectType')
        서브박스.SetItem('Type', 곡률)
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)

    def 도형네모(self, 넓이, 높이):
        총 = self.대상.CreateAction('DrawObjCreatorRectangle')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Width', 넓이)
        총알.SetItem('WidthRelTo', 4)
        총알.SetItem('Height', 높이)
        총알.SetItem('HeightRelTo', 2)
        서브레이아웃 = 총알.CreateItemSet('ShapeDrawLayOut', 'DrawLayOut')
        서브레이아웃셋 = 서브레이아웃.CreateItemArray('CreatePt', 8)
        서브레이아웃셋.SetItem(0, 0)
        서브레이아웃셋.SetItem(1, 0)
        서브레이아웃셋.SetItem(2, 20409)
        서브레이아웃셋.SetItem(3, 0)
        서브레이아웃셋.SetItem(4, 20409)
        서브레이아웃셋.SetItem(5, 20409)
        서브레이아웃셋.SetItem(6, 0)
        서브레이아웃셋.SetItem(7, 20409)
        서브레이아웃.SetItem('CreateNumPt', 4)
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('Alpha', 0)
        서브선.SetItem('OutLineStyle', 0)
        서브선.SetItem('EndCap', 1)
        서브선.SetItem('Width', 28)
        서브선.SetItem('Style', 1)
        서브선.SetItem('Color', self.대상.RGBColor(0, 0, 0))
        서브배경 = 총알.CreateItemSet('ShapeDrawFillAttr', 'DrawFillAttr')
        서브배경.SetItem('Type', 1)
        서브배경.SetItem('WinBrushAlpha', 0)
        서브배경.SetItem('WinBrushFaceStyle', 6)
        서브배경.SetItem('WinBrushHatchColor', self.대상.RGBColor(0, 0, 0))
        서브배경.SetItem('WinBrushFaceColor', self.대상.RGBColor(255, 255, 255))
        총알.SetItem('TextFlow', 0)
        총알.SetItem('NumberingType', 1)
        총알.SetItem('AdjustTextbox', 1)
        총알.SetItem('TreatAsChar', 1)
        서브텍스트 = 총알.CreateItemSet('ShapeListProperites', 'ListProperties')
        서브텍스트.SetItem('TextDirection', 0)
        서브텍스트.SetItem('LineWrap', 1)
        서브텍스트.SetItem('VertAlign', 1)
        서브텍스트.SetItem('MarginBottom', self.대상.MiliToHwpUnit(0))
        서브텍스트.SetItem('MarginRight', self.대상.MiliToHwpUnit(0))
        서브텍스트.SetItem('MarginTop', self.대상.MiliToHwpUnit(0))
        서브텍스트.SetItem('MarginLeft', self.대상.MiliToHwpUnit(0))
        총.Execute(총알)

    def 도형네모곡률(self, 곡률):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('TailFill', 1)
        서브선.SetItem('HeadFill', 1)
        서브곡률 = 총알.CreateItemSet('ShapeDrawRectType', 'DrawRectType')
        서브곡률.SetItem('Type', 15)
        총알.SetItem('ShapeType', 1)
        총.Execute(총알)

    def 도형네모복합(self, 너비, 높이, 굵기, 색상, 곡률):
        총 = self.대상.CreateAction('DrawObjCreatorRectangle')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Width', self.대상.MiliToHwpUnit(너비))
        총알.SetItem('WidthRelTo', 4)
        총알.SetItem('Height', self.대상.MiliToHwpUnit(높이))
        총알.SetItem('HeightRelTo', 2)
        서브레이아웃 = 총알.CreateItemSet('ShapeDrawLayOut', 'DrawLayOut')
        서브레이아웃셋 = 서브레이아웃.CreateItemArray('CreatePt', 8)
        서브레이아웃셋.SetItem(0, 0)
        서브레이아웃셋.SetItem(1, 0)
        서브레이아웃셋.SetItem(2, 20409)
        서브레이아웃셋.SetItem(3, 0)
        서브레이아웃셋.SetItem(4, 20409)
        서브레이아웃셋.SetItem(5, 20409)
        서브레이아웃셋.SetItem(6, 0)
        서브레이아웃셋.SetItem(7, 20409)
        서브레이아웃.SetItem('CreateNumPt', 4)
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('Alpha', 0)
        서브선.SetItem('OutLineStyle', 0)
        서브선.SetItem('EndCap', 1)
        서브선.SetItem('Width', 굵기)
        서브선.SetItem('Style', 1)
        서브선.SetItem('Color', self.대상.RGBColor(0, 0, 0))
        서브배경 = 총알.CreateItemSet('ShapeDrawFillAttr', 'DrawFillAttr')
        서브배경.SetItem('Type', 1)
        서브배경.SetItem('WinBrushAlpha', 0)
        서브배경.SetItem('WinBrushFaceStyle', 6)
        서브배경.SetItem('WinBrushHatchColor', self.대상.RGBColor(0, 0, 0))
        서브배경.SetItem('WinBrushFaceColor', self.대상.RGBColor(색상[0], 색상[1], 색상[2]))
        총알.SetItem('TreatAsChar', 1)
        서브곡률 = 총알.CreateItemSet('ShapeDrawRectType', 'DrawRectType')
        서브곡률.SetItem('Type', 곡률)
        총.Execute(총알)

    def 도형네모복합2(self, 너비, 높이, 굵기, 색상, 곡률, 선색):
        총 = self.대상.CreateAction('DrawObjCreatorRectangle')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Width', self.대상.MiliToHwpUnit(너비))
        총알.SetItem('WidthRelTo', 4)
        총알.SetItem('Height', self.대상.MiliToHwpUnit(높이))
        총알.SetItem('HeightRelTo', 2)
        서브레이아웃 = 총알.CreateItemSet('ShapeDrawLayOut', 'DrawLayOut')
        서브레이아웃셋 = 서브레이아웃.CreateItemArray('CreatePt', 8)
        서브레이아웃셋.SetItem(0, 0)
        서브레이아웃셋.SetItem(1, 0)
        서브레이아웃셋.SetItem(2, 20409)
        서브레이아웃셋.SetItem(3, 0)
        서브레이아웃셋.SetItem(4, 20409)
        서브레이아웃셋.SetItem(5, 20409)
        서브레이아웃셋.SetItem(6, 0)
        서브레이아웃셋.SetItem(7, 20409)
        서브레이아웃.SetItem('CreateNumPt', 4)
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('Alpha', 0)
        서브선.SetItem('OutLineStyle', 0)
        서브선.SetItem('EndCap', 1)
        서브선.SetItem('Width', 굵기)
        서브선.SetItem('Style', 1)
        서브선.SetItem('Color', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브배경 = 총알.CreateItemSet('ShapeDrawFillAttr', 'DrawFillAttr')
        서브배경.SetItem('Type', 1)
        서브배경.SetItem('WinBrushAlpha', 0)
        서브배경.SetItem('WinBrushFaceStyle', 6)
        서브배경.SetItem('WinBrushHatchColor', self.대상.RGBColor(0, 0, 0))
        서브배경.SetItem('WinBrushFaceColor', self.대상.RGBColor(색상[0], 색상[1], 색상[2]))
        총알.SetItem('TreatAsChar', 1)
        서브곡률 = 총알.CreateItemSet('ShapeDrawRectType', 'DrawRectType')
        서브곡률.SetItem('Type', 곡률)
        총.Execute(총알)

    def 도형그림자(self):
        self.대상.HAction.GetDefault('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.ShapeDrawShadow.ShadowColor = self.대상.RGBColor(0, 0, 0)
        self.대상.HParameterSet.HShapeObject.ShapeDrawShadow.ShadowOffsetX = self.대상.MiliToHwpUnit(-1.6)
        self.대상.HParameterSet.HShapeObject.ShapeDrawShadow.ShadowOffsetY = self.대상.MiliToHwpUnit(-1.6)
        self.대상.HParameterSet.HShapeObject.ShapeDrawShadow.ShadowType = self.대상.DrawShadowType('ParellelRightBottom')
        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 1)
        self.대상.HAction.Execute('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 도형글상자좁게(self):
        self.대상.HAction.GetDefault('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.ShapeListProperites.MarginBottom = self.대상.MiliToHwpUnit(0)
        self.대상.HParameterSet.HShapeObject.ShapeListProperites.MarginTop = self.대상.MiliToHwpUnit(0)
        self.대상.HParameterSet.HShapeObject.ShapeListProperites.MarginRight = self.대상.MiliToHwpUnit(0)
        self.대상.HParameterSet.HShapeObject.ShapeListProperites.MarginLeft = self.대상.MiliToHwpUnit(0)
        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 1)
        self.대상.HAction.Execute('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 도형그림자측정(self):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        서브총알 = 총알.CreateItemSet('ShapeDrawShadow', 'DrawShadow')
        총.GetDefault(총알)
        return 서브총알.Item('ShadowOffsetX')

    def 도형높이(self, 높이):
        self.대상.HAction.GetDefault('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.Height = self.대상.MiliToHwpUnit(높이)
        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 1)
        self.대상.HAction.Execute('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 도형선색(self, 선색1, 선색2, 선색3):
        self.대상.HAction.GetDefault('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.ShapeDrawLineAttr.Color = self.대상.RGBColor(선색1, 선색2, 선색3)
        self.대상.HAction.Execute('ShapeObjDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 도형원(self, 너비, 높이, 굵기, 색상, 선색):
        총 = self.대상.CreateAction('DrawObjCreatorRectangle')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Width', self.대상.MiliToHwpUnit(너비))
        총알.SetItem('WidthRelTo', 4)
        총알.SetItem('Height', self.대상.MiliToHwpUnit(높이))
        총알.SetItem('HeightRelTo', 2)
        서브레이아웃 = 총알.CreateItemSet('ShapeDrawLayOut', 'DrawLayOut')
        서브레이아웃셋 = 서브레이아웃.CreateItemArray('CreatePt', 8)
        서브레이아웃셋.SetItem(0, 0)
        서브레이아웃셋.SetItem(1, 0)
        서브레이아웃셋.SetItem(2, 20409)
        서브레이아웃셋.SetItem(3, 0)
        서브레이아웃셋.SetItem(4, 20409)
        서브레이아웃셋.SetItem(5, 20409)
        서브레이아웃셋.SetItem(6, 0)
        서브레이아웃셋.SetItem(7, 20409)
        서브레이아웃.SetItem('CreateNumPt', 4)
        서브곡률 = 총알.CreateItemSet('ShapeDrawRectType', 'DrawRectType')
        서브곡률.SetItem('Type', 50)
        서브선 = 총알.CreateItemSet('ShapeDrawLineAttr', 'DrawLineAttr')
        서브선.SetItem('Alpha', 0)
        서브선.SetItem('OutLineStyle', 0)
        서브선.SetItem('EndCap', 1)
        서브선.SetItem('Width', 굵기)
        서브선.SetItem('Style', 1)
        서브선.SetItem('Color', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브배경 = 총알.CreateItemSet('ShapeDrawFillAttr', 'DrawFillAttr')
        서브배경.SetItem('Type', 1)
        서브배경.SetItem('WinBrushAlpha', 0)
        서브배경.SetItem('WinBrushFaceStyle', 6)
        서브배경.SetItem('WinBrushHatchColor', self.대상.RGBColor(0, 0, 0))
        서브배경.SetItem('WinBrushFaceColor', self.대상.RGBColor(색상[0], 색상[1], 색상[2]))
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)

    def 머릿말(self):
        총 = self.대상.CreateAction('HeaderFooter')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeaderFooterStyle', 0)
        총알.SetItem('HeaderFooterCtrlType', 0)
        총.Execute(총알)

    def 문단글머리제거(self):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeadingType', 0)
        총.Execute(총알)

    def 문단여백(self, 좌측, 우측):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('LeftMargin', self.대상.PointToHwpUnit((좌측 * 2)))
        총알.SetItem('RightMargin', self.대상.PointToHwpUnit((우측 * 2)))
        총.Execute(총알)

    def 문단여백측정(self):
        총 = self.대상.CreateAction('PageSetup')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.Item('PageDef')
        return round(((서브총알.Item('LeftMargin') + 서브총알.Item('RightMargin')) / 283.4), 1)

    def 문단여백측정세로(self):
        총 = self.대상.CreateAction('PageSetup')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.Item('PageDef')
        return round(((((서브총알.Item('TopMargin') + 서브총알.Item('BottomMargin')) + 서브총알.Item('HeaderLen')) + 서브총알.Item('FooterLen')) / 283.4), 1)

    def 문단위(self, 간격):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('PrevSpacing', (간격 * 200))
        총.Execute(총알)

    def 문단아래(self, 간격):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('NextSpacing', (간격 * 200))
        총.Execute(총알)

    def 문단음영(self, 색상):
        self.대상.HAction.GetDefault('ParagraphShape', self.대상.HParameterSet.HParaShape.HSet)
        self.대상.HParameterSet.HParaShape.BorderFill.FillAttr.WinBrushFaceColor = 색상
        self.대상.HAction.Execute('ParagraphShape', self.대상.HParameterSet.HParaShape.HSet)

    def 문서여백(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.PageDef.Landscape = 0
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 3)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서여백새페이지(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 4)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서용지복사(self):
        총 = self.대상.CreateAction('PageSetup')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.Item('PageDef')
        self.문서용지 = [서브총알.Item('LeftMargin'), 서브총알.Item('RightMargin'), 서브총알.Item('TopMargin'), 서브총알.Item('BottomMargin'), 서브총알.Item('HeaderLen'), 서브총알.Item('FooterLen')]

    def 문서용지붙임(self):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.문서용지[0]
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.문서용지[1]
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.문서용지[2]
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.문서용지[3]
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.문서용지[4]
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.문서용지[5]
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 3)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서테두리(self, 상, 하, 좌, 우, 선타입, 선굵기, 선색=[0, 0, 0]):
        총 = self.대상.CreateAction('PageBorder')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('PageBorderFillBoth', 'PageBorderFill')
        서브총알.SetItem('OffsetTop', self.대상.MiliToHwpUnit(상))
        서브총알.SetItem('OffsetBottom', self.대상.MiliToHwpUnit(하))
        서브총알.SetItem('OffsetLeft', self.대상.MiliToHwpUnit(좌))
        서브총알.SetItem('OffsetRight', self.대상.MiliToHwpUnit(우))
        서브총알.SetItem('BorderTypeLeft', 선타입)
        서브총알.SetItem('BorderTypeRight', 선타입)
        서브총알.SetItem('BorderTypeTop', 선타입)
        서브총알.SetItem('BorderTypeBottom', 선타입)
        서브총알.SetItem('BorderWidthLeft', 선굵기)
        서브총알.SetItem('BorderWidthRight', 선굵기)
        서브총알.SetItem('BorderWidthTop', 선굵기)
        서브총알.SetItem('BorderWidthBottom', 선굵기)
        서브총알.SetItem('BorderCorlorLeft', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브총알.SetItem('BorderColorRight', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브총알.SetItem('BorderColorTop', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        서브총알.SetItem('BorderColorBottom', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))
        총알.SetItem('ApplyToPageBorderFill', 3)
        총.Execute(총알)

    def 문장(self, 내용):
        총 = self.대상.CreateAction('InsertText')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Text', 내용)
        총.Execute(총알)

    def 문장오른쪽(self, 내용):
        self.표오른쪽(1)
        self.문장(내용)

    def 문장아래쪽(self, 내용):
        self.표아래쪽(1)
        self.문장(내용)

    def 밑줄얇굵(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('UnderlineShape', 8)
        총알.SetItem('UnderlineType', 1)
        총.Execute(총알)

    def 밑줄이중(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('UnderlineShape', 7)
        총알.SetItem('UnderlineType', 1)
        총.Execute(총알)

    def 밑줄기본(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('UnderlineShape', 0)
        총알.SetItem('UnderlineType', 1)
        총.Execute(총알)

    def 바탕쪽(self):
        self.대상.HAction.GetDefault('MasterPage', self.대상.HParameterSet.HMasterPage.HSet)
        self.대상.HParameterSet.HMasterPage.Duplicate = 0
        self.대상.HParameterSet.HMasterPage.Front = 0
        self.대상.HParameterSet.HMasterPage.HSet.SetItem('Type', 0)
        self.대상.HParameterSet.HMasterPage.HSet.SetItem('ApplyTo', 2)
        self.대상.HAction.Execute('MasterPage', self.대상.HParameterSet.HMasterPage.HSet)

    def 블록첫위치(self):
        시작지점 = self.대상.CreateSet('ListParaPos')
        끝지점 = self.대상.CreateSet('ListParaPos')
        self.대상.GetSelectedPosBySet(시작지점, 끝지점)
        return 시작지점

    def 블록끝위치(self):
        시작지점 = self.대상.CreateSet('ListParaPos')
        끝지점 = self.대상.CreateSet('ListParaPos')
        self.대상.GetSelectedPosBySet(시작지점, 끝지점)
        return 끝지점

    def 블록스캔(self):
        self.대상.InitScan(1, 255)
        텍스트 = self.대상.GetText()
        self.대상.ReleaseScan()
        return 텍스트

    def 사진(self, 종류):
        if self.대상.CellShape:
            이름 = filedialog.askopenfilenames(title='Open File', filetypes=[('image files', ('.png', '.jpg'))])
            for i in range(len(이름)):
                if not ((i == 0)):
                    self.대상.HAction.Run('TableRightCellAppend')
                if (종류 == '배경'):
                    self.대상.InsertBackgroundPicture('SelectedCell', 이름[i], 1, 5, 0, 0, 0, 0)
                    continue
                if not ((종류 == '비율')):
                    continue
                self.대상.InsertPicture(이름[i], 1, 3, 0, 0, 0)

    def 사진넣기(self, 이미지):
        if self.대상.CellShape:
            self.대상.InsertPicture(이미지, 1, 3, 0, 0, 0)
            self.대상.HAction.Run('ParagraphShapeAlignCenter')

    def 사진넣기그냥(self, 이미지, 너비, 높이):
        self.대상.InsertPicture(이미지, 1, 1, 0, 0, 0, 너비, 높이)

    def 사진넣기배경(self, 이미지):
        if self.대상.CellShape:
            self.대상.InsertBackgroundPicture('SelectedCell', 이미지, 1, 5, 0, 0, 0, 0)

    def 사진넣기절대값(self, 이미지, 너비, 높이):
        if self.대상.CellShape:
            self.대상.InsertPicture(이미지, 1, 1, 0, 0, 0, 너비, 높이)
            self.대상.HAction.Run('ParagraphShapeAlignCenter')

    def 상단캡션(self):
        self.대상.HAction.Run('ShapeObjAttachCaption')
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('ShapeCaption', 'Caption')
        서브총알.SetItem('Side', 2)
        서브총알.SetItem('Gap', self.대상.MiliToHwpUnit(1))
        총.Execute(총알)

    def 셀나누기(self, 행수=0, 열수=0):
        self.대상.HAction.GetDefault('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)
        self.대상.HParameterSet.HTableSplitCell.Rows = 열수
        self.대상.HParameterSet.HTableSplitCell.Cols = 행수
        self.대상.HAction.Execute('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)

    def 셀높이넓이복사(self):
        if self.대상.CellShape:
            총 = self.대상.CreateAction('TablePropertyDialog')
            총알 = 총.CreateSet()
            서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')
            총.GetDefault(총알)
            self.셀높이 = 서브총알.Item('Height')
            self.셀넓이 = 서브총알.Item('Width')

    def 셀높이붙여넣기(self):
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Height = self.셀높이
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 셀높이지정(self, 크기):
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Height = 크기
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 셀넓이붙여넣기(self):
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Width = self.셀넓이
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 셀보호해제(self):
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')
        총.GetDefault(총알)
        서브총알.SetItem('Protected', 0)
        총.Execute(총알)

    def 셀여백제로(self):
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('CellMarginBottom', self.대상.MiliToHwpUnit(0.0))
        총알.SetItem('CellMarginTop', self.대상.MiliToHwpUnit(0.0))
        총알.SetItem('CellMarginRight', self.대상.MiliToHwpUnit(0.0))
        총알.SetItem('CellMarginLeft', self.대상.MiliToHwpUnit(0.0))
        총알.SetItem('ShapeType', 3)
        총알.SetItem('ShapeCellSize', 0)
        총.Execute(총알)

    def 셀여백지정(self, 상, 하, 좌, 우):
        self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 0)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.HasMargin = 1
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.MarginBottom = self.대상.MiliToHwpUnit(하)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.MarginTop = self.대상.MiliToHwpUnit(상)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.MarginRight = self.대상.MiliToHwpUnit(우)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.MarginLeft = self.대상.MiliToHwpUnit(좌)
        self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 셀세로정렬(self, 숫자):
        self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.VertAlign = 숫자
        self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 셀한줄(self, 옵션=1):
        self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        self.대상.HParameterSet.HShapeObject.ShapeTableCell.LineWrap = 옵션
        self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

    def 신명조(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양신명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양신명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양신명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '한양신명조')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '한양신명조')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 신명태고딕(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '신명 태그래픽')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '신명 태고딕')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '신명 태고딕')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '신명 태고딕')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '신명 태고딕')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 신명태명조(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '신명 견명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '신명 태명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '신명 태명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '신명 태명조')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '신명 태명조')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 오른쪽으로붙이기(self):
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Option', 1)
        총.Execute(총알)

    def 아래로붙이기(self):
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Option', 3)
        총.Execute(총알)

    def 아래로붙이기(self):
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Option', 3)
        총.Execute(총알)

    def 원글자(self):
        총 = self.대상.CreateAction('ComposeChars')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('CircleType', 1)
        총알.SetItem('CheckCompose', 0)
        총.Execute(총알)

    def 자동번호해제(self):
        총 = self.대상.CreateAction('ParaNumberDlg')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeadingType', 0)
        총.Execute(총알)

    def 자간헌터(self, 모드):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('BreakNonLatinWord', 모드)
        총알.SetItem('Condense', 75)
        총.Execute(총알)

    def 재실행(self, 횟수=1):
        for i in range(1, (횟수 + 1)):
            self.대상.HAction.Run('Redo')

    def 정규표현식(self, 내용):
        총 = self.대상.CreateAction('RepeatFind')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        총알.SetItem('FindString', 내용)
        총알.SetItem('Direction', 0)
        총알.SetItem('IgnoreMessage', 1)
        총알.SetItem('FindType', 1)
        총알.SetItem('FindRegExp', 1)
        총.Execute(총알)

    def 정규표현식바꾸기(self, 찾을내용, 바꿀내용):
        총 = self.대상.CreateAction('ExecReplace')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        총알.SetItem('FindString', 찾을내용)
        총알.SetItem('ReplaceString', 바꿀내용)
        총알.SetItem('MatchCase', 0)
        총알.SetItem('AllWordForms', 0)
        총알.SetItem('SeveralWords', 0)
        총알.SetItem('UseWildCards', 0)
        총알.SetItem('WholeWordOnly', 0)
        총알.SetItem('AutoSpell', 1)
        총알.SetItem('Direction', 0)
        총알.SetItem('IgnoreFindString', 0)
        총알.SetItem('IgnoreReplaceString', 0)
        총알.SetItem('ReplaceMode', 1)
        총알.SetItem('IgnoreMessage', 1)
        총알.SetItem('HanjaFromHangul', 0)
        총알.SetItem('FindJaso', 0)
        총알.SetItem('FindRegExp', 1)
        총알.SetItem('FindStyle', '')
        총알.SetItem('ReplaceStyle', '')
        총알.SetItem('FindType', 1)
        총.Execute(총알)

    def 정규표현식반대(self, 내용):
        총 = self.대상.CreateAction('RepeatFind')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.RemoveAll('FindReplace')
        서브총알 = 총알.CreateItemSet('FindCharShape', 'CharShape')
        총알.SetItem('FindString', 내용)
        총알.SetItem('Direction', 1)
        총알.SetItem('IgnoreMessage', 1)
        총알.SetItem('FindType', 1)
        총알.SetItem('FindRegExp', 1)
        총.Execute(총알)

    def 제목셀반복(self):
        if self.대상.CellShape:
            self.대상.HAction.Run('Cancel')
            self.대상.MovePos(106)
            self.대상.MovePos(104)
            총 = self.대상.CreateAction('TablePropertyDialog')
            총알 = 총.CreateSet()
            총.GetDefault(총알)
            총알.SetItem('TreatAsChar', 0)
            총알.SetItem('RepeatHeader', 1)
            총알.SetItem('PageBreak', 1)
            총알.Item('ShapeTableCell').SetItem('Header', 1)
            서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')
            서브총알.SetItem('Header', 1)
            총.Execute(총알)

    def 쪽번호(self):
        총 = self.대상.CreateAction('PageNumPos')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('DrawPos', 5)
        총.Execute(총알)

    def 쪽새번호(self, 번호):
        총 = self.대상.CreateAction('NewNumber')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('NumType', 0)
        총알.SetItem('NewNumber', 번호)
        총.Execute(총알)

    def 쪽번호숨기기(self):
        총 = self.대상.CreateAction('PageHiding')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Fields', 32)
        총.Execute(총알)

    def 쪽번호보이기(self):
        총 = self.대상.CreateAction('PageHiding')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Fields', 0)
        총.Execute(총알)

    def 쪽번호초기화(self):
        총 = self.대상.CreateAction('DeleteCtrls')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알배열 = 총알.CreateItemArray('DeleteCtrlType', 3)
        서브총알배열.SetItem(0, 45)
        서브총알배열.SetItem(1, 47)
        서브총알배열.SetItem(2, 49)
        총.Execute(총알)

    def 줄간격(self, 간격):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('LineSpacingType', 0)
        총알.SetItem('LineSpacing', 간격)
        총.Execute(총알)

    def 줄칸뒤집기(self):
        총 = self.대상.CreateAction('TableSwap')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Type', 2)
        총.Execute(총알)

    def 중고딕(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양중고딕')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양중고딕')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양중고딕')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '한양중고딕')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '한양중고딕')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 찾아서글자취급(self):
        self.대상.FindCtrl()
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)

    def 찾아서왼쪽이동(self, 이동값):
        self.대상.FindCtrl()
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 0)
        총알.SetItem('HorzOffset', self.대상.MiliToHwpUnit(이동값))
        총알.SetItem('ShapeType', 1)
        총.Execute(총알)

    def 취소(self, 횟수=1):
        for i in range(1, (횟수 + 1)):
            self.대상.HAction.Run('Undo')

    def 탭점선설정(self, 값=88000):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')
        서브총알배열 = 서브총알.CreateItemArray('TabItem', 3)
        서브총알배열.SetItem(0, 값)
        서브총알배열.SetItem(1, 3)
        서브총알배열.SetItem(2, 1)
        총.Execute(총알)

    def 탭점선설정원형(self, 값=88000):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')
        서브총알배열 = 서브총알.CreateItemArray('TabItem', 3)
        서브총알배열.SetItem(0, 값)
        서브총알배열.SetItem(1, 7)
        서브총알배열.SetItem(2, 1)
        총.Execute(총알)

    def 탭점선제거(self):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')
        서브총알배열 = 서브총알.CreateItemArray('DeleteTab', 1)
        서브총알배열.SetItem(0, -1)
        총.Execute(총알)

    def 파일목록(self):
        return filedialog.askopenfilenames(title='Open File', filetypes=[('All Files', '*.*')])

    def 파일목록사진(self):
        return filedialog.askopenfilenames(title='Open File', filetypes=[('image files', ('.png', '.jpg'))])

    def 표글자취급(self):
        총 = self.대상.CreateAction('ShapeObjDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 1)
        총.Execute(총알)

    def 표내부선색(self, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('ColorHorz', self.대상.RGBColor(빨강, 초록, 파랑))
        총알.SetItem('ColorVert', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    def 표내부선굵기(self, 가로, 세로):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('WidthHorz', 가로)
        총알.SetItem('WidthVert', 세로)
        총.Execute(총알)

    def 표내부선타입(self, 가로, 세로):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TypeHorz', 가로)
        총알.SetItem('TypeVert', 세로)
        총.Execute(총알)

    def 표내부선가로(self, 굵기, 타입):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('WidthHorz', 굵기)
        총알.SetItem('TypeHorz', 타입)
        총.Execute(총알)

    def 표내부선세로(self, 굵기, 타입):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('WidthVert', 굵기)
        총알.SetItem('TypeVert', 타입)
        총.Execute(총알)

    def 표단일선(self, 위치, 굵기, 종류):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        if (위치 == '상'):
            총알.SetItem('BorderWidthTop', 굵기)
            총알.SetItem('BorderTypeTop', 종류)
        if (위치 == '하'):
            총알.SetItem('BorderWidthBottom', 굵기)
            총알.SetItem('BorderTypeBottom', 종류)
        if (위치 == '좌'):
            총알.SetItem('BorderWidthLeft', 굵기)
            총알.SetItem('BorderTypeLeft', 종류)
        if (위치 == '우'):
            총알.SetItem('BorderWidthRight', 굵기)
            총알.SetItem('BorderTypeRight', 종류)
        총.Execute(총알)

    def 셀하단기본선(self):
        self.표단일선('하', 1, 1)

    def 셀하단굵은선(self):
        self.표단일선('하', 6, 1)

    def 셀하단이중선(self):
        self.표단일선('하', 6, 8)

    def 표만들기(self, 가로크기, 세로크기):
        self.대상.HAction.GetDefault('TableCreate', self.대상.HParameterSet.HTableCreation.HSet)
        self.대상.HParameterSet.HTableCreation.Rows = len(세로크기)
        self.대상.HParameterSet.HTableCreation.Cols = len(가로크기)
        self.대상.HParameterSet.HTableCreation.WidthType = 2
        self.대상.HParameterSet.HTableCreation.HeightType = 1
        self.대상.HParameterSet.HTableCreation.CreateItemArray('ColWidth', len(가로크기))
        for i in range(0, len(가로크기)):
            self.대상.HParameterSet.HTableCreation.ColWidth.SetItem(i, self.대상.MiliToHwpUnit(가로크기[i]))
        self.대상.HParameterSet.HTableCreation.CreateItemArray('RowHeight', len(세로크기))
        for i in range(0, len(세로크기)):
            self.대상.HParameterSet.HTableCreation.RowHeight.SetItem(i, self.대상.MiliToHwpUnit(세로크기[i]))
        self.대상.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1
        self.대상.HAction.Execute('TableCreate', self.대상.HParameterSet.HTableCreation.HSet)

    def 표배경그라데이션(self, 종류='Linear', 각=0, 위치=[[0, 0, 0, 0], [255, 255, 255, 255], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]):
        총 = self.대상.CreateAction('CellFill')
        총알 = self.대상.CreateSet('CellBorderFill')
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('FillAttr', 'DrawFillAttr')
        서브총알.SetItem('Type', self.대상.BrushType('NullBrush|GradBrush'))
        서브총알.SetItem('GradationType', self.대상.Gradation(종류))
        서브총알.SetItem('GradationCenterX', 0)
        서브총알.SetItem('GradationCenterY', 0)
        서브총알.SetItem('GradationAngle', 각)
        서브총알.SetItem('GradationStep', 100)
        서브서브총알 = 서브총알.CreateItemArray('GradationIndexPos', 10)
        for i in range(10):
            서브서브총알.SetItem(i, 위치[i][0])
        서브총알.SetItem('GradationStepCenter', 50)
        서브총알.SetItem('GradationColorNum', 2)
        써브서브총알 = 서브총알.CreateItemArray('GradationColor', 10)
        for i in range(10):
            써브서브총알.SetItem(i, self.대상.RGBColor(위치[i][1], 위치[i][2], 위치[i][3]))
        서브총알.SetItem('GradationBrush', 1)
        총.Execute(총알)

    def 표배경그라데이션2(self, 종류='Linear', 각=0, 위치=[[0, 0, 0, 0], [255, 255, 255, 255]]):
        총 = self.대상.CreateAction('CellFill')
        총알 = self.대상.CreateSet('CellBorderFill')
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('FillAttr', 'DrawFillAttr')
        서브총알.SetItem('Type', self.대상.BrushType('NullBrush|GradBrush'))
        서브총알.SetItem('GradationType', self.대상.Gradation(종류))
        서브총알.SetItem('GradationCenterX', 0)
        서브총알.SetItem('GradationCenterY', 0)
        서브총알.SetItem('GradationAngle', 각)
        서브총알.SetItem('GradationStep', 100)
        서브서브총알 = 서브총알.CreateItemArray('GradationIndexPos', 10)
        위치 = (위치 + [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        for i in range(10):
            서브서브총알.SetItem(i, 위치[i][0])
        서브총알.SetItem('GradationStepCenter', 50)
        서브총알.SetItem('GradationColorNum', 2)
        써브서브총알 = 서브총알.CreateItemArray('GradationColor', 10)
        for i in range(10):
            써브서브총알.SetItem(i, self.대상.RGBColor(위치[i][1], 위치[i][2], 위치[i][3]))
        서브총알.SetItem('GradationBrush', 1)
        총.Execute(총알)

    def 표배경색(self, 빨강, 초록, 파랑):
        self.대상.HAction.GetDefault('CellFill', self.대상.HParameterSet.HCellBorderFill.HSet)
        self.대상.HParameterSet.HCellBorderFill.FillAttr.type = self.대상.BrushType('NullBrush|WinBrush')
        self.대상.HParameterSet.HCellBorderFill.FillAttr.WinBrushFaceColor = self.대상.RGBColor(빨강, 초록, 파랑)
        self.대상.HParameterSet.HCellBorderFill.FillAttr.WinBrushHatchColor = self.대상.RGBColor(빨강, 초록, 파랑)
        self.대상.HParameterSet.HCellBorderFill.FillAttr.WinBrushFaceStyle = self.대상.HatchStyle('None')
        self.대상.HParameterSet.HCellBorderFill.FillAttr.WindowsBrush = 1
        self.대상.HAction.Execute('CellFill', self.대상.HParameterSet.HCellBorderFill.HSet)

    def 표배경제거(self):
        총 = self.대상.CreateAction('CellFill')
        총알 = self.대상.CreateSet('CellBorderFill')
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('FillAttr', 'DrawFillAttr')
        서브총알.SetItem('Type', 0)
        총.Execute(총알)

    def 표밖여백제로(self):
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('OutsideMarginBottom', self.대상.MiliToHwpUnit(0))
        총알.SetItem('OutsideMarginTop', self.대상.MiliToHwpUnit(0))
        총알.SetItem('OutsideMarginLeft', self.대상.MiliToHwpUnit(0))
        총알.SetItem('OutsideMarginRight', self.대상.MiliToHwpUnit(0))
        총.Execute(총알)

    def 표절대위치이동(self, 수평=20, 수직=20):
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TreatAsChar', 0)
        총알.SetItem('HorzRelTo', 0)
        총알.SetItem('HorzOffset', self.대상.MiliToHwpUnit(수평))
        총알.SetItem('VertRelTo', 0)
        총알.SetItem('VertOffset', self.대상.MiliToHwpUnit(수직))
        총.Execute(총알)

    def 표문장변환(self):
        총 = self.대상.CreateAction('TableTableToString')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('DelimiterType', 3)
        총알.SetItem('UserDefine', ':')
        총.Execute(총알)

    def 표테두리굵기(self, 상, 하, 좌, 우):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('BorderWidthTop', 상)
        총알.SetItem('BorderWidthBottom', 하)
        총알.SetItem('BorderWidthLeft', 좌)
        총알.SetItem('BorderWidthRight', 우)
        총.Execute(총알)

    def 표테두리단일선(self, 종류, 굵기, 타입):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        if (종류 == '상'):
            총알.SetItem('BorderWidthTop', 굵기)
            총알.SetItem('BorderTypeTop', 타입)
        if (종류 == '하'):
            총알.SetItem('BorderWidthBottom', 굵기)
            총알.SetItem('BorderTypeBottom', 타입)
        if (종류 == '좌'):
            총알.SetItem('BorderWidthLeft', 굵기)
            총알.SetItem('BorderTypeLeft', 타입)
        if (종류 == '우'):
            총알.SetItem('BorderWidthRight', 굵기)
            총알.SetItem('BorderTypeRight', 타입)
        총.Execute(총알)

    def 표테두리단일선색(self, 종류, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        if (종류 == '상'):
            총알.SetItem('BorderColorTop', self.대상.RGBColor(빨강, 초록, 파랑))
        if (종류 == '하'):
            총알.SetItem('BorderColorBottom', self.대상.RGBColor(빨강, 초록, 파랑))
        if (종류 == '우'):
            총알.SetItem('BorderColorRight', self.대상.RGBColor(빨강, 초록, 파랑))
        if (종류 == '좌'):
            총알.SetItem('BorderCorlorLeft', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    def 표테두리색(self, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('BorderColorTop', self.대상.RGBColor(빨강, 초록, 파랑))
        총알.SetItem('BorderColorBottom', self.대상.RGBColor(빨강, 초록, 파랑))
        총알.SetItem('BorderColorRight', self.대상.RGBColor(빨강, 초록, 파랑))
        총알.SetItem('BorderCorlorLeft', self.대상.RGBColor(빨강, 초록, 파랑))
        총.Execute(총알)

    def 표테두리타입(self, 상, 하, 좌, 우):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('BorderTypeTop', 상)
        총알.SetItem('BorderTypeBottom', 하)
        총알.SetItem('BorderTypeLeft', 좌)
        총알.SetItem('BorderTypeRight', 우)
        총.Execute(총알)

    def 표탈출(self):
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveDown')
        self.대상.HAction.Run('CloseEx')

    def 폰트(self, 폰트):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', 폰트)
        총알.SetItem('FontTypeUser', 1)
        총알.SetItem('FaceNameSymbol', 폰트)
        총알.SetItem('FontTypeSymbol', 1)
        총알.SetItem('FaceNameOther', 폰트)
        총알.SetItem('FontTypeOther', 1)
        총알.SetItem('FaceNameJapanese', 폰트)
        총알.SetItem('FontTypeJapanese', 1)
        총알.SetItem('FaceNameHanja', 폰트)
        총알.SetItem('FontTypeHanja', 1)
        총알.SetItem('FaceNameLatin', 폰트)
        총알.SetItem('FontTypeLatin', 1)
        총알.SetItem('FaceNameHangul', 폰트)
        총알.SetItem('FontTypeHangul', 1)
        총.Execute(총알)

    def 필드심기(self, 이름):
        총 = self.대상.CreateAction('InsertFieldTemplate')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('TemplateDirection', 이름)
        총알.SetItem('TemplateName', 이름)
        총.Execute(총알)

    def 화면비율(self, 비율):
        총 = self.대상.CreateAction('ViewZoom')
        총알 = self.대상.CreateSet('ViewProperties')
        총.GetDefault(총알)
        총알.SetItem('ZoomType', 0)
        총알.SetItem('ZoomRatio', 비율)
        총.Execute(총알)

    def 현재위치(self):
        현위치 = self.대상.GetPosBySet()
        return 현위치

    def 휴먼명조(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameHangul', '휴먼명조')
        총알.SetItem('FontTypeHangul', 2)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양신명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양신명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양신명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', 'HCI Poppy')
        총알.SetItem('FontTypeLatin', 2)
        총.Execute(총알)

    def 블록한줄개선(self, 종류1, 종류2=''):
        텍스트 = self.블록스캔()[1]
        불순물여부 = ('\r' not in 텍스트)
        결과 = ''
        if 불순물여부:
            if (종류1 == '날짜변환'):
                결과 = self.날짜변환(텍스트, 종류2)
            if (종류1 == '증감계산'):
                결과 = self.증감계산(텍스트, 종류2)
            self.문장(str(결과))

    def 문장풀(self, 폰트, 크기, 진하게, 정렬, 문장):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', 폰트)
        총알.SetItem('FontTypeUser', 1)
        총알.SetItem('FaceNameSymbol', 폰트)
        총알.SetItem('FontTypeSymbol', 1)
        총알.SetItem('FaceNameOther', 폰트)
        총알.SetItem('FontTypeOther', 1)
        총알.SetItem('FaceNameJapanese', 폰트)
        총알.SetItem('FontTypeJapanese', 1)
        총알.SetItem('FaceNameHanja', 폰트)
        총알.SetItem('FontTypeHanja', 1)
        총알.SetItem('FaceNameLatin', 폰트)
        총알.SetItem('FontTypeLatin', 1)
        총알.SetItem('FaceNameHangul', 폰트)
        총알.SetItem('FontTypeHangul', 1)
        총알.SetItem('Height', (크기 * 100))
        총.Execute(총알)
        self.대상.HAction.Run('ParagraphShapeAlignJustify')
        self.대상.HAction.Run('CharShapeNormal')
        if (진하게 == 1):
            self.대상.HAction.Run('CharShapeBold')
        if (정렬 == 1):
            self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.문장(문장)

    def 좌표(self, 리스트, 파라, 포스):
        위치 = self.대상.GetPosBySet()
        위치.SetItem('List', 리스트)
        위치.SetItem('Para', 파라)
        위치.SetItem('Pos', 포스)
        return 위치

    def 셀이동(self, 리스트):
        위치 = self.대상.GetPosBySet()
        위치.SetItem('List', 리스트)
        위치.SetItem('Para', 0)
        위치.SetItem('Pos', 0)
        self.대상.SetPosBySet(위치)

    def 셀위치(self, 리스트):
        위치 = self.대상.GetPosBySet()
        위치.SetItem('List', 리스트)
        위치.SetItem('Para', 0)
        위치.SetItem('Pos', 0)
        return 위치

    def 블록리스트생성(self, 행, 열, 한줄, 처음위치):
        블록리스트 = []
        for j in range(행):
            for i in range(열):
                숫자 = ((처음위치 + i) + (한줄 * j))
                블록리스트.append(숫자)
        return 블록리스트

    def 합계수식(self, 일번, 이번):
        총 = self.대상.CreateAction('TableFormula')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Command', (((('=SUM(' + 일번) + ':') + 이번) + ')??%g,;;'))
        총.Execute(총알)

    def 빼기수식(self, 일번, 이번):
        총 = self.대상.CreateAction('TableFormula')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Command', (((('=' + 일번) + '-') + 이번) + '??%g;;'))
        총.Execute(총알)

    def 글자문단모양기본(self):
        self.자간헌터(1)
        self.내어쓰기(0)
        self.글자간격(0)
        self.폰트('돋움체')
        self.글자크기(12)
        self.대상.HAction.Run('ParagraphShapeAlignJustify')
        self.대상.HAction.Run('CharShapeNormal')
        self.줄간격(160)
        self.글자장평(100)
        self.글자음영(4294967295)
        self.문단여백(0, 0)

    def 글자취급이미지(self, 이미지, 가로, 세로):
        self.표만들기([가로], [세로])
        self.사진넣기배경(이미지)
        self.표테두리타입(0, 0, 0, 0)
        self.표나가기()

    def 글자취급이미지2(self, 이미지, 가로, 세로):
        self.표만들기([가로], [세로])
        self.사진넣기(이미지)
        self.표테두리타입(0, 0, 0, 0)
        self.표나가기()

    def 로고절대값(self, 이미지, 너비, 높이):
        self.표만들기([너비], [높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.표나가기2()

    def 로고절대값오른쪽정렬(self, 이미지, 너비, 높이):
        self.표만들기([너비], [높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.오른쪽정렬()
        self.표나가기2()

    def 로고절대값기본정렬(self, 이미지, 너비, 높이):
        self.표만들기([너비], [높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.기본정렬()
        self.표나가기2()

    def 소제목(self, 번호='Ⅰ', 내용=' 추진 개요', 크기=32):
        self.기본정렬()
        self.표만들기([8, 1, 크기], [9])
        self.셀여백제로()
        self.표테두리색(0, 51, 102)
        self.표배경색(0, 51, 102)
        self.표테두리굵기(8, 8, 8, 8)
        self.폰트('맑은 고딕')
        self.글자크기(18)
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.글자색(255, 255, 255)
        self.문장(번호)
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.표테두리타입(0, 0, 1, 0)
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(0, 1, 0, 0)
        self.표테두리굵기(0, 8, 0, 0)
        self.표테두리색(49, 95, 151)
        self.문장풀('맑은 고딕', 18.1, 1, 0, 내용)
        self.표나가기2()

    def 사례(self):
        self.표만들기([(205 - self.문단여백측정())], [9.5])
        self.표테두리타입(1, 1, 0, 0)
        self.표배경색(253, 254, 235)
        self.문장풀('HY헤드라인M', 16, 1, 0, ' 1. 행정안전부')
        self.표탈출()
        self.표만들기([28, (173 - self.문단여백측정())], [8, 60])
        self.표배경색(7, 66, 7)
        self.폰트('맑은 고딕')
        self.글자크기(14)
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.글자색(255, 255, 255)
        self.문장('사례')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(0, 1, 1, 0)
        self.문장풀('맑은 고딕', 14, 1, 0, '업무 자동화')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableMergeCell')
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.내어쓰기(-11.6)
        self.글자색(51, 51, 153)
        self.문장('❙')
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')
        self.문장('(기존)')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장(' 공무원, 공기업, 공공기관 등등의 한컴오피스 서식 작업을 간소화하여서 업무효율성을 향상시키고 싶습니다!')
        self.대상.HAction.Run('BreakPara')
        self.글자색(51, 51, 153)
        self.문장('❙')
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')
        self.문장('(개선)')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장(' 공무원, 공기업, 공공기관 등등의 한컴오피스 서식 작업을 간소화하여서 업무효율성을 향상시키고 싶습니다!')
        self.대상.HAction.Run('BreakPara')
        self.글자색(51, 51, 153)
        self.문장('❙')
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')
        self.문장('(업무흐름도)')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장(' 공무원, 공기업, 공공기관 등등의 한컴오피스 서식 작업을 간소화하여서 업무효율성을 향상시키고 싶습니다!')
        self.대상.HAction.Run('BreakPara')
        self.글자색(51, 51, 153)
        self.문장('❙')
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeBold')
        self.문장('(주요성과)')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장(' 공무원, 공기업, 공공기관 등등의 한컴오피스 서식 작업을 간소화하여서 업무효율성을 향상시키고 싶습니다!')
        self.표탈출()

    def 상단박스(self, 내용='~을 대상으로 ~예방 및 ~ 홍보를 위한 「~ 캠페인」 을 다음과 같이 추진하고자 합니다.'):
        self.표만들기([(205 - self.문단여백측정())], [25])
        self.표테두리타입(1, 1, 1, 1)
        self.표테두리굵기(8, 8, 8, 8)
        self.표테두리색(51, 51, 153)
        self.글자크기(16)
        self.폰트('HY헤드라인M')
        self.자간헌터(0)
        self.문단여백(5, 5)
        self.문장(내용)
        self.대상.HAction.Run('MoveRight')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    def 심플표(self, 행):
        self.표만들기([(205 - self.문단여백측정())], [5, 9])
        self.표배경색(251, 239, 212)
        self.문장('구  분')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.폰트('맑은 고딕')
        self.글자크기(12)
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.셀나누기(행, 0)
        self.표탈출()

    def 오늘날짜(self):
        self.문장((((((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜점생략(self):
        self.문장((((((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘분기(self):
        년 = datetime.today().year
        분기 = (((datetime.today().month - 1) // 3) + 1)
        self.문장(str(년) + '년 ' + str(분기) + '/4분기')

    def 오늘날짜분리월일요일(self):
        self.문장((((((str(datetime.today().month) + '. ') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 내일날짜분리년(self):
        self.문장((str((datetime.today() + timedelta(days=1)).year) + '. '))

    def 내일날짜분리월일요일(self):
        self.문장((((((str((datetime.today() + timedelta(days=1)).month) + '. ') + str((datetime.today() + timedelta(days=1)).day)) + '.(') + self.임시요일[(datetime.today() + timedelta(days=1)).weekday()]) + ')'))

    def 오늘날짜월일(self):
        self.문장((((((str(datetime.today().month) + '.') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜슬래쉬(self):
        self.문장(((((str(datetime.today().year) + '/') + str(datetime.today().month)) + '/') + str(datetime.today().day)))

    def 오늘날짜년(self):
        self.문장(str(datetime.today().year))

    def 오늘날짜년월(self):
        self.문장((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. '))

    def 오늘날짜기준(self):
        self.문장((((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '. 기준'))

    def 오늘날짜무공백(self):
        self.문장((((((((str(datetime.today().year) + '.') + str(datetime.today().month)) + '.') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜바(self):
        self.문장(((((str(datetime.today().year) + '-') + str(datetime.today().month)) + '-') + str(datetime.today().day)))

    def 오늘날짜숫자만(self):
        self.문장((((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '.'))

    def 오늘날짜숫자만무공백(self):
        self.문장((((((str(datetime.today().year) + '.') + str(datetime.today().month)) + '.') + str(datetime.today().day)) + '.'))

    def 오늘날짜월일요일무공백(self):
        self.문장((((((str(datetime.today().month) + '.') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜한글숫자만(self):
        self.문장((((((str(datetime.today().year) + '년 ') + str(datetime.today().month)) + '월 ') + str(datetime.today().day)) + '일'))

    def 오늘날짜축약(self):
        self.문장((((((((("'" + str(datetime.today().year)[-2:]) + '.') + str(datetime.today().month)) + '.') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜축약요없(self):
        self.문장((((((("'" + str(datetime.today().year)[-2:]) + '.') + str(datetime.today().month)) + '.') + str(datetime.today().day)) + '.'))

    def 오늘날짜축약공백(self):
        self.문장((((((((("'" + str(datetime.today().year)[-2:]) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜축약무공백열콤마(self):
        self.문장((((((((('‘' + str(datetime.today().year)[-2:]) + '.') + str(datetime.today().month)) + '.') + str(datetime.today().day)) + '.(') + self.임시요일[datetime.today().weekday()]) + ')'))

    def 오늘날짜축약요없열콤마(self):
        self.문장((((((('‘' + str(datetime.today().year)[-2:]) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '.'))

    def 오늘학기(self):
        학기 = '1'
        if ((datetime.today().month // 7) == 1):
            학기 = '2'
        self.문장((((str(datetime.today().year) + '학년도 ') + 학기) + '학기'))

    def 다음주간(self):
        오늘 = datetime.today()
        다음주월 = (오늘 + timedelta((7 - 오늘.weekday())))
        다음주금 = (오늘 + timedelta((11 - 오늘.weekday())))
        self.문장((((((((((((((str(다음주월.year) + '.') + str(다음주월.month)) + '.') + str(다음주월.day)) + '.(') + self.임시요일[다음주월.weekday()]) + ') ~ ') + str(다음주금.month)) + '.') + str(다음주금.day)) + '.(') + self.임시요일[다음주금.weekday()]) + ')'))

    def 다음주간월일요일(self):
        오늘 = datetime.today()
        다음주월 = (오늘 + timedelta((7 - 오늘.weekday())))
        다음주금 = (오늘 + timedelta((11 - 오늘.weekday())))
        self.문장((((((((((((str(다음주월.month) + '.') + str(다음주월.day)) + '.(') + self.임시요일[다음주월.weekday()]) + ') ~ ') + str(다음주금.month)) + '.') + str(다음주금.day)) + '.(') + self.임시요일[다음주금.weekday()]) + ')'))

    def 다다음주간월일요일(self):
        오늘 = datetime.today()
        다음주월 = (오늘 + timedelta((14 - 오늘.weekday())))
        다음주금 = (오늘 + timedelta((18 - 오늘.weekday())))
        self.문장((((((((((((str(다음주월.month) + '.') + str(다음주월.day)) + '.(') + self.임시요일[다음주월.weekday()]) + ') ~ ') + str(다음주금.month)) + '.') + str(다음주금.day)) + '.(') + self.임시요일[다음주금.weekday()]) + ')'))

    def 다음월간월일요일(self):
        오늘 = datetime.today()
        if (오늘.month == 12):
            다음달1일 = datetime((오늘.year + 1), 1, 1)
        else:
            다음달1일 = datetime(오늘.year, (오늘.month + 1), 1)
        if (다음달1일.month == 12):
            다음달말 = (datetime((다음달1일.year + 1), 1, 1) - timedelta(days=1))
        else:
            다음달말 = (datetime(다음달1일.year, (다음달1일.month + 1), 1) - timedelta(days=1))
        self.문장((((((((((((str(다음달1일.month) + '.') + str(다음달1일.day)) + '.(') + self.임시요일[다음달1일.weekday()]) + ') ~ ') + str(다음달말.month)) + '.') + str(다음달말.day)) + '.(') + self.임시요일[다음달말.weekday()]) + ')'))

    def 윗첨자입력(self, 입력):
        self.대상.HAction.Run('CharShapeNormal')
        self.대상.HAction.Run('CharShapeSuperscript')
        self.문장(입력)

    def 점선박스(self):
        self.표만들기([((197 - self.문단여백측정()) / 3), ((197 - self.문단여백측정()) / 3), ((197 - self.문단여백측정()) / 3)], [1, 1, 30])
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.대상.HAction.Run('Cancel')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableLeftCell')
        self.표테두리타입(3, 3, 3, 3)
        self.표배경색(242, 242, 242)
        self.대상.HAction.Run('Cancel')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableRightCell')
        self.대상.HAction.Run('TableRightCell')
        self.글자크기(6)
        self.대상.HAction.Run('Cancel')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableLowerCell')
        self.대상.HAction.Run('TableMergeCell')
        self.문장풀('맑은 고딕', 13, 1, 1, '<점선박스제목입니다>')
        self.대상.HAction.Run('TableLowerCell')
        self.대상.HAction.Run('TableCellBlockRow')
        self.대상.HAction.Run('TableMergeCell')
        self.문장풀('맑은 고딕', 12, 0, 0, ' ▸ 내용을 작성하세요!')
        self.표탈출()

    def 제목목차(self):
        self.대상.MovePos(2)
        self.문장풀('HY헤드라인M', 20, 0, 0, '이미지 넣기')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.표만들기([(205 - self.문단여백측정())], [40])
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(12, 12, 1, 1)
        self.표테두리색(102, 153, 255)
        self.문장풀('HY헤드라인M', 30, 0, 1, (str(datetime.today().year) + '년 사업계획'))
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' ')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 1, (((((str(datetime.today().year) + '. ') + str(datetime.today().month)) + '. ') + str(datetime.today().day)) + '.'))
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 26, 0, 1, '행정안전부')
        self.대상.HAction.Run('BreakPage')
        self.표만들기([1, 1, 1, 45, 1, 1, 1], [11])
        self.셀여백제로()
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.표배경색(51, 102, 255)
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(224, 229, 250)
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('HY헤드라인M', 28, 0, 1, '목  차')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(224, 229, 250)
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.대상.HAction.Run('TableResizeExLeft')
        self.표배경색(51, 102, 255)
        self.대상.HAction.Run('TableCellBlockRow')
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.대상.HAction.Run('CloseEx')
        self.대상.HAction.Run('MoveLineEnd')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.대상.HAction.Run('BreakPara')
        self.표만들기([(205 - self.문단여백측정())], [210])
        self.표테두리굵기(6, 6, 6, 6)
        self.표테두리색(81, 75, 172)
        self.줄간격(280)
        self.문장풀('HY헤드라인M', 20, 0, 0, ' Ⅰ. 사업개요')
        self.탭점선설정()
        self.대상.HAction.Run('InsertTab')
        self.문장(' 1')
        self.대상.HAction.Run('BreakPara')
        self.문장(' Ⅱ. 세부내용')
        self.대상.HAction.Run('InsertTab')
        self.문장(' 2')
        self.대상.HAction.Run('BreakPara')
        self.문장(' Ⅲ. 추진과제')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, '    1. 추진기반 구축')
        self.대상.HAction.Run('InsertTab')
        self.문장(' 3')
        self.대상.HAction.Run('BreakPara')
        self.문장('    2. 과제발굴 및 확산')
        self.대상.HAction.Run('InsertTab')
        self.문장(' 4')
        self.대상.HAction.Run('BreakPara')
        self.문장('    3. 추진 역량강화')
        self.대상.HAction.Run('InsertTab')
        self.문장(' 5')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('HY헤드라인M', 20, 0, 0, ' Ⅳ. 추진일정')
        self.대상.HAction.Run('InsertTab')
        self.문장(' 6')
        self.대상.HAction.Run('BreakPara')
        self.표탈출()

    def 중제목(self):
        self.표만들기([(205 - self.문단여백측정())], [12])
        self.표테두리타입(1, 1, 0, 0)
        self.표테두리굵기(8, 8, 8, 8)
        self.표테두리색(51, 51, 153)
        self.문장풀('HY헤드라인M', 20, 1, 1, '제목을 쓰세요!')
        self.표탈출()

    def 참고(self, 내용='참고자료'):
        self.표만들기([18, 1, (182 - self.문단여백측정())], [10])
        self.셀여백제로()
        self.표테두리타입(1, 1, 1, 1)
        self.표테두리굵기(1, 1, 1, 1)
        self.표테두리색(35, 35, 106)
        self.표배경색(35, 35, 106)
        self.폰트('HY헤드라인M')
        self.글자크기(16)
        self.글자색(255, 255, 255)
        self.가운데정렬()
        self.문장('참고')
        self.표오른쪽(1)
        self.표너비줄이기(3)
        self.표테두리타입(0, 0, 1, 1)
        self.표오른쪽(1)
        self.문장풀('HY헤드라인M', 20, 0, 0, (' ' + 내용))
        self.표나가기2()

    def 텍스트새창(self, 텍스트, 좌, 우, 상, 하, 머리, 꼬리):
        self.새창()
        self.문서여백(좌, 우, 상, 하, 머리, 꼬리)
        self.문장(텍스트)

    def 텍스트로붙이기(self):
        self.대상.HAction.Run('Copy')
        self.자동번호해제()
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총.Execute(총알)
        self.대상.HAction.Run('PasteTextOnly')

    def 행안부제목(self):
        self.표만들기([(205 - self.문단여백측정())], [12])
        self.표테두리타입(1, 1, 1, 1)
        self.표테두리굵기(6, 6, 6, 6)
        self.표배경색(223, 230, 247)
        self.문장풀('맑은 고딕', 20, 1, 1, '제목')
        self.표나가기()

    def 행안부참고(self):
        self.표만들기([17, (184 - self.문단여백측정())], [9])
        self.표테두리타입(1, 1, 1, 1)
        self.표테두리굵기(1, 1, 1, 1)
        self.표배경색(223, 230, 247)
        self.문장풀('맑은 고딕', 17, 1, 1, '참고1')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 17, 1, 0, ' 참고1의 제목')
        self.표탈출()

    def 행안부초록표(self):
        self.표만들기([30, (172 - self.문단여백측정())], [9, 7, 7, 7, 7, 7, 7])
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 15, 1, 1, '제목')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 15, 1, 0, '○○○ 신고 절차 간소화로 ○○○ 편의 개선')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '제출기관/부서')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, '○○○○부 ○○○○실 ○○○○국 ○○○○과')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '담당자/연락처')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, '○○○ 사무관, 044-2xx-3xxx (휴대전화번호를 추가로 써도 됨)')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '전자우편')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, 'id____@korea.kr')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '분야')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, '일하는 방식 개선   ※ ')
        self.글자색(255, 129, 0)
        self.문장('분야가 구분되어 있지 않은 경우 셀 삭제')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '관련 수상 이력')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, '없음 (다른 경진대회에서 수상한 적이 있다면 그 내용을 작성)')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 12, 0, 1, '관련 제출 이력')
        self.대상.HAction.Run('TableRightCellAppend')
        self.문장풀('맑은 고딕', 12, 0, 0, '없음 (유사한 경진대회에 제출한 적이 있다면 그 내용을 작성)')
        self.표탈출()

    def 형광펜(self, 빨강, 초록, 파랑):
        self.대상.HAction.GetDefault('MarkPenShape', self.대상.HParameterSet.HMarkpenShape.HSet)
        self.대상.HParameterSet.HMarkpenShape.Color = self.대상.RGBColor(빨강, 초록, 파랑)
        self.대상.HAction.Execute('MarkPenShape', self.대상.HParameterSet.HMarkpenShape.HSet)

    def 형광펜제거(self):
        self.대상.HAction.GetDefault('MarkPenShape', self.대상.HParameterSet.HMarkpenShape.HSet)
        self.대상.HParameterSet.HMarkpenShape.Color = 4294967295
        self.대상.HAction.Execute('MarkPenShape', self.대상.HParameterSet.HMarkpenShape.HSet)

    def PDF를한컴으로(self):
        파일목록 = self.파일목록()
        파일목록변환 = '|'.join(파일목록)
        파일목록변환 = 파일목록변환.replace('/', '\\')
        for i in range(0, len(파일목록)):
            self.대상.Run('CallPDFConverter')
        총 = self.대상.CreateAction('FileOpenPDF')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Attributes', 65536)
        총알.SetItem('FileName', 파일목록변환)
        총알.SetItem('OpenFlag', 0)
        총.Execute(총알)

    def 비전표(self, 이미지):
        self.소제목('Ⅱ', ' 비전 및 추진전략', 55)
        self.표만들기([19, 1, (175 - self.문단여백측정())], [13, 14, 22, 14, 11, 1, 9, 1, 9, 1, 9, 3, 11, 1, 9, 1, 9, 1, 9, 3, 11, 1, 9, 1, 9, 1, 9])
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.폰트('맑은 고딕')
        self.글자크기(1)
        self.줄간격(120)
        self.캔슬()
        self.표처음()
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(32, 58, 123)
        self.폰트('맑은 고딕')
        self.글자크기(17)
        self.진하게()
        self.가운데정렬()
        self.글자색(255, 255, 255)
        self.문장('비전')
        self.표오른쪽(2)
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(223, 230, 247)
        self.문장풀('맑은 고딕', 17, 1, 1, '업무자동화를 통한 정부 생산성 제고')
        self.표오른쪽(3)
        self.사진넣기(이미지)
        self.표오른쪽(1)
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(48, 87, 185)
        self.진하게()
        self.가운데정렬()
        self.글자색(255, 255, 255)
        self.폰트('맑은 고딕')
        self.글자크기(17)
        self.문장('추진')
        self.엔터(1)
        self.문장('전략')
        self.표오른쪽(2)
        self.셀나누기(23, 1)
        self.셀선택()
        self.표오른쪽(6)
        self.셀병합()
        self.셀선택()
        self.셀나누기(1, 2)
        self.대상.HAction.Run('TableDistributeCellHeight')
        self.캔슬()
        self.표오른쪽(2)
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableMergeCell')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.셀나누기(1, 2)
        self.대상.HAction.Run('TableDistributeCellHeight')
        self.대상.HAction.Run('Cancel')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableMergeCell')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.셀나누기(1, 2)
        self.대상.HAction.Run('TableDistributeCellHeight')
        self.대상.HAction.Run('Cancel')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableLeftCell')
        self.표테두리타입(1, 3, 1, 1)
        self.표배경색(255, 231, 216)
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.글자색(0, 0, 255)
        self.폰트('맑은 고딕')
        self.글자크기(13)
        self.문장('추진기반 구축')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(1, 3, 1, 1)
        self.표배경색(255, 247, 204)
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.글자색(0, 0, 255)
        self.폰트('맑은 고딕')
        self.글자크기(13)
        self.문장('과제발굴 및 확산')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(1, 3, 1, 1)
        self.표배경색(205, 242, 228)
        self.대상.HAction.Run('CharShapeBold')
        self.대상.HAction.Run('ParagraphShapeAlignCenter')
        self.글자색(0, 0, 255)
        self.폰트('맑은 고딕')
        self.글자크기(13)
        self.문장('추진 역량강화')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(3, 1, 1, 1)
        self.문장풀('맑은 고딕', 12, 1, 1, '무엇을 위한')
        self.대상.HAction.Run('BreakPara')
        self.문장('기반구축')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(3, 1, 1, 1)
        self.문장풀('맑은 고딕', 12, 1, 1, '범정부적')
        self.대상.HAction.Run('BreakPara')
        self.문장('발굴 지원 및 확산')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(3, 1, 1, 1)
        self.문장풀('맑은 고딕', 12, 1, 1, '무엇을 통한')
        self.대상.HAction.Run('BreakPara')
        self.문장('역량강화')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.사진넣기(이미지)
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(255, 231, 216)
        self.문장풀('맑은 고딕', 13, 1, 0, ' [추진기반 구축] 성공적인 ~을 위한 기반 구축')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 기관별 무엇 책임관 지정')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 관련 민·관·학 협업체계 구축')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 도입‧활용 가이드라인 마련')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(255, 247, 204)
        self.문장풀('맑은 고딕', 13, 1, 0, ' [과제발굴 및 확산] 범정부적 무엇 과제발굴 지원 및 확산')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 설명회 개최')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 우수사례 선정 및 확산')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 전용 커뮤니티 개설 운영')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(205, 242, 228)
        self.문장풀('맑은 고딕', 13, 1, 0, ' [추진 역량강화] 교육‧훈련을 통한 무엇 역량 강화')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 컨설팅 지원')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 무엇 교육‧훈련 프로그램 신설‧운영')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.대상.HAction.Run('TableRightCellAppend')
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 12, 1, 0, ' ▸ 기관별 연구모임 구성‧운영 지원')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableLeftCell')
        self.대상.HAction.Run('TableCellBlock')
        self.대상.HAction.Run('TableCellBlockExtend')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableUpperCell')
        self.대상.HAction.Run('TableMergeCell')
        self.표테두리타입(1, 1, 1, 1)
        self.표배경색(242, 242, 242)
        self.문장풀('맑은 고딕', 17, 1, 1, '추진')
        self.대상.HAction.Run('BreakPara')
        self.문장('과제')
        self.표탈출()

    def 행안부표준보고(self):
        self.행안부제목()
        self.대상.HAction.Run('BreakPara')
        self.자간헌터(1)
        self.내어쓰기(0)
        self.글자간격(0)
        self.줄간격(140)
        self.글자장평(100)
        self.글자음영(4294967295)
        self.문단여백(0, 0)
        self.문장풀('맑은 고딕', 15, 1, 0, '□ 목차 제목')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장(' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('   - 이 부분에 상세내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 15, 1, 0, '□ 목차 제목')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('   - 이 부분에 상세내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 12, 0, 0, '    ※ 이 부분에 참고사항을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용')
        self.대상.HAction.Run('CharShapeSuperscript')
        self.문장('*')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장('을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('   - 이 부분에 상세내용')
        self.대상.HAction.Run('CharShapeSuperscript')
        self.문장('**')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장('을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 12, 0, 0, '     * 이 부분에 첫 번째 주석내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('    ** 이 부분에 두 번째 주석내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 15, 1, 0, '□ 목차 제목')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 12, 0, 0, '    ※ 이 부분에 참고사항을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용')
        self.대상.HAction.Run('CharShapeSuperscript')
        self.문장('*')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장('을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('   - 이 부분에 상세내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 12, 0, 0, '     * 이 부분에 첫 번째 주석내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('맑은 고딕', 15, 1, 0, '□ 목차 제목')
        self.대상.HAction.Run('BreakPara')
        self.대상.HAction.Run('CharShapeNormal')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성 ')
        self.문장풀('휴먼명조', 13, 0, 0, '(12월 초순)')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, '   - 이 부분에 상세내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성 ')
        self.문장풀('휴먼명조', 13, 0, 0, '(12월 초순)')
        self.대상.HAction.Run('BreakPage')
        self.행안부참고()
        self.문장풀('맑은 고딕', 15, 1, 0, '□ 목차 제목')
        self.대상.HAction.Run('BreakPara')
        self.문장풀('휴먼명조', 15, 0, 0, ' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장(' ○ 이 부분에 주요내용을 작성')
        self.대상.HAction.Run('BreakPara')
        self.문장('   - 이 부분에 상세내용을 작성')

    def 글자위치(self, 값):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('OffsetUser', 값)
        총알.SetItem('OffsetSymbol', 값)
        총알.SetItem('OffsetOther', 값)
        총알.SetItem('OffsetJapanese', 값)
        총알.SetItem('OffsetHanja', 값)
        총알.SetItem('OffsetLatin', 값)
        총알.SetItem('OffsetHangul', 값)
        총.Execute(총알)

    def 꼬릿말(self):
        총 = self.대상.CreateAction('HeaderFooter')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('HeaderFooterStyle', 0)
        총알.SetItem('HeaderFooterCtrlType', 1)
        총.Execute(총알)

    def 다단(self):
        총 = self.대상.CreateAction('MultiColumn')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Count', 2)
        총알.SetItem('SameGap', self.대상.MiliToHwpUnit(8))
        총알.SetItem('LineType', self.대상.HwpLineType('Solid'))
        총알.SetItem('LineWidth', self.대상.HwpLineWidth('0.12mm'))
        총알.SetItem('ApplyClass', 864)
        총알.SetItem('ApplyTo', 5)
        총.Execute(총알)

    def 색상다단(self, 종류, 갭, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('MultiColumn')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Count', 2)
        총알.SetItem('SameGap', self.대상.MiliToHwpUnit(갭))
        총알.SetItem('LineType', 종류)
        총알.SetItem('LineWidth', self.대상.HwpLineWidth('0.12mm'))
        총알.SetItem('LineColor', self.대상.RGBColor(빨강, 초록, 파랑))
        총알.SetItem('ApplyClass', 864)
        총알.SetItem('ApplyTo', 5)
        총.Execute(총알)

    def 문서가로돌리기(self):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.Landscape = 1
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 4)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서세로돌리기(self):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.Landscape = 0
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 4)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서여백B4(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리, 타입):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.PaperWidth = self.대상.MiliToHwpUnit(257)
        self.대상.HParameterSet.HSecDef.PageDef.PaperHeight = self.대상.MiliToHwpUnit(364)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 타입)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서여백A4(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리, 타입):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 타입)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서여백A4가로(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.PageDef.Landscape = 1
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 3)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 문서여백A3가로(self, 왼쪽, 오른쪽, 위, 아래, 머리, 꼬리):
        self.대상.HAction.GetDefault('PageSetup', self.대상.HParameterSet.HSecDef.HSet)
        self.대상.HParameterSet.HSecDef.PageDef.PaperWidth = self.대상.MiliToHwpUnit(297)
        self.대상.HParameterSet.HSecDef.PageDef.PaperHeight = self.대상.MiliToHwpUnit(420)
        self.대상.HParameterSet.HSecDef.PageDef.LeftMargin = self.대상.MiliToHwpUnit(왼쪽)
        self.대상.HParameterSet.HSecDef.PageDef.RightMargin = self.대상.MiliToHwpUnit(오른쪽)
        self.대상.HParameterSet.HSecDef.PageDef.TopMargin = self.대상.MiliToHwpUnit(위)
        self.대상.HParameterSet.HSecDef.PageDef.BottomMargin = self.대상.MiliToHwpUnit(아래)
        self.대상.HParameterSet.HSecDef.PageDef.HeaderLen = self.대상.MiliToHwpUnit(머리)
        self.대상.HParameterSet.HSecDef.PageDef.FooterLen = self.대상.MiliToHwpUnit(꼬리)
        self.대상.HParameterSet.HSecDef.PageDef.Landscape = 1
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyClass', 24)
        self.대상.HParameterSet.HSecDef.HSet.SetItem('ApplyTo', 3)
        self.대상.HAction.Execute('PageSetup', self.대상.HParameterSet.HSecDef.HSet)

    def 신명중명조(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양신명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '신명 신명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '신명 중명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '신명 중명조')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '신명 중명조')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 견고딕(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양중고딕')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양중고딕')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양중고딕')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '한양견고딕')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '한양견고딕')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 견명조(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양신명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양신명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양신명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '한양견명조')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '한양견명조')
        총알.SetItem('FontTypeHangul', 2)
        총.Execute(총알)

    def 타임즈뉴로만(self):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', 'Times New Roman')
        총알.SetItem('FontTypeUser', 1)
        총알.SetItem('FaceNameSymbol', 'Times New Roman')
        총알.SetItem('FontTypeSymbol', 1)
        총알.SetItem('FaceNameOther', 'Times New Roman')
        총알.SetItem('FontTypeOther', 1)
        총알.SetItem('FaceNameJapanese', '가는안상수체')
        총알.SetItem('FontTypeJapanese', 1)
        총알.SetItem('FaceNameHanja', '가는안상수체')
        총알.SetItem('FontTypeHanja', 1)
        총알.SetItem('FaceNameLatin', 'Times New Roman')
        총알.SetItem('FontTypeLatin', 1)
        총알.SetItem('FaceNameHangul', '가는안상수체')
        총알.SetItem('FontTypeHangul', 1)
        총.Execute(총알)

    def 신명조크기(self, 크기):
        총 = self.대상.CreateAction('CharShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('FaceNameUser', '명조')
        총알.SetItem('FontTypeUser', 2)
        총알.SetItem('FaceNameSymbol', '한양신명조')
        총알.SetItem('FontTypeSymbol', 2)
        총알.SetItem('FaceNameOther', '한양신명조')
        총알.SetItem('FontTypeOther', 2)
        총알.SetItem('FaceNameJapanese', '한양신명조')
        총알.SetItem('FontTypeJapanese', 2)
        총알.SetItem('FaceNameHanja', '한양신명조')
        총알.SetItem('FontTypeHanja', 2)
        총알.SetItem('FaceNameLatin', '한양신명조')
        총알.SetItem('FontTypeLatin', 2)
        총알.SetItem('FaceNameHangul', '한양신명조')
        총알.SetItem('FontTypeHangul', 2)
        총알.SetItem('Height', (크기 * 100))
        총.Execute(총알)

    def 구분선(self):
        self.표만들기([102], [1])
        self.표테두리타입(1, 0, 0, 0)
        self.표나가기2()

    def 궁극의정리줄선택(self):
        self.대상.MovePos(6)
        self.대상.HAction.Run('Select')
        self.대상.MovePos(7)
