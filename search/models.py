# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some models of the platform for search app"""

from django.db import models


class Categories(models.Model):
    """This table allows of group the category and product
    tables in database and manage of the categories in database."""
    name = models.CharField(max_length=255)
    url = models.TextField()

    class Meta:
        managed = True
        db_table = "Categories"
        ordering = ['id']


class Product(models.Model):
    """This table can handle the data of products with the category table"""
    image_url = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    code = models.CharField(max_length=255, default='')
    nutrition_grade = models.CharField(max_length=255, default='')
    ingredients = models.TextField(default='')
    url = models.TextField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE,
                                   related_name="products")

    class Meta:
        managed = True
        db_table = "Products"
        ordering = ['id']
