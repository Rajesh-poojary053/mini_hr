from django.contrib import admin
from .models import Bank

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['employee', 'bank_name', 'ifsc', 'account_number', 'branch']
