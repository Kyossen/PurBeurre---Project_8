#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
This below, the some models of the platform for users app"""

# Import Django
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """This class is an override of the 'Create user' of the Django
    This gives us some advantages"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """This method take the data, of the precedent method and
        use this datas for known if user is staff or not"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """This method is exactly same that precedent,
        but she use the data for create a super user"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Below is the override say before
    We us use this class because she allow a
    total control on the class 'Create User'"""
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField('email address', unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone = models.CharField(max_length=17,
                             default=None,
                             null=False)
    date_of_birth = models.DateField(default=None,
                                     null=False)
    postal_address = models.CharField(max_length=25,
                                      default=None,
                                      null=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can '
                    'log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Substitution(models.Model):
    """The second model is the model Substitution
    It also create a foreign key on the User table
    This key is used to add a substitution"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="substitutions",
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
