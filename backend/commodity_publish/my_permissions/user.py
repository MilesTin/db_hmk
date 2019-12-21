from rest_framework import permissions
from account.models import *
from order.models import *

class IsOwner(permissions.IsAuthenticated):


    def has_permission(self, request, view):
        if super(IsOwner, self).has_permission(request, view):
            try:
                user = User.objects.get(pk=view.kwargs['pk'])
                if request.user == user:
                    return True
            except KeyError:
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
            return super(IsOwner, self).has_object_permission(request, view, obj)

class IsStuAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if super(IsStuAuthenticated, self).has_permission(request, view):
            if request.user.is_stu_authenticated:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsStuAuthenticated, self).has_object_permission(request, view, obj):
            if request.user.is_stu_authenticated:
                return True

        return False