from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_setup_view, name='profile_setup'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job_view, name='apply_job'),
]