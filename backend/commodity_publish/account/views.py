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
from rest_framework.authentication import authenticate
from rest_framework.decorators import action

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly | permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get', 'post', 'put', 'patch'], permission_classes=[permissions.IsAdminUser | IsOwner])
    def info(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(self.get_serializer(user).data)



    @action(detail=False, methods=['post'])
    def login(self, request, pk=None):
        stuId = request.data.get("stuId","")
        password = request.data.get("password","")
        user = authenticate(request, stuId=stuId, password=password)

        if user:
            serializer = self.get_serializer(user)
            data = serializer.data
            del data['password']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"wrong password"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        try:
            self.create(self, request, *args, **kwargs)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)









