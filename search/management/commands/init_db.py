#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""


# Import lib
from json import JSONDecodeError

import requests

# Import file
from search.models import Categories, Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """This class use a one method only for the imports in the database.
    This imports are the imports of the products and categories
    such category name or product name"""
    help = "Carries out my custom admin function"

    def handle(self, *args, **options):
        list_total_products = []
        total_products = int()
        result = requests.get("https://fr.openfoodfacts.org/categories.json")
        response = result.json()
        i = 0
        a = 0
        while i != len(response['tags']):
            new_categories = Categories(name=response['tags'][i]['name'],
                                        url=response['tags'][i]['url'])
            list_total_products.append(int(response['tags'][i]['products']))
            total_products = sum(list_total_products)
            i += 1
            new_categories.save()

        while a != total_products:
            print(total_products)
            all_Categories = Categories.objects.all()
            for save_products in all_Categories:
                result_products = requests.get(save_products.url + ".json")
                try:
                    response_products = result_products.json()
                except JSONDecodeError:
                    continue
                for save in response_products['products']:
                    if 'id' in save:
                        id_s = requests.get(
                            "https://world.openfoodfacts.org/api/v0/product/" +
                            save['id'] + ".json")
                        id_r = id_s.json()

                        if 'product' in id_r:
                            save = id_r['product']
                            if 'product_name' in save:
                                pass
                            if 'product_name' not in save:
                                save['product_name'] = ''
                            if 'nutrition_grades' in save:
                                pass
                            if 'nutrition_grades' not in save:
                                save['nutrition_grades'] = ''
                            if 'image_url' in save:
                                pass
                            if 'image_url' not in save:
                                save['image_url'] = ''
                            if 'ingredients_text_fr' in save:
                                save['ingredients_text_fr'] = \
                                    save['ingredients_text_fr']
                            if 'ingredients_text_fr' not in save:
                                save['ingredients_text_fr'] = ''

                            if save['id'] not in all_Categories:
                                Categories_id = \
                                    Categories.objects.get(pk=save_products.pk)

                                url = "https://fr.openfoodfacts.org/" \
                                      "product/" + save['id'] + "/" + \
                                      save['product_name']

                                a += 1
                                new_products = Product(
                                    name=save['product_name'],
                                    image_url=save['image_url'],
                                    code=save['id'],
                                    nutrition_grade=save['nutrition_grades'],
                                    ingredients=save['ingredients_text_fr'],
                                    url=url,
                                    categories=Categories_id)
                                new_products.save()
