#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some urls of the platform for users app"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^connect.html', views.connect, name="connect"),
    url(r'^sign_up.html', views.sign_up, name="sign_up"),
    url(r'^dashboard.html', views.dashboard, name="dashboard"),
    url(r'^disconnect.html', views.disconnect, name="disconnect")
]
