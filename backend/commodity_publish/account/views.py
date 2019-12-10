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


from rest_framework.decorators import action
import logging

# Create your views here.


class IsOwner(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        print(view.kwargs)
        user = User.objects.get(pk=view.kwargs['pk'])
        if request.user == user:
            return True

        return False



#user视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    #list, detail权限管理
    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAdminUser()]
        elif self.action == "detail":
            return [permissions.IsAdminUser(), IsOwner()]
        else:
            return super(self.__class__, self).get_permissions()

    def detail(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(self.get_serializer(user).data)

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


    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        try:
            response =  self.create(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)













