import os

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings

from responsive.image import ResizableImage

REAL_PATH = os.path.realpath(os.path.dirname(__file__))
TEST_IMAGE = 'stranger-than-paradise.jpg'


class ResizeTest(TestCase):

    def tearDown(self):
        for f in os.listdir(settings.MEDIA_ROOT):
            if f != TEST_IMAGE:
                os.remove(os.path.join(settings.MEDIA_ROOT, f))

    def test_exists(self):
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, TEST_IMAGE))
        self.assertEquals(img.exists(), True)

    def test_is_resizable(self):
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, TEST_IMAGE))
        self.assertEquals(img.is_resizable(), False)

    def test_resized_file_created(self):
        resized = ''.join([
            os.path.splitext(TEST_IMAGE)[0],
            '-200x200',
            os.path.splitext(TEST_IMAGE)[1],
            ]
        )
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, resized))
        img.process()
        self.assertEquals(img.exists(), True)

ResizeTest = override_settings(
    MEDIA_ROOT=os.path.join(os.path.dirname(REAL_PATH),
                            'fixtures/media/'))(ResizeTest)


class ParserTest(TestCase):

    def test_parse_basic(self):
        test_basic = '%s/img/animage-200x100.jpg' %\
            settings.MEDIA_URL
        img = ResizableImage(test_basic)
        self.assertEquals(img.properties['width'], 200)
        self.assertEquals(img.properties['height'], 100)
        self.assertEquals(img.properties['operation'], None)

    def test_parse_crop(self):
        test_crop = '%s/media/img/another_image-200x100-crop.jpg' %\
            settings.MEDIA_URL
        img = ResizableImage(test_crop)
        self.assertEquals(img.properties['operation'], 'crop')

    def test_target_crop(self):
        test_target_crop = '%s/media/img/img123-200x100-crop=lt.jpg' %\
            settings.MEDIA_URL
        img = ResizableImage(test_target_crop)
        self.assertEquals(img.properties['operation'], 'crop')
        self.assertEquals(img.properties['target'], 'lt')

    def test_fill(self):
        test_target_crop = '%s/media/img/img123-200x100-fill=12,201,1.jpg' %\
            settings.MEDIA_URL
        img = ResizableImage(test_target_crop)
        self.assertEquals(img.properties['operation'], 'fill')
        self.assertEquals(img.properties['colour'], (12, 201, 1))

ParserTest = override_settings(
    MEDIA_ROOT=os.path.join(os.path.dirname(REAL_PATH),
                            'fixtures/media/'))(ParserTest)
