# Generated by Django 5.1.2 on 2024-11-08 09:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('e_commerce', '0001_initial'),
        ('inventory', '0001_initial'),
        ('pos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=True)),
                ('inbound', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbound_reports', to='pos.inbound')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, null=True)),
                ('sub_total', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('tax_amount', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('tendered_amount', models.FloatField(blank=True, default=0, null=True)),
                ('amount_change', models.FloatField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='e_commerce.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('qty', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.stock')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
        ),
    ]
