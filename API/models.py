from django.db import models
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

def categories_changed(sender, **kwargs):
    if kwargs.get('instance').categories.count() > 7:
        raise ValidationError("You can't assign more than seven categories")

class Category(models.Model):
    id = models.BigIntegerField(verbose_name= 'ID', primary_key = True, auto_created = False)
    title = models.CharField(max_length=100, verbose_name='Title')

class Seller(models.Model):
    
    id = models.CharField(max_length=200, verbose_name='Seller ID', primary_key=True, auto_created = False)
    type_CHOICES = [
        ('CORPORATE', 'Corporate'),
        ('INDIVIDUAL', 'Individual')
    ]
    type = models.CharField(max_length=20, choices=type_CHOICES, verbose_name='Seller Type')


class Post(models.Model):
    seller = models.ForeignKey(Seller, related_name='seller_id', on_delete=models.CASCADE, verbose_name='Seller')
    title = models.CharField(max_length=2000, verbose_name = 'Title')
    description = models.CharField(max_length=200000, verbose_name = 'Description')
    categories = models.ManyToManyField(Category, blank=True, default=None)
    price = models.BigIntegerField(default = 0, verbose_name = 'Price')
    date = models.BigIntegerField(verbose_name = 'Date')
    expiryDate = models.BigIntegerField(verbose_name = 'Expiry Date')
    live = models.BooleanField(default = False, verbose_name = 'Live')
    status_CHOICES = [
        ('ACTIVE', 'Active'),
        ('WAITING_APPROVAL', 'Waiting Approval'),
        ('PASSIVATED', 'Passivated'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired')
    ]
    status = models.CharField(max_length=20, choices=status_CHOICES, verbose_name='Status')
    adminID = models.BigIntegerField(default = 0, verbose_name= 'Admin ID')

    def clean(self, *args, **kwargs):
        if self.categories.count() > 7:
            raise ValidationError("You can't assign more than seven regions")
        super(Post, self).clean(*args, **kwargs)