from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Lug'atdan berilgan kalitga mos qiymatni qaytaradi.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(str(key))  # Kalitni string sifatida tekshirish
    return None

@register.filter
def dict_get(dictionary, key):
    try:
        return dictionary.get(key, None)
    except AttributeError:
        return None