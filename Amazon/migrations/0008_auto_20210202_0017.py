# Generated by Django 3.1.4 on 2021-02-01 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0007_shipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='products',
            field=models.ManyToManyField(to='Amazon.Cart'),
        ),
    ]
