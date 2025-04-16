from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Parent

class ParentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Parent
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = [
            'username', 'email','child_name', 'first_name', 'last_name',
            'date_of_birth', 'parents_profession', 'country', 'state',
            'home_phone', 'alt_phone', 'work_phone',
            'emergency_contact', 'emergency_relation'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'previous_employers': forms.Textarea(attrs={'rows': 3}),
        }