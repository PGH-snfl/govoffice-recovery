"""한글(HWP) COM 실행 객체 연결 계층."""

try:
    import pythoncom
    from win32com.client.gencache import EnsureDispatch
except ImportError:  # 비-Windows/비-COM 환경에서도 소스 검증을 허용한다.
    pythoncom = None
    EnsureDispatch = None


class HwpConnectionMixin:
    대상 = None
    보안모듈종류 = "FilePathCheckDLL"
    보안모듈이름 = "FilePathCheckerModuleExample"

    @staticmethod
    def _com확인():
        if pythoncom is None or EnsureDispatch is None:
            raise RuntimeError("한글 자동화에는 pywin32와 한글 오피스가 필요합니다.")

    def _실행중인_한글찾기(self):
        바인딩내용 = pythoncom.CreateBindCtx(0)
        실행중객체테이블 = pythoncom.GetRunningObjectTable()
        실행중객체이름들 = 실행중객체테이블.EnumRunning()

        for 실행중객체이름 in 실행중객체이름들:
            try:
                이름 = 실행중객체이름.GetDisplayName(바인딩내용, 실행중객체이름)
                if 이름.startswith("!HwpObject"):
                    찾은객체 = 실행중객체테이블.GetObject(실행중객체이름)
                    return EnsureDispatch(찾은객체.QueryInterface(pythoncom.IID_IDispatch))
            except ValueError as e:
                print(f"값 오류 : {e}")
            except Exception as 오류:
                print(f"[오류] 실행중 객체 확인 중 문제 발생: {오류}")
        return None

    def _보안모듈등록(self):
        """레지스트리에 등록된 한글 Automation 파일 보안 모듈을 연결한다."""
        if self.대상 is None:
            raise RuntimeError("한글 COM 객체가 없어 보안 모듈을 등록할 수 없습니다.")
        try:
            등록됨 = self.대상.RegisterModule(self.보안모듈종류, self.보안모듈이름)
        except Exception as 오류:
            raise RuntimeError(
                "한글 Automation 보안 모듈 등록 중 오류가 발생했습니다. "
                "FilePathCheckerModuleExample.dll과 HKCU\\Software\\HNC\\HwpAutomation\\Modules "
                "레지스트리 값을 확인하세요."
            ) from 오류
        # 한글은 같은 인스턴스에 이미 등록된 모듈을 다시 등록하면 False를
        # 반환할 수 있다. 예외가 없었다면 기존 등록을 유효한 상태로 본다.
        return True

    def _새한글(self):
        self.대상 = EnsureDispatch("hwpframe.hwpobject")
        self._보안모듈등록()
        self.대상.XHwpWindows.Item(0).Visible = True
        return self.대상

    def 한컴열기(self):
        self._com확인()
        self.대상 = self._실행중인_한글찾기()
        if self.대상 is not None:
            self._보안모듈등록()
            return
        try:
            self._새한글()
            self.문서여백(20, 20, 15, 15, 10, 10)
        except ValueError as e:
            print(f"값 오류 : {e}")
        except Exception as 오류:
            print(f"[오류] 새로운 한컴 객체 생성 중 문제 발생: {오류}")

    def 불러오기(self):
        try:
            self.대상.HAction.Run("FileOpen")
        except (ValueError, Exception) as e:
            print(f"오류 발생 : {e}")
            self._com확인()
            self._새한글()
            self.대상.HAction.Run("FileOpen")

    def 새창(self):
        try:
            self.대상.HAction.Run("FileNew")
            self.문서여백(20, 20, 15, 15, 10, 10)
        except (ValueError, Exception) as e:
            print(f"오류 발생 : {e}")
            self._com확인()
            self._새한글()
            self.문서여백(20, 20, 15, 15, 10, 10)
