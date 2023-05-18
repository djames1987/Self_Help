from . import views
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from ms_identity_web.django.msal_views_and_urls import MsalViews

msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

urlpatterns = [
    path('', views.login, name='login'),
    path('sign_in_status', views.index, name='status'),
    path('token_details', views.token_details, name='token_details'),
    path('password_reset', views.passwordReset, name='password_reset'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('lookup_login', views.lookup_user, name='lookup_user'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('forgot_password_auth', views.forgot_password_auth, name='forgot_password_auth'),
    path('home', views.home, name='home'),
    path('index', views.login, name='index'),
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]