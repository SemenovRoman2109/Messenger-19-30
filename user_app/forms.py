from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label= "Пароль",
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Введіть пароль"
        })
    )
    password2 = forms.CharField(
        label= "Підтвердження паролю",
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Підтвердіть пароль"
        })
    )
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            "email" : forms.EmailInput(attrs={
                "placeholder" : "Введіть пошту"
            })
        }
    def clean(self):
        data = super().clean()
        
        pass1 = data.get('password1')
        pass2 = data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(message= 'Паролі не співпадають')
        
        return data
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email= email).exists():
            raise forms.ValidationError(message= 'Пошта вже існує')
        
        return email
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user
    

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label= "Електрона пошта",
        widget = forms.EmailInput(attrs={
            "placeholder" : "Введіть email"
        })
    )
    password = forms.CharField(
        label= "Пароль",
        widget = forms.PasswordInput(attrs={
            "placeholder" : "Введіть пароль"
        })
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('username')
        if password and email:
            self.user_cache = authenticate(self.request, username = email, password = password)
            if not self.user_cache:
                raise forms.ValidationError(message= 'Невірний email або пароль')
            else:
                self.confirm_login_allowed(user = self.user_cache)
        
        return self.cleaned_data
