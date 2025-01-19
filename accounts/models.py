from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model for the Gas Utility Service Request System.
    
    This model extends Django's AbstractUser to include additional fields
    specific to our application's needs.
    
    Attributes:
        user_type (str): Type of user - either 'customer' or 'support'
        phone_number (str): User's contact number
        address (str): User's physical address
    """
    
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('support', 'Support Representative'),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',
        help_text=_('Designates whether this user is a customer or support representative.')
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        help_text=_('Contact phone number')
    )
    address = models.TextField(
        blank=True,
        help_text=_('Physical address')
    )
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def clean(self):
        """
        Custom validation for the User model.
        """
        super().clean()
        if not self.email:
            raise ValidationError({'email': _('Email address is required.')})
        if not self.first_name or not self.last_name:
            raise ValidationError(_('Both first name and last name are required.'))
            
    def save(self, *args, **kwargs):
        """
        Override save method to ensure validation is called.
        """
        self.full_clean()
        super().save(*args, **kwargs)
        
    def is_support_rep(self):
        """
        Check if the user is a support representative.
        
        Returns:
            bool: True if user is a support representative, False otherwise
        """
        return self.user_type == 'support'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"
