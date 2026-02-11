from django.urls import path
from . import views

urlpatterns = [
    path('', views.bank_list, name='bank_list'),
    path('add/', views.bank_create, name='bank_create'),
    
    # Changed from <int:pk> to <slug:slug>
    path('edit/<slug:slug>/', views.bank_edit, name='bank_edit'),
    path('delete/<slug:slug>/', views.bank_delete, name='bank_delete'),
]
