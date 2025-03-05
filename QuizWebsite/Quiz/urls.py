from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('registerUser',views.register_user,name='register_user'),
    path('loginUser', views.login_user,  name='loginUser'),
    path('Courses', views.Courses, name='Course'),
    path('Quiz', views.Quiz_gen, name='Quiz'),
    path('Exam', views.Exam, name='Exam'),
    path('logout', views.Logout, name='LogOut'),
     path('Login', LoginView.as_view(template_name='Quiz/Login.html'), name='login'),
    path('', LoginView.as_view(template_name='Quiz/Home.html'), name='Home'),
    path('Profile', views.profile, name='Profile'),
    path('Reset Password', LoginView.as_view(template_name='Quiz/ResetPassword.html'), name='Reset_password'),
    path('Resting',views.Reset, name='Rset'),
    path('Leaderboard',views.Leaderboard, name='Leaderboard'),
    ]
