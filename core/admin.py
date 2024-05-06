from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Auction, Bid

class UserAdmin(BaseUserAdmin):
    model = UserProfile
    list_display = ['email', 'name', 'region', 'parent_company', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'region', 'parent_company')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Wallet info', {'fields': ('eth_address','private_address')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'region', 'parent_company', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(UserProfile, UserAdmin)

admin.site.register(Auction)
admin.site.register(Bid)