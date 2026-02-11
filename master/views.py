from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Designation, Grade, Branch, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

# ====================== INLINE FORMS (no forms.py needed) ======================

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['name']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name']

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# ============================ VIEWS ============================

def hr_dashboard(request):
    return render(request, 'master/hr_dashboard.html')

# ------------------ Utility to set slug ------------------
def set_unique_slug(instance, model_class):
    base_slug = slugify(instance.name)
    slug = base_slug
    counter = 1
    while model_class.objects.exclude(id=instance.id).filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    instance.slug = slug

# ------------------ Department ------------------

@login_required
def department_list(request):
    departments = Department.objects.filter(user=request.user)
    return render(request, 'master/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        department = form.save(commit=False)
        department.user = request.user
        set_unique_slug(department, Department)
        department.save()
        return redirect('department_list')
    return render(request, 'master/department_form.html', {'form': form})

@login_required
def department_edit(request, slug):
    department = get_object_or_404(Department, slug=slug, user=request.user)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        department = form.save(commit=False)
        set_unique_slug(department, Department)
        department.save()
        messages.success(request, "Department updated successfully!")
        return redirect('department_list')
    return render(request, 'master/department_form.html', {'form': form})

@login_required
def department_delete(request, slug):
    department = get_object_or_404(Department, slug=slug, user=request.user)
    department.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect('department_list')

# ------------------ Designation ------------------

@login_required
def designation_list(request):
    designations = Designation.objects.filter(user=request.user)
    return render(request, 'master/designation_list.html', {'designations': designations})

@login_required
def designation_create(request):
    form = DesignationForm(request.POST or None)
    if form.is_valid():
        designation = form.save(commit=False)
        designation.user = request.user
        set_unique_slug(designation, Designation)
        designation.save()
        messages.success(request, "Designation added successfully!")
        return redirect('designation_list')
    return render(request, 'master/designation_form.html', {'form': form})

@login_required
def designation_edit(request, slug):
    designation = get_object_or_404(Designation, slug=slug, user=request.user)
    form = DesignationForm(request.POST or None, instance=designation)
    if form.is_valid():
        designation = form.save(commit=False)
        set_unique_slug(designation, Designation)
        designation.save()
        messages.success(request, "Designation updated successfully!")
        return redirect('designation_list')
    return render(request, 'master/designation_form.html', {'form': form})

@login_required
def designation_delete(request, slug):
    designation = get_object_or_404(Designation, slug=slug, user=request.user)
    designation.delete()
    messages.success(request, "Designation deleted successfully!")
    return redirect('designation_list')

# ------------------ Grade ------------------

@login_required
def grade_list(request):
    grades = Grade.objects.filter(user=request.user)
    return render(request, 'master/grade_list.html', {'grades': grades})

@login_required
def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        grade = form.save(commit=False)
        grade.user = request.user
        set_unique_slug(grade, Grade)
        grade.save()
        messages.success(request, "Grade added successfully!")
        return redirect('grade_list')
    return render(request, 'master/grade_form.html', {'form': form})

@login_required
def grade_edit(request, slug):
    grade = get_object_or_404(Grade, slug=slug, user=request.user)
    form = GradeForm(request.POST or None, instance=grade)
    if form.is_valid():
        grade = form.save(commit=False)
        set_unique_slug(grade, Grade)
        grade.save()
        messages.success(request, "Grade updated successfully!")
        return redirect('grade_list')
    return render(request, 'master/grade_form.html', {'form': form})

@login_required
def grade_delete(request, slug):
    grade = get_object_or_404(Grade, slug=slug, user=request.user)
    grade.delete()
    messages.success(request, "Grade deleted successfully!")
    return redirect('grade_list')

# ------------------ Branch ------------------

@login_required
def branch_list(request):
    branches = Branch.objects.filter(user=request.user)
    return render(request, 'master/branch_list.html', {'branches': branches})

@login_required
def branch_create(request):
    form = BranchForm(request.POST or None)
    if form.is_valid():
        branch = form.save(commit=False)
        branch.user = request.user
        set_unique_slug(branch, Branch)
        branch.save()
        messages.success(request, "Branch added successfully!")
        return redirect('branch_list')
    return render(request, 'master/branch_form.html', {'form': form})

@login_required
def branch_edit(request, slug):
    branch = get_object_or_404(Branch, slug=slug, user=request.user)
    form = BranchForm(request.POST or None, instance=branch)
    if form.is_valid():
        branch = form.save(commit=False)
        set_unique_slug(branch, Branch)
        branch.save()
        messages.success(request, "Branch updated successfully!")
        return redirect('branch_list')
    return render(request, 'master/branch_form.html', {'form': form})

@login_required
def branch_delete(request, slug):
    branch = get_object_or_404(Branch, slug=slug, user=request.user)
    branch.delete()
    messages.success(request, "Branch deleted successfully!")
    return redirect('branch_list')

# ------------------ Category ------------------

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'master/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        set_unique_slug(category, Category)
        category.save()
        messages.success(request, "Category added successfully!")
        return redirect('category_list')
    return render(request, 'master/category_form.html', {'form': form})

@login_required
def category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug, user=request.user)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        category = form.save(commit=False)
        set_unique_slug(category, Category)
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect('category_list')
    return render(request, 'master/category_form.html', {'form': form})

@login_required
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug, user=request.user)
    category.delete()
    messages.success(request, "Category deleted successfully!")
    return redirect('category_list')

# ------------------ Redirect Shortcuts for Add Buttons ------------------

@login_required
def add_department(request):
    return redirect('department_create')

@login_required
def add_designation(request):
    return redirect('designation_create')

@login_required
def add_grade(request):
    return redirect('grade_create')

@login_required
def add_branch(request):
    return redirect('branch_create')

@login_required
def add_category(request):
    return redirect('category_create')