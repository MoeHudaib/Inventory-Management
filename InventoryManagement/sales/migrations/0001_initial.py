# Generated by Django 5.1.2 on 2024-10-21 16:18

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("inventory", "0001_initial"),
        ("pos", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MaterialOrder",
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
                ("quantity", models.PositiveIntegerField()),
                ("expiration_date", models.DateField(null=True)),
                ("sold_date", models.DateField(null=True)),
                ("number_sold", models.IntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.stock",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaterialOrderReport",
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
                ("quantity", models.IntegerField()),
                ("expiration_date", models.DateField(null=True)),
                (
                    "inbound",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="material_inbound_reports",
                        to="pos.inbound",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.stock",
                    ),
                ),
                (
                    "outbound",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="material_outbound_reports",
                        to="pos.outbound",
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
            name="MaterialOrderRequisition",
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
                ("quantity", models.IntegerField(null=True)),
                ("sold_date", models.DateTimeField(blank=True, null=True)),
                ("active", models.BooleanField(default=True)),
                ("number_sold", models.IntegerField(default=0)),
                (
                    "material",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.stock",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderRequisition",
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
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("delivery_date", models.DateField()),
                (
                    "shipped_via",
                    models.CharField(
                        blank=True,
                        choices=[("ground", "Ground")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "payment_terms",
                    models.CharField(
                        choices=[("cash", "Cash"), ("credit card", "Credit Card")],
                        max_length=50,
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=3,
                        default=0,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("done", models.BooleanField(default=False)),
                (
                    "inventory",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_requisitions",
                        to="inventory.inventory",
                    ),
                ),
                (
                    "material_order",
                    models.ManyToManyField(
                        related_name="order_requisitions",
                        through="sales.MaterialOrderRequisition",
                        to="inventory.stock",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_requisitions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="materialorderrequisition",
            name="order_requisition",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="material_orders",
                to="sales.orderrequisition",
            ),
        ),
    ]