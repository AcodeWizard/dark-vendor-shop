from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import VendorTerm
from .forms import UserAdminCreationForm, UserAdminChangeForm


User = get_user_model()

# Register your models here.

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to ADD and CHANGE user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'admin', 'staff', 'vendor', 'is_active', 'timestamp', 'updated')
    list_filter = ('admin', 'staff', 'vendor', 'is_active')
    list_editable = ('is_active', 'vendor')
    fieldsets = (
        ('Standard info', {'fields': ('username', 'password')}),
        ('Other info', {'fields': ('pgp_key', 'level', )}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active', 'vendor')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'password1', 'password2')}
         ),
    )
    search_fields = ('username',)
    ordering = ('pk',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register( VendorTerm)

