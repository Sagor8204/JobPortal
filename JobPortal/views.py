from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, RecruiterProfile, JobseekerProfile, Job, Application
from .forms import RegistrationForm, LoginForm, RecruiterProfileForm, JobseekerProfileForm, JobForm
from django.db.models import Q

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'portal/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_setup_view(request):
    if request.user.user_type == 'RECRUITER':
        profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
        form_class = RecruiterProfileForm
    else:
        profile, created = JobseekerProfile.objects.get_or_create(user=request.user)
        form_class = JobseekerProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = form_class(instance=profile)
    
    return render(request, 'portal/profile_setup.html', {'form': form})

@login_required
def post_job_view(request):
    if request.user.user_type != 'RECRUITER':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'portal/post_job.html', {'form': form})

@login_required
def job_list_view(request):
    query = request.GET.get('q', '')
    jobs = Job.objects.filter(
        Q(title__icontains=query) | Q(category__icontains=query) | Q(required_skills__icontains=query)
    ).order_by('-posted_at')
    return render(request, 'portal/job_list.html', {'jobs': jobs, 'query': query})

@login_required
def apply_job_view(request, job_id):
    if request.user.user_type != 'JOBSEEKER':
        messages.error(request, "Only jobseekers can apply for jobs.")
        return redirect('job_list')
    
    job = get_object_or_404(Job, id=job_id)
    if Application.objects.filter(job=job, jobseeker=request.user).exists():
        messages.info(request, "You have already applied for this job.")
    else:
        Application.objects.create(job=job, jobseeker=request.user)
        messages.success(request, f"Applied for {job.title} successfully!")
    
    return redirect('job_list')

@login_required
def dashboard_view(request):
    if request.user.user_type == 'JOBSEEKER':
        try:
            profile = request.user.jobseeker_profile
            seeker_skills = set([s.strip().lower() for s in profile.skills.split(',')])
            all_jobs = Job.objects.all()
            matched_jobs = []
            for job in all_jobs:
                job_skills = set([s.strip().lower() for s in job.required_skills.split(',')])
                if seeker_skills & job_skills:
                    matched_jobs.append(job)
        except JobseekerProfile.DoesNotExist:
            matched_jobs = []
        
        applications = Application.objects.filter(jobseeker=request.user)
        return render(request, 'portal/jobseeker_dashboard.html', {
            'matched_jobs': matched_jobs,
            'applications': applications
        })
    else:
        # Recruiter matching
        my_jobs = Job.objects.filter(recruiter=request.user)
        all_seekers = JobseekerProfile.objects.all()
        matches = [] # List of (job, matched_seeker)
        for job in my_jobs:
            job_skills = set([s.strip().lower() for s in job.required_skills.split(',')])
            for seeker in all_seekers:
                seeker_skills = set([s.strip().lower() for s in seeker.skills.split(',')])
                if job_skills & seeker_skills:
                    matches.append({'job': job, 'seeker': seeker})
        
        return render(request, 'portal/recruiter_dashboard.html', {
            'my_jobs': my_jobs,
            'matches': matches
        })