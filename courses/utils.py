from .models import Settings

def get_max_tests_per_user():
    settings = Settings.objects.first()
    return settings.max_tests_per_user if settings else 10  # Standart qiymat: 10
