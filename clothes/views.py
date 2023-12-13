import logging
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from accounts.auth import admin_only, user_only

from .forms import CategoryForm, ClotheForm, OrderForm
from .models import Cart, Category, Clothes, Order

logger = logging.getLogger(__name__)

def homepage(request):
    logger.info('User accessed homepage.')

    return render(request,'clothes/homepage.html')

@login_required
@admin_only
def category_form(request):
    logger.info(f'Admin {request.user.username} accessed category form.')

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category added successfully')
            return redirect("/clothes/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add category')
            return render(request, 'clothes/category_form.html', {'form_category':form})
    context ={
        'form_category': CategoryForm,
        'activate_category': 'active'
    }
    return render(request, 'clothes/category_form.html', context)


@login_required
@admin_only
def get_category(request):
    categories =  Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_category':'active'
    }
    return render(request, 'clothes/get_category.html', context)

@login_required
@admin_only
def delete_category(request, category_id):
    logger.info(f'Admin {request.user.username} deleted category with ID {category_id}.')

    category = Category.objects.get(id=category_id)
    category.delete()
    messages.add_message(request, messages.SUCCESS, 'Category Deleted Successfully')
    return redirect('/clothes/get_category')

@login_required
@admin_only
def category_update_form(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category updated successfully')
            return redirect("/clothes/get_category")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update category')
            return render(request, 'clothes/category_update_form.html', {'form_category':form})
    context ={
        'form_category': CategoryForm(instance=category),
        'activate_category': 'active'
    }
    return render(request, 'clothes/category_update_form.html', context)

def show_categories(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_category_user': 'active'
    }
    return render(request, 'clothes/show_categories.html', context)

def get_clothes(request):
    clothes = Clothes.objects.all().order_by('-id')
    context = {
        'clothes':clothes,
        'activate_clothe_user': 'active'
    }
    return render(request, 'clothes/get_clothes.html', context)


@login_required
@admin_only
def clothe_form(request):
    if request.method == "POST":
        form = ClotheForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Clothe added successfully')
            return redirect("/clothes/get_clothes")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add clothe')
            return render(request, 'clothes/clothe_form.html', {'form_clothe':form})
    context ={
        'form_clothe': ClotheForm,
        'activate_clothe': 'active'
    }
    return render(request, 'clothes/clothe_form.html', context)

@login_required
@admin_only
def get_clothe(request):
    clothe = Clothes.objects.all().order_by('-id')
    context = {
        'clothes':clothe,
        'activate_clothe':'active'
    }
    return render(request, 'clothes/get_clothes.html', context)

@login_required
@admin_only
def delete_clothe(request, clothe_id):
    clothe = Clothes.objects.get(id=clothe_id)
    os.remove(clothe.clothes_image.path)
    clothe.delete()
    messages.add_message(request, messages.SUCCESS, 'Clothe Deleted Successfully')
    return redirect('/clothes/get_clothes')


@login_required
@admin_only
def clothe_form(request):
    if request.method == "POST":
        form = ClotheForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Clothe added successfully')
            return redirect("/clothes/get_clothes")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add clothe')
            return render(request, 'clothes/clothe_form.html', {'form_clothe':form})
    context ={
        'form_clothe': ClotheForm,
        'activate_clothe': 'active'
    }
    return render(request, 'clothes/clothe_form.html', context)


@login_required
@admin_only
def clothe_update_form(request, clothe_id):
    clothe = Clothes.objects.get(id=clothe_id)
    if request.method == "POST":
        form = ClotheForm(request.POST, request.FILES, instance=clothe)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'clothe updated successfully')
            return redirect("/clothes/get_clothes")
        else:
            messages.add_message(request, messages.ERROR, 'Unable to update clothe')
            return render(request, 'clothes/clothe_form.html', {'form_clothe': form})
    context = {
        'form_clothe': ClotheForm(instance=clothe),
        'activate_clothe': 'active'
    }
    return render(request, 'clothes/clothe_update_form.html', context)

def show_categories(request):
    categories = Category.objects.all().order_by('-id')
    context = {
        'categories':categories,
        'activate_category_user': 'active'
    }
    return render(request, 'clothes/show_categories.html', context)

def show_clothes(request):
    clothes = Clothes.objects.all().order_by('-id')
    context = {
        'clothes':clothes,
        'activate_clothe_user': 'active'
    }
    return render(request, 'clothes/show_clothes.html', context)


def show_description(request,):
    clothes = Clothes.objects.all().order_by('-id')
    context = {
        'clothes':clothes,
        'activate_clothe_user': 'active'
    }
    return render(request, 'clothes/description.html', context)



@login_required
@admin_only
def order(request):
    order = Order.objects.select_related('clothe','user').all().order_by('-id')

    return render(request,'clothes/order.html',{'order':order})


@login_required
@user_only
def add_to_cart(request, clothe_id):
    user = request.user
    clothe = Clothes.objects.get(id=clothe_id)

    check_item_presence = Cart.objects.filter(user=user, clothe=clothe)
    if check_item_presence:
        messages.add_message(request, messages.ERROR, 'Item is already present in cart')
        return redirect('/clothes/get_clothe_user')
    else:
        cart = Cart.objects.create(clothe=clothe, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Item added to cart')
            return redirect('/clothes/mycart')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to add item to cart')


@login_required
@user_only
def show_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user= user)
    context = {
        'items':items,
        'activate_my_cart':'active'
    }
    return render(request, 'clothes/mycart.html', context)

@login_required
@user_only
def remove_cart_item(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.SUCCESS, 'Cart item removed successfully')
    return redirect('/clothes/mycart')


@login_required
@user_only
def order_form(request, clothe_id,cart_id):
    user = request.user
    clothe = Clothes.objects.get(id=clothe_id)
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get('quantity')
            price = clothe.clothes_price
            total_price = int(quantity)*int(price)
            contact_no = request.POST.get('contact_no')
            contact_address = request.POST.get('contact_address')
            order = Order.objects.create(clothe=clothe,
                                         user =user,
                                         quantity=quantity,
                                         total_price=total_price,
                                         contact_no = contact_no,
                                         contact_address =contact_address,
                                         status="Pending"
            )
            if order:
                messages.add_message(request, messages.SUCCESS, 'Item ordered')
                cart_item.delete()
                return redirect('/clothes/my_order')
        else:
            messages.add_message(request, messages.ERROR, 'Something went wrong')
            return render(request, 'clothes/order_form.html', {'order_form':form})
    context = {
        'order_form': OrderForm
    }
    return render(request, 'clothes/order_form.html', context)


@login_required
@user_only
def my_order(request):
    user = request.user
    items = Order.objects.filter(user=user).order_by('-id')
    context = {
        'items':items,
        'activate_myorders':'active'
    }
    return render(request, 'clothes/my_order.html', context)

def search(request):
    search = request.GET.get('z')
    logger.info(f'User {__name__} search.')

    clothes = Clothes.objects.filter(Q(clothes_name__icontains=search))
    return render(request, 'clothes/search.html', {'clothes':clothes})

def about(request):

    logger.info(f'User {__name__} accessed about page.')

    return render(request, 'clothes/about.html')


