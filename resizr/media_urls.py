import re

from django.conf import settings
from django.conf.urls.static import static, url

from .views import ResizerView, DevResizeServer


def resizer_urls():

    if (settings.DEBUG is True and settings.DEV_RESIZE_SERVER is True):

        return static(settings.MEDIA_URL,
                      view=DevResizeServer.as_view(),
                      document_root=settings.MEDIA_ROOT)
    else:

        return [url(
            r'^media/(?P<path>.*)$', ResizerView.as_view()
        )]
