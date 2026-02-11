from django.contrib import admin
from .models import Department, Designation, Grade, Branch, Category

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug']
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'slug']
    prepopulated_fields = {"slug": ("name",)}
