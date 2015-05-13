from django.conf.urls import patterns, url
from .views import ResponsiveView

urlpatterns = patterns(
    '', url(r'^(?P<path>.*)$', ResponsiveView.as_view())
)
