from django.db import models

# Create your models here.

# --- User Model ---
class User(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

# --- Product Model ---
# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     price = models.FloatField()
#     description = models.TextField()
#     category = models.CharField(max_length=100)
#     image_url = models.URLField()
#     sold = models.BooleanField(default=False)
#     is_sale = models.BooleanField(default=False)
#     date_of_sale = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.title

# models.py
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    sold = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    date_of_sale = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


# --- Cart Model ---
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# --- Order Model ---
class Order(models.Model):
    PAYMENT_MODES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)
    created_at = models.DateTimeField(auto_now_add=True) 

# --- OTP Model ---
class OTP(models.Model):
    mobile = models.CharField(max_length=15)
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mobile} - {self.session_id}"
    
    from django.contrib.auth.models import User
from .models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Avoid duplicates

    def __str__(self):
        # return f"{self.user.username} - {self.product.title}"
        return f"{self.user.full_name} - {self.product.title}"