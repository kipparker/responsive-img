import os
import sys

from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.utils.importlib import import_module

from responsive.image import ResizableImage

REAL_PATH = os.path.realpath(os.path.dirname(__file__))
TEST_IMAGE = 'stranger-than-paradise.jpg'


class RemovesImageTest(TestCase):

    def tearDown(self):
        for f in os.listdir(settings.MEDIA_ROOT):
            if f != TEST_IMAGE:
                os.remove(os.path.join(settings.MEDIA_ROOT, f))


class DevServerTest(RemovesImageTest):

    def test_dev_server(self):
        basename = TEST_IMAGE.split('.')[0]
        resized_url = '/media/{0}-200x100.jpg'.format(basename)
        rsp = self.client.get(resized_url, follow=True)
        self.assertEquals(rsp.status_code, 200)
        self.assertEquals(len(rsp.redirect_chain), 1)
        self.assertEquals(rsp.redirect_chain[0][1], 302)

DevServerTest = override_settings(
    MEDIA_ROOT=os.path.join(os.path.dirname(REAL_PATH), 'fixtures/media/'),
    MEDIA_URL='/media/', DEBUG=True)(DevServerTest)


class ViewTest(RemovesImageTest):

    def test_redirect(self):
        basename = TEST_IMAGE.split('.')[0]
        resized_url = '/media/{0}-200x100.jpg'.format(basename)
        rsp = self.client.get(resized_url)
        self.assertEquals(rsp.status_code, 302)

    def test_bad_format(self):
        basename = TEST_IMAGE.split('.')[0]
        resized_url = '/media/{0}200x100.jpg'.format(basename)
        rsp = self.client.get(resized_url)
        self.assertEquals(rsp.status_code, 404)

    def test_doesnt_exist(self):
        resized_url = '/media/this_is_not_an_image-200x100.jpg'
        rsp = self.client.get(resized_url)
        self.assertEquals(rsp.status_code, 404)

ViewTest = override_settings(
    MEDIA_ROOT=os.path.join(os.path.dirname(REAL_PATH), 'fixtures/media/'),
    MEDIA_URL='/media/')(ViewTest)


class ResizeTest(RemovesImageTest):

    def _make_parseable_image(self, img, options):
        return ''.join([
            os.path.splitext(img)[0], options, os.path.splitext(img)[1]
            ]
        )

    def test_exists(self):
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, TEST_IMAGE))
        self.assertEquals(img.exists(), True)

    def test_crop(self):
        resized = self._make_parseable_image(TEST_IMAGE, '-200x200-crop=lt')
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, resized))
        img.process()
        self.assertEquals(img.exists(), True)

    def test_fill(self):
        resized = self._make_parseable_image(
            TEST_IMAGE, '-200x200-fill=1,2,3')
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, resized))
        img.process()
        self.assertEquals(img.exists(), True)

    def test_is_resizable(self):
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, TEST_IMAGE))
        self.assertEquals(img.is_resizable(), False)

    def test_resized_file_created(self):
        resized = self._make_parseable_image(TEST_IMAGE, '-200x200')
        img = ResizableImage(os.path.join(settings.MEDIA_ROOT, resized))
        img.process()
        self.assertEquals(img.exists(), True)


ResizeTest = override_settings(
    MEDIA_ROOT=os.path.join(
        os.path.dirname(REAL_PATH), 'fixtures/media/'))(ResizeTest)


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
