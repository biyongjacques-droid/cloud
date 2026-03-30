from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('logout/', LogoutView.as_view(next_page='connexion'), name='logout'),
]
