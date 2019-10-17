#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some models of the platform for users app"""

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    """The first model is the model Account
    She create a foreign key on the User table
    This key is used to add objects (such as a phone number)
    to the user in the User table."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="User",
                             default=None,
                             null=False)
    phone = models.CharField(max_length=17,
                             default=None,
                             null=False)
    date_of_birth = models.DateField(default=None,
                                     null=False)
    postal_address = models.CharField(max_length=25,
                                      default=None,
                                      null=False)

    class Meta:
        managed = True
        db_table = "Account"
        ordering = ['id']


class Substitution(models.Model):
    """The second model is the model Substitution
    It also create a foreign key on the User table
    This key is used to add a substitution"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="Account",
                             default=None,
                             null=False)
    product = models.CharField(max_length=255,
                               default=None,
                               null=False)
    nutrition_grade = models.CharField(max_length=2,
                                       default=None,
                                       null=False)
    img_url = models.CharField(max_length=255,
                               default=None,
                               null=False)
    code = models.CharField(max_length=255,
                            default=None,
                            null=False)

    class Meta:
        managed = True
        db_table = "Substitution"
        ordering = ['id']
