from django.urls import path
from .views import CheckInOutView, AttendanceReportView

urlpatterns = [
    path('checkin-out/', CheckInOutView.as_view(), name='checkin-out'),
    path('attendance-report/', AttendanceReportView.as_view(), name='attendance-report'),
]
