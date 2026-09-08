from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    # Admin site
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

urlpatterns += [
    # Common
    re_path(r'^', include('core.urls')),
]
