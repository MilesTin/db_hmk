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
from order.models import Order


from rest_framework.decorators import action
import logging
logger = logging.getLogger(__name__)
# Create your views here.


class IsOwner(permissions.IsAuthenticated):


    def has_permission(self, request, view):
        if super(self.__class__, self).has_permission(request, view):
            try:
                user = User.objects.get(pk=view.kwargs['pk'])
                if request.user == user:
                    return True
            except Exception as e:
                #fixme:something bad may happen
                pass
        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user == obj
        elif isinstance(obj, Order):
            stuId_buyer = Order.stuId_buyer
            stuId_seller = Order.stuId_seller
            try:
                seller = User.objects.get(pk=stuId_seller)
                if seller == request.user:
                    return True
            except User.DoesNotExist:
                pass
            try:
                buyer = User.objects.get(pk=stuId_buyer)
                if buyer == request.user:
                    return True
            except User.DoesNotExist:
                pass
            return False
        else:
            return super(self.__class__, self).has_object_permission(request, view, obj)

#user视图集
class UserViewSet(viewsets.ModelViewSet):
    safe_fields = ("stuId", "nickname")
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, IsOwner]
    permission_classes_by_action = {
        'create': [permissions.AllowAny],
        'list': permission_classes,
        'retrieve': [permissions.IsAuthenticatedOrReadOnly],
        'update': permission_classes,
        'destroy': permission_classes,
    }

    #list, detail权限管理
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    # @action(detail=True, methods=['post','in get'])
    # def detail(self, request, *args, **kwargs):
    #     #FIXME:权限管理有点问题,2017能访问2019等等
    #     user = self.get_object()
    #     serializer = self.get_serializer(user, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request, pk=None):
        stuId = request.data.get("stuId","")
        password = request.data.get("password","")
        user = authenticate(request, stuId=stuId, password=password)
        login(request, user)

        if user:
            request.user = user
            request.user.save()
            request.session.save()
            serializer = self.get_serializer(user)
            data = serializer.data

            del data['password']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        logout(request)

        return Response({"msg":"logout successful"}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        try:
            response = super(self.__class__, self).create(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if IsOwner().has_permission(request,self):
            return Response(self.get_serializer(user).data)
        else:
            serializer = self.get_serializer(user)
            data = serializer.data
            safe_data = {}

            try:
                for key in self.safe_fields:
                    safe_data[key] = data[key]
            except KeyError:
                #fixme:这可能会出错
                pass
            return Response(safe_data)















