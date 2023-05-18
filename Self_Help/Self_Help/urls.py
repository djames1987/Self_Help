from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from ms_identity_web.django.msal_views_and_urls import MsalViews

msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()
urlpatterns = [
    path('', include('Reset_Password.urls')),
    path('admin/', admin.site.urls),
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
]