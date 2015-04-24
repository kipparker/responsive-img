from django.conf.urls import patterns, url
from .views import ResizerView

urlpatterns = patterns(
    '', url(r'^(?P<path>.*)$', ResizerView.as_view())
)
