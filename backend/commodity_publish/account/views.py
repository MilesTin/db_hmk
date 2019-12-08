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

from rest_framework.decorators import action
# Create your views here.




class UserDetail(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        return self.retrieve(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserList(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


#user视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    @action(detail=True, methods=['get', 'post', 'put', 'patch'], permission_classes=[permissions.IsAdminUser, permissions.IsAuthenticated])
    def info(self, request, pk=None):

        user = self.get_object()
        serializer = UserSerializer(user)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def login(self, request):
        self.perform_authentication(request)


        if request.user:
            user = self.get_object()
            serializer = self.get_serializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"wrong password"}, status=status.HTTP_403_FORBIDDEN)







