"""
This import is obligatory for the good of the system
"""

from django.conf.urls import url

from . import views

"""
This below, the all urls of the platform
"""
urlpatterns = [
    url(r'^connect.html', views.connect, name="connect"),
    url(r'^sign_up.html', views.sign_up, name="sign_up"),
    url(r'^dashboard.html', views.dashboard, name="dashboard"),
    url(r'^favorites.html', views.favorites, name="favorites"),
    url(r'^result.html', views.result, name="result"),
    url(r'^disconnect.html', views.disconnect, name="disconnect"),
    url(r'^description.html', views.description, name="description"),
    url(r'^copyright.html', views.copyright_page, name="copyright")
]
