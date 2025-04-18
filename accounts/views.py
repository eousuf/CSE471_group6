from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ParentRegisterForm
from .forms import ParentUpdateForm,DaycareRegisterForm,ChildRegistrationForm,StaffRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from accounts.models import Parent,Daycare,Child,Staff
from django.urls import reverse
from django.shortcuts import get_object_or_404
import random
import string
from django.contrib.auth.hashers import make_password
from .models import Child, Group
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('index')  # Redirect to home page
    else:
        form = ParentRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')  # create this page later
        elif user.role == 'staff':
            return reverse_lazy('staff_dashboard')  # create this page later
        else:
            return reverse_lazy('index')  # normal parent home

    
@login_required
def home(request):
    daycare_list = Daycare.objects.all()  # NO filter
    children = request.user.children.all()

    context = {
        'daycare_list': daycare_list,
        'children': children,
    }

    return render(request, 'index.html', context)


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
    children_count = 227  # Placeholder for now
    incidents_count = 14  # Placeholder for now

    # NEW: Fetch all daycares
    daycare_list = Daycare.objects.all()

    context = {
        'parent_count': parent_count,
        'staff_count': staff_count,
        'children_count': children_count,
        'incidents_count': incidents_count,
        'daycare_list': daycare_list,  # Pass to template
        'staff_members': staff_members,
    }
    return render(request, 'accounts/admin_dashboard.html', context)
@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    try:
        staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        messages.error(request, "You are not authorized as a Staff.")
        return redirect('login')

    children = Child.objects.filter(daycare=staff.daycare)

    context = {
        'staff': staff,
        'children': children,
    }
    return render(request, 'accounts/staff_dashboard.html', context)

@login_required
def profile(request):
    parent = request.user
    return render(request, 'accounts/profile.html', {'parent': parent})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ParentUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            print(form.errors)  # For debugging
    else:
        form = ParentUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def register_daycare(request):
    if request.method == 'POST':
        form = DaycareRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Daycare registered successfully!")
            return redirect('admin_dashboard')  # or anywhere you want
    else:
        form = DaycareRegisterForm()
    return render(request, 'accounts/register_daycare.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def daycare_detail(request, daycare_id):
    daycare = Daycare.objects.get(id=daycare_id)
    staff_members = Staff.objects.filter(daycare=daycare)

    # Here later you will filter parents, children, incidents based on daycare
    # For now we will just show dummy numbers
    
    parent_count = 6  # Placeholder
    children_count = 227  # Placeholder
    incidents_count = 14  # Placeholder

    context = {
        'daycare': daycare,
        'staff_members': staff_members,
        'parent_count': parent_count,
        'children_count': children_count,
        'incidents_count': incidents_count,
    }
    return render(request, 'accounts/daycare_detail.html', context)

@login_required
def register_child(request):
    daycare_id = request.GET.get('daycare_id') or request.POST.get('daycare')
    if not daycare_id:
        return redirect('index')

    try:
        daycare = Daycare.objects.get(id=daycare_id)
    except Daycare.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = ChildRegistrationForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.daycare = daycare
            child.save()
            messages.success(request, "Child registered successfully!")
            return redirect('index')  # Redirect to home after success
        else:
            print(form.errors)
    else:
        form = ChildRegistrationForm()

    return render(request, 'accounts/register_child.html', {'form': form, 'daycare': daycare})


import random
import string
from django.contrib.auth.hashers import make_password

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))



@login_required
@user_passes_test(is_admin)
def register_staff(request, daycare_id):
    daycare = get_object_or_404(Daycare, id=daycare_id)

    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.daycare = daycare

            # Generate random username and password
            username = f"{staff.full_name.split()[0].lower()}{random.randint(1000, 9999)}"
            password = generate_random_password()

            # Create associated user
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

            # 🎯 Save username and password to messages
            messages.success(request, f"Staff registered successfully!\nUsername: {username}\nPassword: {password}")

            return redirect('admin_dashboard')
    else:
        form = StaffRegistrationForm()

    return render(request, 'accounts/register_staff.html', {'form': form, 'daycare': daycare})


from .forms import AssignGroupForm

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
@login_required
@csrf_exempt  # <-- IMPORTANT because we're doing manual CSRF in JS
def assign_group_ajax(request, child_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # <-- load JSON body
            group_name = data.get('group')   # <-- get selected group

            if not group_name:
                return JsonResponse({'success': False, 'error': 'Group not provided'})

            child = Child.objects.get(id=child_id)
            child.group = group_name   # <-- just assign the string!
            child.save()

            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})