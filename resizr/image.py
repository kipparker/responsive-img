import re
import os

from django.core.files.storage import default_storage

from PIL import Image
from django.conf import settings

from StringIO import StringIO
import requests

from . import processors


class ResizableImage(object):
    """
    given path, exposes methods to resize an image
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
        self.build_expressions()


    def save_image(self, img):
        if hasattr(settings, 'S3_URL'):
            s3_key = default_storage.open(self.url, 'w')
            img.save(s3_key, quality=80)
            s3_key.close()
            return True
        else:
            return img.save(self.real_path, quality=80)

    def process(self):
        if not self.exists():
            properties = self.get_image_properties()
            img = self.create_thumbnail(properties)
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
        if hasattr(settings, 'S3_URL'):
            url = '%s%s' % (settings.S3_URL, self.base_path(),)
            data = requests.get(url, verify=False)
            raw = ''
            for chunk in data.iter_content():
                if chunk:
                    raw += chunk

            file = StringIO(raw)
            return_image = Image.open(file)
        else:
            return_image = Image.open(self.base_path())
        return return_image

    def get_existing_image(self):
        if hasattr(settings, 'S3_URL'):
            url = '%s%s' % (settings.S3_URL, self.url,)
            data = requests.get(url, verify=False)
            raw = ''
            for chunk in data.iter_content():
                if chunk:
                    raw += chunk

            file = StringIO(raw)
            return_image = Image.open(file)
        else:
            return_image = Image.open(self.base_path())
        return return_image

    def create_thumbnail(self, properties):
        original_image = self.get_image()
        size = (properties['width'], properties['height'])
        if 'crop' in properties:
            img = processors.scale_and_crop(
                original_image,
                size,
                crop=True,
                target=properties.get('target'),
            )

        elif 'fill' in properties:
            img = processors.fill(
                original_image,
                size,
                properties.get('colour')
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
            if key in ('width', 'height'):
                val = int(dict[key])
            if key == 'crop' or key == 'fill':
                val = True
            if key == 'colour':
                val = tuple([int(i) for i in val.split(',')])
            dict[key] = val
        return dict

    def build_expressions(self):
        basename = '(?P<basename>.*)'
        extensions = '(?P<ext>gif|jpg|jpeg|png|JPG)'
        width = '(?P<width>[0-9]+)'
        height = '(?P<height>[0-9]+)'
        crop = '(?P<crop>crop)'
        fill = '(?P<fill>fill)=(?P<colour>\d{1,3},\d{1,3},\d{1,3}[,\d{1,3}]?)'
        target = '(?P<target>[lcr][tmb]+)'

        self.matches = [
            r'%s\-%sx%s-%s\.%s' % (basename, width, height, fill, extensions),
            r'%s\-%sx%s-%s\=%s\.%s' % (basename, width, height, crop,
                                       target, extensions),
            r'%s\-%sx%s-%s\.%s' % (basename, width, height, crop, extensions),
            r'%s\-%sx%s\.%s' % (basename, width, height, extensions),
            r'%s\.%s' % (basename, extensions)
        ]

    def get_image_properties(self):
        self.properties = {}
        for r in self.matches:
            match = re.match(r, self.relative_path)
            if match is not None:
                self.properties = match.groupdict()
                break
        return self.clean_properties(self.properties)

    def base_path(self):
        if self.properties:
            return '%s%s.%s' % (
                settings.MEDIA_ROOT, self.properties['basename'],
                self.properties['ext']
            )
        return self.real_path

    def exists(self):
        if hasattr(settings, 'S3_URL'):
            return default_storage.exists(self.url)
        else:
            return os.path.exists(self.real_path)
