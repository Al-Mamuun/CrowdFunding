from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from .models import Project, FeatureProject, Profile, Donation, Comment, Rating

def home(request):
    total_donors = Donation.objects.count()
    total_projects = Project.objects.count()
    success_rating = 5
    context = {
        "total_donors": total_donors,
        "total_projects": total_projects,
        "success_rating": success_rating,
    }
    return render(request, "Home/home.html", context)

def reset(request):
    return render(request, 'reset/reset.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'Project/project_list.html', {'projects': projects})

def details(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'Project/details.html', {'project': project})

def featureprojectlist(request):
    projects = FeatureProject.objects.all()
    return render(request, 'Project/featureprojectlist.html', {'projects': projects})

def details_featureprojectlist(request, id):
    project = get_object_or_404(FeatureProject, pk=id)
    return render(request, 'Project/Featuredetails.html', {'project': project})

@login_required(login_url='user_signin')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            profile, _ = Profile.objects.get_or_create(user=request.user)
            project.profile = profile
            project.save()
            messages.success(request, "Project uploaded successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There were errors in your form.")
    else:
        form = ProjectForm()
    return render(request, 'Project/upload_project.html', {'form': form})

@login_required(login_url='user_signin')
def update_project(request, id):
    project = get_object_or_404(Project, pk=id)
    if project.owner != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to update this project.")
        return redirect('project_list')

    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('project_list')
        else:
            messages.error(request, "There were errors in the form.")
    return render(request, 'Project/update_project.html', {'form': form})

@login_required(login_url='user_signin')
def delete_p(request, id):
    project = get_object_or_404(Project, pk=id)
    if project.owner != request.user and not request.user.is_staff:
        messages.error(request, "You cannot delete another user's project.")
        return redirect('project_list')
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('project_list')
    return render(request, 'Project/delete.html', {'project': project})

def donate_to_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            if amount > 0:
                profile = request.user.profile if request.user.is_authenticated else Profile.objects.get_or_create(user=None)[0]
                Donation.objects.create(profile=profile, amount=amount, title=f"Donation to {project.title}", project=project)
                project.collectedAmount += amount
                project.save()
                messages.success(request, "Thank you for your donation!")
            else:
                messages.error(request, "Please enter a valid amount.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered.")
        
        return redirect('profile_dashboard')  # ✅ Redirect to profile after donation
    
    return redirect('details', id=project.id)  # fallback for non-POST

def comment_on_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(project=project, content=content)
            messages.success(request, "Comment added!")
        else:
            messages.error(request, "Comment cannot be empty.")
        return redirect('details', id=project.id)

def rate_project(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        try:
            stars = int(request.POST.get('stars'))
            if 1 <= stars <= 5:
                Rating.objects.create(project=project, stars=stars)
                messages.success(request, "Rating submitted successfully!")
            else:
                messages.error(request, "Rating must be between 1 and 5.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value.")
        return redirect('details', id=project.id)

def admin_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or user.is_superuser):
            auth_login(request, user)
            messages.success(request, f"Welcome, Admin {username}!")
            return redirect('/admin/')
        else:
            messages.error(request, "Invalid admin credentials.")
            return redirect('admin_signin')
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        logout(request)
    return render(request, "SignIn/admin_signin.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    return render(request, 'profile/admin_profile.html')


def user_signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            if not (user.is_staff or user.is_superuser):
                auth_login(request, user)
                
                if 'rememberMe' in request.POST:
                    request.session.set_expiry(1209600) 
                else:
                    request.session.set_expiry(0)  
                
                messages.success(request, f"Welcome, {username}!")
                return redirect('profile_dashboard')  
            else:
                messages.error(request, "You do not have access as a standard user.")
                return redirect('user_signin')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('user_signin')

    return render(request, "SignIn/user_signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phn_number = request.POST.get('phn_number')


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

      
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

      
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )

      
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phn_number = phn_number
        profile.save()

    
        messages.success(request, "Account created successfully!")
        auth_login(request, user)
        return redirect('profile_dashboard')

    return render(request, "signup/signup.html")



@login_required
def profile_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    projects = profile.projects.all()
    
    
    for project in projects:
        project.donations_count = project.donations.count()
        project.donations_total = project.donations.aggregate(total=models.Sum('amount'))['total'] or 0
    
    donations = Donation.objects.filter(profile=profile)

    return render(request, "profile/profile.html", {
        "profile": profile,
        "projects": projects,
        "donations": donations,  
    })



@login_required
def delete_profile(request):
    if request.method == "POST":
   
        profile = request.user.profile  

        
        profile.projects.all().delete()  
        Donation.objects.filter(profile=profile).delete()  

  
        user = request.user
        user.delete()

        messages.success(request, "Your profile and account have been successfully deleted.")
        return redirect("home")

    return render(request, "profile/delete_profile.html")
# User Sign-Out
def signout(request):
    if request.user.is_authenticated:
        
        if request.user.is_staff or request.user.is_superuser:
          
            messages.success(request, "You have been logged out successfully, Admin!")
            logout(request)  
            return redirect('home')  
        else:
            
            messages.success(request, "You have been logged out successfully.")
            logout(request)  
            return redirect('user_signin') 
    else:
        
        return redirect('user_signin')

# Update Profile
@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist. Please create a profile first.")
        return redirect('signup')

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_dashboard')
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/update_profile.html", {"form": form})

# Thank You Page
def thank_you(request):
    return render(request, 'Home/thank_you.html')

def search_projects(request):
    query = request.GET.get('query', '')
    projects = Project.objects.filter(title__icontains=query) | Project.objects.filter(description__icontains=query) if query else []
    return render(request, 'Home/search.html', {'projects': projects, 'query': query})

def about(request):
    return render(request, 'our_info/about.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect('contact_us')

        try:
            subject = f"New Contact Us Message from {name}"
            email_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}\n"
            admin_email = settings.DEFAULT_CONTACT_EMAIL
            send_mail(subject, email_body, email, [admin_email])
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('contact_us')
        except Exception as e:
            messages.error(request, "There was an issue processing your request. Please try again later.")

    return render(request, 'our_info/contact_us.html')
