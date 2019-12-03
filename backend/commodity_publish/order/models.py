from django.db import models
from rest_framework.serializers import *
from account.models import User
# Create your models here.
class Commodity(models.Model):
    comId = models.BigAutoField(verbose_name="商品id", primary_key=True)
    name = models.CharField(verbose_name="商品名", max_length=100)
    publish_time = models.DateTimeField(verbose_name="发布时间", auto_created=True)
    price = models.DecimalField(verbose_name="价格",max_digits=20, decimal_places=10)
    description = models.TextField(verbose_name="描述", max_length=300)

    stuId = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="商品发布者", null=True)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ('comId', )


    def __str__(self):
        return "商品 " + self.name +" : " + str(self.comId)

class CommoditySerializer(ModelSerializer):

    class Meta:
        model = Commodity
        fields = "__all__"
