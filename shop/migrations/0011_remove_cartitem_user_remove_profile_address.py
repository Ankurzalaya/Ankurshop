# Generated by Django 4.0.2 on 2022-02-25 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0010_remove_order_profile_order_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="user",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="address",
        ),
    ]
