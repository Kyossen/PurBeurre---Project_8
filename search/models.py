from django.db import models


# Create your models here.


class Account(models.Model):
    wordpass = models.CharField(max_length=12, null=False)
    email = models.CharField(max_length=25, null=False)
    name = models.CharField(max_length=20, null=False)
    surname = models.CharField(max_length=20, null=False)
    """ For V2:
    phone = models.CharField(max_length=15, null=False)
    date_of_birth = models.DateField()
    Postal_address = models.CharField(max_length=255, null=False)
    """

    class Meta:
        managed = True
        db_table = "Account"
        ordering = ['id']