from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.mixins import *
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, stuId, nickname, password):
        if not stuId:
            raise ValueError("请输入学号")
        if not nickname:
            raise ValueError("请输入昵称")
        if not password:
            raise ValueError("请输入密码")
        user = self.model(
            stuId = stuId,
            nickname = nickname,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, stuId, nickname, password):
        user = self.create_user(stuId, nickname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    stuId = models.CharField(verbose_name="学号", max_length=13, unique=True, primary_key=True)
    nickname = models.CharField(verbose_name="昵称", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=100)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    campus = models.CharField(verbose_name="学院", max_length=20, null=True, blank=True)
    class_num = models.CharField(verbose_name="班级号", max_length=20, null=True, blank=True)
    is_stu_authenticated = models.BooleanField(verbose_name="是否认证", default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    USERNAME_FIELD = "stuId"
    REQUIRED_FIELDS = ["nickname", "password"]

    objects = UserManager()

    def __str__(self):
        return self.nickname + " "  + self.stuId

    class Meta(AbstractBaseUser.Meta):
        verbose_name = "用户"
        verbose_name_plural = "用户"



def user_authenticated(validated_data):
    data = validated_data.copy()
    try:
        if data["class_num"] and data["campus"] and data["phone"]:
            data["is_stu_authenticated"] = True
    except:
        data["is_stu_authenticated"] = False
    return data


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ["user_permissions","is_staff", "is_superuser","groups"]

    def update(self, instance, validated_data):
        data = user_authenticated(validated_data)

        return super(UserSerializer, self).update(instance, data)

    def create(self, validated_data):
        data = user_authenticated(validated_data)
        data['password'] = make_password(data['password'])
        return super(UserSerializer, self).create(data)




class UserSerialzierWithCommodityPublished(ModelSerializer):
    pass