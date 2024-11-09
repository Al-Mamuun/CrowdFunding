from django.contrib import admin
from django.urls import path
from HomeAPP import views as M

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
]
