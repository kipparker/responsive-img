from django.conf import settings

from unittest import TestCase
from responsive.template_tags.thumb import create_thumb_url, thumb


class ThumbTest(TestCase):
    def test_thumb(self):
        formatted = create_thumb_url(
            'animage.jpg', width=100, height=200, quality='q=80',
            crop='crop=lt')
        self.assertEquals(
            formatted,
            '%sanimage-100x200-crop=lt-q=80.jpg' % settings.MEDIA_URL)

    def test_crop_tag(self):
        test_string = 'http://any-url.com/animage-%s.png'
        url = "http://any-url.com/animage.png"
        geometry = "300x400"
        crop = "crop=lt"
        fill = "fill=23,45,78"
        self.assertEquals(thumb({}, url, geometry).url, test_string % geometry)
        self.assertEquals(
            thumb({}, url, geometry, crop).url,
            test_string % ('%s-%s' % (geometry, crop)))
        self.assertEquals(
            thumb({}, url, geometry, fill).url,
            test_string % ('%s-%s' % (geometry, fill)))
