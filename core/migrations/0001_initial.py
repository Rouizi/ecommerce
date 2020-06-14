# Generated by Django 3.0.5 on 2020-04-23 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('S', 'Shirt'), ('SW', 'Sport Wear'), ('OW', 'OutWear'), ('D', 'Denim')], max_length=2)),
                ('label', models.CharField(blank=True, choices=[('N', 'New'), ('BS', 'bestseller')], max_length=2, null=True)),
                ('color_label', models.CharField(blank=True, choices=[('P', 'primary'), ('D', 'danger')], max_length=1, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock', models.PositiveIntegerField()),
                ('image1', models.ImageField(upload_to='clothes')),
                ('image2', models.ImageField(upload_to='clothes')),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField()),
                ('items', models.ManyToManyField(to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
