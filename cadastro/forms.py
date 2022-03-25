from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

import cadastro
from cadastro.models import Conta

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(max_length=60,help_text='Campo obrigatorio!')
    date_of_birth = forms.DateField()

    class Meta:
        model = Conta
        fields = ("email", "username","date_of_birth", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # Se um campo for preenchido automaticamente, mas não o outro
        # nossa validação nem senha ou ambas as senhas serão acionada.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

class AuthenticateContaForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
            model = Conta
            fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Login inválido!")

class ContaUpdateForm(forms.ModelForm):

    class Meta:
            model = Conta
            fields =('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                    cadastro = Conta.objects.exclude(pk=self.instance.pk).get(email=email)
            except Conta.DoesNotExist:
                    return email
            raise forms.ValidationError('O email "%s" já está em uso.' % cadastro)

    def clean_username(self):
            if self.is_valid():
                    username = self.cleaned_data['username']
                    try:
                            cadastro = Conta.objects.exclude(pk=self.instance.pk).get(username=username)
                    except Conta.DoesNotExist:
                            return username
                    raise forms.ValidationError('Username "%s" já esta em uso.' % username)



