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
from django.db.models import Q
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

    @action(methods=['get'], detail=False, permission_classes=[IsOwnerAndIsStuAuthenticated])
    def my_commodities(self,request, *args, **kwargs):
        self.request.query_params.appendlist("stuId", request.user.stuId)
        self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False, permission_classes=[IsStuAuthenticated])
    def not_mine(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.filter(~Q(stuId=request.user.stuId))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        if order.status != Order.ORDERED:
            return Response({"msg":"错误订单"}, status=status.HTTP_400_BAD_REQUEST)


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
    def my_ordered_orders(self, request, *args, **kwargs):
        user = self.request.user

        self.request.query_params.appendlist("stuId_seller", user.stuId)
        self.list(self.request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsOwnerAndIsStuAuthenticated])
    def my_buyed_orders(self, request, *args, **kwargs):
        user = self.request.user

        self.request.query_params.appendlist("stuId_buyer", user.stuId)
        self.list(self.request, *args, **kwargs)




