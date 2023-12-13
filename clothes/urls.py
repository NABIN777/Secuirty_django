from django.urls import path
from . import views
app_name='clothes'
urlpatterns = [
    path('homepage' , views.homepage, name='homepage'),
    path('category_form',views.category_form),
    path('get_category', views.get_category),
    path('delete_category/<int:category_id>',views.delete_category),
    path('update_category/<int:category_id>',views.category_update_form),
    # path('get_categories_user', views.show_categories),
    # path('get_clothes_user',views.get_category),

    path('clothes_form', views.clothe_form),
    path('get_clothes', views.get_clothe, name='get_clothe'),
    path('delete_clothes/<int:clothe_id>', views.delete_clothe,name='delete_clothe'),
    path('update_clothes/<int:clothe_id>', views.clothe_update_form),

    path('get_category_user', views.show_categories, name='show_categories'),
    path('get_clothe_user', views.show_clothes),
    path('add_to_cart/<int:clothe_id>', views.add_to_cart),
    path('mycart', views.show_cart_items),
    path('remove_cart_item/<int:cart_id>', views.remove_cart_item),
    path('order_form/<int:clothe_id>/<int:cart_id>', views.order_form),
    path('my_order', views.my_order),
    path('search',views.search),
    path('description',views.show_description),
    path('order',views.order),
    path('about',views.about),


]