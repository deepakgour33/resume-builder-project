from django.contrib import admin
from .models import ResumeProfile, Job, JobApplication

admin.site.register(ResumeProfile)
admin.site.register(Job)
admin.site.register(JobApplication)