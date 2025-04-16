from django.urls import path
from .views import mark_attendance, attendance_report

urlpatterns = [
    path('mark/', mark_attendance, name='mark_attendance'),
    path('report/', attendance_report, name='attendance_report'),
]
