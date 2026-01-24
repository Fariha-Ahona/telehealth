from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 border border-violet-300 rounded-lg focus:ring-violet-500 focus:border-violet-500"
        })
    )

    role = forms.ChoiceField(
        choices=[('patient', 'Patient'), ('doctor', 'Doctor')],
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 border border-violet-300 rounded-lg focus:ring-violet-500 focus:border-violet-500"
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-violet-300 rounded-lg focus:ring-violet-500 focus:border-violet-500"
            }),
            'email': forms.EmailInput(attrs={
                "class": "w-full px-3 py-2 border border-violet-300 rounded-lg focus:ring-violet-500 focus:border-violet-500"
            }),
        }

# accounts/forms.py
from django import forms

class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "w-full px-4 py-3 border border-violet-300 rounded-xl focus:ring-violet-500 focus:border-violet-500"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "w-full px-4 py-3 border border-violet-300 rounded-xl focus:ring-violet-500 focus:border-violet-500"
        })
    )
