# Generated by Django 2.1.5 on 2019-01-12 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20190112_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.BinaryField(),
        ),
    ]
