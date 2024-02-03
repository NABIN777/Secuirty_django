import hashlib

from cryptography.fernet import Fernet
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import *
from django.db import models

# from online_shopping.settings import AUTH_USER_MODEL



# Generate a key for encryption (do this once and keep it secret)
key = Fernet.generate_key()

# Create a Fernet cipher object with the key
cipher = Fernet(key)

class Category(models.Model):
    category_name = models.CharField(max_length=200, null=True, validators=[validators.MinLengthValidator(2)])
    category_description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    category_image = models.FileField(upload_to='static/uploads', null=True)

    def __str__(self):
        return self.category_name


class Clothes(models.Model):
    clothes_name = models.CharField(max_length=200)
    clothes_price = models.FloatField()
    clothes_description = models.TextField(null=True)
    clothes_image = models.FileField(upload_to='static/uploads')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True)  # Original ID field as an integer
    hashed_id = models.CharField(max_length=64, blank=True, null=True)  # Hashed ID field

    # def save(self, *args, **kwargs):
    #     # Hash the id before saving if it exists
    #     if self.id:
    #         id_to_hash = str(self.id)
    #         hashed_id = hashlib.sha256(id_to_hash.encode()).hexdigest()
    #         self.hashed_id = hashed_id
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.clothes_name

class Cart(models.Model):
    clothe = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders')

    created_date = models.DateTimeField(auto_now_add=True)
    # ////
   
    # def save(self, *args, **kwargs):
    #     # Convert clothe_id to string and hash before saving
    #     clothe_id_str = str(self.encrypted_clothe)
    #     hashed_clothe_id = hashlib.sha256(clothe_id_str.encode()).hexdigest()
    #     self.encrypted_clothe_id = hashed_clothe_id
    #     super().save(*args, **kwargs)

    # def get_decrypted_clothe_id(self):
    #     # Decrypt the 'clothe_id' data when needed
    #     # In this case, it's a one-way hash, so there's no decryption
    #     return self.encrypted_clothe_id

import hashlib

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )

    clothe = models.ForeignKey(Clothes, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    total_price = models.IntegerField(null=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True)
    
    # Hashed contact_no
    # contact = models.CharField(max_length=64, blank=True, null=True)
    
    contact_no = models.CharField(validators=[MinLengthValidator(9), MaxLengthValidator(10)], null=True, max_length=64)
    contact_address = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
