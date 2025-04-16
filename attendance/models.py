
from django.db import models
from datetime import date
from children.models import Child  # Import the Child model from your children app

class Attendance(models.Model):
    # Attendance status choices
    PRESENT = 'P'
    ABSENT  = 'A'
    LATE    = 'L'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PRESENT)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.child.name} on {self.date}: {self.get_status_display()}"
