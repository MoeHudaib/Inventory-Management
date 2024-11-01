# Generated by Django 5.1.2 on 2024-10-22 04:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("e_commerce", "0001_initial"),
        ("inventory", "0002_category_date_added_category_date_updated_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="product",
            new_name="item",
        ),
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together={("item", "cart")},
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
                    "cart",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="e_commerce.cart",
                    ),
                ),
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_requisitions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderRequisitionItem",
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
                (
                    "order_requisition",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="material_orders",
                        to="e_commerce.orderrequisition",
                    ),
                ),
            ],
        ),
    ]
