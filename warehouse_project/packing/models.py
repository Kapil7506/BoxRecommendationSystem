from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    length = models.FloatField(help_text="Length in cm")
    width = models.FloatField(help_text="Width in cm")
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in grams")

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Box(models.Model):
    name = models.CharField(max_length=100)
    inner_length = models.FloatField(help_text="Internal length in cm")
    inner_width = models.FloatField(help_text="Internal width in cm")
    inner_height = models.FloatField(help_text="Internal height in cm")
    max_weight = models.FloatField(help_text="Max weight capacity in grams")
    cost = models.DecimalField(max_digits=6, decimal_places=2, help_text="Cost per box in currency")
    is_active = models.BooleanField(default=True)

    @property
    def volume(self):
        return self.inner_length * self.inner_width * self.inner_height

    def __str__(self):
        return f"{self.name} ({self.inner_length}x{self.inner_width}x{self.inner_height}cm)"

class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recommended_box = models.ForeignKey(Box, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")
    is_packed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)