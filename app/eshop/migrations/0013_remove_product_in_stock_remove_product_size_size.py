# Generated by Django 4.2 on 2023-06-12 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0012_alter_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('units_in_stock', models.PositiveIntegerField(verbose_name='Number in Stock')),
                ('size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('6US', '6US'), ('6.5US', '6.5US'), ('7US', '7US'), ('7.5US', '7.5US'), ('8US', '8US'), ('8.5US', '8.5US'), ('9US', '9US'), ('9.5US', '9.5US'), ('10US', '10US'), ('10.5US', '10.5US'), ('11US', '11US'), ('11.5US', '11.5US')], max_length=10, verbose_name='Size')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eshop.product', verbose_name='Choose Product')),
            ],
        ),
    ]
