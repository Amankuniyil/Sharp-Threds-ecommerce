# Generated by Django 4.2 on 2023-04-25 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_product_image_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_1',
            field=models.ImageField(upload_to='photos/products'),
        ),
    ]
