# Generated by Django 2.1.5 on 2019-02-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190202_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(choices=[('Administrator', 'Admin'), ('Staff', 'Staff'), ('Vendor', 'Vendor'), ('Member', 'Member')], default='Member', max_length=120),
        ),
    ]