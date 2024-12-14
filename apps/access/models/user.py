from apps.common.managers import UserManager
from apps.common.model_fields import AppPhoneNumberField, AppSingleChoiceField
from apps.common.models import (
    COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    COMMON_CHAR_FIELD_MAX_LENGTH,
    BaseModel,
)
from django.contrib.auth.models import AbstractUser
from django.db import models

from .config import USER_TITLE_CHOICES
from apps.common.choices import *


class User(BaseModel, AbstractUser):
    """
    User model for the entire application.
    This models holds data other than auth related data.
    Holds information of user.
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    username = None
    email = models.EmailField(unique=True)
    phone_number = AppPhoneNumberField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    password = models.CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    title = AppSingleChoiceField(
        choices_config=USER_TITLE_CHOICES, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )
    first_name = models.CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    last_name = models.CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )


class UserProfile(BaseModel):
    """Ask details from the user to booking the room"""
    name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    age = models.PositiveIntegerField(blank=False, null=False)
    gender = models.CharField(max_length=20, null=False, blank=False, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    address1 = models.TextField(blank=False, null=False)
    
    def __str__(self):
        return self.name
    