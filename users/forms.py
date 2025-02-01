# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ContactMessage

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']  # Forma maydonlari
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ismingiz"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Email manzilingiz"}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Muammo yoki so‘rovingizni yozing", 'rows': 3}),
        }
