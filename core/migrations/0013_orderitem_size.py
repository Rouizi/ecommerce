# Generated by Django 3.0.5 on 2020-05-03 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200503_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Size'),
        ),
    ]
