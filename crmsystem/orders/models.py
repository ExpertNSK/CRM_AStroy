from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class PayMethod(models.Model):
    pay_method = models.CharField(
        'Тип оплаты',
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['pay_method']
        verbose_name = 'Тип оплаты'
        verbose_name_plural = 'Тип оплаты'
    
    def __str__(self):
        return f'{self.pay_method}'


class Loader(models.Model):
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False,
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=150,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        'Номер телефона',
        unique=True,
        blank=False,
        null=False,
    )
    whatsapp = PhoneNumberField(
        'Телефон для whatsapp',
        unique=True,
        blank=True,
        null=False,
    )
    photo = models.ImageField(
        'Фото',
        upload_to='photo/loader/',
        blank=True,
    )
    area = models.CharField(
        'Район проживания',
        max_length=150,
        blank=False,
        null=False,
    )
    create_date = models.DateField(
        'Дата приема',
        auto_now_add=True,
    )
    first_job_date = models.DateField(
        'Дата первого выхода',
        default=None,
        blank=True,
        null=True,
    )
    referer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='loaders',
        verbose_name='Пригласил',
        blank=True,
        null=True,
    )
    passport_serial = models.PositiveIntegerField(
        'Серия паспорта',
        blank=True,
        null=True,
    )
    passport_number = models.PositiveIntegerField(
        'Номер паспорта',
        blank=True,
        null=True,
    )
    passport_given_by = models.CharField(
        'Кем выдан',
        help_text='Как в паспорте',
        max_length=200,
        blank=True,
        null=True,
    )
    passport_givendate = models.DateField(
        'Когда выдан',
        blank=True,
        null=True
    )
    passport_first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Как в паспорте',
        blank=True,
        null=True,
    )
    passport_last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Как в паспорте',
        blank=True,
        null=True,
    )
    passport_middle_name = models.CharField(
        'Отчество',
        max_length=150,
        help_text='Как в паспорте',
        blank=True,
        null=True,
    )
    passport_birthday = models.DateField(
        'День рождения',
        blank=True,
        null=True,
    )
    passport_birthplace = models.CharField(
        'Место рождения',
        help_text='Как в паспорте',
        max_length=50,
        blank=True,
        null=True
    )
    pay_method = models.ForeignKey(
        PayMethod,
        on_delete=models.CASCADE,
        related_name='loaders',
        verbose_name='Тип оплаты',
        blank=True,
        null=True
    )
    pay_requisites = models.CharField(
        'Реквизиты оплаты',
        max_length=150,
        help_text='Номер карты/счета/телефона',
        blank=True,
        null=True
    )
    bank = models.CharField(
        'Банк',
        max_length=150,
        blank=True,
        null=True
    )
    pay_comments = models.TextField(
        'Комментарии к оплате',
        max_length=500,
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Грузчик'
        verbose_name_plural = 'Грузчики'
        ordering = ['last_name']
    
    def __str__(self):
        return (
            f'{self.last_name} {self.first_name} {self.middle_name}'
        )
    
    def save(self):

        if not User.objects.filter(phone=self.phone).exists():
            fake_email = f'{self.phone}@email.ru'
            User.objects.create(
                last_name=self.last_name,
                first_name=self.first_name,
                middle_name=self.middle_name,
                email=fake_email,
                phone=self.phone,
            )
        else:
            if self.phone == self.referer.phone:
                raise ValidationError('Реферал не может пригласить сам себя!')
        if not self.whatsapp:
            self.whatsapp = self.phone
        return super(Loader, self).save()
