from django import forms
from django.utils.safestring import mark_safe

from responsive.template_tags.thumb import create_thumb_url
"""
class Widget(six.with_metaclass(MediaDefiningClass)):
    needs_multipart_form = False  # Determines does this widget need multipart form
    is_localized = False
    is_required = False

    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

class Input(Widget):

    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    input_type = None  # Subclasses must define this.

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html('<input{0} />', flatatt(final_attrs))

class FileInput(Input):
    input_type = 'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
        return super(FileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        return files.get(name, None)

"""


class AdminImageWidget(forms.FileInput):
    """
    An ImageField Widget for admin that shows a thumbnail
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
