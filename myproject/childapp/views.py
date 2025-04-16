from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Child, CheckInOut
from .serializers import CheckInOutSerializer

class CheckInOutView(APIView): 
    def post(self, request, format=None):
       
        serializer = CheckInOutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CheckInOut, ChildAssignment
from .serializers import CheckInOutSerializer, ChildAssignmentSerializer

class AttendanceReportView(APIView):
    def get(self, request, format=None):
       
        checkin_out_records = CheckInOut.objects.all()
        assignments = ChildAssignment.objects.all()
        data = {
            "attendance": CheckInOutSerializer(checkin_out_records, many=True).data,
            "assignments": ChildAssignmentSerializer(assignments, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)
