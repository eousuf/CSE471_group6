from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ChildRegistrationForm

@login_required
def register_child(request):
    if request.method == 'POST':
        form = ChildRegistrationForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            return redirect('profile')  # Adjust this if your profile URL name is different.
    else:
        form = ChildRegistrationForm()
    
    return render(request, 'children/register_child.html', {'form': form})
