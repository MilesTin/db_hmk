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
#todo:test api
from account.views import IsOwner
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from my_permissions.order import *
from my_permissions.commodity import *
from django.db.models import Q


class CommodityViewSets(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [IsCommodityOwner]
    permission_classes_by_action = {
        'create': [IsStuAuthenticated],
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'update': permission_classes,
        'destroy': permission_classes,
    }

    # filter fields
    filterset_fields = ['comId', 'name', 'types']

    def get_permissions(self):
        try:
            if self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        except KeyError:
            pass
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(methods=['get'], detail=False, permission_classes=[IsStuAuthenticated])
    def mine(self,request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        queryset = queryset.filter(stuId=user.stuId)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
    permission_classes = [IsOwner]
    permission_classes_by_action = {
        'create': [IsStuAuthenticated],
        'list': [permissions.IsAdminUser],
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    def get_permissions(self):
        try:
            if self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        except KeyError:
            pass
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
    def disagree(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status !=Order.ORDERED:
            return Response({"msg":"错误订单"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.DISAGRRED
        serializer = self.get_serializer(order, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"msg": "disagree successful"})

    @action(detail=False, methods=['get'], permission_classes=[IsStuAuthenticated])
    def my_seller(self, request, *args, **kwargs):
        user = self.request.user

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.filter(stuId_seller=user.stuId)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsStuAuthenticated])
    def my_buyer(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = queryset.filter(stuId_buyer=user.stuId)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommodityPicsViewSets(viewsets.ModelViewSet):

    queryset = CommodityPics.objects.all()
    serializer_class = CommodityPicsSerializer
    permission_classes = [IsCommodityOwner]
    permission_classes_by_action = {
        'create': IsStuAuthenticated,
        'list': permissions.AllowAny,
        'retrieve': permissions.AllowAny,
        'update': permission_classes,
        'destroy': permission_classes,
    }

    # list, detail权限管理
    def get_permissions(self):
        try:
            if self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        except KeyError:
            pass
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            if user.commodity_set.filter(comId=data['comId']):
                super(CommodityPicsViewSets, self).create(request, *args, **kwargs)
            else:
                return Response({"msg":"not your commodity"}, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        type = self.get_object()
        com = type.comId

        if user.commodity_set.filter(comId=com.comId):
            return super(CommodityPicsViewSets, self).update(request, *args, **kwargs)
        else:
            return Response({"msg":"not your commodity"}, status=status.HTTP_403_FORBIDDEN)


class CommodityTypesViewSets(viewsets.ModelViewSet):
    queryset = CommodityType.objects.all()
    serializer_class = CommodityTypeSerializer
    permission_classes = [IsStuAuthenticated]

    permission_classes_by_action = {
        'create': permission_classes,
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'update': IsCommodityTypesOwner,
        'destroy': IsCommodityTypesOwner,
    }

    # list, detail权限管理
    def get_permissions(self):
        try:
            if self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        except KeyError:
            pass
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            if user.commodity_set.filter(comId=data['comId']):
                return super(CommodityTypesViewSets, self).create(request, *args, **kwargs)
            else:
                return Response({"msg": "not your commodity"}, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        type_obj = self.get_object()
        comId = type_obj.comId
        if comId in user.commodity_set:
            return super(CommodityTypesViewSets, self).update(request, *args, **kwargs)
        else:
            return Response({"msg":"not your commodity"}, status=status.HTTP_403_FORBIDDEN)

