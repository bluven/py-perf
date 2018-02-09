#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from . import views


router = DefaultRouter()
router.register('users', views.UserViewSet)

auth_patterns = [
    path('auth/token/', obtain_jwt_token),
    path('auth/refresh-token/', refresh_jwt_token),
]

urlpatterns = [
    path('api/', include(auth_patterns)),
    url('^api/', include(router.urls)),
]
