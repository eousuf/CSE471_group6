from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, CustomLoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
