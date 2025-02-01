from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='home'),  # Asosiy sahifa
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forget-password/', views.forget_password_view, name='forget_password'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
