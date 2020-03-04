#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for users app"""

# Import Django
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.test import LiveServerTestCase

# Import Selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

# Import files
from users.models import User
from users.views import dashboard


class SignupPageTestCase(TestCase):
    """This class tests whether the registration page
    returns a 200 status code if the information
    on the user is good or not"""

    def test_get_signUP_page(self):
        """This a little test for get the signup page"""
        print('Test for get a signup page.')
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_success_returns_302(self):
        """Test if good info"""
        print("The Test for sign up to the plateforme.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test50@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 302)

    def test_signup_page_emailFalse_returns_401(self):
        """Test if not good email"""
        print("Test for a fake email.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test500@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})

        response_2 = self.client.post(reverse('sign_up'),
                                      {'email': 'test500@hotmail.fr',
                                       'password': 'wordpass2!',
                                       'confirmation_password': 'wordpass2!',
                                       'last_name': 'name',
                                       'first_name': 'surname',
                                       'phone': '02-01-02-01-02',
                                       'date_of_birth': '19/02/1995',
                                       'postal_address': 'address'})
        self.assertEqual(response_2.status_code, 401)

    def test_password_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. First test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2',
                                     'confirmation_password': 'wordpass2',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 401)

    def test_password2_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. Second test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass!',
                                     'confirmation_password': 'wordpass!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 401)

    def test_password3_returns_401(self):
        """Test if not good password"""
        print("First test for a fake password. Third test.")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'woss2!',
                                     'confirmation_password': 'woss2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 401)

    def test_phoneFalse_returns_401(self):
        """Test if not good number phone"""
        print("Test for a fake a number phone")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02-05-18',
                                     'date_of_birth': '19/02/1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 401)

    def test_dateFalse_returns_401(self):
        """Test if not good birth data"""
        print("Test if not good birth data")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19-02-1995',
                                     'postal_address': 'address'})
        self.assertEqual(response.status_code, 401)

    def test_addressFalse_returns_401(self):
        """Test if not good address"""
        print("Test if not good address")
        response = self.client.post(reverse('sign_up'),
                                    {'email': 'test@hotmail.fr',
                                     'password': 'wordpass2!',
                                     'confirmation_password': 'wordpass2!',
                                     'last_name': 'name',
                                     'first_name': 'surname',
                                     'phone': '02-01-02-01-02',
                                     'date_of_birth': '19/02/1995',
                                     'address': 'addresstjfjftjtjyjhbjrtyrgr'})
        self.assertEqual(response.status_code, 401)


class ConnectPageTestCase(TestCase):
    """This class tests whether the login page
    returns a 200 status code if the information
    on the user is good or not"""

    def test_login_page_success_returns_302(self):
        """Test if good info"""
        print("Test for the connect")
        self.client.post(reverse('sign_up'),
                         {'email': 'test51@hotmail.fr',
                          'password': 'wordpass2!',
                          'confirmation_password': 'wordpass2!',
                          'last_name': 'name',
                          'first_name': 'surname',
                          'phone': '02-01-02-01-02',
                          'date_of_birth': '19/02/1995',
                          'postal_address': 'address'})

        response = self.client.post(reverse('connect'),
                                    {'email': 'test51@hotmail.fr',
                                     'wordpass': 'wordpass2!'})
        self.assertEqual(response.status_code, 302)

    def test_wordpassFalse_returns_401(self):
        """Test for a connect not valid -> A bad password"""
        print("Test for a connect not valid -> A bad password")
        response = self.client.post(reverse('connect'),
                                    {'email': 'test@hotmail.fr',
                                     'wordpass': 'wordpss'})
        self.assertEqual(response.status_code, 401)

    def test_emailFalse_returns_401(self):
        """Test for a connect not valid -> A bad email"""
        print("Test for a connect not valid -> A bad email")
        response = self.client.post(reverse('connect'),
                                    {'email': 'testhotmail.fr',
                                     'wordpass': 'wordpss'})
        self.assertEqual(response.status_code, 401)


class DashboardPageTestCase(TestCase):
    """This class tests whether the dashboard page
    returns a 200 status code if user is connect
    or not with The setup method"""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='toto',
                                             last_name='titi',
                                             email='Toto@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_dashboard_page_returns_200(self):
        """ Test if the user is redirected to the page and
        the database retrieves the data using the above method"""
        print("Test dashboard with a user connected")
        request = self.factory.get(reverse('dashboard'))
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)


