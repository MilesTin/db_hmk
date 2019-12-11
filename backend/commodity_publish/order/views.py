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
from my_permissions.order import *
#todo:test api



class CommodityViewSets(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.IsAdminUser, IsOwner]
    permission_classes_by_action = {
        'create': [IsStuAuthenticated],
        'list': [permissions.AllowAny],
        'retrieve': [permissions.IsAuthenticatedOrReadOnly],
        'update': permission_classes,
        'destroy': permission_classes,
    }
    #todo:list 需要讲当前用户发布的物品移除
    # list, detail权限管理
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser, IsOwner]
    permission_classes_by_action = {
        'create': [IsOwnerAndIsStuAuthenticated],
        'list': permission_classes,
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    # list, detail权限管理
    def get_permissions(self):

        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    #传入stuId_buyer
    @action(detail=True, methods=['post'], permission_classes=[IsOwnerAndIsStuAuthenticated])
    def agree(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = Order.AGREED
        serializer = self.get_serializer(order, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"msg":"agree successful"})

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerAndIsStuAuthenticated])
    def dis_agree(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = Order.DISAGRRED
        serializer = self.get_serializer(order, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"msg": "disagree successful"})

    @action(detail=False, methods=['get'], permission_classes=[IsOwnerAndIsStuAuthenticated])
    def my_orders(self, request, *args, **kwargs):
        pass

