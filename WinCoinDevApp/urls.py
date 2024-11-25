# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('investment_plans', views.investment_plans, name='investment_plans'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('blogs', views.blogs, name='blogs'),
    path('earnings', views.earnings, name='earnings'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path("logout_user",views.logout_user, name = "logout_user"),
    path("withdraw",views.withdraw, name = "withdraw"),
    path("withdraw",views.withdraw, name = "withdraw"),
    path("insufficient_funds",views.insufficient_funds, name = "insufficient_funds"),
    path('deposit/<str:package>/', views.deposit, name='deposit'),
    path('pending_withdrawal/', views.pending_withdrawal, name='pending_withdrawal'),
    path("pending",views.pending, name = "pending"),
    path("transaction_history",views.transaction_history, name = "transaction_history"),
    path("packages",views.packages, name = "packages"),
    path("update_balance",views.update_balance, name = "update_balance"),
    path('upload_proof/<str:package>/', views.upload_proof, name='upload_proof'),
    path('profile_page', views.profile_page, name='profile_page'),
    # Add more URL papackages

]