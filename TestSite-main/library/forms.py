# Official_LMS/library/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser

# Used for registering new users and includes additional fields such as 'full_name'.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # The form works with the CustomUser model
        fields = ('username', 'full_name', 'email', 'password1', 'password2')  # Fields to be included in the form

# UserUpdateForm is used for updating existing user information.
# It allows users to update their username, email, and full name.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # The form works with the CustomUser model
        fields = ['username', 'email', 'full_name']  # Fields to be included in the form

# CustomPasswordChangeForm extends Django's PasswordChangeForm.
# Used for changing passwords
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the parent class's constructor
        # Apply a 'form-control' CSS class to all form fields for consistent styling
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # Set the placeholder attribute to the field label
