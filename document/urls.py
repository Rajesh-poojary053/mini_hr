from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.document_upload, name='document_upload'),
    
    
    path('edit/<slug:slug>/', views.document_edit, name='document_edit'),
    path('delete/<slug:slug>/', views.document_delete, name='document_delete'),
]
