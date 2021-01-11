# Generated by Django 3.1.5 on 2021-01-11 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('kitchen', '0004_products_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='products',
            name='text',
        ),
        migrations.AddField(
            model_name='products',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='unit',
            field=models.TextField(null=True),
        ),
    ]
