from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from optimizer.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),  # Default to login page
    path('optimize/', include('optimizer.urls')),
]