from django.db import models
from django.conf import settings  # to reference the user model

class Child(models.Model):
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='children'
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    medical_history = models.TextField(blank=True, null=True)
    emergency_contacts = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} (Age: {self.age})"
