# Generated by Django 2.1.5 on 2019-01-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20190112_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(max_length=5000),
        ),
    ]
