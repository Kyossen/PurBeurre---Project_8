from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.connect, name="connect"),
    url(r'^$', views.dashboard, name="dashboard"),
    url(r'^search/templates/', views.favorites, name="favorites"),
    url(r'^search/templates/', views.sign_up, name="sign_up"),
    url(r'^search/templates/', views.result, name="result"),
]
