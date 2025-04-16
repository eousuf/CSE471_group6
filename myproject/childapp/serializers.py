from rest_framework import serializers
from .models import Child, CheckInOut, ChildAssignment

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'

class CheckInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInOut
        fields = '__all__'

class ChildAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildAssignment
        fields = '__all__'
