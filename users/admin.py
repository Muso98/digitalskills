from django.contrib import admin
from .models import User, ContactMessage  # Bir nechta modelni import qilish

# Modellarni admin panelida ro'yxatga olish
admin.site.register(User)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')  # Admin panelda ko‘rinadigan ustunlar
    search_fields = ('name', 'email')  # Qidirish imkoniyati
    list_filter = ('created_at',)  # Filtrlash