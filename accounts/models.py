from django.db import models
from django.contrib.auth.models import AbstractUser

class Parent(AbstractUser):
    # name = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.username
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
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
    