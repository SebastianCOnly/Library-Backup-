# Official_LMS/library/account_creation.py
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormWithFullName(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'password1', 'password2')
