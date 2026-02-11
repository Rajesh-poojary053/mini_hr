from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime, get_current_timezone
from datetime import datetime
import re

from .models import CompanyUser
from employee.models import Employee


# ✅ Inline Form: Password Login Form
class PasswordLoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


# ✅ Helper: Clear Django messages
def clear_messages(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass


import re
from django.contrib import messages
from django.shortcuts import render, redirect
from authentication.models import CompanyUser  # or wherever CompanyUser is defined
from django.contrib.messages import get_messages

# Utility to clear messages before setting new ones
def clear_messages(request):
    list(get_messages(request))

# ✅ Signup View (with confirm password)
def signup_view(request):
    clear_messages(request)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        hr_name = request.POST.get('hr_name')
        mobile = request.POST.get('mobile')
        company_name = request.POST.get('company_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if CompanyUser.objects.filter(email=email).exists():
            messages.error(request, "❌ User with this email already exists.")
            return redirect('signup')

        if not re.match(r'^[6-9]\d{9}$', mobile):
            messages.error(request, "❌ Invalid mobile number. Use 10-digit Indian number.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "❌ Password and Confirm Password do not match.")
            return redirect('signup')

        # Create the new user
        user = CompanyUser.objects.create_user(
            email=email,
            company_name=company_name,
            hr_name=hr_name,
            mobile=mobile
        )
        user.set_password(password)
        user.is_verified = True
        user.save()

        # ✅ Show success message and redirect to login
        messages.success(request, "✅ Signup successful! Please login.")
        return redirect('password_login')

    return render(request, 'authentication/signup.html')


# ✅ Login View
def password_login_view(request):
    clear_messages(request)
    form = PasswordLoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"🎉 Welcome back, {user.hr_name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "❌ Invalid email or password.")

    return render(request, 'authentication/login.html', {'form': form})


# ✅ Logout View
def logout_view(request):
    logout(request)
    clear_messages(request)
    messages.info(request, "👋 You have been logged out.")
    return redirect('signup')


# ✅ Main Dashboard View
@login_required
def dashboard_view(request):
    clear_messages(request)
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    employees = Employee.objects.filter(user=request.user)
    total = employees.count()
    active = employees.filter(is_active=True).count()
    inactive = total - active
    recent = employees.order_by('-created_at').first()

    return render(request, 'authentication/dashboard.html', {
        'greeting': greeting,
        'hr_name': request.user.hr_name,
        'current_time': datetime.now().strftime('%I:%M %p'),
        'total_employees': total,
        'active_employees': active,
        'inactive_employees': inactive,
        'recent_employee': recent,
    })


# ✅ Greeting Page View
@login_required
def greeting_page(request):
    clear_messages(request)
    current_time = localtime().astimezone(get_current_timezone())
    hour = current_time.hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 17:
        greeting = "Good Afternoon"
    elif hour < 20:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    time_str = current_time.strftime("%I:%M %p").lstrip("0")

    return render(request, 'authentication/greeting.html', {
        'greeting': greeting,
        'hr_name': request.user.hr_name,
        'time_str': time_str,
    })


# ✅ HR Dashboard View
@login_required
def hr_dashboard_view(request):
    clear_messages(request)
    return render(request, 'authentication/hr_dashboard.html')
