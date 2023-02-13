from django.urls import path
from web3auth import views

app_name = 'web3auth'

urlpatterns = [
    path(r'^login_api/$', views.login_api, name='web3auth_login_api'),
    path(r'^signup_api/$', views.signup_api, name='web3auth_signup_api'),
    path(r'^signup/$', views.signup_view, name='web3auth_signup'),
]
