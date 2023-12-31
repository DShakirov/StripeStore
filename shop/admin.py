from django.contrib import admin
from .models import Item, Order, Discount, Tax, Currency


class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price', 'currency']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_price']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Currency)
