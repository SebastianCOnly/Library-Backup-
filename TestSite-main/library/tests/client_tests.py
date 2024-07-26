# Documentation for pytest-django: https://pytest-django.readthedocs.io/en/latest/index.html
# Marking test functions in Pytest: https://docs.pytest.org/en/stable/how-to/mark.html

import pytest
from django.urls import reverse

# Functionality Testing
"""

This file tests the client while logged in as a patron (Regular user)
or as a library employee (Admin account)."""

""" Bug report as of 7/24: When returning books, user cannot return 
    all books they have checkout. Sometimes, there will be leftover books 
    checked out on account even if user has selected to return all their
    books. """

# Tests client view of home page while user is logged in
def test_regular_user_view(client, user):
    
    client.force_login(user)
    response = client.get('') # The home page is labeled as '' in urls.py
    
    assert response.status_code == 200

# Tests client view as an admin user
def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    
    assert response.status_code == 200

# Add item to empty cart
def test_add_to_bag(client, user):
    client.force_login(user)

    url = reverse('add_to_cart', 
                  kwargs={'book_id': 1})

    response = client.get(url)

    assert response.status_code == 200
    assert 'ButtermilkUser' in response.content
