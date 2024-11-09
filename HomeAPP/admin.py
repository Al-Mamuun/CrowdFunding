from django.contrib import admin
from .models import User, Project, Donation, Rating, Comment, Report,FeatureProject

admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(FeatureProject)
