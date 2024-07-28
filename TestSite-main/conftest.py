## Contains configuration settings for Pytest ##

import pytest

from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
from typing import Dict
from unittest.mock import Mock, patch

client = Client()

# Custom fixtures

# Enables database access for all tests without the need to invoke '@pytest.mark.django_db'
@pytest.fixture
def enable_db_access_for_all_tests(db):
    pass

# Creates a dummy user for testing purposes
@pytest.fixture
def user(django_user_model):
    username = 'ButtermilkUser'
    password = 'myPass1234'
    emailAddr = 'realEmailHere@CSUFakeMail.com'
    dummyUser = django_user_model.objects.create_user(
                                                 username=username, 
                                                 password=password,
                                                 email=emailAddr)
    return dummyUser

@pytest.fixture
def titleOne():
    return 'The Lightning Thief'

@pytest.fixture
def titleTwo():
    return 'riordan'
