from django.contrib import admin

from orders.models import Loader, PayMethod, KindOfWork, Status, Counteragent, ContactCounterAgent, Contactperson


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['status',]
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(PayMethod)
class PayMethodAdmin(admin.ModelAdmin):
    list_display = ['pay_method',]
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(KindOfWork)
class KindOfWorkAdmin(admin.ModelAdmin):
    list_display = ['kind_of_work',]
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ContactsInLine(admin.TabularInline):
    model = Counteragent.contacts.through
    extra = 0
    min_num = 1
    list_display = ('fio', 'phone')


@admin.register(Contactperson)
class ContactpersonAdmin(admin.ModelAdmin):
    fields = ('fio', 'post', 'email', 'phone')
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

@admin.register(Loader)
class LoaderAdmin(admin.ModelAdmin):
    '''Admin model for Loader'''
    list_display = [
        'user',
        'area',
        'phone',
    ]
    list_display_links = ['user',]
    list_filter = ['area', 'status']
    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
                'middle_name',
                'phone',
                'whatsapp',
                'photo',
                'area',
                'kind_of_work',
                'status',
                'referer',
            ),
        }),
        ('Паспортные данные', {
            'classes': ('collapse',),
            'fields': (
                'passport_serial',
                'passport_number',
                'passport_given_by',
                'passport_givendate',
                'passport_first_name',
                'passport_last_name',
                'passport_middle_name',
                'passport_birthday',
                'passport_birthplace',
                'passport_address',
                'passport_photo_main',
                'passport_photo_address'
            ),
        }),
        ('Платежные данные', {
            'classes': ('collapse',),
            'fields': (
                'pay_method',
                'pay_requisites',
                'bank',
                'pay_comments',
            ),
        }),
    )

    def user(self, obj):
        return obj


@admin.register(Counteragent)
class CounterAgentLegal(admin.ModelAdmin):
    list_display = [
        'short_name',
        'type'
    ]
    list_display_links = ['short_name']
    list_filter = ['type']
    fieldsets = (
        (None, {
            'fields': (
                'type',
                'legal_name',
                'short_name',
                'kind_of_work'
            ),
        }),
        ('Реквизиты', {
            'classes': ('collapse',),
            'fields': (
                'inn',
                'kpp',
                'legal_address',
                'actual_address',
                'payment_account',
                'correspondent_account',
                'bik',
                'bank',
            ),
        }),
    )
    inlines = (
        ContactsInLine,
    )