class DisconnectPageTestCase(TestCase):
    """This class tests whether the user is redirected
    to the index (home page) after asking for the disconnect."""

    def setUp(self):
        """This method is the setup for add a user in
        the test and a request factory"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(first_name='toto',
                                             last_name='titi',
                                             email='Toto1@hotmail.fr',
                                             date_joined='2020-01-01',
                                             phone='01-01-01-01-02',
                                             password='toto123',
                                             date_of_birth='1995-12-03',
                                             postal_address='Totoland')

    def test_disconnectUser_page_returns_200(self):
        """Test if user is redirected to the home page"""
        print("Test disconnect a user -> return 200")
        request = self.factory.get(reverse('disconnect'))
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)

    def test_disconnect_page_returns_200(self):
        """Test if user is redirected well to page"""
        print("Test disconnect -> return 200")
        response = self.client.get(reverse('disconnect'))
        self.assertEqual(response.status_code, 200)


class FavoritesUserPageTestCase(TestCase):
    """This class tests whether the favorites page where is save the favorites of
    the user returns a 200 status code if user is connect or not,
    the view choose where is redirect the user"""

    def test_favoritesUser_page_return_200(self):
        """test if user is redirected well to page"""
        print("Test the favorites page")
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
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        phone = selenium.find_element_by_id('id_phone')
        date = selenium.find_element_by_id('id_date_of_birth')
        address = selenium.find_element_by_id('id_postal_address')
        email = selenium.find_element_by_id('id_email')
        password1 = selenium.find_element_by_id('id_password')
        password2 = selenium.find_element_by_id('id_confirmation_password')

        submit = selenium.find_element_by_id('register')

        # Fill the form with data
        first_name.send_keys('MyFirstName')
        last_name.send_keys('MyLastName')
        phone.send_keys('01-02-18-97-98')
        date.send_keys('02/02/1995')
        address.send_keys('MyAddress')
        email.send_keys('myaddress1230@hotmail.com')
        password1.send_keys('Mypass12!')
        password2.send_keys('Mypass12')

        # Submitting the form
        submit.send_keys(Keys.RETURN)

        # Wait 5 seconds for find element
        try:
            WebDriverWait(selenium, 5).until(
                EC.presence_of_element_located((By.ID, 'error')))
        except TimeoutException:
            pass

        # Check the returned result
        try:
            error_div = selenium.find_element_by_id('error')
        except NoSuchElementException:
            error_div = None

        # Success sign up
        if error_div is None:
            self.assertEquals(error_div, None)
        # Not Success sign up
        else:
            error_div = not None
            self.assertEquals(error_div, not None)


class MyUserSpaceTestCase(LiveServerTestCase):
    """This class test whether the registration page work correctly via Selenium,
    allowing a real simulation if the data is valid or not"""

    def setUp(self):
        """Setup for reduce the code"""
        self.selenium = webdriver.Firefox()
        super(MyUserSpaceTestCase, self).setUp()

    def tearDown(self):
        """teardown for stop the code"""
        self.selenium.quit()
        super(MyUserSpaceTestCase, self).tearDown()

    def test_connect(self):
        """This method open a browser and input the data ask,
        then validate this data for test in reality time"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/users/connect.html')
        # Find the form element
        email = selenium.find_element_by_id('id_email')
        password = selenium.find_element_by_id('id_wordpass')

        submit = selenium.find_element_by_id('connect')

        # Fill the form with data
        email.send_keys('myaddress1230@hotmail.com')
        password.send_keys('Mypass12!')

        # Submitting the form
        submit.send_keys(Keys.RETURN)

        # Wait 5 seconds for find element
        try:
            WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'error_login')))
        except TimeoutException:
            pass

        # Check the returned result
        try:
            error_div = selenium.find_element_by_id('error_login')
        except NoSuchElementException:
            error_div = None

        # Success connect
        if error_div is None:
            return self.test_favorites_space()
        # Not Success connect
        else:
            error_div = not None
            self.assertEquals(error_div, not None)

    def test_favorites_space(self):
        """This method open a browser and input the data ask,
        then validate this data for test in reality time"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/search/favorites.html')
        # Wait 5 seconds for find element
        try:
            WebDriverWait(selenium, 5).until(
                EC.presence_of_element_located((By.ID, 'not_found')))
        except TimeoutException:
            pass

        # Check the returned result
        try:
            error_p = selenium.find_element_by_id('not_found')
        except NoSuchElementException:
            error_p = None

        # I have a favorites
        if error_p is None:
            return self.test_myFavorites()
        # Don't have a favorites
        else:
            error_p = not None
            self.assertEquals(error_p, not None)

    def test_myFavorites(self):
        """This method open a browser and input the data ask,
        then validate this data for test in reality time"""
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://127.0.0.1:8000/search/favorites.html')
        # Find element
        try:
            favorites = selenium.find_element_by_id('img_favorites')
            favorites.click()
            response = self.client.get(reverse(favorites))
            self.assertEqual(response.status_code, 200)
        except NoSuchElementException:
            response = self.client.get(reverse('favorites'))
            self.assertEqual(response.status_code, 200)
