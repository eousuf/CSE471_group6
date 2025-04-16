from django import forms
from .models import Child  # Import your Child model from children/models.py

class ChildRegistrationForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'medical_history', 'emergency_contacts']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a common CSS class to each field for consistent styling.
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # Optionally, add placeholders:
        self.fields['name'].widget.attrs.update({'placeholder': "Enter your child's name"})
        self.fields['age'].widget.attrs.update({'placeholder': "Enter your child's age"})
        self.fields['medical_history'].widget.attrs.update({'placeholder': "Enter any known medical conditions"})
        self.fields['emergency_contacts'].widget.attrs.update({'placeholder': "Enter emergency contact details"})
