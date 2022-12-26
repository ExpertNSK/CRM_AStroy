from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password

from crmsystem.settings import USER_ROLE_CHOICE


class UserManager(BaseUserManager):
    '''Custom User manager'''
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Адрес электронной почты asdasdasd обязателен!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        role = extra_fields.get('role')
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''Custom User Model'''
    objects = UserManager()
    username = None
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
    middle_name = models.CharField(
        'Отчество',
        max_length=150,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    phone = PhoneNumberField(
        'Номер телефона',
        blank=False,
        null=False,
        unique=True
    )
    role = models.PositiveIntegerField(
        'Роль',
        blank=False,
        null=False,
        choices=USER_ROLE_CHOICE,
        default=3
    )
    USERNAME_FIELD = ('phone')
    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
    ]

    @property
    def is_admin(self):
        return (
            self.role == 1
            or
            self.is_superuser
        )
    
    @property
    def is_staff(self):
        return (
            self.role == 2
            or
            self.is_admin
        )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return (
            f'{self.last_name} {self.first_name} {self.middle_name} - '
            f'({str(self.phone)[-4:-2]}-{str(self.phone)[-2:]})'
        )
    
    def save(self, *args, **kwargs):
        user = super(User, self)
        user.set_password(self.password)
        user.save(*args, **kwargs)
        return super(User, self)


class Course(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
