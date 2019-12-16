from django.db import models
from rest_framework.serializers import *
from account.models import User
import uuid
import os
from account.models import UserSerializer

class Commodity(models.Model):
    comId = models.BigAutoField(verbose_name="商品id", primary_key=True)
    name = models.CharField(verbose_name="商品名", max_length=100)
    publish_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    price = models.DecimalField(verbose_name="价格",max_digits=20, decimal_places=10)
    description = models.TextField(verbose_name="描述", max_length=300)

    stuId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商品发布者")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ('comId', )


    def __str__(self):
        return  self.name +" : " + str(self.comId)





class Order(models.Model):
    ORDERED = 0
    AGREED = 1
    DISAGRRED = 2

    status_choices = (
        (ORDERED, "已经被预定"),
        (AGREED, "预定已同意"),
        (DISAGRRED, "预定不同意")
    )

    orderId = models.BigAutoField(verbose_name="订单id", primary_key=True)
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=ORDERED)
    appointment_time = models.DateTimeField(verbose_name="预约时间", auto_created=True)
    finished_time = models.DateTimeField(verbose_name="结束时间", null=True,blank=True)
    stuId_buyer = models.ForeignKey(User, verbose_name="买家", on_delete=models.SET_NULL, related_name="buyer_orders", null=True,blank=True)
    stuId_seller = models.ForeignKey(User, verbose_name="卖家", on_delete=models.CASCADE, related_name="seller_orders")
    comId = models.OneToOneField(Commodity, verbose_name="商品", on_delete=models.CASCADE, related_name="com_order")#一个物品只能有一个订单
    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def __str__(self):
        return str(self.orderId) +" : " + str(self.status)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # print(os.path.join(str(instance.comId.comId), "pics", filename))
    return os.path.join(str(instance.comId.comId), "pics", filename)


class CommodityPics(models.Model):
    comId = models.ForeignKey(Commodity, verbose_name="商品", on_delete=models.CASCADE, related_name="pics")
    pic = models.ImageField(verbose_name="图片", upload_to=user_directory_path)


    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
        unique_together = ("comId", "pic")
        ordering = ('comId',)

class CommodityType(models.Model):
    comId = models.ForeignKey(Commodity, verbose_name="商品", on_delete=models.CASCADE, related_name="types")
    type = models.CharField(verbose_name="类型", max_length=20)

    class Meta:
        verbose_name = "商品类型"
        verbose_name_plural = "商品类型"
        unique_together = ("comId", "type")
        ordering = ("comId",)




class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        exclude = []

    def create(self, validated_data):
        comId = validated_data['comId']
        orders = Order.objects.filter(comId=comId)
        stuId_seller = validated_data["stuId_seller"]

        if orders:
            raise  Exception("order已存在")
        elif not Commodity.objects.filter(stuId=stuId_seller):
            raise Exception("商品{} 不属于卖家 {}".format(comId, stuId_seller))
        else:
            return super(OrderSerializer,self).create(**validated_data)


class CommodityPicsSerializer(ModelSerializer):

    class Meta:
        model = CommodityPics
        exclude = []


class CommodityTypeSerializer(ModelSerializer):


    class Meta:
        model = CommodityType
        exclude = []


class CommoditySerializer(ModelSerializer):
    pics = CommodityPicsSerializer(many=True, read_only=True,)
    types = CommodityTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Commodity
        exclude = []
#根据订单信息确定状态






