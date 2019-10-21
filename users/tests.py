#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for users app"""

# Import Django

from django.urls import reverse
from django.test import TestCase
from django.test import LiveServerTestCase

# Import Selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


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


class SignupTestCase(LiveServerTestCase):
    """This class test whether the registration page work correctly via Selenium,
    allowing a real simulation if the data is valid or not"""

    def setUp(self):
        """Setup for reduce the code"""
        self.selenium = webdriver.Firefox()
        super(SignupTestCase, self).setUp()

    def tearDown(self):
        """teardown for stop the code"""
        self.selenium.quit()
        super(SignupTestCase, self).tearDown()

    def test_register(self):
        """This method open a browser and input the data ask,
        then validate this data for test in reality time"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/users/sign_up.html')
        # Find the form element
        first_name = selenium.find_element_by_id('id_surname')
        last_name = selenium.find_element_by_id('id_name')
        phone = selenium.find_element_by_id('id_phone')
        date = selenium.find_element_by_id('id_date_of_birth')
        address = selenium.find_element_by_id('id_postal_address')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_wordpass')
        password2 = selenium.find_element_by_id('id_wordpass_2')

        submit = selenium.find_element_by_id('register')

        # Fill the form with data
        first_name.send_keys('MyFirstName')
        last_name.send_keys('MyLastName')
        phone.send_keys('01-02-18-97-98')
        date.send_keys('02/02/1995')
        address.send_keys('MyAddress')
        email.send_keys('mytestaddress@hotmail.com')
        password1.send_keys('Mypass12!')
        password2.send_keys('Mypass12!')

        # Submitting the form
        submit.send_keys(Keys.RETURN)

        # Wait 5 seconds for find element
        try:
            WebDriverWait(selenium, 5).until(EC.presence_of_element_located((By.ID, 'error')))
        except TimeoutException:
            pass

        # Check the returned result
        try:
            error_div = selenium.find_element_by_id('error')
        except NoSuchElementException:
            error_div = None
        print(error_div)
        self.assertEquals(error_div, None)
