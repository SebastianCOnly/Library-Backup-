# Official_LMS/urls.py

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ensures that any files in the MEDIA_ROOT directory can be accessed via URLs that start with MEDIA_URL.
