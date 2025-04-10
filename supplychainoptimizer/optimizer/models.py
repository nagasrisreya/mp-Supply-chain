from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    storage_capacity = models.IntegerField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    demand = models.IntegerField()

class Transportation(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    cost_per_unit = models.FloatField()
    distance = models.FloatField()

class Inventory(models.Model):
    supplier = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    units_shipped = models.IntegerField()
    total_cost = models.FloatField()
    supplier_utilization = models.FloatField()
    warehouse_utilization = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier} -> {self.warehouse} ({self.product})"