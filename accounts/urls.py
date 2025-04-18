from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, CustomLoginView
from .views import admin_dashboard, staff_dashboard,register_daycare,daycare_detail
urlpatterns = [
    path('', views.home, name='index'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),    
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/profile/'
    ), name='change_password'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('register_daycare/', register_daycare, name='register_daycare'),
    path('daycare/<int:daycare_id>/', daycare_detail, name='daycare_detail'),
    path('children/register/', views.register_child, name='children_register'),
    path('staff/register/<int:daycare_id>/', views.register_staff, name='register_staff'),
    path('accounts/assign_group_ajax/<int:child_id>/', views.assign_group_ajax, name='assign_group_ajax'),




]

