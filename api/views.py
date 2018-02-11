#!/usr/bin/env python
# coding=utf-8


from __future__ import unicode_literals
import logging

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db.models import Q
from silk.profiling.profiler import silk_profile

from .serializers import UserSerializer, UserCreateSerializer


LOG = logging.getLogger(__name__)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @silk_profile()
    def list(self, request, *args, **kwargs):
        print('*')
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @list_route(url_path='me')
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)

    @list_route(methods=['put'], url_path='change-password')
    def change_password(self, request):
        user = request.user
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if not user.check_password(old_password):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response(UserSerializer(request.user).data)

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()

        if self.action == 'list':
            keyword = self.request.query_params.get('keyword', '').strip()

            if keyword:
                queryset = queryset.filter(Q(username__startswith=keyword) | Q(email__startswith=keyword))

        return queryset.order_by('id')

