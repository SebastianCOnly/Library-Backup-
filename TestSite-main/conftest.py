## Contains configuration settings for Pytest ##

import pytest
import uuid

from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection

client = Client()
"""
pytest_plugins = ('TestSite-main.testsupport.pytest-progress',
                  'TestSite-main.testsupport.pytest-django', 
                  'TestSite-main.testsupport.pytest-pikachu') # Optional surprised pikachu face when tests succeed
"""

# Custom fixtures

# Enables database access to all tests without
# the need to invoke '@pytest.mark.django_db'
@pytest.fixture
def enable_db_access_for_all_tests(db):
    pass

'''
# Assigns a dummy password for the user
@pytest.fixture(scope='class')
def dummyPassword():
   return 'myPass1234'

# Assigns a dummy full name to the user
@pytest.fixture(scope='class')
def dummyFullName():
  return 'Buttermilk Ragdoll'

# Assigns a dummy email address
@pytest.fixture(scope='class')
def dummyEmail():
   return 'thisIsReal@CSUFmail.com'

# Creates a dummy user account for testing purposes
@pytest.fixture
def createUser(django_user_model, dummyPassword, dummyFullName, dummyEmail):
   
   # Generating user data
   def generateUser(**kwargs):
       kwargs['full_name'] = dummyFullName
       #kwargs['password1'] = dummyPassword
       #kwargs['password2'] = dummyPassword
       kwargs['password'] = dummyPassword
       kwargs['email'] = dummyEmail

       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       
       return django_user_model.objects.create_user(**kwargs)
   
   return generateUser

'''