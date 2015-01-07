from PIL import Image, ImageOps, ImageDraw, ImageChops
from django.conf import settings

from skylark.resizer import processors
from unittest import TestCase
from skylark.resizer.template_tags.thumb import create_thumb_url

class ThumbTest(TestCase):
    def test_thumb(self):
        formatted = create_thumb_url('animage.jpg', width=100, height=200,
                                      quality='q=80', crop='crop=lt')
        self.assertEquals(formatted, '%sanimage-100x200-crop=lt-q=80.jpg'
                                      % settings.MEDIA_URL)
