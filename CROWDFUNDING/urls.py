from django.contrib import admin
from django.urls import path
from HomeAPP import views as M
from DropDown import views as D

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',M.home,name='home'),
    path('in/',M.signin,name='signin'),
    path('up/',M.signup,name='signup'),
    path('pass/',M.reset,name='reset'),
    path('projects/', M.project_list, name='project_list'),
    path('sign-in/', M.signin, name='sign_in'),
    path('profile/', M.profile, name='profile'),
    path('sign-up/', M.signup, name='sign_up'),
    path('upload/', M.Upload_project, name='upload'),
    path('new/',M.featureprojectlist, name='new'),
    path('edu/',D.education,name='education'),
    path('bus/',D.bussiness,name='bussiness'),
    path('medical/',D.medical,name='medical'),
]
