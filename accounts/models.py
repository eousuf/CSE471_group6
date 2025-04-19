from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings

class Parent(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('admin', 'Admin'),
        ('staff', 'Daycare Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='parent')
    
    email = models.EmailField(unique=True)
    child_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    parents_profession = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    home_phone = models.CharField(max_length=20, blank=True)
    alt_phone = models.CharField(max_length=20, blank=True)
    work_phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_relation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class Daycare(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='daycares',
        null=True,    # <-- ADD THIS
        blank=True    # <-- ADD THIS
    )

    def __str__(self):
        return self.name
    
from .models import Daycare  # Import Daycare model
class Group(models.Model):
    name = models.CharField(max_length=100)
    min_age = models.IntegerField(help_text="Minimum age in years")
    max_age = models.IntegerField(help_text="Maximum age in years")
    daycare = models.ForeignKey(Daycare, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.min_age}-{self.max_age} yrs)"

class Child(models.Model):
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='children'
    )
    daycare = models.ForeignKey(
        Daycare,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    group = models.CharField(
        max_length=50,
        choices=[
            ('Infant', 'Infant'),
            ('Toddlers', 'Toddlers'),
            ('Preschool', 'Preschool'),
            ('School Aged', 'School Aged'),
        ],
        blank=True,
        null=True
    )
    medical_history = models.TextField(blank=True, null=True)
    emergency_contacts = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} (Age: {self.age})"
    
    def save(self, *args, **kwargs):
        if self.daycare:
            possible_groups = Group.objects.filter(daycare=self.daycare, min_age__lte=self.age, max_age__gte=self.age)
            if possible_groups.exists():
                self.group = possible_groups.first()
        super().save(*args, **kwargs)



class Staff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # link to Django user
    daycare = models.ForeignKey('Daycare', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=50)  # example: "Teacher", "Manager", etc.
    daycare = models.ForeignKey(Daycare, on_delete=models.CASCADE)
    plain_password = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.full_name
    
class Schedule(models.Model):
    GROUP_CHOICES = [
        ('Infant', 'Infant'),
        ('Toddler', 'Toddler'),
        ('Preschool', 'Preschool'),
        ('School Aged', 'School Aged'),
    ]

    group = models.CharField(max_length=50, choices=GROUP_CHOICES)
    activity_name = models.CharField(max_length=100)
    activity_time = models.TimeField()
    activity_date = models.DateField(auto_now_add=True)  # Optional, today's date

    def __str__(self):
        return f"{self.group} - {self.activity_name} at {self.activity_time}"
    


class Attendance(models.Model):
    child_name = models.ForeignKey(
        'Parent', 
        on_delete=models.CASCADE, 
        related_name="attendance_child",  # Changed related_name to avoid conflict
        limit_choices_to={'role': 'parent'}
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="attendance_staff"  # Changed related_name to avoid conflict
    )

    def __str__(self):
        return f"{self.child_name} - {self.date} - {self.status}"
