from django.shortcuts import render
from django.shortcuts import render, redirect
from accounts.auth import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from clothes.models import *
from django.contrib import messages




@login_required
@admin_only
def admins_dashboard(request):
    clothes = Clothes.objects.all()
    clothes_count = clothes.count()
    user = User.objects.filter(is_active=1)
    customer = User.objects.filter(is_staff=0).count()

    user_count = user.count()
    admin = User.objects.filter(is_staff=1)
    admin_count = admin.count()
    image=Clothes.objects.filter(clothes_image=not None).count()
    order=Order.objects.all().count()


    context ={
        'clothes': clothes_count,
        'userc': user_count,
        'admin':admin_count,
        'image':image,
        'customer':customer,
        'order':order,
    }
    return render(request, 'admins/dashboard.html', context)

@login_required
@admin_only
def show_users(request):
    users = User.objects.filter(is_staff=0).order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'admins/users.html', context)

@login_required
@admin_only
def show_admins(request):
    admins = User.objects.filter(is_staff=1).order_by('-id')
    context = {
        'admins': admins
    }
    return render(request, 'admins/admins.html', context)


@login_required
@admin_only
def promote_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User promoted to admin')
    return redirect('/admins/admins')


@login_required
@admin_only
def demote_admin(request, user_id):
    admin = User.objects.get(id=user_id)
    admin.is_staff = False
    admin.save()
    messages.add_message(request, messages.SUCCESS, 'Admin demoted to user')
    return redirect('/admins/users')
