
from django.urls import path,include

urlpatterns = [
    path('clothes/',include('clothes.urls',namespace='clothes')),
    path('admins/',include('admins.urls')),
    path('',include('accounts.urls')),
    

]
