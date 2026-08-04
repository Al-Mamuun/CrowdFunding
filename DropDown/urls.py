from django.urls import path
from . import views

urlpatterns = [
    path('education/', views.education, name='education'),
    path('business/', views.bussiness, name='business'),
    path('medical/', views.medical, name='medical'),
    path('disaster/', views.disaster, name='disaster'),
    path('education-info/', views.education_info, name='educationInfo'),
    path('business-info/', views.bussiness_info, name='bussinessInfo'),
    path('medical-info/', views.medical_info, name='medicalInfo'),
    path('disaster-info/', views.disaster_info, name='disasterInfo'),
]
