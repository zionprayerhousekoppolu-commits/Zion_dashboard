from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# custom validator to ensure no numbers in language names
def validate_no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('This field cannot contain numbers....')

# Create your models here.
class languageList(models.Model):
    
      # Validation for alphabetic characters only (a-z, A-Z)
    alpha_only = RegexValidator(r'^[a-zA-Z]+$', message = 'This field can only contain alphabetic characters.')
    
    # Valiadtor for alphabetic and spaces
    alpha_space_only = RegexValidator(r'^[a-zA-Z\s]+$', message = 'This field can only contain alphabetic characters and spaces.')
    
    languageCode = models.CharField(
        max_length=10, 
        unique=True,
        validators=[alpha_only, validate_no_numbers], null=True, blank=True 
        )
    
    languages = models.CharField(
        max_length=25, 
        unique=True,
        validators=[validate_no_numbers], null=True, blank=True
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.languages