# Documentation for pytest-django: https://pytest-django.readthedocs.io/en/latest/index.html
# Marking test functions in Pytest: https://docs.pytest.org/en/stable/how-to/mark.html

import pytest
import uuid

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Functionality Testing

# Checks if valid user account creation & login is valid for regular patrons
@pytest.mark.django_db # Requesting database access
def test_user_authorized(client, createUser):
    ##

