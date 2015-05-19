from responsive.widgets import AdminImageWidget
from unittest import TestCase


class FakeImage(object):
    url = 'http://domain.com/an-image.png'
    name = '/an-image.png'


class WidgetTest(TestCase):
    def test_widget(self):
        test_widget = AdminImageWidget()
        img = FakeImage()
        self.assertIn(
            '/an-image-50x50-fill=255,255,255.png',
            test_widget.render(name='image', value=img),
        )
