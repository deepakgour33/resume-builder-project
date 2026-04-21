from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.user_logout, name="logout"),

    # Resume
    path("resume/", views.resume_form, name="resume"),
    path("resume-preview/", views.resume_preview, name="resume_preview"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),

    # Jobs
    path("jobs/", views.job_list, name="job_list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),

    # AI
    path("ai-insights/", views.ai_insights, name="ai_insights"),
]