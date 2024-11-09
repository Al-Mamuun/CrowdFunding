from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
# class User(AbstractUser):
#     bio = models.TextField(blank=True)
#     isAdmin = models.BooleanField(default=False)

#     # Use related_name to avoid clashes with Django's default User model
#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_set',  # Unique related name for your custom User model
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups',
#     )
    
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions_set',  # Unique related name for your custom User model
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

#     def __str__(self):
#         return self.username  # Add a string representation for the User model


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goalAmount = models.FloatField()
    collectedAmount = models.FloatField(default=0.0)
    createdAt = models.DateField(auto_now_add=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.FloatField()
    donationDate = models.DateField(auto_now_add=True)

class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stars = models.IntegerField()
    ratingDate = models.DateField(auto_now_add=True)

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    commentDate = models.DateField(auto_now_add=True)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reportReason = models.TextField()
    reportDate = models.DateField(auto_now_add=True)
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.username}"

