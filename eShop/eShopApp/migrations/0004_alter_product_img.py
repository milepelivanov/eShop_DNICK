# Generated by Django 4.2.4 on 2023-08-22 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eShopApp', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.URLField(max_length=255),
        ),
    ]