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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['comId', 'name', 'types']
    search_fields = ["name", "types"]
    ordering_fields = ["publish_time", "name", "price"]

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

    @action(methods=['get','options'], detail=False, permission_classes=[IsStuAuthenticated])
    def mine(self,request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        #删掉所有已经被预定或者已同意的订单
        orders_agreed_ordered = Order.objects.filter(Q(status=Order.AGREED) | Q(status=Order.ORDERED))
        orders_agreed_ordered_comids = orders_agreed_ordered.values_list("comId")
        queryset = queryset.filter(~Q(comId__in=orders_agreed_ordered_comids))
        queryset = queryset.filter(stuId=user.stuId)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get','options'], detail=False, permission_classes=[IsStuAuthenticated])
    def not_mine(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        # 删掉所有已经被预定或者已同意的订单
        orders_agreed_ordered = Order.objects.filter(Q(status=Order.AGREED) | Q(status=Order.ORDERED))
        orders_agreed_ordered_comids = orders_agreed_ordered.values_list("comId")
        queryset = queryset.filter(~Q(comId__in=orders_agreed_ordered_comids))
        # 效率太低，删掉
        queryset = queryset.filter(~Q(stuId=request.user.stuId))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #修改request中stuId
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #使得本人创建的商品只能是本人的
            serializer.save(stuId=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderBuyerOrIsOrderSeller]
    permission_classes_by_action = {
        'create': [IsStuAuthenticated],
        'list': [permissions.AllowAny],
        'retrieve': permission_classes,
        'update': permission_classes,
        'destroy': permission_classes,
    }
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["finished_time", "appointment_time"]
    filterset_fields = ["status"]

    #add a empty Response to make post ui available
    def list(self, request, *args, **kwargs):
        return Response()

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
    @action(detail=True, methods=['post','options'], permission_classes=[IsOrderSeller])
    def agree(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status != Order.ORDERED:
            return Response({"msg":"错误订单"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = Order.AGREED
        order.save()
        serializer = self.get_serializer(order)

        return Response(serializer.data)

    @action(detail=True, methods=['post','options'], permission_classes=[IsOrderSeller])
    def disagree(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status !=Order.ORDERED:
            return Response({"msg":"错误订单"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.DISAGRRED
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=False, methods=['get','options'], permission_classes=[IsStuAuthenticated])
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

    @action(detail=False, methods=['get','options'], permission_classes=[IsStuAuthenticated])
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stuId_buyer=self.request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=True, methods=['get','options'], permission_classes=[IsOrderBuyerOrIsOrderSeller, IsOrderAgreed])
    def users_info(self, request, *args, **kwargs):
        order = self.get_object()
        stuId_buyer = order.stuId_buyer
        stuId_seller = order.stuId_seller
        buyer_serializer = UserSerializer(stuId_buyer)
        seller_serializer = UserSerializer(stuId_seller)

        return Response({"buyer":buyer_serializer.data, "seller":seller_serializer.data})
class CommodityPicsViewSets(viewsets.ModelViewSet):

    queryset = CommodityPics.objects.all()
    serializer_class = CommodityPicsSerializer
    permission_classes = [IsCommodityPicsOwner]
    permission_classes_by_action = {
        'create': [IsStuAuthenticated],
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'update': permission_classes,
        'destroy': permission_classes,
    }

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comId']
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
                return super(CommodityPicsViewSets, self).create(request, *args, **kwargs)#fix the response bug
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
        'update': [IsCommodityTypesOwner],
        'destroy': [IsCommodityTypesOwner],
    }
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comId']
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

