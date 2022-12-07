from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=150,
        blank=False,
        null=False
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        blank=False,
        null=False,
        unique=True
    )
