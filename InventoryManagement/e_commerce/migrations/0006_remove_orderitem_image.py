# Generated by Django 5.1.2 on 2024-11-14 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0005_alter_order_additional_info_alter_order_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='image',
        ),
    ]