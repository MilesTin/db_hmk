from .user import *
from .order import *


class IsCommodityOwner(IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsCommodityOwner, self).has_permission(request, view):
            try:
                commodity = Commodity.objects.get(pk=view.kwargs['pk'])
                if request.user == commodity.stuId:
                    return True
            except KeyError:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsCommodityOwner, self).has_object_permission(request, view, obj):
            try:
                commodity = Commodity.objects.get(pk=view.kwargs['pk'])
                if request.user == commodity.stuId:
                    return True
            except KeyError:
                return False

        return False


class IsCommodityTypesOwner(IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsCommodityTypesOwner, self).has_permission(request, view):
            try:
                commodity_type = CommodityType.objects.get(pk=view.kwargs['pk'])
                com_id = commodity_type.comId
                print(com_id)
                if com_id in request.user.commodity_set:
                    return True

            except KeyError:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsCommodityTypesOwner, self).has_object_permission(request,view, obj):
            try:
                commodity_type = CommodityType.objects.get(pk=view.kwargs['pk'])
                com_id = commodity_type.comId
                if com_id in request.user.commodity_set:
                    return True

            except KeyError:
                return False

        return False


class IsCommodityPicsOwner(IsStuAuthenticated):

    def has_permission(self, request, view):
        if super(IsCommodityPicsOwner, self).has_permission(request, view):
            try:
                commodity_pic = CommodityPics.objects.get(pk=view.kwargs['pk'])
                com_id = commodity_pic.comId
                print(com_id)
                if com_id in request.user.commodity_set:
                    return True

            except KeyError:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if super(IsCommodityPicsOwner, self).has_object_permission(request,view, obj):
            try:
                commodity_pic = CommodityPics.objects.get(pk=view.kwargs['pk'])
                com_id = commodity_pic.comId
                if com_id in request.user.commodity_set:
                    return True

            except KeyError:
                return False

        return False