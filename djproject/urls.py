from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import core

admin.autodiscover()

urlpatterns = patterns('',
    # Admin site
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
    
urlpatterns += patterns('',
    # Common 
    (r'^', include('core.urls')),
)
