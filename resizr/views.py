import logging

from django.views.generic.base import View
from django.http.response import (HttpResponse, HttpResponseBadRequest,
                                    HttpResponseRedirect)
from django.views.static import serve
from django.http import Http404
from django.conf import settings

from image import ResizableImage
# Create your views here.



class DevResizeServer(View):
    """
    Proxies requests to ResizerView on 404
    Serves in place of server proxy if 404 rules when using
    the development static files server
    """

    def get(self, *args, **kwargs):
        try:
            response =  serve(self.request, self.kwargs['path'],
                              settings.MEDIA_ROOT)
        except Http404:
            return ResizerView.as_view()(*args, **kwargs)
        return response


class ResizerView(View):
    def get(self, *args, **kwargs):
        response_image = None
        img = ResizableImage(self.request.path)
        try:
            response_image = img.process()
        except IOError:
            if not img.exists():
                raise Http404
            return HttpResponseBadRequest('Could not parse resize attributes')
        if img.exists():
            return HttpResponseRedirect(img.url)
        raise Http404
