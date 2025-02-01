from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_redirect, name='home'),  # Asosiy sahifa (home) yo'naltirish
    path('users/', include('users.urls')),  # Foydalanuvchilar uchun URL yo'nalishlari
    path('courses/', include('courses.urls')),  # Kurslar uchun URL yo'nalishlari
    path('accounts/', include('django.contrib.auth.urls')),  # Tizimga kirish/chiqish uchun URL
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # Tilni o‘zgartirish

]

# Media fayllar uchun sozlash
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
