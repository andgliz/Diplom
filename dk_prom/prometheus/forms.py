from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

Groups = (
    ("1", "Ассорти"),
    ("2", "Радость"),
    ("3", "220 Вольт"),
    ("4", "Наш дом"),
    ("5", "Родничок"),
)


class FirstLessonForm(forms.Form):
    name = forms.CharField(max_length=255, label='Имя')
    surname = forms.CharField(max_length=255, label='Фамилия')
    child_name = forms.CharField(max_length=255, label='Имя ребёнка')
    age = forms.IntegerField(max_value=18, label='Возраст ребёнка')
    mail = forms.EmailField(label='Почта')
    group = forms.ChoiceField(choices=Groups, label='Интересующий коллектив')


class AddEventForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Events
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
        }
    prepopulated_fields = {"slug": ("title",)}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Логин"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Пароль"}))


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'
