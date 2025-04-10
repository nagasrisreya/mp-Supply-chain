from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('optimize/', views.optimize, name='optimize'),
    path('inventory/', views.inventory, name='inventory'),
    path('delete-all-inventory/', views.delete_all_inventory, name='delete_all_inventory'),
    path('delete-single-inventory/<int:id>/', views.delete_single_inventory, name='delete_single_inventory'),
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('logout/', views.logout_view, name='logout'),
]