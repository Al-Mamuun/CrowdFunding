from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile
from .forms import SignUpForm
from django.contrib.auth import login
from .forms import *

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone_number = request.POST.get('phone_number')

        if password == confirm_password:  # Check if passwords match
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Create the user profile
            Profile.objects.create(user=user, mobile=phone_number)
            login(request, user)  # Log in the user
            return redirect('profile')  # Redirect to the profile page
        else:
            return render(request, 'signup/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'signup/signup.html')

# Create your views here.

def home(request):
    return render(request, template_name='Home/home.html')

def signin(request):
    return render(request, template_name='Signin/signin.html')


def signup(request):
    return render(request, template_name='signup/signup.html')

def reset(request):
    return render(request, template_name='reset/reset.html')

from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'Project/project_list.html', {'projects': projects})

def featureprojectlist(request):
    projects = FeatureProject.objects.all()
    return render(request, 'Project/featureprojectlist.html', {'projects': projects})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            # If the profile does not exist, create it
            Profile.objects.get_or_create(user=user)
            return redirect('profile')  # Redirect to the profile page
        else:
            # Invalid credentials handling
            return render(request, 'SignIn/signin.html', {'error': 'Invalid credentials'})

    return render(request, 'SignIn/signin.html')

def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'profile/profile.html', {'profile': profile})
    return redirect('signin')  # Redirect to sign-in if not authenticated

def Upload_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project/upload_project.html', {'form': form})

