## Contains configuration settings for Pytest ##

import pytest

from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection

client = Client()

# Custom fixtures

# Enables database access to all tests without
# the need to invoke '@pytest.mark.django_db'
@pytest.fixture
def enable_db_access_for_all_tests(db):
    pass

@pytest.fixture
def user(django_user_model):
    username = "ButtermilkUser"
    password = "myPass1234"
    dummyUser = django_user_model.objects.create_user(username=username, 
                                                 password=password)
    return dummyUser