from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_signin/', views.admin_signin, name='admin_signin'),
    path('user_signin/', views.user_signin, name='user_signin'),
    path('sign-up/', views.signup, name='signup'),
    path('pass/', views.reset, name='reset'),
    path('projects/', views.project_list, name='project_list'),
    path('details/<int:id>/', views.details, name='details'),
    path('upload/', views.create_project, name='upload'),
    path('update/<int:id>/', views.update_project, name='update'),
    path('delete/<int:id>/', views.delete_p, name='delete'),
    path('feature-projects/', views.featureprojectlist, name='feature_projects'),
    path('feature-projects/<int:id>/', views.details_featureprojectlist, name='feature_project_details'),
    path('projects/<int:id>/donate/', views.donate_to_project, name='donate_to_project'),
    path('projects/<int:id>/comment/', views.comment_on_project, name='comment_on_project'),
    path('projects/<int:id>/rate/', views.rate_project, name='rate_project'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('signout/', views.signout, name='signout'),  
    path('profile/update/', views.update_profile, name='update_profile'),  
    path('thank-you/', views.thank_you, name='thank_you'),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
    path('search/', views.search_projects, name='search_results'),
    path('about/', views.about, name='about'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('contact', views.contact_us, name='contact'),
]
