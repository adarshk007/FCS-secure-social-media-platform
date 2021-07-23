from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

# admin.site.register(Account)

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'first_name', 'last_name', 'phone_no', 'date_joined', 'last_login', 'is_casual_user', 'is_premium_user', 'is_commercial_user', 'is_verified', 'is_admin', 'is_staff', 'is_active', 'premium_type')
	search_fields = ('email', 'username')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)