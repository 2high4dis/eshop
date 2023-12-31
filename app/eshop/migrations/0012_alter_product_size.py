# Generated by Django 4.2 on 2023-06-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0011_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('6US', '6US'), ('6.5US', '6.5US'), ('7US', '7US'), ('7.5US', '7.5US'), ('8US', '8US'), ('8.5US', '8.5US'), ('9US', '9US'), ('9.5US', '9.5US'), ('10US', '10US'), ('10.5US', '10.5US'), ('11US', '11US'), ('11.5US', '11.5US')], max_length=10, verbose_name='Size'),
        ),
    ]
