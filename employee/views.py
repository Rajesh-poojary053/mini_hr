from django import forms
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Employee
from master.models import Department, Designation, Grade, Branch, Category
from document.models import Document


# ✅ Employee Form (exclude slug)
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user', 'created_at', 'slug']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EmployeeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['department'].queryset = Department.objects.filter(user=user)
            self.fields['designation'].queryset = Designation.objects.filter(user=user)
            self.fields['grade'].queryset = Grade.objects.filter(user=user)
            self.fields['branch'].queryset = Branch.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('dob')
        doj = cleaned_data.get('doj')

        if dob and (date.today().year - dob.year) < 18:
            self.add_error('dob', 'Employee must be at least 18 years old.')

        if doj and dob and (doj.year - dob.year) < 18:
            self.add_error('doj', 'Joining age must be at least 18 years old.')


# ✅ List View
@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    employee_queryset = Employee.objects.filter(user=request.user)

    if query:
        employee_queryset = employee_queryset.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(department__name__icontains=query) |
            Q(designation__name__icontains=query)
        )

    paginator = Paginator(employee_queryset.order_by('id'), 10)
    page_number = request.GET.get('page')
    employees = paginator.get_page(page_number)

    return render(request, 'employee/employee_list.html', {
        'employees': employees,
        'query': query
    })


# ✅ Create View
@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, user=request.user)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, "✅ Employee added successfully!")
            return redirect('employee_list')
    else:
        form = EmployeeForm(user=request.user)

    return render(request, 'employee/employee_form.html', {'form': form})


# ✅ Edit View
@login_required
def employee_edit(request, slug):
    emp = get_object_or_404(Employee, slug=slug, user=request.user)
    form = EmployeeForm(request.POST or None, instance=emp, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Employee updated successfully!")
        return redirect('employee_list')
    return render(request, 'employee/employee_form.html', {'form': form})


# ✅ Delete View
@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk, user=request.user)
    emp.delete()
    messages.success(request, "🗑️ Employee deleted successfully!")
    return redirect('employee_list')


# ✅ Stats View
@login_required
def employee_stats(request):
    total = Employee.objects.filter(user=request.user).count()
    active = Employee.objects.filter(user=request.user, is_active=True).count()
    inactive = Employee.objects.filter(user=request.user, is_active=False).count()

    return render(request, 'employee/employee_stats.html', {
        'total': total,
        'active': active,
        'inactive': inactive
    })


# ✅ Detail View by Slug
@login_required
def employee_detail(request, slug):
    emp = get_object_or_404(Employee, slug=slug, user=request.user)
    documents = Document.objects.filter(employee=emp)
    return render(request, 'employee/employee_detail.html', {
        'emp': emp,
        'documents': documents
    })
