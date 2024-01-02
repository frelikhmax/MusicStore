from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.db import models


class StoreItemManager(models.Manager):

    def new(self):
        return StoreItem.objects.all().order_by('id')


# Create your models here.

class MusicProduct(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(max_length=256, blank=True, null=False)

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    music_product = models.ForeignKey('MusicProduct', on_delete=models.CASCADE, related_name='store_items', blank=False,
                                      null=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    price = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = StoreItemManager()

    def __str__(self):
        return str(self.music_product.name) + ' ' + str(self.price)


class OrderItem(models.Model):
    store_item = models.ForeignKey('StoreItem', on_delete=models.CASCADE, related_name='order_items', blank=False,
                                   null=False)
    quantity = models.IntegerField(default=0, blank=False, null=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)

    def __str__(self):
        return str(self.order.id) + ' ' + str(self.store_item.music_product.name)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' ' + str(self.date)
