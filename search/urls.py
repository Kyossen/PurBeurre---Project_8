from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.connect, name="connect"),
    url(r'^templates/sign_up.html', views.sign_up, name="sign_up"),
    url(r'^templates/dashboard.html', views.dashboard, name="dashboard"),
    url(r'^templates/favorites.html', views.favorites, name="favorites"),
    url(r'^templates/result.html', views.result, name="result"),
    url(r'^templates/disconnect.html', views.disconnect, name="disconnect"),
]

