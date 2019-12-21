from django.db import models
from rest_framework.serializers import *
from account.models import User
import uuid
import os
from account.models import UserSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core import validators as django_validators
from rest_framework import validators

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


#
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
    appointment_time = models.DateTimeField(verbose_name="预约时间", auto_now=True, editable=False)
    finished_time = models.DateTimeField(verbose_name="结束时间", null=True,blank=True)
    stuId_buyer = models.ForeignKey(User, verbose_name="买家", on_delete=models.SET_NULL, related_name="buyer_orders", null=True,blank=True)
    stuId_seller = models.ForeignKey(User, verbose_name="卖家", on_delete=models.CASCADE, related_name="seller_orders")
    comId = models.ForeignKey(Commodity, verbose_name="商品", on_delete=models.SET_NULL, related_name="com_order", null=True)
    #一个物品可以有多个订单，但只有不同意时有多个订单，即ORDERED， DISAGREEED只能有一个
    #fixme:在

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def __str__(self):
        return str(self.orderId) +" : " + self.status_choices[self.status][1]

    def clean(self):
        if self.finished_time:
            if self.finished_time <= self.appointment_time:
                raise ValidationError("结束时间早与开始时间")

        if self.stuId_seller == self.stuId_buyer:
            raise ValidationError("卖家买家为同一人")

        return super(Order, self).clean()

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
    comId = serializers.IntegerField(validators=[validators.UniqueValidator,])
    class Meta:
        model = Order
        exclude = []

    def create(self, validated_data):
        comId = validated_data['comId']
        orders = Order.objects.filter(comId=comId)
        stuId_seller = validated_data["stuId_seller"]

        if orders:
            raise Exception("order已存在")
        elif not Commodity.objects.filter(stuId=stuId_seller):
            raise Exception("商品{} 不属于卖家 {}".format(comId, stuId_seller))
        else:
            return super(OrderSerializer,self).create(**validated_data)

    #validate_comId not working
    @classmethod
    def validate_comId(cls, comId):
        # 检查comId对应商品是否有状态为AGREEED或ORDERED的订单
        order_set = Order.objects.filter(Q(comId=comId) & (Q(status=Order.AGREED) | Q(status=Order.ORDERED)))
        if order_set:
            raise serializers.ValidationError("此商品已经有有效订单存在")
        print(order_set)
        return comId

    def validate(self, attrs):
        instance = Order(**attrs)
        instance.clean()
        return super(OrderSerializer, self).validate(attrs)


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
    price = serializers.DecimalField(max_digits=20, decimal_places=10,min_value=0,max_value=100000, )

    class Meta:
        model = Commodity
        exclude = []
#根据订单信息确定状态






