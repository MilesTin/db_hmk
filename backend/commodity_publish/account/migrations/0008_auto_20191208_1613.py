# Generated by Django 2.2.7 on 2019-12-08 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_class_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AddField(
            model_name='user',
            name='is_authenticatedss',
            field=models.BooleanField(default=False, verbose_name='是否认证'),
        ),
    ]
