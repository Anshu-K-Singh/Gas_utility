from rest_framework import serializers
from .models import ServiceRequest, RequestUpdate
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestUpdateSerializer(serializers.ModelSerializer):
    staff_member_name = serializers.SerializerMethodField()

    class Meta:
        model = RequestUpdate
        fields = ('id', 'service_request', 'staff_member', 'staff_member_name', 
                 'comment', 'created_at')
        read_only_fields = ('staff_member',)

    def get_staff_member_name(self, obj):
        return f"{obj.staff_member.first_name} {obj.staff_member.last_name}"

class ServiceRequestSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    updates = RequestUpdateSerializer(many=True, read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = ('id', 'customer', 'customer_name', 'request_type', 'details', 
                 'status', 'created_at', 'updated_at', 'resolved_at', 
                 'attachment', 'updates')
        read_only_fields = ('customer', 'status', 'resolved_at')

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)
