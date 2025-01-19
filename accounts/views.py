from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    
    This view handles user registration with comprehensive error handling
    and validation of all required fields.
    """
    
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {
                    'message': _('User registered successfully.'),
                    'user': UserSerializer(user, context=self.get_serializer_context()).data
                },
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {
                    'error': _('Validation error'),
                    'detail': str(e),
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Get the error details from the serializer if available
            if hasattr(serializer, 'errors'):
                error_detail = serializer.errors
            else:
                error_detail = str(e)
                
            # Format the error response
            error_response = {
                'error': _('Registration failed'),
                'detail': error_detail
            }
            
            # If there are field-specific errors, include them
            if isinstance(error_detail, dict):
                error_response.update(error_detail)
            
            return Response(
                error_response,
                status=status.HTTP_400_BAD_REQUEST
            )

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    
    This view allows authenticated users to view and update their profile
    information with proper validation.
    """
    
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {
                    'message': _('Profile updated successfully.'),
                    'user': UserUpdateSerializer(user, context=self.get_serializer_context()).data
                }
            )
        except ValidationError as e:
            return Response(
                {
                    'error': _('Validation error'),
                    'detail': str(e),
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            error_detail = serializer.errors if hasattr(serializer, 'errors') else str(e)
            return Response(
                {
                    'error': _('Profile update failed'),
                    'detail': error_detail
                },
                status=status.HTTP_400_BAD_REQUEST
            )
