# Documentation for pytest-django: https://pytest-django.readthedocs.io/en/latest/index.html
# Marking test functions in Pytest: https://docs.pytest.org/en/stable/how-to/mark.html
import pytest
import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Functionality Testing

""" Bug report as of 7/24: When returning books, user cannot return 
    all books they have checkout. Sometimes, there will be leftover books 
    checked out on account even if user has selected to return all their
    books. """

# Custom fixtures

# Assigns a dummy password as a string literal
@pytest.fixture
def dummyPassword():
   return 'myPass1234'

# Our dummy user's full name is Buttermilk the Cat
@pytest.fixture
def dummyFullName():
  return 'Buttermilk the Cat'

# Creates a dummy user account for testing purposes
@pytest.fixture
def createUser(db, django_user_model, dummyPassword, dummyFullName):
   
   # Generating user data
   def generateUser(**kwargs):
       kwargs['full_name'] = dummyFullName
       kwargs['password1'] = dummyPassword
       kwargs['password2'] = dummyPassword

       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       
       return django_user_model.objects.create_user(**kwargs)
   
   return generateUser

# Checks if valid user account creation & login is valid for regular patrons
@pytest.mark.django_db # Requesting database access
def test_user_authorized(client, createUser):
    ##