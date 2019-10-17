#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the somes urls of the platform for search app"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^favorites.html', views.favorites, name="favorites"),
    url(r'^result.html', views.result, name="result"),
    url(r'^description.html', views.description, name="description"),
    url(r'^copyright.html', views.copyright_page, name="copyright")
]
