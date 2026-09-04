"""PowerPoint COM 연결 계층."""

try:
    from win32com.client import GetActiveObject
    from win32com.client.gencache import EnsureDispatch
except ImportError:  # COM 없는 환경에서도 소스와 API를 검사할 수 있게 한다.
    GetActiveObject = None
    EnsureDispatch = None


class PowerPointConnectionMixin:
    피피티 = None

    @staticmethod
    def _com함수확인():
        if GetActiveObject is None or EnsureDispatch is None:
            raise RuntimeError("PowerPoint 자동화에는 pywin32가 필요합니다.")

    def _새프레젠테이션(self):
        self.피피티 = EnsureDispatch("PowerPoint.Application")
        self.피피티.Visible = True
        현재피피티 = self.피피티.Presentations.Add()
        현재피피티.Slides.Add(1, 12)
        현재피피티.PageSetup.SlideWidth = 960
        현재피피티.PageSetup.SlideHeight = 540

    def 시작(self):
        """실행 중인 PowerPoint에 연결하고, 없으면 새 프레젠테이션을 만든다."""
        self._com함수확인()
        try:
            self.피피티 = GetActiveObject("PowerPoint.Application")
        except ValueError as e:
            print(f"값 오류 : {e}")
            self._새프레젠테이션()
        except Exception as e:
            print(f"오류 발생 : {e}")
            self._새프레젠테이션()

