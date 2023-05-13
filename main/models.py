import os
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from PIL import Image
from autoslug import AutoSlugField
from django.core.files.storage import default_storage
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode
from translated_fields import TranslatedField

Size = [
  ('M', "M"),
  ('L', "L"),
  ('XL', "XL"),
  ('XXL', "XXL"),
]

Packing = [
  ('notyet', "Not yet"),
  ('packed', "Packed")
]

Shipment = [
  ('pending', "Pending"),
  ('on-the-way', "On the way"),
  ('deliverd', "Deliverd"),
  ('reject', "Reject"),
  ('cancel', "Cancel")
]

PaymentStatus = [
  ('pending', "Pending"),
  ('received', "Received"),
  ('case-back', "Cash Back"),
]

Gender = [
  ('male', "Male"),
  ('female', "Female"),
  ('other', "Other"),
]


# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=255)
  slug=AutoSlugField(populate_from="name", primary_key=True)
  image = models.ImageField(upload_to='media/category/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.image:
      img = Image.open(self.image.path)

      if img.width > 800 or img.height > 600:
        output_size = (800, 600)
        img.thumbnail(output_size)
        img.save(self.image.path)
        img.close()
      
  def __str__(self):
    return self.name

@receiver(post_delete, sender=Category)
def delete_file(sender, instance, **kwargs):
  if instance.image:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)
  
class Product(models.Model):
  name = models.CharField(max_length=255)
  slug = AutoSlugField(populate_from="name", primary_key=True)
  brand = models.CharField(max_length=255)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  cross_price = models.DecimalField(max_digits=10, decimal_places=2)
  selling_price = models.DecimalField(max_digits=10, decimal_places=2)

  desc = CKEditor5Field('Text', config_name='extends')

  meta_description = models.TextField(max_length=155)
  meta_keywords = models.TextField(max_length=155)
  draft = models.BooleanField(default=False)

  main_image = models.ImageField(upload_to='media/products/')
  hover_image = models.ImageField(upload_to='media/products/')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.main_image:
      img = Image.open(self.main_image.path)

      if img.width > 800 or img.height > 600:
        output_size = (800, 600)
        img.thumbnail(output_size)
        img.save(self.main_image.path)
        img.close()

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.hover_image:
      img = Image.open(self.hover_image.path)

      if img.width > 800 or img.height > 600:
        output_size = (800, 600)
        img.thumbnail(output_size)
        img.save(self.hover_image.path)
        img.close()

@receiver(post_delete, sender=Product)      
def delete_file(sender, instance, **kwargs):
  if instance.main_image:
    if os.path.isfile(instance.main_image.path):
      os.remove(instance.main_image.path)

@receiver(post_delete, sender=Product)      
def delete_file(sender, instance, **kwargs):
  if instance.hover_image:
    if os.path.isfile(instance.hover_image.path):
      os.remove(instance.hover_image.path)

class ProductSize(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
  size = models.CharField(choices=Size, max_length=4, default=Size[1])
  qty = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.product.name,self.size}"

class VariantImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
  image = models.ImageField(upload_to='media/product-variant/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.image:
      img = Image.open(self.image.path)

      if img.width > 800 or img.height > 600:
        output_size = (800, 600)
        img.thumbnail(output_size)
        img.save(self.image.path)
        img.close()
      
@receiver(post_delete, sender=VariantImage)
def delete_file(sender, instance, **kwargs):
  if instance.image.path:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)
  

class Reviews(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
  review = models.DecimalField(max_digits=2, decimal_places=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
  cId = models.AutoField(primary_key=True)
  full_name = models.CharField(max_length=255)
  phone = models.CharField(max_length=50)
  email = models.CharField(max_length=255, blank=True, null=True)
  district = models.CharField(max_length=100)
  street = models.CharField(max_length=255)
  gender = models.CharField(choices=Gender, max_length=20, default=Gender[1])
  height = models.CharField(max_length=50, blank=True, null=True)
  weight = models.CharField(max_length=50, blank=True, null=True)
  image = models.ImageField(upload_to='media/customer/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.full_name
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.image:
      img = Image.open(self.image.path)

      if img.width > 800 or img.height > 600:
        output_size = (800, 600)
        img.thumbnail(output_size)
        img.save(self.image.path)
        img.close()

@receiver(post_delete, sender=Customer)
def delete_file(sender, instance, **kwargs):
  if instance.image.path:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)
      
      
class Payment(models.Model):
  pId = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  image = models.ImageField(upload_to='media/payment/', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.image:
      img = Image.open(self.image.path)

      if img.width > 500 or img.height > 500:
        output_size = (500, 500)
        img.thumbnail(output_size)
        img.save(self.image.path)
        img.close()

@receiver(post_delete, sender=Payment)
def delete_file(sender, instance, **kwargs):
  if instance.image:
    if os.path.isfile(instance.image.path):
      os.remove(instance.image.path)

class Orders(models.Model):
  oId = models.AutoField(primary_key=True)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default="")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
  qty = models.PositiveIntegerField()
  size = models.CharField("Size", choices=Size, max_length=4, default=Size[0])

  amount = models.DecimalField(max_digits=6, decimal_places=2)
  payment_mode = models.ForeignKey(Payment, on_delete=models.CASCADE)
  payment_status = models.CharField("Payment Status", choices=PaymentStatus, max_length=20, default=PaymentStatus[0])
  shipment = models.CharField("Shipment Status", choices=Shipment, max_length=20, default=Shipment[0])
  packing = models.CharField("Packing Status", choices=Packing, max_length=20, default=Packing[0])

  order_date = models.DateField(blank=True, null=True)
  delivery_date = models.DateField(blank=True, null=True)

  remarks = models.TextField(null=True, blank=True)
  
  def __str__(self):
    return self.customer.full_name
  
class Expenses(models.Model):
  eId = models.AutoField(primary_key=True)
  title = models.TextField()
  weight = models.CharField(max_length=50, blank=True, null=True)
  length = models.CharField(max_length=50, blank=True, null=True)
  unit_price = models.DecimalField(max_digits=6, decimal_places=2)
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  refrences = models.CharField(max_length=255, blank=False, null=False)
  activity_date = models.DateField()
  remarks = models.TextField(blank=True, null=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
  
  
class SoldProduct(models.Model):
  sId = models.AutoField(primary_key=True)
  product = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
  sold_qty = models.IntegerField()
  remarks = models.TextField(blank=True, null=True)
    
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  @property
  def remaining_qty(self):
    remaining_qty = self.product.qty - self.sold_qty
    return remaining_qty
  
  @property
  def total_qty(self):
    total_qty = self.product.qty
    return total_qty



      
    