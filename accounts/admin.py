from django.contrib import admin
from .models import User, OTP_CODES
# Register your models here.

admin.site.register(User)

class OTPAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

admin.site.register(OTP_CODES, OTPAdmin)