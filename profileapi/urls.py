
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include("rest_framework.urls")),
    path('api/rest-auth/', include("rest_auth.urls")),
    path('api/rest-auth/registration', include("rest_auth.registration.urls")),
    path('api/', include("profiles.urls"))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
