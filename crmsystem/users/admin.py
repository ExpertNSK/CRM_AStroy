from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password

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
            'email', 'password', 'role',)
        }),
    )


    def user(self, obj):
        return obj
    
    def save_model(self, request, obj, form, change):
        user = User.objects.filter(phone=obj.phone).get()
        if not user:
            obj.password = make_password(obj.password)
        else:
            if user.password != obj.password:
                obj.password = make_password(obj.password)
        return super().save_model(request, obj, form, change)


admin.site.unregister(Group)
