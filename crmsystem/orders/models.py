from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class Status(models.Model):
    status = models.CharField(
        'Статус',
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['status']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
    
    def __str__(self):
        return f'{self.status}'


class KindOfWork(models.Model):
    kind_of_work = models.CharField(
        'Тип работы',
        max_length=50,
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['kind_of_work']
        verbose_name = 'Тип работ'
        verbose_name_plural = 'Типы работ'
    
    def __str__(self):
        return f'{self.kind_of_work}'


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
    kind_of_work = models.ForeignKey(
        KindOfWork,
        on_delete=models.CASCADE,
        verbose_name='Тип работ',
        default=None,
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name='Статус',
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
    passport_address = models.TextField(
        'Прописка',
        max_length=200,
        blank=True,
        null=True
    )
    passport_photo_main = models.ImageField(
        'Фото главной страницы',
        upload_to='photo/passports/',
        blank=True
    )
    passport_photo_address = models.ImageField(
        'Фото прописки',
        upload_to='photo/passports/',
        blank=True
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
                password='1234567890',
            )
        else:
            if self.phone == self.referer.phone:
                raise ValidationError('Реферал не может пригласить сам себя!')
        if not self.whatsapp:
            self.whatsapp = self.phone
        return super(Loader, self).save()


class Counteragent(models.Model):
    type = models.CharField(
        'Тип контрагента',
        choices=settings.TYPES_COUNTERAGENTS,
        max_length=50,
        blank=False,
        null=False
    )
    legal_name = models.CharField(
        'Юридическое наименование',
        max_length=200,
        unique=True,
        blank=False,
        null=False
    )
    short_name = models.CharField(
        'Краткое наименование',
        max_length=200,
        unique=True,
        blank=False,
        null=False
    )
    inn = models.IntegerField(
        'ИНН',
        unique=True,
        blank=True,
        null=True
    )
    kpp = models.IntegerField(
        'КПП',
        blank=True,
        null=True
    )
    legal_address = models.TextField(
        'Юридический адрес',
        max_length=200,
        blank=True,
        null=True
    )
    actual_address = models.TextField(
        'Фактический адрес',
        max_length=200,
        help_text='Оставьте пустым, если совпадает с юридическим.',
        blank=True,
        null=True
    )
    payment_account = models.IntegerField(
        'Рассчетный счёт',
        blank=True,
        null=True
    )
    correspondent_account = models.IntegerField(
        'Корреспондентский счёт',
        blank=True,
        null=True
    )
    bik = models.IntegerField(
        'БИК',
        blank=True,
        null=True
    )
    bank = models.CharField(
        'Наименование банка',
        max_length=50,
        blank=True,
        null=True
    )
    kind_of_work = models.ForeignKey(
        KindOfWork,
        on_delete=models.CASCADE,
        verbose_name='Виды работ',
        blank=False,
        null=False
    )
    contacts = models.ManyToManyField(
        'Contactperson',
        through='ContactCounterAgent',
        verbose_name='Контактное лицо'
    )

    class Meta:
        ordering = ['short_name']
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'
    
    def __str__(self):
        return f'{self.short_name}'
    

class Contactperson(models.Model):
    fio = models.CharField(
        'Ф.И.О',
        max_length=150,
        blank=False,
        null=False
    )
    post = models.CharField(
        'Должность',
        max_length=50,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=250,
        blank=True,
        null=True
    )
    phone = PhoneNumberField(
        'Номер телефона',
        unique=True,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
    
    def __str__(self):
        return f'{self.post} - {self.fio} тел: {self.phone}'


class ContactCounterAgent(models.Model):
    counteragent = models.ForeignKey(
        Counteragent,
        on_delete=models.CASCADE,
        verbose_name='Контрагент'
    )
    contact_person = models.ForeignKey(
        Contactperson,
        on_delete=models.CASCADE,
        verbose_name='Контактное лицо'
    )

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
