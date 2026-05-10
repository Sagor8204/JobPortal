from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('RECRUITER', 'Recruiter'),
        ('JOBSEEKER', 'Jobseeker'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    display_name = models.CharField(max_length=100)

class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    company_description = models.TextField()
    website = models.URLField(blank=True)

    def __str__(self):
        return self.company_name

class JobseekerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='jobseeker_profile')
    skills = models.CharField(max_length=500, help_text="Comma separated skills")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    recruiter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs_posted')
    title = models.CharField(max_length=200)
    openings = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.CharField(max_length=500, help_text="Comma separated skills")
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    jobseeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker.username} applied for {self.job.title}"