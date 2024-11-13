from django.shortcuts import render

# Create your views here.

def education(request):
    return render(request, 'dropdown/education.html')

def bussiness(request):
    return render(request, 'dropdown/bussiness.html')

def medical(request):
    return render(request, 'dropdown/medical.html')

def disaster(request):
     return render(request, 'dropdown/disaster.html')

def education_info(request):
    return render(request, 'dropdown/Info/education.html')

def bussiness_info(request):
    return render(request, 'dropdown/Info/business.html')

def medical_info(request):
    return render(request, 'dropdown/Info/medical.html')

def disaster_info(request):
     return render(request, 'dropdown/Info/disaster.html')