from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'lastname', 'firstname', 'uid_number']
    list_display = ('username', 'lastname', 'firstname', 'uid_number')
