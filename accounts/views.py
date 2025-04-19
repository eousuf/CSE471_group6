from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
import string
import json
from django.contrib.auth.hashers import make_password

from .models import Parent, Daycare, Child, Staff, Schedule, Attendance
from .forms import (
    ParentRegisterForm,
    ParentUpdateForm,
    DaycareRegisterForm,
    ChildRegistrationForm,
    StaffRegistrationForm,
    ScheduleForm,
    AttendanceForm,
)

# — Registration / Login —————————————————————————

def register(request):
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = ParentRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'staff':
            # staff go to the home page
            return reverse_lazy('index')
        return reverse_lazy('index')

# — Home / Dashboards ——————————————————————————

@login_required
def home(request):
    daycare_list = Daycare.objects.all()
    children = request.user.children.all()
    return render(request, 'index.html', {
        'daycare_list': daycare_list,
        'children': children
    })

def is_admin(user):
    return user.role == 'admin'

def is_staff(user):
    return user.role == 'staff'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    daycares = Daycare.objects.filter(admin=request.user)
    staff_members = Staff.objects.filter(daycare__in=daycares)
    parent_count = Parent.objects.filter(role='parent').count()
    staff_count = staff_members.count()
    children_count = 227  # placeholder
    incidents_count = 14  # placeholder

    return render(request, 'accounts/admin_dashboard.html', {
        'parent_count': parent_count,
        'staff_count': staff_count,
        'children_count': children_count,
        'incidents_count': incidents_count,
        'daycare_list': Daycare.objects.all(),
        'staff_members': staff_members,
    })

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    try:
        staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        messages.error(request, "You are not authorized as a staff member.")
        return redirect('login')

    children = Child.objects.filter(daycare=staff.daycare)
    return render(request, 'accounts/staff_dashboard.html', {
        'staff': staff,
        'children': children
    })

# — Profile ———————————————————————————————————

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'parent': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ParentUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ParentUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

# — Daycare / Child / Staff Registration —————————————————

@login_required
@user_passes_test(is_admin)
def register_daycare(request):
    if request.method == 'POST':
        form = DaycareRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Daycare registered successfully!")
            return redirect('admin_dashboard')
    else:
        form = DaycareRegisterForm()
    return render(request, 'accounts/register_daycare.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def daycare_detail(request, daycare_id):
    daycare = get_object_or_404(Daycare, id=daycare_id)
    staff_members = Staff.objects.filter(daycare=daycare)
    return render(request, 'accounts/daycare_detail.html', {
        'daycare': daycare,
        'staff_members': staff_members,
        'parent_count': 6,       # placeholder
        'children_count': 227,   # placeholder
        'incidents_count': 14,   # placeholder
    })

@login_required
def register_child(request):
    daycare_id = request.GET.get('daycare_id') or request.POST.get('daycare')
    if not daycare_id:
        return redirect('index')
    daycare = get_object_or_404(Daycare, id=daycare_id)

    if request.method == 'POST':
        form = ChildRegistrationForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.daycare = daycare
            child.save()
            messages.success(request, "Child registered successfully!")
            return redirect('index')
    else:
        form = ChildRegistrationForm()
    return render(request, 'accounts/register_child.html', {
        'form': form,
        'daycare': daycare
    })

def generate_random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@login_required
@user_passes_test(is_admin)
def register_staff(request, daycare_id):
    daycare = get_object_or_404(Daycare, id=daycare_id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.daycare = daycare
            username = f"{staff.full_name.split()[0].lower()}{random.randint(1000,9999)}"
            password = generate_random_password()
            staff.user = Parent.objects.create(
                username=username,
                email=f"{username}@staffdaycare.com",
                password=make_password(password),
                role='staff',
                is_active=True,
            )
            staff.username = username
            staff.plain_password = password
            staff.save()
            messages.success(request,
                f"Staff registered! Username: {username}, Password: {password}"
            )
            return redirect('admin_dashboard')
    else:
        form = StaffRegistrationForm()
    return render(request, 'accounts/register_staff.html', {
        'form': form,
        'daycare': daycare
    })

# — AJAX: Assign Group ——————————————————————————

@login_required
@csrf_exempt
def assign_group_ajax(request, child_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = data.get('group')
        if not group_name:
            return JsonResponse({'success': False, 'error': 'Group not provided'})
        try:
            child = Child.objects.get(id=child_id)
            child.group = group_name
            child.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# — Schedule List ————————————————————————————

@login_required
def schedule_list(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    schedules = Schedule.objects.all()
    return render(request, 'accounts/schedule_list.html', {
        'form': form,
        'schedules': schedules
    })

# — Attendance ——————————————————————————————

@login_required
@user_passes_test(is_staff)
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.staff = request.user
            attendance.save()
            return redirect('mark_attendance')
    else:
        form = AttendanceForm(initial={'date': timezone.now().date()})
    return render(request, 'attendance/mark_attendance.html', {
        'form': form
    })

@login_required
@user_passes_test(is_staff)
def attendance_report(request, period='daily'):
    today = timezone.now().date()
    if period == 'daily':
        records = Attendance.objects.filter(date=today)
    elif period == 'weekly':
        week_start = today - datetime.timedelta(days=today.weekday())
        records = Attendance.objects.filter(date__gte=week_start)
    else:  # monthly
        month_start = today.replace(day=1)
        records = Attendance.objects.filter(date__gte=month_start)

    return render(request, 'attendance/report.html', {
        'attendance': records,
        'period': period
    })
