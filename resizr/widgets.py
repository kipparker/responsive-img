from django import forms
from django.utils.safestring import mark_safe

from .template_tags.thumb import create_thumb_url

class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            resized = create_thumb_url(value.name, width=50,
                                       height=50, fill="fill=255,255,255")
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s"  height=50/></a> '
                           % (value.url, resized)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
