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

class CommodityViewSets(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'DETAIL':
            return [IsOwner, permissions.IsAuthenticatedOrReadOnly]


class OrderViewSets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

