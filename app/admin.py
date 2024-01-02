from django.contrib import admin


# Register your models here.

from .models import MusicProduct, StoreItem, OrderItem, Order

admin.site.register(MusicProduct)
admin.site.register(StoreItem)
admin.site.register(OrderItem)
admin.site.register(Order)
