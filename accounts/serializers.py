from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration and detail view.
    
    This serializer handles user registration with proper validation
    for all required fields including password confirmation.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email',
                 'first_name', 'last_name', 'user_type', 'phone_number', 'address')
        extra_kwargs = {
            'first_name': {'required': True, 'error_messages': {
                'required': _('First name is required.')
            }},
            'last_name': {'required': True, 'error_messages': {
                'required': _('Last name is required.')
            }},
            'email': {'required': True, 'error_messages': {
                'required': _('Email address is required.')
            }},
            'username': {'error_messages': {
                'required': _('Username is required.'),
                'unique': _('A user with this username already exists.')
            }}
        }

    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('A user with this email already exists.'))
        return value

    def validate_phone_number(self, value):
        """Validate phone number format."""
        if value and not value.replace('+', '').isdigit():
            raise serializers.ValidationError(_('Phone number can only contain digits and + symbol.'))
        return value

    def validate(self, attrs):
        """Validate password match and user type."""
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({
                'password': _("Password fields didn't match.")
            })
            
        if attrs.get('user_type') not in dict(User.USER_TYPE_CHOICES):
            raise serializers.ValidationError({
                'user_type': _('Invalid user type selected.')
            })
            
        return attrs

    def create(self, validated_data):
        """Create new user with validated data."""
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                user_type=validated_data.get('user_type', 'customer'),
                phone_number=validated_data.get('phone_number', ''),
                address=validated_data.get('address', '')
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    
    This serializer handles updating user details while ensuring
    proper validation of the updated fields.
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False}
        }

    def validate_email(self, value):
        """Validate email uniqueness on update."""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(_('A user with this email already exists.'))
        return value

    def validate_phone_number(self, value):
        """Validate phone number format."""
        if value and not value.replace('+', '').isdigit():
            raise serializers.ValidationError(_('Phone number can only contain digits and + symbol.'))
        return value
