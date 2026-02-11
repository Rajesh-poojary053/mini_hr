from django.urls import path
from . import views

urlpatterns = [
    # HR Dashboard
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),

    # ------------------ Department ------------------
    path('department/', views.department_list, name='department_list'),
    path('department/add/', views.department_create, name='department_create'),
    path('department/edit/<slug:slug>/', views.department_edit, name='department_edit'),
    path('department/delete/<slug:slug>/', views.department_delete, name='department_delete'),
    path('add-department/', views.add_department, name='add_department'),

    # ------------------ Designation ------------------
    path('designation/', views.designation_list, name='designation_list'),
    path('designation/add/', views.designation_create, name='designation_create'),
    path('designation/edit/<slug:slug>/', views.designation_edit, name='designation_edit'),
    path('designation/delete/<slug:slug>/', views.designation_delete, name='designation_delete'),
    path('add-designation/', views.add_designation, name='add_designation'),

    # ------------------ Grade ------------------
    path('grade/', views.grade_list, name='grade_list'),
    path('grade/add/', views.grade_create, name='grade_create'),
    path('grade/edit/<slug:slug>/', views.grade_edit, name='grade_edit'),
    path('grade/delete/<slug:slug>/', views.grade_delete, name='grade_delete'),
    path('add-grade/', views.add_grade, name='add_grade'),

    # ------------------ Branch ------------------
    path('branch/', views.branch_list, name='branch_list'),
    path('branch/add/', views.branch_create, name='branch_create'),
    path('branch/edit/<slug:slug>/', views.branch_edit, name='branch_edit'),
    path('branch/delete/<slug:slug>/', views.branch_delete, name='branch_delete'),
    path('add-branch/', views.add_branch, name='add_branch'),

    # ------------------ Category ------------------
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.category_create, name='category_create'),
    path('category/edit/<slug:slug>/', views.category_edit, name='category_edit'),
    path('category/delete/<slug:slug>/', views.category_delete, name='category_delete'),
    path('add-category/', views.add_category, name='add_category'),
]
