from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Bank
from employee.models import Employee
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ValidationError
import re

# ✅ Inline BankForm
class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['employee', 'bank_name', 'ifsc', 'account_number', 'branch']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BankForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['employee'].queryset = Employee.objects.filter(user=user)

    def clean_ifsc(self):
        ifsc = self.cleaned_data['ifsc'].upper()
        if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc):
            raise ValidationError("❌ Enter a valid IFSC code (e.g., SBIN0001234)")
        return ifsc

    def clean_account_number(self):
        acc = self.cleaned_data['account_number']
        if not acc.isdigit() or not (9 <= len(acc) <= 18):
            raise ValidationError("❌ Account number must be 9-18 digits.")
        return acc

# ✅ LIST
@login_required
def bank_list(request):
    query = request.GET.get('q')
    banks = Bank.objects.filter(employee__user=request.user)

    if query:
        banks = banks.filter(
            Q(employee__full_name__icontains=query) |
            Q(bank_name__icontains=query) |
            Q(ifsc__icontains=query) |
            Q(account_number__icontains=query) |
            Q(branch__icontains=query)
        )

    return render(request, 'bank/bank_list.html', {'banks': banks})

# ✅ CREATE
@login_required
def bank_create(request):
    form = BankForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        bank = form.save(commit=False)
        bank.user = request.user
        bank.save()
        messages.success(request, "✅ Bank details added successfully!")
        return redirect('bank_list')
    return render(request, 'bank/bank_form.html', {'form': form})

# ✅ EDIT with slug
@login_required
def bank_edit(request, slug):
    bank = get_object_or_404(Bank, slug=slug, employee__user=request.user)
    form = BankForm(request.POST or None, instance=bank, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Bank details updated successfully!")
        return redirect('bank_list')
    return render(request, 'bank/bank_form.html', {'form': form})

# ✅ DELETE with slug
@login_required
def bank_delete(request, slug):
    bank = get_object_or_404(Bank, slug=slug, employee__user=request.user)
    bank.delete()
    messages.success(request, "✅ Bank details deleted successfully!")
    return redirect('bank_list')
