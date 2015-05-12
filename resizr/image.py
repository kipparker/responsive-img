import re
# import os

from django.core.files.storage import default_storage

from PIL import Image
from django.conf import settings

# from StringIO import StringIO
# import requests

from . import processors

RE_IMAGE_URL = ('(?P<basename>.*)\\-(?P<width>[0-9]+)x(?P<height>[0-9]+)'
                '(\-(?P<operation>crop|fill))?'
                '(=((?P<colour>\d{1,3},\d{1,3},\d{1,3}[,\d{1,3}]?)|'
                '(?P<target>[lcr][tmb]+)))?'
                '\\.(?P<ext>gif|jpg|jpeg|png|JPG)')

"""TODO
Allow using an additional extension to convert the image
eg. myimage.gif.png
Make the default image type PNG
implement transparencies
Test django storages
Add testing

"""


class ResizableImage(object):
    """
    given a path, creates an object with methods to resize the image
    """

    def __init__(self, path, *arg, **kwargs):
        """
        Path will be everything from the /
        """
        self.url = path
        self.relative_path = self.url[
            (self.url.find(settings.MEDIA_URL) + len(settings.MEDIA_URL)):
        ]
        self.real_path = '%s%s' % (settings.MEDIA_ROOT, self.relative_path)
        match = re.match(RE_IMAGE_URL, self.relative_path)
        try:
            self.properties = self.clean_properties(match.groupdict())
        except AttributeError:
            self.properties = None

    def is_resizable(self):
        return self.properties is not None

    def save_image(self, img):
        f = default_storage.open(self.relative_path, 'w')
        img.save(f, quality=80)

    def process(self):
        if not self.exists():
            img = self.create_thumbnail()
            self.save_image(img)
            return img
        else:
            return None

    def get_url(self):
        if hasattr(settings, 'S3_URL'):
            return settings.S3_URL + self.url
        else:
            return self.url

    def get_image(self):
        return Image.open(default_storage.open(self.base_path(), 'r').file)

    def create_thumbnail(self):
        original_image = self.get_image()
        size = (self.properties['width'], self.properties['height'])
        if self.properties['operation'] == 'crop':
            img = processors.scale_and_crop(
                original_image,
                size,
                crop=True,
                target=self.properties['target'],
            )

        elif self.properties['operation'] == 'fill':
            img = processors.fill(
                original_image,
                size,
                self.properties['colour']
            )
        else:
            img = processors.scale_and_crop(
                original_image,
                size,
            )
        return img

    def clean_properties(self, dict):
        """
        Convert the properties into attributes, by calculation where necessary
        """
        self.crop = False
        for key, val in dict.items():
            if key in ('width', 'height') and val is not None:
                val = int(dict[key])
            if key == 'crop' or key == 'fill' and val is not None:
                val = True
            if key == 'colour' and val is not None:
                val = tuple([int(i) for i in val.split(',')])
            dict[key] = val
        return dict

    def base_path(self):
        if hasattr(self, 'properties'):
            return '%s.%s' % (
                self.properties['basename'], self.properties['ext']
            )
        return self.real_path

    def exists(self):
        return default_storage.exists(self.relative_path)
