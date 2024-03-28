# Generated by Django 5.0.3 on 2024-03-28 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Parts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderHeaders',
            fields=[
                ('OrderID', models.IntegerField(primary_key=True, serialize=False)),
                ('CustomerID', models.IntegerField()),
                ('OrderDate', models.DateTimeField()),
                ('RequiredDate', models.DateTimeField()),
                ('ShipDate', models.DateTimeField()),
                ('Status', models.CharField(max_length=255)),
                ('ShippingMethod', models.CharField(max_length=255)),
                ('FrieghtCharge', models.FloatField()),
                ('TaxAmount', models.FloatField()),
                ('TotalAmount', models.FloatField()),
                ('PaymentReceived', models.BooleanField()),
                ('Notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='orderDetails',
            fields=[
                ('OrderDetailID', models.IntegerField(primary_key=True, serialize=False)),
                ('Quantity', models.IntegerField()),
                ('UnitPrice', models.FloatField()),
                ('LineTotal', models.CharField(max_length=255)),
                ('Status', models.CharField(max_length=255)),
                ('PartID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parts.parts')),
                ('OrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Orders.orderheaders')),
            ],
        ),
    ]
