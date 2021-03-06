# Generated by Django 3.0.5 on 2020-04-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200424_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='color_label',
            field=models.CharField(blank=True, choices=[('P', 'primary-color'), ('D', 'danger-color')], max_length=1, null=True),
        ),
    ]
