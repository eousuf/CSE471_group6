from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ParentRegisterForm
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
