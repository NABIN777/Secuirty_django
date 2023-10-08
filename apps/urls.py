from django.urls import path;
from firstone import views;

urlpatterns = [
    path('',views.show_firstone,name='firstone'),
    path('new',views.show_new)
    
]
