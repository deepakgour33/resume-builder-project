from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .forms import ResumeForm
from .models import ResumeProfile, Job, JobApplication


def home(request):
    suggestion = "Complete your resume to get AI insights."
    score = 20
    status = "Resume Started"

    if request.user.is_authenticated:
        resume = ResumeProfile.objects.filter(user=request.user).first()

        if resume:
            score = 50
            status = "Resume In Progress"

            if not resume.projects or resume.projects.strip() == "":
                suggestion = "Add at least 2 projects to improve your ATS score."
                score = 50

            elif not resume.certifications or resume.certifications.strip() == "":
                suggestion = "Adding certifications can improve recruiter trust."
                score = 70

            elif len(resume.skills.split(",")) < 5:
                suggestion = "Try adding more technical skills."
                score = 80

            else:
                suggestion = "Excellent! Your resume looks strong and ATS ready."
                score = 95
                status = "Resume Completed"

    return render(request, "home.html", {
        "suggestion": suggestion,
        "score": score,
        "status": status,
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(
                request,
                "login.html",
                {"error": "Invalid username or password"},
            )

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    resume = ResumeProfile.objects.filter(user=request.user).first()

    score = 20
    status = "Resume Started"
    suggestion = "Complete your resume to unlock AI optimization."
    completed_sections = 0

    if resume:
        fields = [
            resume.full_name,
            resume.email,
            resume.phone,
            resume.location,
            resume.skills,
            resume.education,
            resume.projects,
            resume.experience,
            resume.certifications,
            resume.languages,
            resume.strengths,
            resume.objective,
        ]

        completed_sections = sum(1 for field in fields if field)

        score = min(completed_sections * 8, 100)

        if score < 40:
            status = "Resume Started"
            suggestion = "Add more sections to improve your ATS score."
        elif score < 70:
            status = "Resume In Progress"
            suggestion = "Good progress! Add projects and certifications."
        else:
            status = "Recruiter Ready"
            suggestion = "Excellent! Your resume is highly optimized."

    total_jobs = Job.objects.count()

    return render(request, "dashboard.html", {
        "score": score,
        "status": status,
        "suggestion": suggestion,
        "completed_sections": completed_sections,
        "total_jobs": total_jobs,
    })


@login_required
def resume_form(request):
    resume, created = ResumeProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect("resume_preview")
    else:
        form = ResumeForm(instance=resume)

    return render(request, "resume_form.html", {"form": form})


@login_required
def resume_preview(request):
    resume = ResumeProfile.objects.get(user=request.user)
    return render(request, "resume_preview.html", {"resume": resume})


@login_required
def download_pdf(request):
    resume = ResumeProfile.objects.get(user=request.user)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="resume.pdf"'

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, y, resume.full_name)
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Email: {resume.email}")
    y -= 20
    p.drawString(50, y, f"Phone: {resume.phone}")
    y -= 20
    p.drawString(50, y, f"Location: {resume.location}")
    y -= 30

    p.drawString(50, y, f"Skills: {resume.skills}")
    y -= 20
    p.drawString(50, y, f"Education: {resume.education}")
    y -= 20
    p.drawString(50, y, f"Projects: {resume.projects}")
    y -= 20
    p.drawString(50, y, f"Experience: {resume.experience}")
    y -= 20
    p.drawString(50, y, f"Certifications: {resume.certifications}")

    p.showPage()
    p.save()

    return response


@login_required
def job_list(request):
    jobs = Job.objects.all()
    resume = ResumeProfile.objects.filter(user=request.user).first()

    recommended_role = "General Developer"

    if resume and resume.skills:
        skills = resume.skills.lower()

        if (
            "python" in skills
            and "django" in skills
            and (
                "html" in skills
                or "css" in skills
                or "javascript" in skills
            )
        ):
            recommended_role = "Full Stack Developer"

        elif "python" in skills and "django" in skills:
            recommended_role = "Python Django Developer"

        elif (
            "html" in skills
            or "css" in skills
            or "javascript" in skills
            or "react" in skills
        ):
            recommended_role = "Frontend Developer"

        elif "pandas" in skills or "sql" in skills:
            recommended_role = "Data Analyst"

    return render(request, "job_list.html", {
        "jobs": jobs,
        "recommended_role": recommended_role,
    })


@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    JobApplication.objects.create(user=request.user, job=job)
    return redirect("my_applications")


@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    return render(request, "my_applications.html", {"applications": applications})


@login_required
def ai_insights(request):
    resume = ResumeProfile.objects.filter(user=request.user).first()

    score = 20
    status = "Resume Started"
    suggestion = "Complete your resume to unlock AI optimization."

    if resume:
        score = 50
        status = "Resume In Progress"

        if not resume.projects or resume.projects.strip() == "":
            suggestion = "Add more projects to improve ATS score."

        elif not resume.certifications or resume.certifications.strip() == "":
            score = 70
            suggestion = "Add certifications to increase trust."

        elif len(resume.skills.split(",")) < 5:
            score = 85
            suggestion = "Add more technical skills for better matching."

        else:
            score = 100
            status = "Recruiter Ready"
            suggestion = "Excellent! Your profile is fully optimized."

    return render(request, "ai_insights.html", {
        "score": score,
        "status": status,
        "suggestion": suggestion,
    })