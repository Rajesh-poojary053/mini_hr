from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 🔐 Authentication: Signup, Login, Logout
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.password_login_view, name='password_login'),
    path('logout/', views.logout_view, name='logout'),

    # 📊 Dashboard & HR Pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('greeting/', views.greeting_page, name='greeting_page'),
    path('hr-dashboard/', views.hr_dashboard_view, name='hr_dashboard'),

    # 🔁 Password Reset Flow (Forgot Password)
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='authentication/forgot_password.html',
            email_template_name='authentication/password_reset_email.html',
            subject_template_name='authentication/password_reset_subject.txt',
            extra_email_context={
                'protocol': 'http',
                'domain': '127.0.0.1:8000',
            }
        ),
        name='password_reset'
    ),
    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='authentication/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='authentication/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='authentication/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
