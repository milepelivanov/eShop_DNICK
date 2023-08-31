# Generated by Django 4.2.4 on 2023-08-31 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eShopApp', '0006_remove_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], default='N', max_length=1),
        ),
    ]
