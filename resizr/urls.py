from django.conf.urls import patterns, include, url
from django.conf import settings
from .views import *

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', ResizerView.as_view())
)
