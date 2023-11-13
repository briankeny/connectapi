from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
import authentication.urls as auth_urls
import posts.urls as p_urls

urlpatterns = [
    path('', include(auth_urls)),
    path('', include(p_urls)),
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
]

# Add this line to serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


