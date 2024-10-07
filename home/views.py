from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request,'home\home.html')

def Signin (request):
    return render(request,'signin\Signin.html')

def Signup(request):
    return render(request,'signup\signup.html')