# Generated by Django 2.2.7 on 2019-12-08 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20191208_1613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_authenticatedss',
            new_name='is_stu_authenticated',
        ),
    ]
