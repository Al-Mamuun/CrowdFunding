from django.shortcuts import render

# Create your views here.

def education(request):
    return render(request, 'dropdown/education.html')

def bussiness(request):
    return render(request, 'dropdown/bussiness.html')

def medical(request):
    return render(request, 'dropdown/medical.html')