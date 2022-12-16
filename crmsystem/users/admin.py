from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''Admin model for User'''
    list_display = [
        'user',
        'email',
        'phone',
        'role',
    ]
    list_display_links = ['user']
    list_filter = ['role']
    fieldsets = (
        (None, {'fields':
            ('last_name', 'first_name',
            'middle_name', 'phone',
            'email', 'role',)
        }),
    )


    def user(self, obj):
        return obj
