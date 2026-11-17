from django.contrib import admin
from .models import Product, Box, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'recommended_box', 'is_packed', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Box)