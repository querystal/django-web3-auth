from django.conf.urls import url

from web3auth import views

urlpatterns = [
    url(r'^login_api/$', views.login_api, name='login_api'),
    url(r'^login/$', views.login_view),
    url(r'^signup/$', views.signup_view),
]
