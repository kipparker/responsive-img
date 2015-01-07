import os

from PIL import Image
from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings

from resizr.image import ResizableImage

REAL_PATH = os.path.realpath(os.path.dirname(__file__))
TEST_IMAGE = 'stranger-than-paradise.jpg'

class ResizerTest(TestCase):
    def test_exists(self):
        path = '%simages/stills/1/%s' % (settings.MEDIA_URL, TEST_IMAGE)
        img = ResizableImage(path)
        self.assertEquals(img.exists(), True)

    def test_resized_file_created(self):
        resized = ''.join([
            os.path.splitext('stranger-than-paradise.jpg')[0],
            '-200x200',
            os.path.splitext('stranger-than-paradise.jpg')[1],
            ]
        )
        path = '%simages/stills/1/%s' % (settings.MEDIA_URL, resized)
        img = ResizableImage(path)
        img.process()
        self.assertEquals(img.exists(), True)
