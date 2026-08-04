from django.contrib import admin
from .models import Project, Donation, Rating, Comment,FeatureProject

admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(FeatureProject)
