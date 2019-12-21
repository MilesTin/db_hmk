from my_permissions.user import *
from rest_framework import permissions
from order.models import *
from account.models import *
from rest_framework.permissions import SAFE_METHODS


class IsOrderBuyer(IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsOrderBuyer, self).has_permission(request, view):
            try:
                order = Order.objects.get(pk=view.kwargs['pk'])
                if order.stuId_seller == request.user:
                    return True
            except KeyError:
                pass

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsOrderBuyer, self).has_object_permission(request, view, obj):
            try:

                if obj.stuId_buyer == request.user:
                    return True
            except KeyError:
                pass

        return False


class IsOrderSeller(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if super(IsOrderSeller, self).has_permission(request, view):
            try:
                order = Order.objects.get(pk=view.kwargs['pk'])
                if order.stuId_seller == request.user:
                    return True
            except KeyError:
                pass
            except Exception as e:
                print(str(e))

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsOrderSeller, self).has_object_permission(request, view, obj):
            try:
                if obj.stuId_seller == request.user:
                    return True
            except KeyError:
                pass

        return False
class IsOwnerOrReadOnly(IsOwner):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(IsOwnerOrReadOnly, self).has_permission(request,self)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(IsOwnerOrReadOnly, self).has_object_permission(request, view, obj)





class IsOwnerAndIsStuAuthenticated(IsOwner, IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsOwnerAndIsStuAuthenticated, self).has_permission(request, view) and super(IsOwner, self).has_permission(request, view):
            return True
        return False


    def has_object_permission(self, request, view, obj):
        if super(IsOwnerAndIsStuAuthenticated, self).has_object_permission(request, view, obj) and super(IsOwner, self).has_object_permission(request,view, obj):
            return True

        return False

class IsOrderBuyerOrIsOrderSeller(IsOrderBuyer, IsOrderSeller):
    """
    订单卖家或卖家
    """
    def has_permission(self, request, view):
        if super(IsOrderBuyerOrIsOrderSeller, self).has_permission(request, view) or \
                super(IsOrderBuyer, self).has_permission(request, view):
            return True

        return False


    def has_object_permission(self, request, view, obj):
        if super(IsOrderBuyerOrIsOrderSeller, self).has_object_permission(request, view, obj) or \
                super(IsOrderBuyer, self).has_object_permission(request, view, obj):
            return True

        return False


class IsOrderAgreed(IsOrderBuyerOrIsOrderSeller):

    def has_object_permission(self, request, view, obj):
        if super(IsOrderAgreed, self).has_object_permission(request, view,  obj):
            if obj.status == Order.AGREED:
                return True

        return False
