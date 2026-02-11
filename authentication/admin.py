from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CompanyUser, OTP
from employee.models import Employee
from bank.models import Bank
from document.models import Document

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0
    show_change_link = True

@admin.register(CompanyUser)
class CompanyUserAdmin(UserAdmin):
    model = CompanyUser
    list_display = ('email', 'company_name', 'hr_name', 'mobile', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'company_name', 'hr_name', 'mobile')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'display_banks', 'display_documents')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('company_name', 'hr_name', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
        ('Related Data (Read-only)', {'fields': ('display_banks', 'display_documents')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'company_name', 'hr_name', 'mobile', 'password1', 'password2', 'is_verified', 'is_staff', 'is_superuser')}),
    )

    def display_banks(self, obj):
        banks = Bank.objects.filter(employee__user=obj)
        if not banks.exists():
            return "-"
        return "\n".join([
            f"{bank.employee.full_name} - {bank.bank_name} ({bank.ifsc})\nAccount: {bank.account_number} | Branch: {bank.branch}"
            for bank in banks
        ])
    display_banks.short_description = "Bank Details"

    def display_documents(self, obj):
        docs = Document.objects.filter(employee__user=obj)
        if not docs.exists():
            return "-"
        return "\n".join([
            f"{doc.employee.full_name} - {doc.doc_type} ({doc.upload.name})"
            for doc in docs
        ])
    display_documents.short_description = "Documents"

    inlines = [EmployeeInline]

admin.site.register(OTP)
