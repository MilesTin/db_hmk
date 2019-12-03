from django.db import models
from rest_framework.serializers import ModelSerializer

# Create your models here.
class User(models.Model):
    stuId = models.CharField(verbose_name="学号", max_length=13, primary_key=True)
    nickname = models.CharField(verbose_name="昵称", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=100)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    campus = models.CharField(verbose_name="学院", max_length=20, null=True)
    class_num = models.CharField(verbose_name="班级号", max_length=20, null=True)

    def __str__(self):
        return self.nickname + " "  + self.stuId

    class Meta:
        verbose_name = "用户"


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ["password"]


class UserSerializerWithPassword(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class UserSerialzierWithCommodityPublished(ModelSerializer):

    commodities =