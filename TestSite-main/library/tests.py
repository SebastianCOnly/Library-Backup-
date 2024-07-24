# Documentation for pytest-django: https://pytest-django.readthedocs.io/en/latest/index.html
# Marking test functions in Pytest: https://docs.pytest.org/en/stable/how-to/mark.html

import pytest
import uuid

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Functionality Testing

# Custom fixtures

# Generate a password as a string literal
@pytest.fixture
def fakePassword():
   return 'myPass1234'

# Creates a fake user
@pytest.fixture
def createUser(db, django_user_model, fakePassword):
   
   def generateUser(**kwargs):
       kwargs['password'] = fakePassword

       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())

       return django_user_model.objects.create_user(**kwargs)
   return generateUser

# Checks if valid user account creation & login is valid for regular patrons
@pytest.mark.django_db # Requesting database access
def test_user_authorized(client, createUser):
    name = createUser(name='realPatron') # Username
    url = reverse('user-detail-view', kwargs={'pk': name.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'realPatron' in response.content

