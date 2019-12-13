from my_permissions.user import IsOwner
from rest_framework import permissions
from order.models import *
from account.models import *
from rest_framework.permissions import SAFE_METHODS

class IsOrderSeller(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if super(self.__class__, self).has_permission(request, view):
            try:
                order = Order.objects.get(pk=view.kwargs['pk'])
                if order.stuId_seller == request.user.stuId:
                    return True
            except KeyError:
                pass

        return False

class IsOwnerOrReadOnly(IsOwner):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(self.__class__, self).has_permission(request,self)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(self.__class__, self).has_object_permission(request, view, obj)


class IsStuAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if super(IsStuAuthenticated, self).has_permission(request, view):
            if request.user.is_stu_authenticated:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsStuAuthenticated, self).has_object_permission(request, view):
            if request.user.is_stu_authenticated:
                return True

        return False


class IsOwnerAndIsStuAuthenticated(IsOwner, IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsOwnerAndIsStuAuthenticated, self).has_permission(request, view) and super(IsOwner, self).has_permission(request, view):
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if super(IsOwnerAndIsStuAuthenticated, self).has_object_permission(request, view, obj) and super(IsOwner, self).has_object_permission(request,view, obj):
            return True

        return False