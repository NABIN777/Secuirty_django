from django.shortcuts import render

# Create your views here.
def show_firstone(request):
    return render(request,'firstone/firstone.html')
    