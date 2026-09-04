# Source Generated with Decompyle++
# File: ���Ķ��̺귯��_�⺻.marshal (Python 3.13)

import pythoncom
from win32com.client.gencache import EnsureDispatch
from tkinter import filedialog
from datetime import datetime, timedelta
import re
from decimal import Decimal
import os
import json

def 랜덤정수(최대정수):
    return os.urandom(None(4), byteorder = 'big') % 최대정수


def 랜덤선택(리스트):
    최대정수 = len(리스트)
    뽑는순서 = os.urandom(None(4), byteorder = 'big') % 최대정수
    return 리스트[뽑는순서]


def 한컴기본():
    '''\xed\x95\x9c\xec\xbb\xb4\xea\xb8\xb0\xeb\xb3\xb8'''
    __firstlineno__ = 20
    대상 = None
    글머리 = '  - '
    셀높이 = 1000
    셀넓이 = 1000
    문서용지 = [
        0,
        0,
        0,
        0,
        0,
        0]
    임시요일 = [
        '월',
        '화',
        '수',
        '목',
        '금',
        '토',
        '일']
    임시카운트 = 0
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
    원숫자 = [
        '',
        '①',
        '②',
        '③',
        '④',
        '⑤',
        '⑥',
        '⑦',
        '⑧',
        '⑨',
        '⑩',
        '⑪',
        '⑫',
        '⑬',
        '⑭',
        '⑮']
    네모숫자 = [
        '',
        '󰊱',
        '󰊲',
        '󰊳',
        '󰊴',
        '󰊵',
        '󰊶',
        '󰊷',
        '󰊸',
        '󰊹']
    가숫자 = [
        '',
        '가',
        '나',
        '다',
        '라',
        '마',
        '바',
        '사',
        '아',
        '자',
        '차',
        '카',
        '타',
        '파',
        '하']
    패브릭스바옵션 = 1
    중제목카운트 = 0
    소제목카운트 = 0
    참고카운트 = 0
    붙임카운트 = 0
    가제목카운트 = 0
    원숫자카운트 = 0
    네모숫자카운트 = 0
    궁극의정리위치보정 = 0
    위치저장 = 0
    방금처리 = 0
    
    def 방금처리0(self):
        self.방금처리 = 0

    
    def 한컴열기(self):
        기존한컴 = False
        바인딩내용 = None(0)
        실행중객체테이블 = None()
        실행중객체이름들 = 실행중객체테이블.EnumRunning()
        for 실행중객체이름 in 실행중객체이름들:
            
            try:
                이름 = 실행중객체이름.GetDisplayName(바인딩내용, 실행중객체이름)
                if 이름.startswith('!HwpObject'):
                    pass
                if 이름.startswith('!HwpObject'):
                    찾은객체 = 실행중객체테이블.GetObject(실행중객체이름)
                    self.대상 = EnsureDispatch(찾은객체.QueryInterface(pythoncom.IID_IDispatch))
                    if self.대상:
                        기존한컴 = True
                    

        pythoncom.CreateBindCtx
        if 기존한컴:
            pass
        if not 기존한컴:
            
            try:
                self.대상 = EnsureDispatch('hwpframe.hwpobject')
                self.대상.XHwpWindows.Item(0).Visible = True
                self.문서여백(20, 20, 15, 15, 10, 10)
            except ValueError:
                e = None
                print(f'''값 오류 : {e}''')

            return None
            return None
            if ValueError:
                e = None
                print(f'''값 오류 : {e}''')
                e = None
                del e
                continue
                e = None
                del e
        if Exception:
            오류 = None
            print(f'''[오류] 실행중 객체 확인 중 문제 발생: {오류}''')
            오류 = None
            del 오류
            continue
            오류 = None
            del 오류
        if Exception:
            오류 = None
            print(f'''[오류] 새로운 한컴 객체 생성 중 문제 발생: {오류}''')
            오류 = None
            del 오류
            return None
            오류 = None
            del 오류

    
    def 불러오기(self):
        
        try:
            self.대상.HAction.Run('FileOpen')
        except ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            한컴 = EnsureDispatch('HWPFrame.HwpObject')
            한컴.XHwpWindows.Item(0).Visible = True
            self.대상 = 한컴
            self.대상.HAction.Run('FileOpen')

        return None
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            한컴 = EnsureDispatch('HWPFrame.HwpObject')
            한컴.XHwpWindows.Item(0).Visible = True
            self.대상 = 한컴
            self.대상.HAction.Run('FileOpen')
            e = None
            del e
            return None
            e = None
            del e

    
    def 새창(self):
        
        try:
            self.대상.HAction.Run('FileNew')
            self.문서여백(20, 20, 15, 15, 10, 10)
        except ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            한컴 = EnsureDispatch('HWPFrame.HwpObject')
            한컴.XHwpWindows.Item(0).Visible = True
            self.대상 = 한컴
            self.문서여백(20, 20, 15, 15, 10, 10)

        return None
        if Exception:
            e = None
            print(f'''값 오류 : {e}''')
            한컴 = EnsureDispatch('HWPFrame.HwpObject')
            한컴.XHwpWindows.Item(0).Visible = True
            self.대상 = 한컴
            self.문서여백(20, 20, 15, 15, 10, 10)
            e = None
            del e
            return None
            e = None
            del e

    
    def 가운데정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignCenter')

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 고정여백(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    
    def 객체찾기(self):
        self.대상.FindCtrl()

    
    def 기본정렬(self):
        self.대상.HAction.Run('ParagraphShapeAlignJustify')

    
    def 기본글자(self):
        self.대상.HAction.Run('CharShapeNormal')

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 글자작게(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 글자크게(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    
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

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 엔터(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    
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

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 표너비줄이기(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 표높이줄이기(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 표오른쪽(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    
    def 표오른쪽끝(self):
        self.대상.MovePos(105)

    
    def 표왼쪽끝(self):
        self.대상.MovePos(104)

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
pass):
        
        def 표왼쪽(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    pass

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
continueNone):
        
        def 표아래쪽(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    continue
                    return None

    if (lambda self, 횟수: for None in range(0, 횟수):
if None:
continueNone):
        
        def 표위쪽(self, 횟수):
            for None in range(0, 횟수):
                if None:
                    continue
                    return None

    
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
        return [
            높이,
            너비]

    
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

    if (lambda self, 간격: 총 = self.대상.CreateAction('CharShape')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('SpacingJapanese', 간격)총알.SetItem('SpacingHanja', 간격)총알.SetItem('SpacingLatin', 간격)총알.SetItem('SpacingHangul', 간격)총알.SetItem('SpacingUser', 간격)총알.SetItem('SpacingSymbol', 간격)총알.SetItem('SpacingOther', 간격)총.Execute(총알)):
        
        def 글자간격(self, 간격):
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

    if (lambda self, 간격: 총 = self.대상.CreateAction('CharShape')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('ShadowType', self.대상.CharShadowType('Drop'))총알.SetItem('ShadowOffsetY', 간격)총알.SetItem('ShadowOffsetX', 간격)총.Execute(총알)):
        
        def 글자그림자(self, 간격):
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
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Apply', 번호)
        총.Execute(총알)

    
    def 글자스타일조회(self):
        총 = self.대상.CreateAction('Style')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        return 총알.Item('Apply')

    if (lambda self, 색상: 총 = self.대상.CreateAction('CharShape')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('ShadeColor', 색상)총.Execute(총알)):
        
        def 글자음영(self, 색상):
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
        총알.SetItem('Height', 크기 * 100)
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
        서브총알.SetItem('Height', 크기 * 100)
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

    
    def 글자폰트바꾸기(self, 폰트1, 폰트2):
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
        총.Execute(총알)

    
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

    if (lambda self, 파일명: 총 = self.대상.CreateAction('InsertFile')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('FileName', 파일명)총.Execute(총알)):
        
        def 끼워넣기(self, 파일명):
            총 = self.대상.CreateAction('InsertFile')
            총알 = 총.CreateSet()
            총.GetDefault(총알)
            총알.SetItem('FileName', 파일명)
            총.Execute(총알)

    
    def 내어쓰기(self, 값):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Indentation', self.대상.PointToHwpUnit(값 * 2))
        총.Execute(총알)

    
    def 내용만붙이기(self):
        총 = self.대상.CreateAction('Paste')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Option', 5)
        총.Execute(총알)

    if (lambda self, 선종류, 선굵기: 총 = self.대상.CreateAction('CellBorder')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('DiagonalWidth', 선굵기)if 선종류 == '앞':
총알.SetItem('SlashFlag', 2)총알.SetItem('BackSlashFlag', 0)if 선종류 == '뒤':
총알.SetItem('SlashFlag', 0)총알.SetItem('BackSlashFlag', 2)총.Execute(총알)):
        
        def 대각선(self, 선종류, 선굵기):
            총 = self.대상.CreateAction('CellBorder')
            총알 = 총.CreateSet()
            총.GetDefault(총알)
            총알.SetItem('DiagonalWidth', 선굵기)
            if 선종류 == '앞':
                총알.SetItem('SlashFlag', 2)
            총알.SetItem('BackSlashFlag', 0)
            if 선종류 == '뒤':
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
        총알.SetItem('LeftMargin', self.대상.PointToHwpUnit(좌측 * 2))
        총알.SetItem('RightMargin', self.대상.PointToHwpUnit(우측 * 2))
        총.Execute(총알)

    
    def 문단여백측정(self):
        총 = self.대상.CreateAction('PageSetup')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.Item('PageDef')
        return round((서브총알.Item('LeftMargin') + 서브총알.Item('RightMargin')) / 283.4, 1)

    
    def 문단여백측정세로(self):
        총 = self.대상.CreateAction('PageSetup')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.Item('PageDef')
        return round((서브총알.Item('TopMargin') + 서브총알.Item('BottomMargin') + 서브총알.Item('HeaderLen') + 서브총알.Item('FooterLen')) / 283.4, 1)

    
    def 문단위(self, 간격):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('PrevSpacing', 간격 * 200)
        총.Execute(총알)

    
    def 문단아래(self, 간격):
        총 = self.대상.CreateAction('ParagraphShape')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('NextSpacing', 간격 * 200)
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
        self.문서용지 = [
            서브총알.Item('LeftMargin'),
            서브총알.Item('RightMargin'),
            서브총알.Item('TopMargin'),
            서브총알.Item('BottomMargin'),
            서브총알.Item('HeaderLen'),
            서브총알.Item('FooterLen')]

    
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

    if (lambda self, 상, 하, 좌, 우, 선타입, 선굵기, 선색: 총 = self.대상.CreateAction('PageBorder')총알 = 총.CreateSet()총.GetDefault(총알)서브총알 = 총알.CreateItemSet('PageBorderFillBoth', 'PageBorderFill')서브총알.SetItem('OffsetTop', self.대상.MiliToHwpUnit(상))서브총알.SetItem('OffsetBottom', self.대상.MiliToHwpUnit(하))서브총알.SetItem('OffsetLeft', self.대상.MiliToHwpUnit(좌))서브총알.SetItem('OffsetRight', self.대상.MiliToHwpUnit(우))서브총알.SetItem('BorderTypeLeft', 선타입)서브총알.SetItem('BorderTypeRight', 선타입)서브총알.SetItem('BorderTypeTop', 선타입)서브총알.SetItem('BorderTypeBottom', 선타입)서브총알.SetItem('BorderWidthLeft', 선굵기)서브총알.SetItem('BorderWidthRight', 선굵기)서브총알.SetItem('BorderWidthTop', 선굵기)서브총알.SetItem('BorderWidthBottom', 선굵기)서브총알.SetItem('BorderCorlorLeft', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))서브총알.SetItem('BorderColorRight', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))서브총알.SetItem('BorderColorTop', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))서브총알.SetItem('BorderColorBottom', self.대상.RGBColor(선색[0], 선색[1], 선색[2]))총알.SetItem('ApplyToPageBorderFill', 3)총.Execute(총알)):
        
        def 문서테두리(self, 상, 하, 좌, 우, 선타입, 선굵기, 선색):
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

    
    def 블록전체스캔(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        결과텍스트 = []
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                텍스트 = 텍스트.replace('\r', '').replace('\n', '')
                결과텍스트.append(텍스트)
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        return 결과텍스트
        if ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e

    
    def 블록문장스캔(self):
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
        return 결과텍스트
        if ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e

    
    def 사진(self, 종류):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            이름 = None(title = 'Open File', filetypes = [
                ('image files', ('.png', '.jpg'))])
            for i in range(len(이름)):
                if not i == 0:
                    pass
                self.대상.HAction.Run('TableRightCellAppend')
                if 종류 == '배경':
                    self.대상.InsertBackgroundPicture('SelectedCell', 이름[i], 1, 5, 0, 0, 0, 0)
                    continue
                if not 종류 == '비율':
                    continue
                self.대상.InsertPicture(이름[i], 1, 3, 0, 0, 0)
        return None

    
    def 사진넣기(self, 이미지):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.InsertPicture(이미지, 1, 3, 0, 0, 0)
            self.대상.HAction.Run('ParagraphShapeAlignCenter')
        return None

    
    def 사진넣기그냥(self, 이미지, 너비, 높이):
        self.대상.InsertPicture(이미지, 1, 1, 0, 0, 0, 너비, 높이)

    
    def 사진넣기배경(self, 이미지):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.InsertBackgroundPicture('SelectedCell', 이미지, 1, 5, 0, 0, 0, 0)
        return None

    
    def 사진넣기절대값(self, 이미지, 너비, 높이):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.InsertPicture(이미지, 1, 1, 0, 0, 0, 너비, 높이)
            self.대상.HAction.Run('ParagraphShapeAlignCenter')
        return None

    
    def 상단캡션(self):
        self.대상.HAction.Run('ShapeObjAttachCaption')
        총 = self.대상.CreateAction('TablePropertyDialog')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        서브총알 = 총알.CreateItemSet('ShapeCaption', 'Caption')
        서브총알.SetItem('Side', 2)
        서브총알.SetItem('Gap', self.대상.MiliToHwpUnit(1))
        총.Execute(총알)

    if (lambda self, 행수, 열수: self.대상.HAction.GetDefault('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)self.대상.HParameterSet.HTableSplitCell.Rows = 열수self.대상.HParameterSet.HTableSplitCell.Cols = 행수self.대상.HAction.Execute('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)):
        
        def 셀나누기(self, 행수, 열수):
            self.대상.HAction.GetDefault('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)
            self.대상.HParameterSet.HTableSplitCell.Rows = 열수
            self.대상.HParameterSet.HTableSplitCell.Cols = 행수
            self.대상.HAction.Execute('TableSplitCell', self.대상.HParameterSet.HTableSplitCell.HSet)

    
    def 셀높이넓이복사(self):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            총 = self.대상.CreateAction('TablePropertyDialog')
            총알 = 총.CreateSet()
            서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')
            총.GetDefault(총알)
            self.셀높이 = 서브총알.Item('Height')
            self.셀넓이 = 서브총알.Item('Width')
        return None

    
    def 셀높이붙여넣기(self):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Height = self.셀높이
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        return None

    
    def 셀높이지정(self, 크기):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Height = 크기
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        return None

    
    def 셀넓이붙여넣기(self):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Width = self.셀넓이
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        return None

    
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
        총알.SetItem('CellMarginBottom', self.대상.MiliToHwpUnit(0))
        총알.SetItem('CellMarginTop', self.대상.MiliToHwpUnit(0))
        총알.SetItem('CellMarginRight', self.대상.MiliToHwpUnit(0))
        총알.SetItem('CellMarginLeft', self.대상.MiliToHwpUnit(0))
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

    
    def 셀전체크기(self):
        if (lambda : 총 = self.대상.CreateAction('PageSetup')총알 = 총.CreateSet()총.GetDefault(총알)서브총알 = 총알.Item('PageDef')서브총알.Item('LeftMargin') + 서브총알.Item('RightMargin')):
            
            def 페이지넓이():
                총 = self.대상.CreateAction('PageSetup')
                총알 = 총.CreateSet()
                총.GetDefault(총알)
                서브총알 = 총알.Item('PageDef')
                return 서브총알.Item('LeftMargin') + 서브총알.Item('RightMargin')

            if (lambda : 총 = self.대상.CreateAction('PageSetup')총알 = 총.CreateSet()총.GetDefault(총알)서브총알 = 총알.Item('PageDef')서브총알.Item('TopMargin') + 서브총알.Item('BottomMargin') + 서브총알.Item('HeaderLen') + 서브총알.Item('FooterLen')):
                
                def 페이지높이():
                    총 = self.대상.CreateAction('PageSetup')
                    총알 = 총.CreateSet()
                    총.GetDefault(총알)
                    서브총알 = 총알.Item('PageDef')
                    return 서브총알.Item('TopMargin') + 서브총알.Item('BottomMargin') + 서브총알.Item('HeaderLen') + 서브총알.Item('FooterLen')

                넓이 = None()
        높이 = None()
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
            self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Width = 58962 - 넓이
            self.대상.HParameterSet.HShapeObject.ShapeTableCell.Height = 83520 - 높이
            self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
        return None

    if (lambda self, 옵션: self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)self.대상.HParameterSet.HShapeObject.ShapeTableCell.LineWrap = 옵션self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)):
        
        def 셀한줄(self, 옵션):
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

    if (lambda self, 횟수: for i in range(1, 횟수 + 1):
self.대상.HAction.Run('Redo')):
        
        def 재실행(self, 횟수):
            for i in range(1, 횟수 + 1):
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
            pass
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
        return None

    
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

    if (lambda self, 횟수: for i in range(1, 횟수 + 1):
self.대상.HAction.Run('Undo')):
        
        def 취소(self, 횟수):
            for i in range(1, 횟수 + 1):
                self.대상.HAction.Run('Undo')

    
    def 컨트롤표목록(self):
        표목록 = []
        컨트롤 = self.대상.HeadCtrl.Next.Next
        if 컨트롤:
            pass
        if 컨트롤:
            if 컨트롤.CtrlID == 'tbl':
                pass
            표목록.append(컨트롤)
            컨트롤 = 컨트롤.Next
            if 컨트롤:
                pass
            if 컨트롤:
                continue
        return 표목록

    if (lambda self, 값: 총 = self.대상.CreateAction('ParagraphShape')총알 = 총.CreateSet()총.GetDefault(총알)서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')서브총알배열 = 서브총알.CreateItemArray('TabItem', 3)서브총알배열.SetItem(0, 값)서브총알배열.SetItem(1, 3)서브총알배열.SetItem(2, 1)총.Execute(총알)):
        
        def 탭점선설정(self, 값):
            총 = self.대상.CreateAction('ParagraphShape')
            총알 = 총.CreateSet()
            총.GetDefault(총알)
            서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')
            서브총알배열 = 서브총알.CreateItemArray('TabItem', 3)
            서브총알배열.SetItem(0, 값)
            서브총알배열.SetItem(1, 3)
            서브총알배열.SetItem(2, 1)
            총.Execute(총알)

    if (lambda self, 값: 총 = self.대상.CreateAction('ParagraphShape')총알 = 총.CreateSet()총.GetDefault(총알)서브총알 = 총알.CreateItemSet('TabDef', 'TabDef')서브총알배열 = 서브총알.CreateItemArray('TabItem', 3)서브총알배열.SetItem(0, 값)서브총알배열.SetItem(1, 7)서브총알배열.SetItem(2, 1)총.Execute(총알)):
        
        def 탭점선설정원형(self, 값):
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
        return None(title = 'Open File', filetypes = [
            ('All Files', '*.*')])

    
    def 파일목록사진(self):
        return None(title = 'Open File', filetypes = [
            ('image files', ('.png', '.jpg'))])

    
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
        if 위치 == '상':
            총알.SetItem('BorderWidthTop', 굵기)
        총알.SetItem('BorderTypeTop', 종류)
        if 위치 == '하':
            총알.SetItem('BorderWidthBottom', 굵기)
        총알.SetItem('BorderTypeBottom', 종류)
        if 위치 == '좌':
            총알.SetItem('BorderWidthLeft', 굵기)
        총알.SetItem('BorderTypeLeft', 종류)
        if 위치 == '우':
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

    if (lambda self, 종류, 각, 위치: 총 = self.대상.CreateAction('CellFill')총알 = self.대상.CreateSet('CellBorderFill')총.GetDefault(총알)서브총알 = 총알.CreateItemSet('FillAttr', 'DrawFillAttr')서브총알.SetItem('Type', self.대상.BrushType('NullBrush|GradBrush'))서브총알.SetItem('GradationType', self.대상.Gradation(종류))서브총알.SetItem('GradationCenterX', 0)서브총알.SetItem('GradationCenterY', 0)서브총알.SetItem('GradationAngle', 각)서브총알.SetItem('GradationStep', 100)서브서브총알 = 서브총알.CreateItemArray('GradationIndexPos', 10)for i in range(10):
서브서브총알.SetItem(i, 위치[i][0])서브총알.SetItem('GradationStepCenter', 50)서브총알.SetItem('GradationColorNum', 2)써브서브총알 = 서브총알.CreateItemArray('GradationColor', 10)for i in range(10):
써브서브총알.SetItem(i, self.대상.RGBColor(위치[i][1], 위치[i][2], 위치[i][3]))서브총알.SetItem('GradationBrush', 1)총.Execute(총알)):
        
        def 표배경그라데이션(self, 종류, 각, 위치):
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

    if (lambda self, 종류, 각, 위치: 총 = self.대상.CreateAction('CellFill')총알 = self.대상.CreateSet('CellBorderFill')총.GetDefault(총알)서브총알 = 총알.CreateItemSet('FillAttr', 'DrawFillAttr')서브총알.SetItem('Type', self.대상.BrushType('NullBrush|GradBrush'))서브총알.SetItem('GradationType', self.대상.Gradation(종류))서브총알.SetItem('GradationCenterX', 0)서브총알.SetItem('GradationCenterY', 0)서브총알.SetItem('GradationAngle', 각)서브총알.SetItem('GradationStep', 100)서브서브총알 = 서브총알.CreateItemArray('GradationIndexPos', 10)위치 = 위치 + [
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0],
[
0,
0,
0,
0]]for i in range(10):
서브서브총알.SetItem(i, 위치[i][0])서브총알.SetItem('GradationStepCenter', 50)서브총알.SetItem('GradationColorNum', 2)써브서브총알 = 서브총알.CreateItemArray('GradationColor', 10)for i in range(10):
써브서브총알.SetItem(i, self.대상.RGBColor(위치[i][1], 위치[i][2], 위치[i][3]))서브총알.SetItem('GradationBrush', 1)총.Execute(총알)):
        
        def 표배경그라데이션2(self, 종류, 각, 위치):
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
            위치 = 위치 + [
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0],
                [
                    0,
                    0,
                    0,
                    0]]
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

    if (lambda self, 수평, 수직: 총 = self.대상.CreateAction('TablePropertyDialog')총알 = 총.CreateSet()총.GetDefault(총알)총알.SetItem('TreatAsChar', 0)총알.SetItem('HorzRelTo', 0)총알.SetItem('HorzOffset', self.대상.MiliToHwpUnit(수평))총알.SetItem('VertRelTo', 0)총알.SetItem('VertOffset', self.대상.MiliToHwpUnit(수직))총.Execute(총알)):
        
        def 표절대위치이동(self, 수평, 수직):
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
        if 종류 == '상':
            총알.SetItem('BorderWidthTop', 굵기)
        총알.SetItem('BorderTypeTop', 타입)
        if 종류 == '하':
            총알.SetItem('BorderWidthBottom', 굵기)
        총알.SetItem('BorderTypeBottom', 타입)
        if 종류 == '좌':
            총알.SetItem('BorderWidthLeft', 굵기)
        총알.SetItem('BorderTypeLeft', 타입)
        if 종류 == '우':
            총알.SetItem('BorderWidthRight', 굵기)
        총알.SetItem('BorderTypeRight', 타입)
        총.Execute(총알)

    
    def 표테두리단일선색(self, 종류, 빨강, 초록, 파랑):
        총 = self.대상.CreateAction('CellBorderFill')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        if 종류 == '상':
            pass
        총알.SetItem('BorderColorTop', self.대상.RGBColor(빨강, 초록, 파랑))
        if 종류 == '하':
            pass
        총알.SetItem('BorderColorBottom', self.대상.RGBColor(빨강, 초록, 파랑))
        if 종류 == '우':
            pass
        총알.SetItem('BorderColorRight', self.대상.RGBColor(빨강, 초록, 파랑))
        if 종류 == '좌':
            pass
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

    
    def 한글화(self, 숫자):
        숫자문자열 = str(숫자)
        리턴값 = ''
        문자열길이 = len(숫자문자열)
        한글수 = [
            '',
            '일',
            '이',
            '삼',
            '사',
            '오',
            '육',
            '칠',
            '팔',
            '구',
            '십']
        한글단 = [
            '',
            '십',
            '백',
            '천',
            '',
            '십',
            '백',
            '천',
            '',
            '십',
            '백',
            '천',
            '',
            '십',
            '백',
            '천']
        for i in range(0, 문자열길이):
            중간값 = 한글수[int(숫자문자열[문자열길이 - 1 - i])]
            if 한글수[int(숫자문자열[문자열길이 - 1 - i])] != '':
                pass
            중간값 += 한글단[i]
            if i == 4:
                pass
            중간값 += '만'
            if i == 8:
                pass
            중간값 += '억'
            if i == 12:
                pass
            중간값 += '조'
            리턴값 = 중간값 + 리턴값
        if 숫자 % 100000000 == 0:
            pass
        리턴값 = 리턴값.replace('만', '')
        if 숫자 % 0xE8D4A51000 == 0:
            pass
        리턴값 = 리턴값.replace('억', '')
        return 리턴값

    
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

    
    def 날짜변환(self, 데이터, 종류):
        결과값 = ''
        데이터초기값 = 데이터
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
        if None('^\\d{6}$', 데이터):
            pass
        if None('^\\d{6}$', 데이터):
            년 = int(데이터[:2])
        데이터 = f'''{데이터[:4]}-{데이터[4:6]}-{데이터[6:]}'''
        if None('^\\d{4}$', 데이터):
            pass
        if None('^\\d{4}$', 데이터):
            pass
        데이터 = f'''{datetime.today(None().year)[0:2]}{데이터[:2]}-{데이터[2:4]}-01'''
        데이터 = 데이터.rstrip('.')
        데이터 = None('[./-]', '-', 데이터)
        if len(데이터) < 8:
            데이터 = 데이터.rstrip('-')
            if None('\\d{4}-\\d{1,2}', 데이터):
                pass
            if None('\\d{4}-\\d{1,2}', 데이터):
                데이터 = 데이터 + '-01'
            elif None('\\d{1,2}-\\d{1,2}', 데이터):
                pass
            if None('\\d{1,2}-\\d{1,2}', 데이터):
                pass
        임시요일 = [
            '월',
            '화',
            '수',
            '목',
            '금',
            '토',
            '일']
        
        try:
            데이터 = None(데이터, '%Y-%m-%d')
            if 종류 == '점':
                pass
            결과값 = 데이터.strftime('%Y.%m.%d.')
            if 종류 == '점띄':
                pass
            결과값 = str(데이터.strftime('%Y.%m.%d.')).replace('.', '. ').strip()
            if 종류 == '바':
                pass
            결과값 = 데이터.strftime('%Y-%m-%d')
            if 종류 == '슬래시':
                pass
            결과값 = 데이터.strftime('%Y/%m/%d')
            if 종류 == '바요일':
                pass
            결과값 = 데이터.strftime('%Y-%m-%d') + '(' + 임시요일[데이터.weekday()] + ')'
            if 종류 == '점띄요일':
                pass
            결과값 = str(데이터.year) + '. ' + str(데이터.month) + '. ' + str(데이터.day) + '.(' + 임시요일[데이터.weekday()] + ')'
            if 종류 == '한글':
                pass
            결과값 = str(데이터.year) + '년 ' + str(데이터.month) + '월 ' + str(데이터.day) + '일 ' + 임시요일[데이터.weekday()] + '요일'
            if 종류 == '없점':
                pass
            결과값 = str(데이터.year) + '.' + str(데이터.month) + '.' + str(데이터.day) + '.'
            if 종류 == '없점띄':
                pass
            결과값 = str(데이터.year) + '. ' + str(데이터.month) + '. ' + str(데이터.day) + '.'
            if 종류 == '없바':
                pass
            결과값 = str(데이터.year) + '-' + str(데이터.month) + '-' + str(데이터.day)
            if 종류 == '없슬래시':
                pass
            결과값 = str(데이터.year) + '/' + str(데이터.month) + '/' + str(데이터.day)
            if 종류 == '없바요일':
                pass
            결과값 = str(데이터.year) + '-' + str(데이터.month) + '-' + str(데이터.day) + '(' + 임시요일[데이터.weekday()] + ')'
            if 종류 == '축약년월':
                pass
            결과값 = "'" + str(데이터.year)[2:4] + '. ' + str(데이터.month) + '.'
        except ValueError:
            str

        return None if int(데이터.split('-')[0]) <= 12 else str

    
    def 증감계산(self, 데이터, 종류):
        
        def 로으로(단어):
            if 단어:
                pass
            if not 단어:
                pass
            return '으로'
            마지막 = 단어[-1]
            기준 = ord('가')
            유니코드 = ord(마지막) - 기준
            if 유니코드 < 0 or 유니코드 > 11171:
                pass
            return '으로'
            종성 = 유니코드 % 28
            if 종성 == 0:
                pass
            return '로'
            if 종성 == 8:
                pass
            return '로'
            return '으로'

        결과값 = ''
        데이터초기값 = 데이터
        데이터초기값 = 데이터초기값.split('로')[0]
        if '→' in 데이터초기값 or ():
            pass
        elif '>' in 데이터초기값:
            pass
        if ():
            None('[^0-9.]', '', 앞) = re.sub
            뒤 = None('[^0-9.]', '', 뒤)
            임시퍼센트 = 0
            임시증감 = ''
            임시증감기호 = ''
            소수자리기준 = 0
            소수자리기준2 = 0
            if '.' in 앞:
                pass
        소수자리기준 = len(앞.split('.')[1])
        if '.' in 앞:
            pass
        소수자리기준2 = len(뒤.split('.')[1])
        소수자리기준 = max(소수자리기준, 소수자리기준2)
        if float(앞) < float(뒤):
            임시퍼센트 = ((float(뒤) - float(앞)) / float(앞)) * 100
            임시절대값 = float(뒤) - float(앞)
            임시증감 = '증가'
            임시증감기호 = '↑'
        elif float(앞) > float(뒤):
            임시퍼센트 = ((float(앞) - float(뒤)) / float(앞)) * 100
            임시절대값 = float(앞) - float(뒤)
            임시증감 = '감소'
        임시증감기호 = '↓'
        
        try:
            if 종류 == '퍼센트정수':
                if float(앞) == float(뒤):
                    결과값 = 앞 + '%→' + 뒤 + '%로 변화없음'
                return 결과값
        except ValueError:
            데이터초기값.split('>') + () + re.sub + '→' + 뒤 + 단위 + '→' + 뒤 + 단위

        결과값 = re.sub + '%→' + 뒤 + '%로 ' + str(round(임시퍼센트)) + '% ' + 임시증감 + '(' + str(round(임시절대값)) + '%p' + 임시증감기호 + ')'
        return 결과값
        if 종류 == '퍼센트소수':
            if float(앞) == float(뒤):
                결과값 = 앞 + '%→' + 뒤 + '%로 변화없음'
            return 결과값
        결과값 = None('[\\d.]', '', 앞) + '%→' + 뒤 + '%로 ' + str(round(임시퍼센트, 소수자리기준)) + '% ' + 임시증감 + '(' + str(round(임시절대값, 소수자리기준)) + '%p' + 임시증감기호 + ')'
        return 결과값
        if 종류 == '단위정수':
            if float(앞) == float(뒤):
                결과값 = 로으로 + None(단위) + ' 변화없음'
            return 결과값
        결과값 = 로으로 + None(단위) + ' ' + str(round(임시퍼센트)) + '% ' + 임시증감 + '(' + str(round(임시절대값)) + 단위 + 임시증감기호 + ')'
        return 결과값
        if 종류 == '단위소수':
            if float(앞) == float(뒤):
                결과값 = 로으로 + None(단위) + ' 변화없음'
            return 결과값
        결과값 = 로으로 + None(단위) + ' ' + str(round(임시퍼센트, 소수자리기준)) + '% ' + 임시증감 + '(' + str(round(임시절대값, 소수자리기준)) + 단위 + 임시증감기호 + ')'
        return 결과값

    if (lambda self, 종류1, 종류2: 텍스트 = self.블록스캔()[1]불순물여부 = '\r' not in 텍스트결과 = ''if 불순물여부:
passif 불순물여부:
if 종류1 == '날짜변환':
pass결과 = self.날짜변환(텍스트, 종류2)if 종류1 == '증감계산':
pass결과 = self.증감계산(텍스트, 종류2)self.문장(str(결과))None):
        
        def 블록한줄개선(self, 종류1, 종류2):
            텍스트 = self.블록스캔()[1]
            불순물여부 = '\r' not in 텍스트
            결과 = ''
            if 불순물여부:
                pass
            if 불순물여부:
                if 종류1 == '날짜변환':
                    pass
                결과 = self.날짜변환(텍스트, 종류2)
                if 종류1 == '증감계산':
                    pass
                결과 = self.증감계산(텍스트, 종류2)
                self.문장(str(결과))
            return None

    
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
        총알.SetItem('Height', 크기 * 100)
        총.Execute(총알)
        self.대상.HAction.Run('ParagraphShapeAlignJustify')
        self.대상.HAction.Run('CharShapeNormal')
        if 진하게 == 1:
            pass
        self.대상.HAction.Run('CharShapeBold')
        if 정렬 == 1:
            pass
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

    
    def 셀정보(self):
        if self.대상.CellShape:
            pass
        if self.대상.CellShape:
            정상 = 1
            블록마지막 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
            마지막위치 = self.대상.GetPosBySet()
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            self.대상.MovePos(201)
            처음위치 = self.대상.GetPosBySet()
            self.대상.SetPosBySet(처음위치)
            self.대상.ReleaseScan()
            블록처음 = self.대상.KeyIndicator()[-1][1:].split(')')[0]
            블록처음열 = None('[^A-z]', '', 블록처음)
            블록처음행 = None('[^0-9]', '', 블록처음)
            블록마지막열 = None('[^A-z]', '', 블록마지막)
            블록마지막행 = None('[^0-9]', '', 블록마지막)
            열 = (ord(블록마지막열) - ord(블록처음열)) + 1
            행 = (int(블록마지막행) - int(블록처음행)) + 1
            한줄 = 마지막위치.Item('List') - 처음위치.Item('List') - 열 - 1
            소수체크 = 0
            if not 행 == 1:
                한줄 = 한줄 / (int(행) - 1)
            소수체크 = 한줄 - int(한줄)
            if 열 == 1 and 행 == 1:
                정상 = 0
                self.새창()
                self.문서여백(20, 20, 15, 15, 10, 10)
                self.글자크기(15)
                self.폰트('맑은 고딕')
                self.문장('드래그할때 오른쪽아래(↘) 방향으로 해야 정상작동해요!, 만약 셀1개면 다른탭을 이용하세요!')
            elif 소수체크 > 0:
                self.새창()
                self.문서여백(20, 20, 15, 15, 10, 10)
                self.글자크기(15)
                self.폰트('맑은 고딕')
                self.문장('드래그할때 오른쪽아래(↘) 방향으로 해야 정상작동해요!, 만약 셀1개면 다른탭을 이용하세요!')
                정상 = 0
            elif 행 >= 2:
                self.대상.SetPosBySet(self.셀위치(처음위치.Item('List') + 한줄))
                if not re.sub == None('[^A-z]', '', self.대상.KeyIndicator()[-1][1:].split(')')[0]):
                    self.새창()
                    self.문서여백(20, 20, 15, 15, 10, 10)
                    self.글자크기(15)
                    self.폰트('맑은 고딕')
                    self.문장('드래그할때 오른쪽아래(↘) 방향으로 해야 정상작동해요!, 만약 셀1개면 다른탭을 이용하세요!')
                정상 = 0
                if int(블록처음행) >= 2:
                    self.대상.SetPosBySet(self.셀위치(처음위치.Item('List') - 한줄))
                    if not re.sub == None('[^A-z]', '', self.대상.KeyIndicator()[-1][1:].split(')')[0]):
                        self.새창()
                        self.문서여백(20, 20, 15, 15, 10, 10)
                        self.글자크기(15)
                        self.폰트('맑은 고딕')
                        self.문장('드래그할때 오른쪽아래(↘) 방향으로 해야 정상작동해요!, 만약 셀1개면 다른탭을 이용하세요!')
            정상 = 0
        return (정상, 처음위치.Item('List'), 행, 열, 한줄, 블록처음행, 블록처음열, 블록마지막행, 블록마지막열)

    
    def 블록리스트생성(self, 행, 열, 한줄, 처음위치):
        블록리스트 = []
        for j in range(행):
            for i in range(열):
                숫자 = 처음위치 + i + 한줄 * j
                블록리스트.append(숫자)
        return 블록리스트

    
    def 합계수식(self, 일번, 이번):
        총 = self.대상.CreateAction('TableFormula')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Command', '=SUM(' + 일번 + ':' + 이번 + ')??%g,;;')
        총.Execute(총알)

    
    def 빼기수식(self, 일번, 이번):
        총 = self.대상.CreateAction('TableFormula')
        총알 = 총.CreateSet()
        총.GetDefault(총알)
        총알.SetItem('Command', '=' + 일번 + '-' + 이번 + '??%g;;')
        총.Execute(총알)

    
    def 블록텍스트(self):
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
        return 결과텍스트
        if ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return 결과텍스트
        e = None
        del e

    
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
        self.글자음영(0xFFFFFFFF)
        self.문단여백(0, 0)

    
    def 글자좌표리스트(self, 내용):
        self.대상.MovePos(2)
        결과리스트 = []
        좌표개수 = 0
        self.정규표현식(내용)
        시작지점 = self.대상.CreateSet('ListParaPos')
        끝지점 = self.대상.CreateSet('ListParaPos')
        self.대상.GetSelectedPosBySet(시작지점, 끝지점)
        if 시작지점.Item('Pos') == None:
            pass
        else:
            좌표개수 = 좌표개수 + 1
        for i in range(좌표개수):
            self.정규표현식(내용)
            시작지점 = self.대상.CreateSet('ListParaPos')
            끝지점 = self.대상.CreateSet('ListParaPos')
            self.대상.GetSelectedPosBySet(시작지점, 끝지점)
            self.대상.HAction.Run('Cancel')
            self.대상.SetPosBySet(self.좌표(시작지점.Item('List'), 시작지점.Item('Para'), 시작지점.Item('Pos') + 1))
            self.대상.HAction.Run('Select')
            self.대상.SetPosBySet(self.좌표(끝지점.Item('List'), 끝지점.Item('Para'), 끝지점.Item('Pos') - 2))
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            텍스트 = 블록스캔[1]
            self.대상.ReleaseScan()
            결과리스트.append([
                시작지점,
                끝지점,
                텍스트])
            self.대상.HAction.Run('Cancel')
        return 결과리스트

    
    def 글자크기좌표리스트(self, 크기):
        self.대상.MovePos(2)
        결과리스트 = []
        좌표개수 = 0
        self.글자크기찾기(크기)
        시작지점 = self.대상.CreateSet('ListParaPos')
        끝지점 = self.대상.CreateSet('ListParaPos')
        self.대상.GetSelectedPosBySet(시작지점, 끝지점)
        if 시작지점.Item('Pos') == None:
            pass
        else:
            좌표개수 = 좌표개수 + 1
        for i in range(좌표개수):
            self.글자크기찾기(크기)
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            텍스트 = 블록스캔[1]
            self.대상.ReleaseScan()
            페이지위치 = self.대상.KeyIndicator()[3]
            결과리스트.append([
                페이지위치,
                텍스트])
            self.대상.HAction.Run('Cancel')
        return 결과리스트

    
    def 글자취급이미지(self, 이미지, 가로, 세로):
        self.표만들기([
            가로], [
            세로])
        self.사진넣기배경(이미지)
        self.표테두리타입(0, 0, 0, 0)
        self.표나가기()

    
    def 글자취급이미지2(self, 이미지, 가로, 세로):
        self.표만들기([
            가로], [
            세로])
        self.사진넣기(이미지)
        self.표테두리타입(0, 0, 0, 0)
        self.표나가기()

    if (lambda self, 글머리, 폰트, 크기, 내어쓰기, 진하게, 위, 줄간: 시작지점 = self.블록첫위치()self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]한글찾기 = None('[(가-힣0-9a-zA-Z“]+')결과텍스트 = ''체크 = 0try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]결과텍스트 = 결과텍스트 + 글머리 + 글꼬리블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]체크 = 1if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()self.문장(결과텍스트)if 체크 == 1:
종료지점 = self.현재위치()self.대상.SetPosBySet(시작지점)self.대상.HAction.Run('Select')self.대상.SetPosBySet(종료지점)self.글자스타일(0)self.자간헌터(0)self.내어쓰기(내어쓰기)self.글자간격(0)self.대상.HAction.Run('ParagraphShapeAlignJustify')self.대상.HAction.Run('CharShapeNormal')if 진하게 == 1:
passself.대상.HAction.Run('CharShapeBold')if 폰트 == '신명조':
self.신명조()elif 폰트 == '중고딕':
self.중고딕()elif 폰트 == '진휴먼명조':
self.휴먼명조()else:
self.폰트(폰트)self.글자크기(크기)self.줄간격(줄간)self.글자장평(100)self.글자음영(0xFFFFFFFF)self.문단여백(0, 0)self.문단위(위)NoneNoneif ValueError:
e = re.compileprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()체크 = 0e = Nonedel econtinuee = Nonedel eif Exception:
e = Noneprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()체크 = 0self.대상.ReleaseScan()self.새창()self.문서여백(20, 20, 15, 15, 10, 10)self.글자크기(15)self.폰트('맑은 고딕')self.문장('표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.')e = Nonedel econtinuee = Nonedel e):
        
        def 글머리지정(self, 글머리, 폰트, 크기, 내어쓰기, 진하게, 위, 줄간):
            시작지점 = self.블록첫위치()
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            블록스캔값 = 블록스캔[0]
            텍스트 = 블록스캔[1]
            한글찾기 = None('[(가-힣0-9a-zA-Z“]+')
            결과텍스트 = ''
            체크 = 0
            
            try:
                if 블록스캔값 == 2 or 블록스캔값 == 3:
                    글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                    결과텍스트 = 결과텍스트 + 글머리 + 글꼬리
                    블록스캔 = self.대상.GetText()
                    블록스캔값 = 블록스캔[0]
                    텍스트 = 블록스캔[1]
                    체크 = 1
                    if 블록스캔값 == 2:
                        continue
                    if 블록스캔값 == 3:
                        continue

            self.대상.ReleaseScan()
            self.문장(결과텍스트)
            if 체크 == 1:
                종료지점 = self.현재위치()
                self.대상.SetPosBySet(시작지점)
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(종료지점)
                self.글자스타일(0)
                self.자간헌터(0)
                self.내어쓰기(내어쓰기)
                self.글자간격(0)
                self.대상.HAction.Run('ParagraphShapeAlignJustify')
                self.대상.HAction.Run('CharShapeNormal')
                if 진하게 == 1:
                    pass
                self.대상.HAction.Run('CharShapeBold')
                if 폰트 == '신명조':
                    self.신명조()
                elif 폰트 == '중고딕':
                    self.중고딕()
                elif 폰트 == '진휴먼명조':
                    self.휴먼명조()
                else:
                    self.폰트(폰트)
                self.글자크기(크기)
                self.줄간격(줄간)
                self.글자장평(100)
                self.글자음영(0xFFFFFFFF)
                self.문단여백(0, 0)
                self.문단위(위)
            return None
            return None
            if ValueError:
                e = re.compile
                print(f'''값 오류 : {e}''')
                self.대상.ReleaseScan()
                체크 = 0
                e = None
                del e
                continue
                e = None
                del e
            if Exception:
                e = None
                print(f'''오류 발생 : {e}''')
                self.대상.ReleaseScan()
                체크 = 0
                self.대상.ReleaseScan()
                self.새창()
                self.문서여백(20, 20, 15, 15, 10, 10)
                self.글자크기(15)
                self.폰트('맑은 고딕')
                self.문장('표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.')
                e = None
                del e
                continue
                e = None
                del e

    
    def 글머리기본(self, 글머리):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        한글찾기 = None('[가-힣0-9a-zA-Z]+')
        결과텍스트 = ''
        체크 = 0
        카운트 = 0
        지울배열 = [
            '1.',
            '2.',
            '3.',
            '4.',
            '5.',
            '6.',
            '7.',
            '8.',
            '9.',
            '10',
            '11',
            '12',
            '13',
            '14',
            '가.',
            '나.',
            '다.',
            '라.',
            '마.',
            '바.',
            '사.',
            '아.',
            '자.',
            '차.',
            '카.',
            '타.',
            '파.',
            '하.',
            '1)',
            '2)',
            '3)',
            '4)',
            '5)',
            '6)',
            '7)',
            '8)',
            '9)',
            '10',
            '11',
            '12',
            '13',
            '14',
            '가)',
            '나)',
            '다)',
            '라)',
            '마)',
            '바)',
            '사)',
            '아)',
            '자)',
            '차)',
            '카)',
            '타)',
            '파)',
            '하)']
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                if 글꼬리[0:2] in 지울배열:
                    글꼬리 = 글꼬리[3:len(글꼬리)]
                글꼬리 = 글꼬리[한글찾기.search(글꼬리).start():len(글꼬리)]
                결과텍스트 = 결과텍스트 + 글머리[0] + 글머리[카운트 + 1] + ' ' + 글꼬리
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                카운트 = 카운트 + 1
                if 카운트 > 13:
                    pass
                카운트 = 0
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.compile
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            체크 = 0
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            체크 = 0
            self.대상.ReleaseScan()
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트('맑은 고딕')
            self.문장('표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.')
            e = None
            del e
            return None
            e = None
            del e

    
    def 답번호기본(self):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        한글찾기 = None('[(ㄱ-ㅎ가-힣0-9a-zA-Z]+')
        답배열 = [
            '①',
            '②',
            '③',
            '④',
            '⑤',
            '⑥',
            '⑦',
            '⑧',
            '⑨',
            '⑩',
            '⑪',
            '⑫',
            '⑬',
            '⑭',
            '⑮']
        답카운트 = 0
        결과텍스트 = ''
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = None if 답카운트 < 15 else re.compile
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
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트('맑은 고딕')
            self.문장('표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.')
            e = None
            del e
            return None
            e = None
            del e

    
    def 문장쌈(self, 앞, 뒤):
        블록스캔 = self.블록스캔()
        텍스트 = 블록스캔[1]
        if '\r' not in 텍스트:
            
            try:
                self.문장(앞 + 텍스트 + 뒤)
            except ValueError:
                e = None
                print(f'''값 오류 : {e}''')

            return None
            return None
            if Exception:
                e = None
                print(f'''오류 발생 : {e}''')
                e = None
                del e
                return None
                e = None
                del e

    
    def 로고절대값(self, 이미지, 너비, 높이):
        self.표만들기([
            너비], [
            높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.표나가기2()

    
    def 로고절대값오른쪽정렬(self, 이미지, 너비, 높이):
        self.표만들기([
            너비], [
            높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.오른쪽정렬()
        self.표나가기2()

    
    def 로고절대값기본정렬(self, 이미지, 너비, 높이):
        self.표만들기([
            너비], [
            높이])
        self.셀여백제로()
        self.표테두리타입(0, 0, 0, 0)
        self.사진넣기절대값(이미지, 너비, 높이)
        self.기본정렬()
        self.표나가기2()

    
    def 블록계산(self):
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
        블록스캔 = self.블록스캔()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        불순물여부 = '\r' not in 텍스트
        if 불순물여부:
            pass
        if 불순물여부:
            
            try:
                텍스트 = 텍스트.replace('더하기', '+').replace('곱하기', '*').replace('나누기', '/').replace('빼기', '-').replace('더하기', '+')
                산식 = None('[^\\d\\(\\)\\-\\*\\/\\+.]', '', 텍스트)
                토큰덩어리 = None(패턴, ' ', 산식).split(' ')
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
            except ValueError:
                e = None
                print(f'''값 오류 : {e}''')

            re.compile
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
            self.문장(str(계산스택[-1]))
        return None
        return None
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e

    
    def 블록글머리(self, 종류):
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        한글찾기 = None('[(가-힣0-9a-zA-Z]+')
        결과텍스트 = ''
        
        try:
            if 종류 == '복사':
                if 블록스캔값 == 2 or 블록스캔값 == 3:
                    self.글머리 = 텍스트[0:한글찾기.search(텍스트).start()]
                결과텍스트 = 텍스트
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
            텍스트 = 블록스캔[1]
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                글꼬리 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                if 종류 == '복사':
                    pass
                결과텍스트 = 결과텍스트 + self.글머리 + 글꼬리
                if 종류 == '붙임':
                    pass
                결과텍스트 = 결과텍스트 + self.글머리 + 글꼬리
                if 종류 == '삭제':
                    pass
                결과텍스트 = 결과텍스트 + 글꼬리
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.compile
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
            self.새창()
            self.문서여백(20, 20, 15, 15, 10, 10)
            self.글자크기(15)
            self.폰트('맑은 고딕')
            self.문장('표, 사진, 비어있는 줄을 포함하면 작동 안할거에요.')
            e = None
            del e
            return None
            e = None
            del e

    
    def 블록금액비율(self, 일번이름, 이번이름, 삼번이름, 사번이름, 일번값, 이번값, 삼번값, 사번값):
        블록스캔 = self.블록스캔()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        불순물여부 = '\r' not in 텍스트
        if 불순물여부:
            pass
        if 불순물여부:
            텍스트 = None('\\([^)]*\\)', '', 텍스트)
            
            try:
                숫자만 = None('[^0-9]', '', 텍스트)
                전체값 = 일번값 + 이번값 + 삼번값 + 사번값
                출력배열 = []
                if not 일번값 == 0:
                    출력배열.append(일번이름 + ' ' + format(round(float(숫자만) * 일번값 / 전체값), ','))
                출력배열.append(', ')
                if not 이번값 == 0:
                    출력배열.append(이번이름 + ' ' + format(round(float(숫자만) * 이번값 / 전체값), ','))
                출력배열.append(', ')
                if not 삼번값 == 0:
                    출력배열.append(삼번이름 + ' ' + format(round(float(숫자만) * 삼번값 / 전체값), ','))
                출력배열.append(', ')
                if not 사번값 == 0:
                    출력배열.append(사번이름 + ' ' + format(round(float(숫자만) * 사번값 / 전체값), ','))
                출력배열.append(', ')
                if len(출력배열) >= 2:
                    pass
                출력배열.pop()
                출력값 = ''
                for 요소 in 출력배열:
                    출력값 = 출력값 + 요소
                re.sub
                if not len(출력배열) == 0:
                    self.문장(텍스트 + '(' + 출력값 + ')')

            return None
        return None
        return None
        if ValueError:
            e = None
            print(f'''값 오류 : {e}''')
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = None
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e

    
    def 블록순환(self, 종류):
        시작지점 = self.블록첫위치()
        체크 = 0
        self.대상.InitScan(1, 255)
        블록스캔 = self.대상.GetText()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        결과텍스트 = []
        찐결과 = ''
        
        try:
            if 블록스캔값 == 2 or 블록스캔값 == 3:
                체크 = 1
                텍스트 = 텍스트.replace('\r\n', '')
                결과텍스트.append(텍스트)
                블록스캔 = self.대상.GetText()
                블록스캔값 = 블록스캔[0]
                텍스트 = 블록스캔[1]
                if 블록스캔값 == 2:
                    continue
                if 블록스캔값 == 3:
                    continue

        self.대상.ReleaseScan()
        if 종류 == '짧은차순':
            결과텍스트.sort(key = len)
        elif 종류 == '오름차순':
            결과텍스트.sort()
        elif 종류 == '내림차순':
            pass
        결과텍스트.sort(reverse = True)
        크기 = len(결과텍스트)
        for i in range(0, 크기):
            if i == 크기 - 1:
                찐결과 = 찐결과 + 결과텍스트[i]
                continue
            찐결과 = 찐결과 + 결과텍스트[i] + '\r\n'
        self.문장(찐결과)
        if 체크 == 1:
            종료지점 = self.현재위치()
            self.대상.SetPosBySet(시작지점)
            self.대상.HAction.Run('Select')
            self.대상.SetPosBySet(종료지점)
        return None
        return None
        if ValueError:
            e = None
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

    if (lambda self, 종류, 내용1, 내용2, 내용3, 내용4, 내용5, 내용6: 시작지점 = self.블록첫위치()체크 = 0self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
체크 = 1if 종류 == '앞':
텍스트 = str(내용1) + 텍스트elif 종류 == '뒤':
if '\r\n' in 텍스트:
위치 = 텍스트.find('\r')텍스트 = 텍스트[:위치] + str(내용1) + 텍스트[위치:]else:
텍스트 = 텍스트 + str(내용1)elif 종류 == '삭제':
텍스트 = 텍스트.replace(내용1, '')elif 종류 == '바꾸기':
텍스트 = 텍스트.replace(내용1, 내용2)텍스트 = 텍스트.replace(내용3, 내용4)텍스트 = 텍스트.replace(내용5, 내용6)elif 종류 == '맨앞제거':
텍스트 = 텍스트[1:]elif 종류 == '맨앞표':
텍스트 = '표:' + 텍스트elif 종류 == '탭띄숫자':
엔터 = 0if '\r\n' in 텍스트:
pass엔터 = 1텍스트 = 텍스트.replace('\r', '').replace('\n', '')텍스트 = 텍스트 + '\t' + ' 00'if 엔터 == 1:
pass텍스트 = 텍스트 + '\r'elif 종류 == '탭띄숫자1':
엔터 = 0if '\r\n' in 텍스트:
pass엔터 = 1텍스트 = 텍스트.replace('\r', '').replace('\n', '')텍스트 = 텍스트 + '\t' + ' 0'if 엔터 == 1:
pass텍스트 = 텍스트 + '\r'elif 종류 == '맨앞어절제거':
엔터 = 0if '\r\n' in 텍스트:
pass엔터 = 1텍스트 = ' '.join(텍스트.strip().split()[1:])if 엔터 == 1:
pass텍스트 = 텍스트 + '\r'elif 종류 == '맨뒤제거':
엔터 = 0if '\r\n' in 텍스트:
pass엔터 = 1텍스트 = 텍스트.replace('\r', '').replace('\n', '')텍스트 = 텍스트[:-1]if 엔터 == 1:
pass텍스트 = 텍스트 + '\r'elif 종류 == '맨뒤어절제거':
엔터 = 0if '\r\n' in 텍스트:
pass엔터 = 1텍스트 = ' '.join(텍스트.strip().split()[:-1])if 엔터 == 1:
pass텍스트 = 텍스트 + '\r'결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()self.문장(결과텍스트)if 체크 == 1:
종료지점 = self.현재위치()self.대상.SetPosBySet(시작지점)self.대상.HAction.Run('Select')self.대상.SetPosBySet(종료지점)NoneNoneif ValueError:
e = Noneprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel eNonee = Nonedel eif Exception:
e = Noneprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel eNonee = Nonedel e):
        
        def 블록여러줄(self, 종류, 내용1, 내용2, 내용3, 내용4, 내용5, 내용6):
            시작지점 = self.블록첫위치()
            체크 = 0
            self.대상.InitScan(1, 255)
            블록스캔 = self.대상.GetText()
            블록스캔값 = 블록스캔[0]
            텍스트 = 블록스캔[1]
            결과텍스트 = ''
            
            try:
                if 블록스캔값 == 2 or 블록스캔값 == 3:
                    체크 = 1
                    if 종류 == '앞':
                        텍스트 = str(내용1) + 텍스트
                    elif 종류 == '뒤':
                        if '\r\n' in 텍스트:
                            위치 = 텍스트.find('\r')
                            텍스트 = 텍스트[:위치] + str(내용1) + 텍스트[위치:]
                        else:
                            텍스트 = 텍스트 + str(내용1)
                    elif 종류 == '삭제':
                        텍스트 = 텍스트.replace(내용1, '')
                    elif 종류 == '바꾸기':
                        텍스트 = 텍스트.replace(내용1, 내용2)
                        텍스트 = 텍스트.replace(내용3, 내용4)
                        텍스트 = 텍스트.replace(내용5, 내용6)
                    elif 종류 == '맨앞제거':
                        텍스트 = 텍스트[1:]
                    elif 종류 == '맨앞표':
                        텍스트 = '표:' + 텍스트
                    elif 종류 == '탭띄숫자':
                        엔터 = 0
                        if '\r\n' in 텍스트:
                            pass
                        엔터 = 1
                        텍스트 = 텍스트.replace('\r', '').replace('\n', '')
                        텍스트 = 텍스트 + '\t' + ' 00'
                        if 엔터 == 1:
                            pass
                        텍스트 = 텍스트 + '\r'
                    elif 종류 == '탭띄숫자1':
                        엔터 = 0
                        if '\r\n' in 텍스트:
                            pass
                        엔터 = 1
                        텍스트 = 텍스트.replace('\r', '').replace('\n', '')
                        텍스트 = 텍스트 + '\t' + ' 0'
                        if 엔터 == 1:
                            pass
                        텍스트 = 텍스트 + '\r'
                    elif 종류 == '맨앞어절제거':
                        엔터 = 0
                        if '\r\n' in 텍스트:
                            pass
                        엔터 = 1
                        텍스트 = ' '.join(텍스트.strip().split()[1:])
                        if 엔터 == 1:
                            pass
                        텍스트 = 텍스트 + '\r'
                    elif 종류 == '맨뒤제거':
                        엔터 = 0
                        if '\r\n' in 텍스트:
                            pass
                        엔터 = 1
                        텍스트 = 텍스트.replace('\r', '').replace('\n', '')
                        텍스트 = 텍스트[:-1]
                        if 엔터 == 1:
                            pass
                        텍스트 = 텍스트 + '\r'
                    elif 종류 == '맨뒤어절제거':
                        엔터 = 0
                        if '\r\n' in 텍스트:
                            pass
                        엔터 = 1
                        텍스트 = ' '.join(텍스트.strip().split()[:-1])
                        if 엔터 == 1:
                            pass
                    텍스트 = 텍스트 + '\r'
                    결과텍스트 = 결과텍스트 + 텍스트
                    블록스캔 = self.대상.GetText()
                    블록스캔값 = 블록스캔[0]
                    텍스트 = 블록스캔[1]
                    if 블록스캔값 == 2:
                        continue
                    if 블록스캔값 == 3:
                        continue

            self.대상.ReleaseScan()
            self.문장(결과텍스트)
            if 체크 == 1:
                종료지점 = self.현재위치()
                self.대상.SetPosBySet(시작지점)
                self.대상.HAction.Run('Select')
                self.대상.SetPosBySet(종료지점)
            return None
            return None
            if ValueError:
                e = None
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

    
    def 블록여백정리(self):
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
        결과텍스트 = None(' +', ' ', 결과텍스트)
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.sub
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

    
    def 블록엔터코드(self):
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
        결과텍스트 = repr(결과텍스트)
        print(결과텍스트)
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = None
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

    
    def 블록엔터정리(self):
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
        결과텍스트 = None('(\r\n)+', '\r\n', 결과텍스트)
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.sub
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

    
    def 블록엔터정리공백정리(self):
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
        결과텍스트 = None('(\r\n)+', '\r\n', 결과텍스트)
        결과텍스트 = None(' +', ' ', 결과텍스트)
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.sub
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = re.sub
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e

    
    def 블록엔터제거공백정리(self):
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
        결과텍스트 = None('(\\r\\n)+', ' ', 결과텍스트)
        결과텍스트 = None(' +', ' ', 결과텍스트)
        결과텍스트 = None('(?<=[가-힣])ㆍ\\s+', 'ㆍ', 결과텍스트)
        self.문장(결과텍스트)
        return None
        if ValueError:
            e = re.sub
            print(f'''값 오류 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = re.sub
            print(f'''오류 발생 : {e}''')
            self.대상.ReleaseScan()
            e = None
            del e
            return None
            e = None
            del e

    
    def 블록한줄(self, 종류):
        블록스캔 = self.블록스캔()
        블록스캔값 = 블록스캔[0]
        텍스트 = 블록스캔[1]
        불순물여부 = '\r' not in 텍스트
        if 불순물여부:
            pass
        if 불순물여부:
            if 종류 == '금액한글화':
                
                try:
                    텍스트 = None('[^0-9]', '', 텍스트)
                    self.문장('금' + format(int(텍스트), ',') + '원(금' + self.한글화(int(텍스트)) + '원)')
                except ValueError:
                    e = 일
                    print(f'''값 오류 : {e}''')

                return None
                if 종류 == '인국공금액한글화':
                    
                    try:
                        텍스트 = None('[^0-9]', '', 텍스트)
                        self.문장('일금 ' + self.한글화(int(텍스트)) + ' 원정(₩' + format(int(텍스트), ',') + ')')
                    except ValueError:
                        e = 일
                        print(f'''값 오류 : {e}''')

                    return None
                    if 종류 == '천원':
                        
                        try:
                            곱하기 = 1
                            if '천원' in 텍스트:
                                곱하기 = 1000
                            elif '백만원' in 텍스트:
                                곱하기 = 1000000
                            elif '억' in 텍스트:
                                pass
                            곱하기 = 100000000
                            텍스트 = None('[^0-9.]', '', 텍스트)
                            텍스트 = Decimal(텍스트) * 곱하기
                            round(텍스트 / 1000)(',' + '천원')
                        except ValueError:
                            e = 일
                            print(f'''값 오류 : {e}''')

                        return None
                        if 종류 == '백만원':
                            
                            try:
                                곱하기 = 1
                                if '천원' in 텍스트:
                                    곱하기 = 1000
                                elif '백만원' in 텍스트:
                                    곱하기 = 1000000
                                elif '억' in 텍스트:
                                    pass
                                곱하기 = 100000000
                                텍스트 = None('[^0-9.]', '', 텍스트)
                                텍스트 = Decimal(텍스트) * 곱하기
                                round(텍스트 / 1000000)(',' + '백만원')
                            except ValueError:
                                e = 일
                                print(f'''값 오류 : {e}''')

                            return None
                            if 종류 == '블록콤마넣기':
                                
                                try:
                                    숫자 = int(텍스트)
                                    self.문장(format(숫자, ','))
                                except ValueError:
                                    e = 일
                                    print(f'''값 오류 : {e}''')

                                return None
                                if 종류 == '블록콤마빼기':
                                    텍스트 = 텍스트.replace(',', '')
                                    self.문장(텍스트)
            return None
            if 종류 == '블록주민변환':
                년도 = None('[^0-9]', '', 텍스트)
                if len(년도) == 6:
                    년 = int(년도[:2])
                    self.문장(년도)
                return None
            return None
            if 종류 == '블록나이':
                텍스트 = None('\\([^)]*\\)', '', 텍스트)
                년도 = None('[^0-9]', '', 텍스트)
                if len(년도) == 6:
                    년 = int(년도[:2])
                    월 = int(년도[2:4])
                    일 = int(년도[4:])
                    나이 = None().year - 년
                    if datetime.today > None().month:
                        나이 -= 1
                    elif datetime.today == None().month and datetime.today > None().day:
                        pass
                    나이 -= 1
                    self.문장(텍스트 + '(' + str(나이) + ')')
                return None
                if len(년도) == 8:
                    년 = int(년도[:4])
                    월 = int(년도[4:6])
                    일 = int(년도[6:])
                    나이 = None().year - 년
                    if datetime.today > None().month:
                        나이 -= 1
                    elif datetime.today == None().month and datetime.today > None().day:
                        pass
                    나이 -= 1
                    self.문장(텍스트 + '(' + str(나이) + ')')
                return None
            return None
            if 종류 == '블록개월':
                텍스트 = None('\\([^)]*\\)', '', 텍스트)
                년도 = None('[^0-9]', '', 텍스트)
                if len(년도) == 6:
                    년 = int(년도[:2])
                    월 = int(년도[2:4])
                    일 = int(년도[4:])
                    나이 = None().year - 년
                    개월 = None().month - 월
                    if datetime.today > None().day:
                        pass
                    개월 -= 1
                    self.문장(텍스트 + '(' + str(나이 * 12 + 개월) + ')')
                return None
                if len(년도) == 8:
                    년 = int(년도[:4])
                    월 = int(년도[4:6])
                    일 = int(년도[6:])
                    나이 = None().year - 년
                    개월 = None().month - 월
                    if datetime.today > None().day:
                        pass
                    개월 -= 1
                    self.문장(텍스트 + '(' + str(나이 * 12 + 개월) + ')')
                return None
            return None
        return None
        return None
        if Exception:
            e = 일
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = 일
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = 일
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = 일
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e
        if Exception:
            e = 일
            print(f'''오류 발생 : {e}''')
            e = None
            del e
            return None
            e = None
            del e

    
    def 사진표만들기(self):
        이름 = None(title = 'Open File', filetypes = [
            ('image files', ('.png', '.jpg'))])
        표너비값 = (203 - self.문단여백측정()) / 2
        self.표만들기([
            표너비값,
            표너비값], [
            30,
            4])
        self.표전체()
        self.표테두리타입(0, 0, 0, 0)
        self.표내부선타입(0, 0)
        self.글자크기(12)
        self.가운데정렬()
        self.진하게()
        self.폰트('맑은 고딕')
        self.대상.HAction.Run('Copy')
        self.캔슬()
        self.표처음()
        for i in range(len(이름)):
            if not i == 0:
                pass
            self.표오른쪽(1)
            self.대상.InsertBackgroundPicture('SelectedCell', 이름[i], 1, 5, 0, 0, 0, 0)
            if not i % 2 == 1:
                continue
            그림제목 = None('\\(([^()]+)\\)(?!.*\\()', 이름[i - 1])
            self.표오른쪽(1)
            self.문장(그림제목.group(1))
            그림제목 = None('\\(([^()]+)\\)(?!.*\\()', 이름[i])
            self.표오른쪽(1)
            self.문장(그림제목.group(1))
            if i == len(이름) - 1:
                continue
            self.아래로붙이기()
        re.search

    if (lambda self, 번호, 내용, 크기: self.기본정렬()self.표만들기([
8,
1,
크기], [
9])self.셀여백제로()self.표테두리색(0, 51, 102)self.표배경색(0, 51, 102)self.표테두리굵기(8, 8, 8, 8)self.폰트('맑은 고딕')self.글자크기(18)self.대상.HAction.Run('CharShapeBold')self.대상.HAction.Run('ParagraphShapeAlignCenter')self.글자색(255, 255, 255)self.문장(번호)self.대상.HAction.Run('TableRightCellAppend')self.대상.HAction.Run('TableResizeExLeft')self.대상.HAction.Run('TableResizeExLeft')self.대상.HAction.Run('TableResizeExLeft')self.표테두리타입(0, 0, 1, 0)self.대상.HAction.Run('TableRightCellAppend')self.표테두리타입(0, 1, 0, 0)self.표테두리굵기(0, 8, 0, 0)self.표테두리색(49, 95, 151)self.문장풀('맑은 고딕', 18.1, 1, 0, 내용)self.표나가기2()):
        
        def 소제목(self, 번호, 내용, 크기):
            self.기본정렬()
            self.표만들기([
                8,
                1,
                크기], [
                9])
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
            self.표만들기([
                205 - self.문단여백측정()], [
                9.5])
            self.표테두리타입(1, 1, 0, 0)
            self.표배경색(253, 254, 235)
            self.문장풀('HY헤드라인M', 16, 1, 0, ' 1. 행정안전부')
            self.표탈출()
            self.표만들기([
                28,
                173 - self.문단여백측정()], [
                8,
                60])
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

        if (lambda self, 내용: self.표만들기([
205 - self.문단여백측정()], [
25])self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(8, 8, 8, 8)self.표테두리색(51, 51, 153)self.글자크기(16)self.폰트('HY헤드라인M')self.자간헌터(0)self.문단여백(5, 5)self.문장(내용)self.대상.HAction.Run('MoveRight')self.대상.HAction.Run('BreakPara')self.대상.HAction.Run('ParagraphShapeAlignJustify')):
            
            def 상단박스(self, 내용):
                self.표만들기([
                    205 - self.문단여백측정()], [
                    25])
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

            
            def 셀공백제거(self):
                if self.대상.CellShape:
                    pass
                if self.대상.CellShape:
                    마지막위치 = self.대상.GetPosBySet()
                    self.대상.InitScan(1, 255)
                    블록스캔 = self.대상.GetText()
                    self.대상.MovePos(201)
                    처음위치 = self.대상.GetPosBySet()
                    self.대상.ReleaseScan()
                    for i in range(처음위치.Item('List'), 마지막위치.Item('List') + 1):
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
                        결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()
                        결과텍스트 = ' '.join(결과텍스트.split())
                        self.문장(결과텍스트)
                return None
                return None
                if ValueError:
                    e = None
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

            
            def 셀숫자오른쪽정렬(self):
                if self.대상.CellShape:
                    pass
                if self.대상.CellShape:
                    마지막위치 = self.대상.GetPosBySet()
                    self.대상.InitScan(1, 255)
                    블록스캔 = self.대상.GetText()
                    self.대상.MovePos(201)
                    처음위치 = self.대상.GetPosBySet()
                    self.대상.ReleaseScan()
                    for i in range(처음위치.Item('List'), 마지막위치.Item('List') + 1):
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
                        if None('[0-9,]+', 결과텍스트.strip()):
                            pass
                        if None('[0-9,]+', 결과텍스트.strip()):
                            self.오른쪽정렬()
                        self.문단여백(0, 10)
                        self.문장(결과텍스트)
                return None
                return None
                if ValueError:
                    e = None
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

            
            def 셀엔터변환(self):
                if self.대상.CellShape:
                    pass
                if self.대상.CellShape:
                    마지막위치 = self.대상.GetPosBySet()
                    self.대상.InitScan(1, 255)
                    블록스캔 = self.대상.GetText()
                    self.대상.MovePos(201)
                    처음위치 = self.대상.GetPosBySet()
                    self.대상.ReleaseScan()
                    for i in range(처음위치.Item('List'), 마지막위치.Item('List') + 1):
                        self.대상.SetPosBySet(self.셀위치(i))
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
                return None
                return None
                if ValueError:
                    e = None
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

            
            def 셀너비자동조절(self):
                if (lambda 셀너비: self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)self.대상.HParameterSet.HShapeObject.ShapeTableCell.Width = 셀너비self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)):
                    
                    def 셀너비붙여넣기(셀너비):
                        self.대상.HAction.GetDefault('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)
                        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeType', 3)
                        self.대상.HParameterSet.HShapeObject.HSet.SetItem('ShapeCellSize', 1)
                        self.대상.HParameterSet.HShapeObject.ShapeTableCell.Width = 셀너비
                        self.대상.HAction.Execute('TablePropertyDialog', self.대상.HParameterSet.HShapeObject.HSet)

                    if (lambda : 총 = self.대상.CreateAction('TablePropertyDialog')총알 = 총.CreateSet()서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')총.GetDefault(총알)서브총알.Item('Width')):
                        
                        def 행너비측정():
                            총 = self.대상.CreateAction('TablePropertyDialog')
                            총알 = 총.CreateSet()
                            서브총알 = 총알.CreateItemSet('ShapeTableCell', 'Cell')
                            총.GetDefault(총알)
                            return 서브총알.Item('Width')

                if self.대상.CellShape:
                    pass
                if self.대상.CellShape:
                    self.대상.HAction.Run('Cancel')
                    self.대상.MovePos(106)
                    self.대상.MovePos(105)
                    끝셀 = self.대상.KeyIndicator()[-1][1:].split(')')[0][0]
                    행개수 = (ord(끝셀) - ord('A')) + 1
                    self.대상.MovePos(104)
                    행너비목록 = []
                    for i in range(행개수):
                        행너비측정(None())
                        if not i < 행개수 - 1:
                            continue
                        self.표오른쪽(1)
                    self.대상.MovePos(104)
                    전체너비합 = sum(행너비목록)
                    문서너비 = self.대상.MiliToHwpUnit(208 - 0.7 * 행개수 - self.문단여백측정())
                    for i in range(행개수):
                        self.대상.HAction.Run('TableCellBlock')
                        self.대상.HAction.Run('TableCellBlockExtend')
                        self.대상.MovePos(107)
                        None(int(문서너비 * (행너비목록[i] / 전체너비합)))
                        self.대상.MovePos(106)
                        self.대상.HAction.Run('Cancel')
                        if not i < 행개수 - 1:
                            continue
                        self.표오른쪽(1)
                    (self,)
                return None

            if (lambda self, 종류, 종류2: try:
if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
for None in range(len(블록리스트)):
self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')if 종류 == '셀번호매기기':
try:
if i == 0:
self.대상.InitScan(1, 255)self.대상.ReleaseScan()except ValueError:
e = datetime.todayprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()처음숫자 = 1self.문장(str(처음숫자 + i))continueif 종류 == '나누기천':
self.대상.InitScan(1, 255)self.대상.GetText() = None블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9]', '', 결과텍스트)self.문장(str(round(int(결과텍스트) / 1000)))continueif 종류 == '표대반올림':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)self.문장(str(int(round(float(결과텍스트)))))continueif 종류 == '원':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()곱하기 = 1if '천원' in 결과텍스트:
곱하기 = 1000elif '백만원' in 결과텍스트:
곱하기 = 1000000elif '억' in 결과텍스트:
pass곱하기 = 100000000결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과텍스트 = Decimal(결과텍스트) * 곱하기round(결과텍스트)(',' + '원')continueif 종류 == '천원':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()곱하기 = 1if '천원' in 결과텍스트:
곱하기 = 1000elif '백만원' in 결과텍스트:
곱하기 = 1000000elif '억' in 결과텍스트:
pass곱하기 = 100000000결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과텍스트 = Decimal(결과텍스트) * 곱하기round(결과텍스트 / 1000)(',' + '천원')continueif 종류 == '백만원':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()곱하기 = 1if '천원' in 결과텍스트:
곱하기 = 1000elif '백만원' in 결과텍스트:
곱하기 = 1000000elif '억' in 결과텍스트:
pass곱하기 = 100000000결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과텍스트 = Decimal(결과텍스트) * 곱하기round(결과텍스트 / 1000000)(',' + '백만원')continueif 종류 == '억원':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()곱하기 = 1if '천원' in 결과텍스트:
곱하기 = 1000elif '백만원' in 결과텍스트:
곱하기 = 1000000elif '억' in 결과텍스트:
pass곱하기 = 100000000결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과텍스트 = Decimal(결과텍스트) * 곱하기round(결과텍스트 / 100000000)(',' + '억원')continueif 종류 == '곱하기천':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)self.문장(str(round(int(결과텍스트) * 1000)))continueif 종류 == '가지치기':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()결과텍스트 = ' '.join(결과텍스트.split())self.문장(결과텍스트)continueif 종류 == '괄호제거':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()self.문장(결과텍스트)continueif 종류 == '괄호안에만':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()선택자 = None('\\(([^)]+)')결과텍스트 = 선택자.findall(결과텍스트)self.문장(결과텍스트[0])continueif 종류 == '숫자만':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()숫자만 = None('[^0-9.]', '', 결과텍스트)self.문장(숫자만)continueif 종류 == '주민암호화':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()숫자만 = None('[^0-9,]', '', 결과텍스트)self.문장(숫자만)continueif 종류 == '표대더하기':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과값 = Decimal(결과텍스트) + Decimal(종류2)self.문장(str(결과값))continueif 종류 == '표대빼기':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과값 = Decimal(결과텍스트) - Decimal(종류2)self.문장(str(결과값))continueif 종류 == '표대곱하기':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과값 = Decimal(결과텍스트) * Decimal(종류2)self.문장(str(결과값))continueif 종류 == '표대나누기':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('[^0-9.]', '', 결과텍스트)결과값 = Decimal(결과텍스트) / Decimal(종류2)self.문장(str(결과값))continueif 종류 == '주민변환':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()년도 = None('[^0-9]', '', 결과텍스트)if len(년도) == 6:
년 = int(년도[:2])self.문장(년도)continueif 종류 == '날짜변환':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()출력값 = self.날짜변환(결과텍스트, 종류2)self.문장(출력값)continueif 종류 == '나이':
self.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)년도 = None('[^0-9]', '', 결과텍스트)if len(년도) == 6:
년 = int(년도[:2])월 = int(년도[2:4])일 = int(년도[4:])나이 = None().year - 년if datetime.today > None().month:
나이 -= 1elif datetime.today == None().month and datetime.today > None().day:
pass나이 -= 1self.문장(결과텍스트 + '(' + str(나이) + ')')continueif len(년도) == 8:
년 = int(년도[:4])월 = int(년도[4:6])일 = int(년도[6:])나이 = None().year - 년if datetime.today > None().month:
나이 -= 1elif datetime.today == None().month and datetime.today > None().day:
pass나이 -= 1self.문장(결과텍스트 + '(' + str(나이) + ')')continuecontinueif not 종류 == '개월':
continueself.대상.InitScan(1, 255)블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]결과텍스트 = ''try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 = 결과텍스트 + 텍스트블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)년도 = None('[^0-9]', '', 결과텍스트)if len(년도) == 6:
년 = int(년도[:2])월 = int(년도[2:4])일 = int(년도[4:])나이 = None().year - 년개월 = None().month - 월if datetime.today > None().day:
pass개월 -= 1self.문장(결과텍스트 + '(' + str(나이 * 12 + 개월) + ')')continueif len(년도) == 8:
년 = int(년도[:4])월 = int(년도[4:6])일 = int(년도[6:])나이 = None().year - 년개월 = None().month - 월if datetime.today > None().day:
pass개월 -= 1self.문장(결과텍스트 + '(' + str(나이 * 12 + 개월) + ')')continuedatetime.todayNoneNoneif Exception:
e = datetime.todayprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()처음숫자 = 1e = Nonedel econtinuee = Nonedel eif ValueError:
e = datetime.todayprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 일print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = datetime.todayprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = datetime.todayprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 일print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 월print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 월print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 일print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = datetime.todayprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 월print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 일print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 월print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 월print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = datetime.todayprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = 월print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 일print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = datetime.todayprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 월print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = 월print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = datetime.todayprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.sub if datetime.today > None().year % 100 else 년print(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.sub if len(숫자만) == 13 else re.subprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.compileprint(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = re.subprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = re.subprint(f'''값 오류 : {e}''')e = Nonedel eNonee = Nonedel eif Exception:
e = re.sub if len(숫자만) == 13 else re.subprint(f'''오류 발생 : {e}''')e = Nonedel eNonee = Nonedel e):
                
                def 셀순환(self, 종류, 종류2):
                    
                    try:
                        if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
                            for None in range(len(블록리스트)):
                                self.대상.HAction.Run('Select')
                                self.대상.HAction.Run('Select')
                                self.대상.HAction.Run('Select')
                                if 종류 == '셀번호매기기':
                                    
                                    try:
                                        if i == 0:
                                            self.대상.InitScan(1, 255)
                                        self.대상.ReleaseScan()
                                    except ValueError:
                                        e = datetime.today
                                        print(f'''값 오류 : {e}''')
                                        self.대상.ReleaseScan()
                                        처음숫자 = 1

                                    self.문장(str(처음숫자 + i))
                                    continue
                                if 종류 == '나누기천':
                                    self.대상.InitScan(1, 255)
                                    self.대상.GetText() = None
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
                                    결과텍스트 = None('[^0-9]', '', 결과텍스트)
                                    self.문장(str(round(int(결과텍스트) / 1000)))
                                    continue
                                if 종류 == '표대반올림':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    self.문장(str(int(round(float(결과텍스트)))))
                                    continue
                                if 종류 == '원':
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
                                    곱하기 = 1
                                    if '천원' in 결과텍스트:
                                        곱하기 = 1000
                                    elif '백만원' in 결과텍스트:
                                        곱하기 = 1000000
                                    elif '억' in 결과텍스트:
                                        pass
                                    곱하기 = 100000000
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과텍스트 = Decimal(결과텍스트) * 곱하기
                                    round(결과텍스트)(',' + '원')
                                    continue
                                if 종류 == '천원':
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
                                    곱하기 = 1
                                    if '천원' in 결과텍스트:
                                        곱하기 = 1000
                                    elif '백만원' in 결과텍스트:
                                        곱하기 = 1000000
                                    elif '억' in 결과텍스트:
                                        pass
                                    곱하기 = 100000000
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과텍스트 = Decimal(결과텍스트) * 곱하기
                                    round(결과텍스트 / 1000)(',' + '천원')
                                    continue
                                if 종류 == '백만원':
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
                                    곱하기 = 1
                                    if '천원' in 결과텍스트:
                                        곱하기 = 1000
                                    elif '백만원' in 결과텍스트:
                                        곱하기 = 1000000
                                    elif '억' in 결과텍스트:
                                        pass
                                    곱하기 = 100000000
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과텍스트 = Decimal(결과텍스트) * 곱하기
                                    round(결과텍스트 / 1000000)(',' + '백만원')
                                    continue
                                if 종류 == '억원':
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
                                    곱하기 = 1
                                    if '천원' in 결과텍스트:
                                        곱하기 = 1000
                                    elif '백만원' in 결과텍스트:
                                        곱하기 = 1000000
                                    elif '억' in 결과텍스트:
                                        pass
                                    곱하기 = 100000000
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과텍스트 = Decimal(결과텍스트) * 곱하기
                                    round(결과텍스트 / 100000000)(',' + '억원')
                                    continue
                                if 종류 == '곱하기천':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    self.문장(str(round(int(결과텍스트) * 1000)))
                                    continue
                                if 종류 == '가지치기':
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
                                    결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()
                                    결과텍스트 = ' '.join(결과텍스트.split())
                                    self.문장(결과텍스트)
                                    continue
                                if 종류 == '괄호제거':
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
                                    결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)
                                    결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()
                                    self.문장(결과텍스트)
                                    continue
                                if 종류 == '괄호안에만':
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
                                    선택자 = None('\\(([^)]+)')
                                    결과텍스트 = 선택자.findall(결과텍스트)
                                    self.문장(결과텍스트[0])
                                    continue
                                if 종류 == '숫자만':
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
                                    숫자만 = None('[^0-9.]', '', 결과텍스트)
                                    self.문장(숫자만)
                                    continue
                                if 종류 == '주민암호화':
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
                                    숫자만 = None('[^0-9,]', '', 결과텍스트)
                                    self.문장(숫자만)
                                    continue
                                if 종류 == '표대더하기':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과값 = Decimal(결과텍스트) + Decimal(종류2)
                                    self.문장(str(결과값))
                                    continue
                                if 종류 == '표대빼기':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과값 = Decimal(결과텍스트) - Decimal(종류2)
                                    self.문장(str(결과값))
                                    continue
                                if 종류 == '표대곱하기':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과값 = Decimal(결과텍스트) * Decimal(종류2)
                                    self.문장(str(결과값))
                                    continue
                                if 종류 == '표대나누기':
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
                                    결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                    결과값 = Decimal(결과텍스트) / Decimal(종류2)
                                    self.문장(str(결과값))
                                    continue
                                if 종류 == '주민변환':
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
                                    년도 = None('[^0-9]', '', 결과텍스트)
                                    if len(년도) == 6:
                                        년 = int(년도[:2])
                                    self.문장(년도)
                                    continue
                                if 종류 == '날짜변환':
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
                                    출력값 = self.날짜변환(결과텍스트, 종류2)
                                    self.문장(출력값)
                                    continue
                                if 종류 == '나이':
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
                                    결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)
                                    년도 = None('[^0-9]', '', 결과텍스트)
                                    if len(년도) == 6:
                                        년 = int(년도[:2])
                                        월 = int(년도[2:4])
                                        일 = int(년도[4:])
                                        나이 = None().year - 년
                                        if datetime.today > None().month:
                                            나이 -= 1
                                        elif datetime.today == None().month and datetime.today > None().day:
                                            pass
                                        나이 -= 1
                                        self.문장(결과텍스트 + '(' + str(나이) + ')')
                                        continue
                                    if len(년도) == 8:
                                        년 = int(년도[:4])
                                        월 = int(년도[4:6])
                                        일 = int(년도[6:])
                                        나이 = None().year - 년
                                        if datetime.today > None().month:
                                            나이 -= 1
                                        elif datetime.today == None().month and datetime.today > None().day:
                                            pass
                                        나이 -= 1
                                        self.문장(결과텍스트 + '(' + str(나이) + ')')
                                        continue
                                    continue
                                if not 종류 == '개월':
                                    continue
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
                                결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)
                                년도 = None('[^0-9]', '', 결과텍스트)
                                if len(년도) == 6:
                                    년 = int(년도[:2])
                                    월 = int(년도[2:4])
                                    일 = int(년도[4:])
                                    나이 = None().year - 년
                                    개월 = None().month - 월
                                    if datetime.today > None().day:
                                        pass
                                    개월 -= 1
                                    self.문장(결과텍스트 + '(' + str(나이 * 12 + 개월) + ')')
                                    continue
                                if len(년도) == 8:
                                    년 = int(년도[:4])
                                    월 = int(년도[4:6])
                                    일 = int(년도[6:])
                                    나이 = None().year - 년
                                    개월 = None().month - 월
                                    if datetime.today > None().day:
                                        pass
                                    개월 -= 1
                                    self.문장(결과텍스트 + '(' + str(나이 * 12 + 개월) + ')')
                                    continue
                            datetime.today

                    return None
                    return None
                    if Exception:
                        e = datetime.today
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        처음숫자 = 1
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = datetime.today
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 일
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = datetime.today
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = datetime.today
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 일
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 월
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 월
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 일
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = datetime.today
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 월
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 일
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 월
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 월
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = datetime.today
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = 월
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 일
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = datetime.today
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 월
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = 월
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = datetime.today
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub if datetime.today > None().year % 100 else 년
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub if len(숫자만) == 13 else re.sub
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.compile
                        print(f'''값 오류 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if Exception:
                        e = re.sub
                        print(f'''오류 발생 : {e}''')
                        self.대상.ReleaseScan()
                        e = None
                        del e
                        continue
                        e = None
                        del e
                    if ValueError:
                        e = re.sub
                        print(f'''값 오류 : {e}''')
                        e = None
                        del e
                        return None
                        e = None
                        del e
                    if Exception:
                        e = re.sub if len(숫자만) == 13 else re.sub
                        print(f'''오류 발생 : {e}''')
                        e = None
                        del e
                        return None
                        e = None
                        del e

                if (lambda self, 앞내용, 뒷내용, 삭제: try:
if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
for None in range(len(블록리스트)):
self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.InitScan(1, 255)try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 + 텍스트 = ''블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = str(앞내용) + 결과텍스트 + str(뒷내용)결과텍스트 = 결과텍스트.replace(삭제, '')self.문장(결과텍스트)블록스캔[0]NoneNoneif ValueError:
e = self.대상.GetText()print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = Noneprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = (블록마지막열,)print(f'''값 오류 : {e}''')e = Nonedel eNonee = Nonedel eif Exception:
e = 0print(f'''오류 발생 : {e}''')e = Nonedel eNonee = Nonedel e):
                    
                    def 셀앞뒤붙임(self, 앞내용, 뒷내용, 삭제):
                        
                        try:
                            if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
                                for None in range(len(블록리스트)):
                                    self.대상.HAction.Run('Select')
                                    self.대상.HAction.Run('Select')
                                    self.대상.HAction.Run('Select')
                                    self.대상.InitScan(1, 255)
                                    
                                    try:
                                        if 블록스캔값 == 2 or 블록스캔값 == 3:
                                            결과텍스트 + 텍스트 = ''
                                            블록스캔 = self.대상.GetText()
                                            블록스캔값 = 블록스캔[0]
                                            텍스트 = 블록스캔[1]
                                            if 블록스캔값 == 2:
                                                continue
                                            if 블록스캔값 == 3:
                                                continue

                                    self.대상.ReleaseScan()
                                    결과텍스트 = str(앞내용) + 결과텍스트 + str(뒷내용)
                                    결과텍스트 = 결과텍스트.replace(삭제, '')
                                    self.문장(결과텍스트)
                                블록스캔[0]

                        return None
                        return None
                        if ValueError:
                            e = self.대상.GetText()
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
                        if ValueError:
                            e = (블록마지막열,)
                            print(f'''값 오류 : {e}''')
                            e = None
                            del e
                            return None
                            e = None
                            del e
                        if Exception:
                            e = 0
                            print(f'''오류 발생 : {e}''')
                            e = None
                            del e
                            return None
                            e = None
                            del e

                    if (lambda self, 찾기1, 바꾸기1, 찾기2, 바꾸기2, 찾기3, 바꾸기3: try:
if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
for None in range(len(블록리스트)):
self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.HAction.Run('Select')self.대상.InitScan(1, 255)try:
if 블록스캔값 == 2 or 블록스캔값 == 3:
결과텍스트 + 텍스트 = ''블록스캔 = self.대상.GetText()블록스캔값 = 블록스캔[0]텍스트 = 블록스캔[1]if 블록스캔값 == 2:
continueif 블록스캔값 == 3:
continueself.대상.ReleaseScan()결과텍스트 = 결과텍스트.replace(찾기1, 바꾸기1)결과텍스트 = 결과텍스트.replace(찾기2, 바꾸기2)결과텍스트 = 결과텍스트.replace(찾기3, 바꾸기3)self.문장(결과텍스트)블록스캔[0]NoneNoneif ValueError:
e = self.대상.GetText()print(f'''값 오류 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif Exception:
e = Noneprint(f'''오류 발생 : {e}''')self.대상.ReleaseScan()e = Nonedel econtinuee = Nonedel eif ValueError:
e = (블록마지막열,)print(f'''값 오류 : {e}''')e = Nonedel eNonee = Nonedel eif Exception:
e = 0print(f'''오류 발생 : {e}''')e = Nonedel eNonee = Nonedel e):
                        
                        def 셀찾아서바꾸기(self, 찾기1, 바꾸기1, 찾기2, 바꾸기2, 찾기3, 바꾸기3):
                            
                            try:
                                if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
                                    for None in range(len(블록리스트)):
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.대상.InitScan(1, 255)
                                        
                                        try:
                                            if 블록스캔값 == 2 or 블록스캔값 == 3:
                                                결과텍스트 + 텍스트 = ''
                                                블록스캔 = self.대상.GetText()
                                                블록스캔값 = 블록스캔[0]
                                                텍스트 = 블록스캔[1]
                                                if 블록스캔값 == 2:
                                                    continue
                                                if 블록스캔값 == 3:
                                                    continue

                                        self.대상.ReleaseScan()
                                        결과텍스트 = 결과텍스트.replace(찾기1, 바꾸기1)
                                        결과텍스트 = 결과텍스트.replace(찾기2, 바꾸기2)
                                        결과텍스트 = 결과텍스트.replace(찾기3, 바꾸기3)
                                        self.문장(결과텍스트)
                                    블록스캔[0]

                            return None
                            return None
                            if ValueError:
                                e = self.대상.GetText()
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
                            if ValueError:
                                e = (블록마지막열,)
                                print(f'''값 오류 : {e}''')
                                e = None
                                del e
                                return None
                                e = None
                                del e
                            if Exception:
                                e = 0
                                print(f'''오류 발생 : {e}''')
                                e = None
                                del e
                                return None
                                e = None
                                del e

                        
                        def 셀이중순환(self, 종류):
                            
                            try:
                                if (블록마지막열, 합계리스트, 순서, 합계리스트[순서] += 데이터리스트[i], []) or (블록마지막열, 합계리스트, 순서, 합계리스트[순서] += 데이터리스트[i], []) or (블록마지막열, 합계리스트, 순서, 합계리스트[순서] += 데이터리스트[i], []) or (블록마지막열, 합계리스트, 순서, 합계리스트[순서] += 데이터리스트[i], []) or 정상 == 1:
                                    for None in range(len(블록리스트)):
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.대상.InitScan(1, 255)
                                        
                                        try:
                                            if 블록스캔값 == 2 or 블록스캔값 == 3:
                                                결과텍스트 + 텍스트 = ''
                                                블록스캔 = self.대상.GetText()
                                                블록스캔값 = 블록스캔[0]
                                                텍스트 = 블록스캔[1]
                                                if 블록스캔값 == 2:
                                                    continue
                                                if 블록스캔값 == 3:
                                                    continue

                                        self.대상.ReleaseScan()
                                        결과텍스트 = 결과텍스트.replace('\r', '').replace('\n', '').strip()
                                        결과텍스트 = ' '.join(결과텍스트.split())
                                        if 종류 == '셀퍼센트' or 종류 == '셀다중퍼센트':
                                            결과텍스트 = None('\\([^)]*\\)', '', 결과텍스트)
                                        결과텍스트 = None('[^0-9.]', '', 결과텍스트)
                                        데이터리스트.append(결과텍스트)
                                        self.문장(결과텍스트)
                                    re.sub
                                    if 종류 == '셀퍼센트':
                                        데이터리스트 = list(map(float, 데이터리스트))
                                        총합 = sum(데이터리스트)
                                        for i in range(len(블록리스트)):
                                            self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            임시입력값 = round((데이터리스트[i] / 총합) * 100, 1)
                                            if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                                                데이터리스트[i] = int(데이터리스트[i])
                                            self.문장(str(데이터리스트[i]) + '\r' + '(' + str(임시입력값) + '%)')
                                        블록스캔[0]
                                    return None
                                    if 종류 == '셀다중퍼센트':
                                        데이터리스트 = list(map(float, 데이터리스트))
                                        for None in :
                                            pass
                                        , [], 합계리스트 = self.대상.GetText(), range(0, len(데이터리스트), int(열))
                                        i = None
                                        총합 = sum(데이터리스트)
                                        for i in range(len(블록리스트)):
                                            self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            임시입력값 = round((데이터리스트[i] / 합계리스트[int(i / int(열))]) * 100, 1)
                                            if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                                                데이터리스트[i] = int(데이터리스트[i])
                                            self.문장(str(데이터리스트[i]) + '\r' + '(' + str(임시입력값) + '%)')
                                        self.블록리스트생성(행, 열, 한줄, 처음위치)
                                    return None
                                    if 종류 == '셀다중퍼센트세로':
                                        데이터리스트 = list(map(float, 데이터리스트))
                                        합계리스트 = [
                                            0] * 열
                                        for i in range(len(데이터리스트)):
                                            순서 = i % 열
                                        self.셀정보()
                                        for None in range(len(블록리스트)):
                                            self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            임시입력값 = round((데이터리스트[i] / 합계리스트[i % 열]) * 100, 1)
                                            if 데이터리스트[i] - int(데이터리스트[i]) == 0:
                                                데이터리스트[i] = int(데이터리스트[i])
                                            self.문장(str(데이터리스트[i]) + '\r' + '(' + str(임시입력값) + '%)')
                                    return None
                                    if 종류 == '셔플':
                                        for i in range(len(데이터리스트) - 1, 0, -1):
                                            j = 랜덤정수(i)
                                            데이터리스트[j], 데이터리스트[i] = 데이터리스트[i], 데이터리스트[j]
                                        for i in range(len(블록리스트)):
                                            self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            self.대상.HAction.Run('Select')
                                            self.문장(str(데이터리스트[i]))
                                    return None
                                    if not 종류 == '문자오름차순':
                                        pass
                                    필터리스트 = []
                                    for j in range(행):
                                        숫자 = int(열 * j)
                                        필터리스트.append([
                                            데이터리스트[숫자],
                                            숫자])
                                    if 종류 == '문자오름차순':
                                        pass
                                    필터리스트.sort(key = (lambda x: x[0]))
                                    if 종류 == '문자내림차순':
                                        pass
                                    필터리스트.sort(key = (lambda x: x[0]), reverse = True)
                                    if 종류 == '숫자오름차순':
                                        pass
                                    필터리스트.sort(key = (lambda x: int(x[0])))
                                    if 종류 == '숫자내림차순':
                                        pass
                                    필터리스트.sort(key = (lambda x: -int(x[0])))
                                    if 종류 == '짧은차순':
                                        pass
                                    필터리스트.sort(key = (lambda x: len(x[0])))
                                    데이터배열 = []
                                    for 기준 in 필터리스트:
                                        for i in range(열):
                                            숫자 = int(기준[1] + i)
                                            데이터배열.append(숫자)
                                    for i in range(len(블록리스트)):
                                        self.대상.SetPosBySet(self.셀위치(블록리스트[i]))
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.대상.HAction.Run('Select')
                                        self.문장(데이터리스트[데이터배열[i]])

                            return None
                            return None
                            if ValueError:
                                e = None
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
                            
                            if ValueError:
                                i, e = None, None, None
                                print(f'''값 오류 : {e}''')
                                e = None
                                del e
                                return None
                                e = None
                                del e
                            if Exception:
                                e = None
                                print(f'''오류 발생 : {e}''')
                                e = None
                                del e
                                return None
                                e = None
                                del e

                        
                        def 심플표(self, 행):
                            self.표만들기([
                                205 - self.문단여백측정()], [
                                5,
                                9])
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
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜점생략(self):
                            str + datetime.today(None().day) + '('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘분기(self):
                            년 = None().year
                            분기 = (None().month - 1) // 3 + 1
                            self.문장(f'''{년}년 {분기}/4분기''')

                        
                        def 오늘날짜분리월일요일(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 내일날짜분리년(self):
                            datetime.today(None()((None + timedelta(days = 1)).year) + '. ')

                        
                        def 내일날짜분리월일요일(self):
                            self.임시요일(datetime.today + None()[(None + timedelta(days = 1)).weekday()] + ')')

                        
                        def 오늘날짜월일(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜슬래쉬(self):
                            None(str + datetime.today(None().day))

                        
                        def 오늘날짜년(self):
                            str(datetime.today(None().year))

                        
                        def 오늘날짜년월(self):
                            None(str + datetime.today(None().month) + '. ')

                        
                        def 오늘날짜기준(self):
                            None(str + datetime.today(None().day) + '. 기준')

                        
                        def 오늘날짜무공백(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜바(self):
                            None(str + datetime.today(None().day))

                        
                        def 오늘날짜숫자만(self):
                            None(str + datetime.today(None().day) + '.')

                        
                        def 오늘날짜숫자만무공백(self):
                            None(str + datetime.today(None().day) + '.')

                        
                        def 오늘날짜월일요일무공백(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜한글숫자만(self):
                            None(str + datetime.today(None().day) + '일')

                        
                        def 오늘날짜축약(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜축약요없(self):
                            None(str + datetime.today(None().day) + '.')

                        
                        def 오늘날짜축약공백(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜축약무공백열콤마(self):
                            str + datetime.today(None().day) + '.('(self.임시요일 + datetime.today[None().weekday()] + ')')

                        
                        def 오늘날짜축약요없열콤마(self):
                            None(str + datetime.today(None().day) + '.')

                        
                        def 오늘학기(self):
                            학기 = '1'
                            if None().month // 7 == 1:
                                pass
                            학기 = '2'
                            str(datetime.today(None().year) + '학년도 ' + 학기 + '학기')

                        
                        def 다음주간(self):
                            오늘 = None()
                            다음주월 = 오늘 + timedelta(7 - 오늘.weekday())
                            다음주금 = 오늘 + timedelta(11 - 오늘.weekday())
                            self.문장(str(다음주월.year) + '.' + str(다음주월.month) + '.' + str(다음주월.day) + '.(' + self.임시요일[다음주월.weekday()] + ') ~ ' + str(다음주금.month) + '.' + str(다음주금.day) + '.(' + self.임시요일[다음주금.weekday()] + ')')

                        
                        def 다음주간월일요일(self):
                            오늘 = None()
                            다음주월 = 오늘 + timedelta(7 - 오늘.weekday())
                            다음주금 = 오늘 + timedelta(11 - 오늘.weekday())
                            self.문장(str(다음주월.month) + '.' + str(다음주월.day) + '.(' + self.임시요일[다음주월.weekday()] + ') ~ ' + str(다음주금.month) + '.' + str(다음주금.day) + '.(' + self.임시요일[다음주금.weekday()] + ')')

                        
                        def 다다음주간월일요일(self):
                            오늘 = None()
                            다음주월 = 오늘 + timedelta(14 - 오늘.weekday())
                            다음주금 = 오늘 + timedelta(18 - 오늘.weekday())
                            self.문장(str(다음주월.month) + '.' + str(다음주월.day) + '.(' + self.임시요일[다음주월.weekday()] + ') ~ ' + str(다음주금.month) + '.' + str(다음주금.day) + '.(' + self.임시요일[다음주금.weekday()] + ')')

                        
                        def 다음월간월일요일(self):
                            오늘 = None()
                            self.문장(str(다음달1일.month) + '.' + str(다음달1일.day) + '.(' + self.임시요일[다음달1일.weekday()] + ') ~ ' + str(다음달말.month) + '.' + str(다음달말.day) + '.(' + self.임시요일[다음달말.weekday()] + ')')

                        
                        def 역가로합(self):
                            
                            try:
                                if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
                                    if 열 >= 2:
                                        if 블록처음열 != 'A':
                                            for None in range(행):
                                                self.합계수식(블록처음열 + 포인트행, 블록마지막열 + 포인트행)
                                        return None
                                    return None

                            return None
                            return None
                            if ValueError:
                                print(f'''값 오류 : {e}''')
                                del e
                                return None
                                del e
                            if Exception:
                                print(f'''오류 발생 : {e}''')
                                None = None
                                del e
                                return None
                                e = None
                                del e

                        
                        def 역세로합(self):
                            
                            try:
                                if (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or (블록마지막열,) or 정상 == 1:
                                    if 행 >= 2:
                                        if int(블록처음행) >= 2:
                                            for None in range(열):
                                                self.합계수식(포인트수정열 + 블록처음행, 포인트수정열 + 블록마지막행)
                                        return None
                                    return None

                            return None
                            return None
                            if ValueError:
                                print(f'''값 오류 : {e}''')
                                del e
                                return None
                                del e
                            if Exception:
                                print(f'''오류 발생 : {e}''')
                                None = None
                                del e
                                return None
                                e = None
                                del e

                        
                        def 윗첨자입력(self, 입력):
                            self.대상.HAction.Run('CharShapeNormal')
                            self.대상.HAction.Run('CharShapeSuperscript')
                            self.문장(입력)

                        
                        def 전체셀보호해제(self):
                            if self.대상.CellShape:
                                pass
                            if self.대상.CellShape:
                                self.셀보호해제()
                            return None
                            컨트롤 = self.대상.HeadCtrl
                            if 컨트롤:
                                pass
                            if 컨트롤:
                                if 컨트롤.CtrlID == 'tbl':
                                    위치 = 컨트롤.GetAnchorPos(0)
                                    self.대상.SetPosBySet(위치)
                                    self.대상.FindCtrl()
                                    self.대상.HAction.Run('ShapeObjTableSelCell')
                                    self.대상.HAction.Run('TableCellBlockExtend')
                                    self.대상.HAction.Run('TableCellBlockExtend')
                                self.셀보호해제()
                                컨트롤 = 컨트롤.Next
                                if 컨트롤:
                                    pass
                                if 컨트롤:
                                    continue
                            return None

                        
                        def 점선박스(self):
                            self.표만들기([
                                (197 - self.문단여백측정()) / 3,
                                (197 - self.문단여백측정()) / 3,
                                (197 - self.문단여백측정()) / 3], [
                                1,
                                1,
                                30])
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
                            self.표만들기([
                                205 - self.문단여백측정()], [
                                40])
                            self.표테두리타입(1, 1, 0, 0)
                            self.표테두리굵기(12, 12, 1, 1)
                            self.표테두리색(102, 153, 255)
                            30(0, 1, None, str, datetime.today(None().year) + '년 사업계획')
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
                            str(datetime.today(None().year) + '. ', None, str + datetime.today(None().month) + '. ', None, str + datetime.today(None().day) + '.')
                            self.대상.HAction.Run('BreakPara')
                            self.대상.HAction.Run('BreakPara')
                            self.대상.HAction.Run('BreakPara')
                            self.대상.HAction.Run('BreakPara')
                            self.대상.HAction.Run('BreakPara')
                            self.대상.HAction.Run('BreakPara')
                            self.문장풀('HY헤드라인M', 26, 0, 1, '행정안전부')
                            self.대상.HAction.Run('BreakPage')
                            self.표만들기([
                                1,
                                1,
                                1,
                                45,
                                1,
                                1,
                                1], [
                                11])
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
                            self.표만들기([
                                205 - self.문단여백측정()], [
                                210])
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
                            self.표만들기([
                                205 - self.문단여백측정()], [
                                12])
                            self.표테두리타입(1, 1, 0, 0)
                            self.표테두리굵기(8, 8, 8, 8)
                            self.표테두리색(51, 51, 153)
                            self.문장풀('HY헤드라인M', 20, 1, 1, '제목을 쓰세요!')
                            self.표탈출()

                        
                        def 짧순정답(self):
                            시작지점 = self.블록첫위치()
                            체크 = 0
                            self.대상.InitScan(1, 255)
                            블록스캔 = self.대상.GetText()
                            블록스캔값 = 블록스캔[0]
                            텍스트 = 블록스캔[1]
                            한글찾기 = None('[(ㄱ-ㅎ가-힣0-9a-zA-Z]+')
                            결과텍스트 = []
                            찐결과 = ''
                            
                            try:
                                if 블록스캔값 == 2 or 블록스캔값 == 3:
                                    체크 = 1
                                    텍스트 = 텍스트.replace('\r\n', '')
                                    텍스트 = 텍스트[한글찾기.search(텍스트).start():len(텍스트)]
                                    결과텍스트.append(텍스트)
                                    블록스캔 = self.대상.GetText()
                                    블록스캔값 = 블록스캔[0]
                                    텍스트 = 블록스캔[1]
                                    if 블록스캔값 == 2:
                                        continue
                                    if 블록스캔값 == 3:
                                        continue

                            self.대상.ReleaseScan()
                            결과텍스트.sort(key = len)
                            크기 = len(결과텍스트)
                            답배열 = [
                                '①',
                                '②',
                                '③',
                                '④',
                                '⑤',
                                '⑥',
                                '⑦',
                                '⑧',
                                '⑨',
                                '⑩',
                                '⑪',
                                '⑫',
                                '⑬',
                                '⑭',
                                '⑮']
                            for i in range(0, 크기):
                                if i < 15:
                                    if i == 크기 - 1:
                                        찐결과 = 찐결과 + ' ' + 답배열[i] + ' ' + 결과텍스트[i]
                                        continue
                                    찐결과 = 찐결과 + ' ' + 답배열[i] + ' ' + 결과텍스트[i] + '\r\n'
                                    continue
                                if i == 크기 - 1:
                                    찐결과 = 찐결과 + 결과텍스트[i]
                                    continue
                                찐결과 = 찐결과 + 결과텍스트[i] + '\r\n'
                            re.compile
                            self.문장(찐결과)
                            if 체크 == 1:
                                종료지점 = self.현재위치()
                                self.대상.SetPosBySet(시작지점)
                                self.대상.HAction.Run('Select')
                                self.대상.SetPosBySet(종료지점)
                            return None
                            return None
                            if ValueError:
                                e = None
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
18,
1,
182 - self.문단여백측정()], [
10])self.셀여백제로()self.표테두리타입(1, 1, 1, 1)self.표테두리굵기(1, 1, 1, 1)self.표테두리색(35, 35, 106)self.표배경색(35, 35, 106)self.폰트('HY헤드라인M')self.글자크기(16)self.글자색(255, 255, 255)self.가운데정렬()self.문장('참고')self.표오른쪽(1)self.표너비줄이기(3)self.표테두리타입(0, 0, 1, 1)self.표오른쪽(1)self.문장풀('HY헤드라인M', 20, 0, 0, ' ' + 내용)self.표나가기2()):
                            
                            def 참고(self, 내용):
                                self.표만들기([
                                    18,
                                    1,
                                    182 - self.문단여백측정()], [
                                    10])
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
                                self.문장풀('HY헤드라인M', 20, 0, 0, ' ' + 내용)
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
                                self.표만들기([
                                    205 - self.문단여백측정()], [
                                    12])
                                self.표테두리타입(1, 1, 1, 1)
                                self.표테두리굵기(6, 6, 6, 6)
                                self.표배경색(223, 230, 247)
                                self.문장풀('맑은 고딕', 20, 1, 1, '제목')
                                self.표나가기()

                            
                            def 행안부참고(self):
                                self.표만들기([
                                    17,
                                    184 - self.문단여백측정()], [
                                    9])
                                self.표테두리타입(1, 1, 1, 1)
                                self.표테두리굵기(1, 1, 1, 1)
                                self.표배경색(223, 230, 247)
                                self.문장풀('맑은 고딕', 17, 1, 1, '참고1')
                                self.대상.HAction.Run('TableRightCellAppend')
                                self.문장풀('맑은 고딕', 17, 1, 0, ' 참고1의 제목')
                                self.표탈출()

                            
                            def 행안부초록표(self):
                                self.표만들기([
                                    30,
                                    172 - self.문단여백측정()], [
                                    9,
                                    7,
                                    7,
                                    7,
                                    7,
                                    7,
                                    7])
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
                                self.대상.HParameterSet.HMarkpenShape.Color = 0xFFFFFFFF
                                self.대상.HAction.Execute('MarkPenShape', self.대상.HParameterSet.HMarkpenShape.HSet)

                            
                            def PDF를한컴으로(self):
                                파일목록 = self.파일목록()
                                파일목록변환 = '|'.join(파일목록)
                                파일목록변환 = 파일목록변환.replace('/', '\\')
                                for None in range(0, len(파일목록)):
                                    if None:
                                        continue
                                총 = self.대상.CreateAction('FileOpenPDF')
                                총알 = 총.CreateSet()
                                총.GetDefault(총알)
                                총알.SetItem('Attributes', 65536)
                                총알.SetItem('FileName', 파일목록변환)
                                총알.SetItem('OpenFlag', 0)
                                총.Execute(총알)

                            
                            def 비전표(self, 이미지):
                                self.소제목('Ⅱ', ' 비전 및 추진전략', 55)
                                self.표만들기([
                                    19,
                                    1,
                                    175 - self.문단여백측정()], [
                                    13,
                                    14,
                                    22,
                                    14,
                                    11,
                                    1,
                                    9,
                                    1,
                                    9,
                                    1,
                                    9,
                                    3,
                                    11,
                                    1,
                                    9,
                                    1,
                                    9,
                                    1,
                                    9,
                                    3,
                                    11,
                                    1,
                                    9,
                                    1,
                                    9,
                                    1,
                                    9])
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
                                self.글자음영(0xFFFFFFFF)
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
                                총알.SetItem('Height', 크기 * 100)
                                총.Execute(총알)

                            
                            def 구분선(self):
                                self.표만들기([
                                    102], [
                                    1])
                                self.표테두리타입(1, 0, 0, 0)
                                self.표나가기2()

                            
                            def 궁극의정리줄선택(self):
                                self.대상.MovePos(6)
                                self.대상.HAction.Run('Select')
                                self.대상.MovePos(7)

                            
                            def 마크다운배열생성(self):
                                
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
                                return 배열

                            
                            def 마크다운배열생성2(self):
                                
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
                                                

                                if (lambda : 블록내용 = self.블록텍스트()줄나누기 = 블록내용.split('\r\n')중간처리 = []for 아이템 in 줄나누기:
텍스트 = 아이템.strip()if 텍스트.startswith(('□', '네모 ')):
passif 텍스트.startswith(('□', '네모 ')):
텍스트 = None('^(□|네모)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '네모:' + 텍스트elif 텍스트.startswith(('○', '원 ')):
passif 텍스트.startswith(('○', '원 ')):
텍스트 = None('^(○|원)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '원:' + 텍스트elif 텍스트.startswith(('-', '바 ')):
passif 텍스트.startswith(('-', '바 ')):
텍스트 = None('^(-|바)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '바:' + 텍스트elif 텍스트.startswith(('※', '당구 ', '당구장 ')):
passif 텍스트.startswith(('※', '당구 ', '당구장 ')):
텍스트 = None('^(※|당구장|당구)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '당구장:' + 텍스트elif 텍스트.startswith('부서 '):
passif 텍스트.startswith('부서 '):
텍스트 = None('^(부서)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '부서:' + 텍스트elif 텍스트.startswith('제목 '):
passif 텍스트.startswith('제목 '):
텍스트 = None('^(제목)\\s*', '', 텍스트, count = 1)텍스트.lstrip(':')텍스트 = '제목:' + 텍스트중간처리.append(텍스트)re.sub중간처리 = None(중간처리)for None in :
if None:
continue콜론처리, 중간처리, 콜론나누기, s = re.sub특수문자제거(키워드처리(엔터처리(None(콜론나누기))))):
                                    
                                    def 마크다운읽기():
                                        블록내용 = self.블록텍스트()
                                        줄나누기 = 블록내용.split('\r\n')
                                        중간처리 = []
                                        for 아이템 in 줄나누기:
                                            텍스트 = 아이템.strip()
                                            if 텍스트.startswith(('□', '네모 ')):
                                                pass
                                            if 텍스트.startswith(('□', '네모 ')):
                                                텍스트 = None('^(□|네모)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                                텍스트 = '네모:' + 텍스트
                                            elif 텍스트.startswith(('○', '원 ')):
                                                pass
                                            if 텍스트.startswith(('○', '원 ')):
                                                텍스트 = None('^(○|원)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                                텍스트 = '원:' + 텍스트
                                            elif 텍스트.startswith(('-', '바 ')):
                                                pass
                                            if 텍스트.startswith(('-', '바 ')):
                                                텍스트 = None('^(-|바)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                                텍스트 = '바:' + 텍스트
                                            elif 텍스트.startswith(('※', '당구 ', '당구장 ')):
                                                pass
                                            if 텍스트.startswith(('※', '당구 ', '당구장 ')):
                                                텍스트 = None('^(※|당구장|당구)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                                텍스트 = '당구장:' + 텍스트
                                            elif 텍스트.startswith('부서 '):
                                                pass
                                            if 텍스트.startswith('부서 '):
                                                텍스트 = None('^(부서)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                                텍스트 = '부서:' + 텍스트
                                            elif 텍스트.startswith('제목 '):
                                                pass
                                            if 텍스트.startswith('제목 '):
                                                텍스트 = None('^(제목)\\s*', '', 텍스트, count = 1)
                                                텍스트.lstrip(':')
                                            텍스트 = '제목:' + 텍스트
                                            중간처리.append(텍스트)
                                        re.sub
                                        중간처리 = None(중간처리)
                                        for None in :
                                            if None:
                                                continue
                                                콜론처리, 중간처리, 콜론나누기, s = re.sub
                                                return 특수문자제거(키워드처리(엔터처리(None(콜론나누기))))

                                    배열 = None()
                                return 배열

                            
                            def JSON에서변환(self):
                                블록내용 = self.블록텍스트()
                                블록내용 = None(블록내용)
                                접두사 = {
                                    1: '네모:',
                                    2: '원:',
                                    3: '바:',
                                    4: '점:' }
                                보관함 = []
                                if (lambda 블록내용, 레벨: 접두 = 접두사.get(레벨, '')if isinstance(블록내용, dict):
passif isinstance(블록내용, dict):
for None in 블록내용.items():
if ():
if isinstance(value, (dict, list)):
passif isinstance(value, (dict, list)):
보관함.append(f'''{접두}{key}''')None(value, 레벨 + 1)continue()Noneif isinstance(블록내용, list):
passif isinstance(블록내용, list):
for None in 블록내용:
if isinstance(item, (dict, list)):
passif isinstance(item, (dict, list)):
None(item, 레벨)continueNone):
                                    if (lambda 블록내용, 레벨: 접두 = 접두사.get(레벨, '')if isinstance(블록내용, dict):
passif isinstance(블록내용, dict):
for None in 블록내용.items():
if ():
if isinstance(value, (dict, list)):
passif isinstance(value, (dict, list)):
보관함.append(f'''{접두}{key}''')None(value, 레벨 + 1)continue()Noneif isinstance(블록내용, list):
passif isinstance(블록내용, list):
for None in 블록내용:
if isinstance(item, (dict, list)):
passif isinstance(item, (dict, list)):
None(item, 레벨)continueNone):
                                        
                                        def 변환기(블록내용, 레벨):
                                            접두 = 접두사.get(레벨, '')
                                            if isinstance(블록내용, dict):
                                                pass
                                            if isinstance(블록내용, dict):
                                                for None in 블록내용.items():
                                                    if ():
                                                        if isinstance(value, (dict, list)):
                                                            pass
                                                        if isinstance(value, (dict, list)):
                                                            보관함.append(f'''{접두}{key}''')
                                                            None(value, 레벨 + 1)
                                                            continue
                                                ()
                                            return None
                                            if isinstance(블록내용, list):
                                                pass
                                            if isinstance(블록내용, list):
                                                for None in 블록내용:
                                                    if isinstance(item, (dict, list)):
                                                        pass
                                                    if isinstance(item, (dict, list)):
                                                        None(item, 레벨)
                                                        continue
                                            return None

                                None(블록내용)
                                출력내용 = '\r\n'.join(보관함)
                                출력내용 = 출력내용.replace('네모:제목', '제목')
                                self.문장(출력내용)

                            __static_attributes__ = ('\xea\xb8\x80\xeb\xa8\xb8\xeb\xa6\xac', '\xeb\x8c\x80\xec\x83\x81', '\xeb\xac\xb8\xec\x84\x9c\xec\x9a\xa9\xec\xa7\x80', '\xeb\xb0\xa9\xea\xb8\x88\xec\xb2\x98\xeb\xa6\xac', '\xec\x85\x80\xeb\x84\x93\xec\x9d\xb4', '\xec\x85\x80\xeb\x86\x92\xec\x9d\xb4')
                            return None

한컴기본 = None(한컴기본, '\xed\x95\x9c\xec\xbb\xb4\xea\xb8\xb0\xeb\xb3\xb8')
