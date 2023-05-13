# Generated by Django 4.2.1 on 2023-05-13 10:22

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/category/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cId', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default=('female', 'Female'), max_length=20)),
                ('height', models.CharField(blank=True, max_length=50, null=True)),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/customer/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('eId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('weight', models.CharField(blank=True, max_length=50, null=True)),
                ('length', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('refrences', models.CharField(max_length=255)),
                ('activity_date', models.DateField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('pId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/payment/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=255)),
                ('cross_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('desc', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('meta_description', models.TextField(max_length=155)),
                ('meta_keywords', models.TextField(max_length=155)),
                ('draft', models.BooleanField(default=False)),
                ('main_image', models.ImageField(upload_to='media/products/')),
                ('hover_image', models.ImageField(upload_to='media/products/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')], default=('l', 'L'), max_length=4)),
                ('qty', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/product-variant/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='SoldProduct',
            fields=[
                ('sId', models.AutoField(primary_key=True, serialize=False)),
                ('sold_qty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.productsize')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.DecimalField(decimal_places=0, max_digits=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('oId', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField()),
                ('size', models.CharField(choices=[('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL')], default=('m', 'M'), max_length=4, verbose_name='Size')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('received', 'Received'), ('case-back', 'Cash Back')], default=('pending', 'Pending'), max_length=20, verbose_name='Payment Status')),
                ('shipment', models.CharField(choices=[('pending', 'Pending'), ('on-the-way', 'On the way'), ('deliverd', 'Deliverd'), ('reject', 'Reject'), ('cancel', 'Cancel')], default=('pending', 'Pending'), max_length=20, verbose_name='Shipment Status')),
                ('packing', models.CharField(choices=[('notyet', 'Not yet'), ('packed', 'Packed')], default=('notyet', 'Not yet'), max_length=20, verbose_name='Packing Status')),
                ('order_date', models.DateField(blank=True, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('customer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.customer')),
                ('payment_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.payment')),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
    ]
