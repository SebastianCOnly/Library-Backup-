# Documentation for pytest-django: https://pytest-django.readthedocs.io/en/latest/index.html
# Marking test functions in Pytest: https://docs.pytest.org/en/stable/how-to/mark.html

import pytest

from django.test import TestCase
from django.contrib.auth.models import User

# Functionality Testing

# Checks if valid user account creation & login is valid
@pytest.mark.django_db # Requesting database access
def test_user_account_valid():
    # WORDS
