from django.contrib import admin

from orders.models import Loader, PayMethod


@admin.register(PayMethod)
class PayMethodAdmin(admin.ModelAdmin):
    list_display = ['pay_method',]


@admin.register(Loader)
class LoaderAdmin(admin.ModelAdmin):
    '''Admin model for Loader'''
    list_display = [
        'user',
        'area',
        'phone',
    ]
    list_display_links = ['user',]
    list_filter = ['area']
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
                'passport_birthplace'
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
