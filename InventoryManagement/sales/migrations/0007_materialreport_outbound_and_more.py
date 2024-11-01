# Generated by Django 5.1.2 on 2024-10-29 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pos", "0007_remove_outbound_date_added_remove_outbound_tax_and_more"),
        ("sales", "0006_materialreport"),
    ]

    operations = [
        migrations.AddField(
            model_name="materialreport",
            name="outbound",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="pos.outbound",
            ),
        ),
        migrations.AlterField(
            model_name="materialreport",
            name="expiration_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
