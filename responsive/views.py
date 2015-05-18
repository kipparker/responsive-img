from django.views.generic.base import View
from django.http.response import HttpResponseRedirect
from django.views.static import serve
from django.http import Http404
from django.conf import settings

from image import ResizableImage
# Create your views here.


class DevResizeServer(View):
    """
    Proxies requests to ResponsiveView on 404
    Serves in place of server proxy if 404 rules when using
    the development static files server
    """

    def get(self, *args, **kwargs):
        try:
            response = serve(self.request, self.kwargs['path'],
                             settings.MEDIA_ROOT)
        except Http404:
            return ResponsiveView.as_view()(*args, **kwargs)
        return response


class ResponsiveView(View):
    def get(self, *args, **kwargs):
        img = ResizableImage(self.request.path)
        if not img.is_resizable():
            raise Http404("This image could not be parsed")
        try:
            img.process()
        except IOError:
            if not img.exists():
                raise Http404("Image does not exist")
        if img.exists():
            return HttpResponseRedirect(img.url)
        raise Http404
