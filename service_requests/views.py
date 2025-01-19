from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import ServiceRequest, RequestUpdate
from .serializers import ServiceRequestSerializer, RequestUpdateSerializer

class IsSupportRep(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_support_rep()

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_support_rep():
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.filter(customer=user)

class ServiceRequestDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ServiceRequestSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.is_support_rep():
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.filter(customer=user)

    def perform_update(self, serializer):
        instance = self.get_object()
        new_status = self.request.data.get('status')
        
        if new_status and new_status != instance.status:
            if new_status == 'resolved' and instance.status != 'resolved':
                serializer.validated_data['resolved_at'] = timezone.now()
            elif new_status != 'resolved' and instance.status == 'resolved':
                serializer.validated_data['resolved_at'] = None
                
        serializer.save()

class RequestUpdateCreateView(generics.CreateAPIView):
    serializer_class = RequestUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupportRep]

    def perform_create(self, serializer):
        serializer.save(staff_member=self.request.user)
