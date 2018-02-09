#!/usr/bin/env python
# coding=utf-8

from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers


class DateTimeTzAwareField(serializers.DateTimeField):

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_representation(value)


def readonly_datetime_field():
    return DateTimeTzAwareField(format="%Y-%m-%d %H:%M:%S", read_only=True)


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name",
                  "is_superuser", "is_active", "is_staff", "date_joined", "last_login")

    date_joined = readonly_datetime_field()
    last_login = readonly_datetime_field()
