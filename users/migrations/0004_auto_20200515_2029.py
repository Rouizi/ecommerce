# Generated by Django 3.0.5 on 2020-05-15 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200513_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='billing_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='billing_zip',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='shipping_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='shipping_zip',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
