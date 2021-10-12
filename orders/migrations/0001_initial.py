# Generated by Django 3.2.8 on 2021-10-11 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(default=None, max_length=20, null=True)),
                ('mrid', models.CharField(default=None, max_length=20, null=True)),
                ('refid', models.CharField(default=None, max_length=20, null=True)),
                ('marketplace', models.CharField(max_length=100)),
                ('purchased_at', models.DateTimeField(default=None, null=True)),
                ('amount', models.FloatField()),
                ('shipping_amount', models.FloatField(default=0)),
                ('commission_amount', models.FloatField(default=0)),
                ('processing_fee', models.FloatField(default=0)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lengow', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('price_unit', models.FloatField()),
                ('category', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.product')),
            ],
        ),
    ]
