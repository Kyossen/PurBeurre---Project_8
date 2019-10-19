#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for users app"""

# Import Django
from django.urls import reverse
from django.test import TestCase


class SignupPageTestCase(TestCase):
    """This class tests whether the registration page
    returns a 200 status code if the information
    on the user is good or not"""

    def test_signup_page_success_returns_200(self):
        """Test if good info"""
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpass',
                                     'wordpass_2': 'wordpass',
                                     'name': 'name',
                                     'surname': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_b': '19/02/1995',
                                     'address': 'address'})
        self.assertEqual(response.status_code, 200)

    def test_signup_page_notSuccess_returns_200(self):
        """Test if not good info"""
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpass',
                                     'wordpass_2': 'wordpass2',
                                     'name': 'name',
                                     'surname': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_b': '19/02/1995',
                                     'address': 'address'})
        self.assertEqual(response.status_code, 200)


class ConnectPageTestCase(TestCase):
    """This class tests whether the login page
    returns a 200 status code if the information
    on the user is good or not"""

    def test_login_page_success_returns_200(self):
        """Test if good info"""
        response = self.client.post(reverse('connect'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpass'})
        self.assertEqual(response.status_code, 200)

    def test_login_page_notSuccess_returns_200(self):
        """Test if food is find"""
        response = self.client.post(reverse('connect'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpass'})
        self.assertEqual(response.status_code, 200)


class DashboardPageTestCase(TestCase):
    """This class tests whether the dashboard page
    returns a 200 status code if user is connect or not,
    the view choose where is redirect the user"""

    def test_dashboard_page_returns_200(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class FavoritesUserPageTestCase(TestCase):
    """This class tests whether the favorites page where is save the favorites of
    the user returns a 200 status code if user is connect or not,
    the view choose where is redirect the user"""
    def test_favoritesUser_page_return_200(self):
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
