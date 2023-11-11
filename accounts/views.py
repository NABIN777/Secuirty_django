import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import cache_control
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice

from accounts.auth import admin_only, unauthenticated_user, user_only
# from accounts.custom_totp_device import CustomTOTPDevice
from clothes.models import Clothes

from .forms import LoginForm

CACHE_TIMEOUT = 60 * 15  # 1
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes in seconds
SESSION_EXPIRY_MINUTES = 1
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


def homepage(request):
    clothes = Clothes.objects.all().order_by('-id')[:3]
    context = {
        'clothes': clothes
    }
    return render(request, 'accounts/homepage.html',context)

def logout_user(request):
    logout(request)
    request.session.flush()
    response = redirect('/login')
    response.delete_cookie('sessionid')  # Remove the sessionid cookie
    request.META.pop("CSRF_COOKIE_USED", None)
    response.delete_cookie('csrftoken')
    return response

@unauthenticated_user
def login_user(request):
    logger = logging.getLogger('django')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']

            # Check if the user is locked out
            lockout_key = f'lockout_{username}'
            if cache.get(lockout_key):
                messages.add_message(request, messages.ERROR, "Sorry, your account is locked. Please try again later.")
                return render(request, 'accounts/login.html', {'form_login': form})

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f'User {username} logged in.')

                # Reset login attempts
                cache.delete(f'login_attempts_{username}')

                if user.is_staff:
                    return redirect('/admins')  # Redirect staff members
                else:
                    # Set session expiry (in seconds)
                    request.session.set_expiry(int(timedelta(minutes=SESSION_EXPIRY_MINUTES).total_seconds()))
                    # return redirect('verify_otp')  # Redirect non-staff members to OTP verification

            # Increment failed login attempts
            increment_login_attempts(username)

            # Check if the user has reached the maximum login attempts
            if get_login_attempts(username) >= MAX_LOGIN_ATTEMPTS:
                cache.set(lockout_key, True, LOCKOUT_DURATION)
                messages.add_message(request, messages.ERROR, "Sorry, your account is locked. Please try again later.")
            else:
                messages.add_message(request, messages.ERROR, "Invalid username or password.")

            return render(request, 'accounts/login.html', {'form_login': form})

    context = {
        'form_login': LoginForm(),
        'activate_login': 'active'
    }
    return render(request, 'accounts/login.html', context)


def increment_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)

    if attempts is None:
        cache.set(attempts_key, 1, LOCKOUT_DURATION)
    else:
        cache.incr(attempts_key)


def get_login_attempts(username):
    attempts_key = f'login_attempts_{username}'
    attempts = cache.get(attempts_key)

    if attempts is None:
        attempts = 0

    return attempts

@unauthenticated_user
def register_user(request):
    logger = logging.getLogger('django')
    logger.info(f'User {request.user.username} register in.')
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User registered successfully')
            return redirect('/login')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to register user')
            return render(request, 'accounts/register.html', {'form_register':form})
    context={
        'form_register':UserCreationForm,
        'activate_register': 'active'
    }
    return render(request, 'accounts/register.html', context)


@login_required
@admin_only
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
            if request.user.is_staff:
                return redirect('/admins')
            else:
                return redirect('/clothes/index')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify the form fields')
            return render(request, 'accounts/password_change.html', {'password_change_form':form})
    context = {
        'password_change_form':PasswordChangeForm(request.user)
    }
    return render(request, 'accounts/password_change.html', context)

# def otp_verification(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         totp_device = CustomTOTPDevice.objects.get(user=request.user, confirmed=True)

#         # Initialize TOTP instance with the secret key
#         verifier = TOTP(key=totp_device.bin_key)
#         if verifier.verify(otp):
#             messages.success(request, 'OTP verification successful.')
#             # Perform any additional actions after successful OTP verification
#             return redirect('homepage')
#         else:
#             messages.error(request, 'Invalid OTP. Please try again.')

#     return render(request, 'otp.html')

