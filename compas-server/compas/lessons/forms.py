from .models import Users
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegistrationForm(forms.ModelForm): #добавить валидацию сложности пароля
    password = forms.CharField(
        label='Введите пароль',
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Users
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if (password and password2) and password != password2:
            raise ValidationError('Пароли должны совпадать')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def save(self, commit=True):
        user = super().save(commit=False) #создает объект User в памяти но не в БД (обращение к родительскому классу)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    password = forms.CharField(
        label='Password',
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Users
