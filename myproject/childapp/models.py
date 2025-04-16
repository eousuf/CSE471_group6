
# Create your models here.
from django.db import models

class Child(models.Model):
    name = models.CharField(max_length=100)
    # add other relevant fields (e.g., age, class, etc.)

    def __str__(self):
        return self.name

class CheckInOut(models.Model):
    CHECKIN = 'IN'
    CHECKOUT = 'OUT'
    STATUS_CHOICES = [
        (CHECKIN, 'Check In'),
        (CHECKOUT, 'Check Out'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='records')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.child.name} - {self.status} at {self.timestamp}"


class ChildAssignment(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='assignments')
    assignment_detail = models.TextField()
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Assignment for {self.child.name}"
