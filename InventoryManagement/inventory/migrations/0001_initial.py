# Generated by Django 5.1.2 on 2024-10-21 16:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Inventory",
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
                ("name", models.CharField(max_length=255)),
                ("rows_number", models.IntegerField()),
                ("columns_number", models.IntegerField()),
                ("layers_number", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "Inventories",
            },
        ),
        migrations.CreateModel(
            name="Stock",
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
                ("vocab_no", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=255, null=True)),
                ("description1", models.TextField(null=True)),
                ("description2", models.TextField(null=True)),
                (
                    "image",
                    models.ImageField(default="avatar.jpg", upload_to="stock_images/"),
                ),
                (
                    "unit",
                    models.CharField(
                        choices=[("kg", "Kilogram"), ("l", "Liter"), ("m", "Meter")],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("unit_cost", models.FloatField(null=True)),
                ("stocks_on_hand", models.IntegerField(default=0)),
                ("stocks_committed", models.IntegerField(default=0)),
                ("stocks_availability", models.IntegerField(editable=False)),
                ("stored_stocks", models.IntegerField(default=0)),
                ("exp_date", models.DateField(blank=True, null=True)),
                ("source", models.CharField(blank=True, max_length=255, null=True)),
                ("sold_number", models.IntegerField(default=0)),
                ("threshold", models.FloatField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InventoryLocation",
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
                ("row", models.IntegerField(null=True)),
                ("column", models.IntegerField(null=True)),
                ("layer", models.IntegerField(null=True)),
                ("reserved", models.BooleanField(default=True, null=True)),
                (
                    "inventory",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.inventory",
                    ),
                ),
                (
                    "stock",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.stock",
                    ),
                ),
            ],
            options={
                "unique_together": {("inventory", "row", "column", "layer")},
            },
        ),
    ]