from django import forms

class SupplyChainForm(forms.Form):
    # Supplier fields
    supplier_name = forms.CharField(label="Supplier Name", max_length=100)
    supplier_location = forms.CharField(label="Supplier Location", max_length=100)
    supplier_capacity = forms.IntegerField(label="Supplier Capacity")

    # Warehouse fields
    warehouse_name = forms.CharField(label="Warehouse Name", max_length=100)
    warehouse_location = forms.CharField(label="Warehouse Location", max_length=100)
    warehouse_capacity = forms.IntegerField(label="Warehouse Storage Capacity")

    # Product fields
    product_name = forms.CharField(label="Product Name", max_length=100)
    product_cost = forms.FloatField(label="Product Cost")
    product_demand = forms.IntegerField(label="Product Demand")

    # Transportation fields
    transportation_source = forms.CharField(label="Transportation Source", max_length=100)
    transportation_destination = forms.CharField(label="Transportation Destination", max_length=100)
    transportation_cost_per_unit = forms.FloatField(label="Transportation Cost Per Unit")
    transportation_distance = forms.FloatField(label="Transportation Distance")