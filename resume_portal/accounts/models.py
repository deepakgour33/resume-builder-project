from django.db import models
from django.contrib.auth.models import User

class ResumeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    objective = models.TextField(blank=True)
    skills = models.TextField()
    strengths = models.TextField(blank=True)

    education = models.TextField()
    cgpa = models.CharField(max_length=20, blank=True)

    experience = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    languages = models.TextField(blank=True)

    def __str__(self):
        return self.full_name
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"