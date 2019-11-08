#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the tests
This below, the somes test of the platform for search app"""

# Import Django
from django.urls import reverse
from django.test import TestCase

# Import file
from .models import Product, Categories


class IndexPageTestCase(TestCase):
    """This class tests whether the index
    page returns a 200 status code"""
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class CopyrightPageTestCase(TestCase):
    """This class tests whether the copyright
    page returns a 200 status code"""
    def test_copyright_page(self):
        response = self.client.get(reverse('copyright'))
        self.assertEqual(response.status_code, 200)


class ResultPageTestCase(TestCase):
    """This class tests whether the result page
    returns a 200 status code if a food is found or not"""

    def test_result_find_page_returns_200(self):
        """Test if food is find"""
        categories = Categories.objects.create(name='TestCategories',
                                               url='test')
        categories_id = Categories.objects.get(pk=categories.pk)
        product = Product.objects.create(name='TestProduct',
                                         image_url='image',
                                         code='code',
                                         nutrition_grade='test',
                                         ingredients='test',
                                         url='test', categories=categories_id)
        response = self.client.post(reverse('result'), {'food': product.name})
        self.assertEqual(response.status_code, 200)

    def test_result_page_returns_notExist(self):
        """Test if food not is find or not exist"""
        response = self.client.post(reverse('result'), {'food': 'NotExist'})
        self.assertEqual(response.status_code, 401)


class DescriptionPageTestCase(TestCase):
    """This class tests whether the description page
    returns a status code 200 if a food is found or not
    via its code"""

    def test_description_find_page_returns_200(self):
        """Test with a good code"""
        categories = Categories.objects.create(name='TestCategories',
                                               url='test')
        categories_id = Categories.objects.get(pk=categories.pk)
        product = Product.objects.create(name='TestProduct',
                                         image_url='image',
                                         code='code',
                                         nutrition_grade='test',
                                         ingredients='test',
                                         url='test', categories=categories_id)
        response = self.client.get(reverse('description'),
                                   {'product': product.code})
        self.assertEqual(response.status_code, 200)

    def test_description_page_returns_badCode(self):
        """Test with a bad code"""
        response = self.client.get(reverse('description'),
                                   {'product': 'BadCode'})
        self.assertEqual(response.status_code, 200)


class FavoritesPageTestCase(TestCase):
    """This class tests whether the favorites page returns a status code 200 if a
    food is found or not via its code. this class allow also
    of test if a food is save"""

    def test_Favorites_find_page_returns_200(self):
        """Test with a good code"""
        categories = Categories.objects.create(name='TestCategories',
                                               url='test')
        categories_id = Categories.objects.get(pk=categories.pk)
        product = Product.objects.create(name='TestProduct',
                                         image_url='image',
                                         code='code',
                                         nutrition_grade='test',
                                         ingredients='test',
                                         url='test', categories=categories_id)
        response = self.client.get(reverse('favorites'),
                                   {'product': product.code})
        self.assertEqual(response.status_code, 200)

    def test_favorites_page_returns_badCode(self):
        """Test with a bad code"""
        response = self.client.get(reverse('favorites'),
                                   {'product': 'BadCode'})
        self.assertEqual(response.status_code, 200)



