from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import *
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import *
from django.contrib.auth import login, logout, authenticate
from account.views import IsOwner
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend

#todo:test api
class IsOwnerOrReadOnly(IsOwner):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(IsOwner, self).has_permission(request,self)


class CommodityViewSets(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"
    permission_classes = [permissions.IsAdminUser, IsOwnerOrReadOnly]
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list': [permissions.AllowAny],
        'retrieve': [permissions.IsAuthenticatedOrReadOnly],
        'update': permission_classes,
        'destroy': permission_classes,
    }


    # list, detail权限管理
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    # def list(self, request, *args, **kwargs):



class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

