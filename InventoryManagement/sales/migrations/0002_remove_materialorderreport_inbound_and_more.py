# Generated by Django 5.1.2 on 2024-10-22 04:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("e_commerce", "0002_rename_product_cartitem_item_and_more"),
        ("inventory", "0002_category_date_added_category_date_updated_and_more"),
        ("pos", "0003_inbounditem_outbounditem_and_more"),
        ("sales", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="materialorderreport",
            name="inbound",
        ),
        migrations.RemoveField(
            model_name="materialorderreport",
            name="material",
        ),
        migrations.RemoveField(
            model_name="materialorderreport",
            name="outbound",
        ),
        migrations.RemoveField(
            model_name="materialorderreport",
            name="user",
        ),
        migrations.RemoveField(
            model_name="materialorderrequisition",
            name="material",
        ),
        migrations.RemoveField(
            model_name="materialorderrequisition",
            name="order_requisition",
        ),
        migrations.RemoveField(
            model_name="orderrequisition",
            name="material_order",
        ),
        migrations.RemoveField(
            model_name="orderrequisition",
            name="inventory",
        ),
        migrations.RemoveField(
            model_name="orderrequisition",
            name="staff",
        ),
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100)),
                ("sub_total", models.FloatField(default=0)),
                ("grand_total", models.FloatField(default=0)),
                ("tax_amount", models.FloatField(default=0)),
                ("tax", models.FloatField(default=0)),
                ("tendered_amount", models.FloatField(default=0)),
                ("amount_change", models.FloatField(default=0)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "order_requisition",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="e_commerce.orderrequisition",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SaleItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField(default=0)),
                ("qty", models.FloatField(default=0)),
                ("total", models.FloatField(default=0)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.stock",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sales.sale"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="MaterialOrder",
        ),
        migrations.DeleteModel(
            name="MaterialOrderReport",
        ),
        migrations.DeleteModel(
            name="MaterialOrderRequisition",
        ),
        migrations.DeleteModel(
            name="OrderRequisition",
        ),
    ]