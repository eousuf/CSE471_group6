from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Parent, Daycare,Staff

class ParentRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Parent.ROLE_CHOICES, required=True)

    class Meta:
        model = Parent
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
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

class DaycareRegisterForm(forms.ModelForm):
    class Meta:
        model = Daycare
        fields = ['name', 'address', 'phone', 'email', 'website', 'established_date']
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import Child, Daycare

class ChildRegistrationForm(forms.ModelForm):
    daycare = forms.ModelChoiceField(queryset=Daycare.objects.all(), required=True)

    class Meta:
        model = Child
        fields = ['daycare', 'name', 'age', 'medical_history', 'emergency_contacts']
    def __init__(self, *args, **kwargs):
        super(ChildRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['daycare'].widget = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'placeholder': "Enter your child's name"})
        self.fields['age'].widget.attrs.update({'placeholder': "Enter your child's age"})
        self.fields['medical_history'].widget.attrs.update({'placeholder': "Enter any known medical conditions"})
        self.fields['emergency_contacts'].widget.attrs.update({'placeholder': "Enter emergency contact details"})
class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['full_name', 'phone_number', 'position']

from django import forms
from .models import Child, Group

class AssignGroupForm(forms.Form):
    child = forms.ModelChoiceField(queryset=Child.objects.none())
    group = forms.ModelChoiceField(queryset=Group.objects.none())

    def __init__(self, daycare, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['child'].queryset = Child.objects.filter(daycare=daycare)
        self.fields['group'].queryset = Group.objects.filter(daycare=daycare)
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['group', 'activity_name', 'activity_time']



from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['child_name', 'date', 'status']
