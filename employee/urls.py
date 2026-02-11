from django.urls import path
from . import views
from .views import employee_detail
urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_create, name='employee_create'),
    path('edit/<slug:slug>/', views.employee_edit, name='employee_edit'),
    path('delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('employee/stats/', views.employee_stats, name='employee_stats'),
    path('employee/detail/<slug:slug>/', employee_detail, name='employee_detail'),

    
]
