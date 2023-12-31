# Generated by Django 4.2 on 2023-06-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0006_remove_shippinginfo_ship_via_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(upload_to='media/items/uploads', verbose_name='Upload an Image'),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='image',
            field=models.ImageField(null=True, upload_to='media/reviews/uploads', verbose_name='Upload an Image'),
        ),
    ]
