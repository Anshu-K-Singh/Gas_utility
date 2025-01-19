from django.urls import path
from .views import ServiceRequestListCreateView, ServiceRequestDetailView, RequestUpdateCreateView

urlpatterns = [
    path('requests/', ServiceRequestListCreateView.as_view(), name='service-request-list'),
    path('requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='service-request-detail'),
    path('request-updates/', RequestUpdateCreateView.as_view(), name='request-update-create'),
]
