# Generated by Django 5.1.2 on 2024-10-24 03:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pos", "0004_outbound_sale_outbound_tax_outbound_tax_amount_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inbounditem",
            old_name="item",
            new_name="material",
        ),
        migrations.RenameField(
            model_name="outbounditem",
            old_name="item",
            new_name="material",
        ),
    ]
