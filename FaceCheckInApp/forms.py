from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser  # Ensure this is the correct import
from .models import Enrollment


class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'First Name'
        }),
        max_length=30, required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Last Name'
        }),
        max_length=30, required=True
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Username'
        }),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Email'
        }),
        max_length=254, required=True, help_text='Required. Inform a valid email address.')

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Phone Number'
        }),
        max_length=15, required=False
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Password'
        }),
        required=True
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Confirm Password'
        }),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('photo1', 'photo2', 'photo3')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Username'
        }),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            'placeholder': 'Enter Password'
        }),
        required=True
    )
