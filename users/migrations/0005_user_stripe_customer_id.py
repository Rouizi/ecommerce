# Generated by Django 3.0.5 on 2020-05-28 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200515_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]