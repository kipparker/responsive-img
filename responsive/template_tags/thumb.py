from django import template
from django.conf import settings
register = template.Library()


class ProfileImage():

    def __init__(self, url, width=None, height=None):
        self.url = url
        self.width = width
        self.height = height

    def __unicode__(self):
        return self.url


def create_thumb_url(url, width=None, height=None, crop=None, fill=None, quality=None):
    name = url.split('.')
    basename, file_type = '.'.join(name[:-1]), name[-1]

    thumb_url = '%s-' % basename

    if width:
        thumb_url += '%s' % width

    thumb_url += 'x'

    if height:
        thumb_url += '%s' % height

    if crop:
        thumb_url += '-%s' % crop

    elif fill:
        thumb_url += '-%s' % fill

    if quality:
        thumb_url += '-q=%s' % quality.split('=')[-1]

    thumb_url += '.%s' % file_type

    return settings.MEDIA_URL + thumb_url


@register.assignment_tag(takes_context=True)
def thumb(context, url, geometry, *args, **kwargs):
    """
    Format is:
    {% thumbnail url widthxheight "[crop]" "[quality]" as name %}

    returns

    basename-widthxheight-crop[=lt]-q80.png

    basename-widthxheight-fill[=200,100,50,0]-q80.png

    TODO - return correct width and height after proportional resize

    """
    width, height = geometry.split('x')

    crop, fill, quality = None, None, None
    for arg in args:
        if arg.startswith('crop'):
            crop = arg
        if arg.startswith('quality='):
            quality = arg
        if arg.startswith('fill'):
            fill = arg

    thumb_url = create_thumb_url(url, width, height, crop, fill, quality)

    pi = ProfileImage(thumb_url,
                      width,
                      height
                      )
    return pi
