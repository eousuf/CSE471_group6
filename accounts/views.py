from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ParentRegisterForm
from .forms import ParentUpdateForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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
        return reverse_lazy('index')
    
def home(request):
    return render(request, 'index.html')

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
