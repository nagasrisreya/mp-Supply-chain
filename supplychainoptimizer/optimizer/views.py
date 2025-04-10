from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SupplyChainForm
from .solver import optimize_supply_chain
from .models import Inventory  # Import the Inventory model
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def optimize(request):
    if request.method == 'POST':
        form = SupplyChainForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            supplier_name = form.cleaned_data['supplier_name']
            supplier_location = form.cleaned_data['supplier_location']
            supplier_capacity = form.cleaned_data['supplier_capacity']

            warehouse_name = form.cleaned_data['warehouse_name']
            warehouse_location = form.cleaned_data['warehouse_location']
            warehouse_capacity = form.cleaned_data['warehouse_capacity']

            product_name = form.cleaned_data['product_name']
            product_cost = form.cleaned_data['product_cost']
            product_demand = form.cleaned_data['product_demand']

            transportation_source = form.cleaned_data['transportation_source']
            transportation_destination = form.cleaned_data['transportation_destination']
            transportation_cost_per_unit = form.cleaned_data['transportation_cost_per_unit']
            transportation_distance = form.cleaned_data['transportation_distance']

            # Structure the data for the solver
            suppliers = {
                supplier_name: {
                    'location': supplier_location,
                    'capacity': supplier_capacity,
                }
            }

            warehouses = {
                warehouse_name: {
                    'location': warehouse_location,
                    'storage_capacity': warehouse_capacity,
                }
            }

            products = {
                product_name: {
                    'cost': product_cost,
                    'demand': product_demand,
                }
            }

            # Correct structure for transportation_costs
            transportation_costs = {
                transportation_source: {
                    transportation_destination: transportation_cost_per_unit,  # Only the cost per unit
                }
            }

            # Call the solver
            results = optimize_supply_chain(suppliers, warehouses, products, transportation_costs)

            # Calculate analysis data
            total_units_shipped = sum(results.values())
            total_cost = sum(
                transportation_costs[s][w] * results[(s, w, p)]
                for (s, w, p) in results
            )

            supplier_utilization = (total_units_shipped / suppliers[supplier_name]['capacity']) * 100
            warehouse_utilization = (total_units_shipped / warehouses[warehouse_name]['storage_capacity']) * 100

            # Save results to the Inventory model
            for (s, w, p), units in results.items():
                Inventory.objects.create(
                    supplier=s,
                    warehouse=w,
                    product=p,
                    units_shipped=units,
                    total_cost=total_cost,
                    supplier_utilization=supplier_utilization,
                    warehouse_utilization=warehouse_utilization,
                )

            # Pass results and analysis data to the template
            context = {
                'results': results,
                'total_units_shipped': total_units_shipped,
                'total_cost': total_cost,
                'supplier_utilization': supplier_utilization,
                'warehouse_utilization': warehouse_utilization,
            }

            return render(request, 'optimizer/results.html', context)
    else:
        form = SupplyChainForm()

    return render(request, 'optimizer/optimize.html', {'form': form})

@login_required
@never_cache
def home(request):
    return render(request, 'optimizer/home.html')

@login_required
@never_cache
def inventory(request):
    # Fetch all inventory records
    inventory_items = Inventory.objects.all()
    return render(request, 'optimizer/inventory.html', {'inventory_items': inventory_items})

@login_required
@never_cache
def delete_all_inventory(request):
    if request.method == 'POST':
        # Delete all inventory records
        Inventory.objects.all().delete()
        messages.success(request, 'All inventory records have been deleted successfully.')
        return redirect('inventory')  # Redirect to the inventory page
    else:
        # If not a POST request, redirect to the inventory page
        return redirect('inventory')

@login_required
@never_cache
def delete_single_inventory(request, id):
    if request.method == 'POST':
        # Get the specific inventory record or return 404 if not found
        inventory_item = get_object_or_404(Inventory, id=id)
        # Delete the single record
        inventory_item.delete()
        messages.success(request, 'The inventory record has been deleted successfully.')
        return redirect('inventory')  # Redirect to the inventory page
    else:
        # If not a POST request, redirect to the inventory page
        return redirect('inventory')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'optimizer/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Your account has been created. You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'optimizer/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')

from django.shortcuts import render

def help_page(request):
    return render(request, 'optimizer/help.html')