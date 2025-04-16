
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from children.models import Child
from .models import Attendance
from .forms import AttendanceForm

# Optionally, ensure the user is staff; modify this check as needed.
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def mark_attendance(request):
    today = date.today()
    # Ensure an attendance record exists for each child for today
    for child in Child.objects.all():
        Attendance.objects.get_or_create(child=child, date=today)
    # Get today's attendance records, ordering by child's name.
    queryset = Attendance.objects.filter(date=today).order_by('child__name')
    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)
    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect('attendance_report')
    else:
        formset = AttendanceFormSet(queryset=queryset)
    context = {
        'formset': formset,
        'today': today,
    }
    return render(request, 'attendance/mark_attendance.html', context)




from datetime import timedelta

@login_required
@user_passes_test(is_staff)
def attendance_report(request):
    report_type = request.GET.get('type', 'daily')  # 'daily', 'weekly', or 'monthly'
    today = date.today()
    if report_type == 'daily':
        start_date = today
        end_date = today
    elif report_type == 'weekly':
        start_date = today - timedelta(days=today.weekday())  # Monday
        end_date = start_date + timedelta(days=6)              # Sunday
    elif report_type == 'monthly':
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(day=31)
        else:
            next_month = today.replace(month=today.month+1, day=1)
            end_date = next_month - timedelta(days=1)
    else:
        start_date = today
        end_date = today

    report_attendance = Attendance.objects.filter(date__range=(start_date, end_date)).order_by('date', 'child__name')
    context = {
        'report_attendance': report_attendance,
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'attendance/attendance_report.html', context)
