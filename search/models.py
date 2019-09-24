from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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
