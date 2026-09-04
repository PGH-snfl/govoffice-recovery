"""PowerPoint 프레젠테이션과 슬라이드 조작."""


class SlideMixin:
    def 화면(self, 종류):
        # 원본 바이트코드에서도 ``종류``는 받지만 사용하지 않는다.
        현재피피티 = self.피피티.ActivePresentation
        현재피피티.PageSetup.SlideWidth = 960
        현재피피티.PageSetup.SlideHeight = 540

    def 다음페이지(self):
        현재피피티 = self.피피티.ActivePresentation
        현재피피티.Slides.Add(현재피피티.Slides.Count + 1, 12)
        self.피피티.ActiveWindow.View.GotoSlide(현재피피티.Slides.Count)

