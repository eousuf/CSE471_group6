from django.shortcuts import render, redirect
from .forms import ParentRegisterForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = ParentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = ParentRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
