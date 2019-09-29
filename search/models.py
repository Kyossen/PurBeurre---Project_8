"""
This import is obligatory for the good of the system
"""

from django.db import models
from django.contrib.auth.models import User

"""
This below, the all models of the platform
"""


"""
The first model is the model Account
She create a foreign key on the User table
This key is used to add objects (such as a phone number)
    to the user in the User table.
"""


class Account(models.Model):
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


"""
The second model is the model Substitution
It also create a foreign key on the User table
This key is used to add a substitution
This substitution is used to find which user has registered a product
Thus, a user can register a product in this table
    to display it in these favorite products
"""


class Substitution(models.Model):
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

    class Meta:
        managed = True
        db_table = "Substitution"
        ordering = ['id']
