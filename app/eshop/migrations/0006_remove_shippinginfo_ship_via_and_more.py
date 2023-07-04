# Generated by Django 4.2 on 2023-06-11 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0005_department_department_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippinginfo',
            name='ship_via',
        ),
        migrations.AlterField(
            model_name='department',
            name='department_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eshop.city'),
        ),
    ]