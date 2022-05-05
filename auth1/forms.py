from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import RegisterUser

class RegistrationForm(UserCreationForm):

    name = forms.CharField(max_length=100, help_text="Enter name")
    email = forms.EmailField(max_length=200, help_text="Enter a valid email address.")
    contact_number = forms.CharField(max_length=15, help_text="Enter valid phone number")
    date_of_birth = forms.DateField(help_text="Enter valid phone Birth date")
    
    class Meta:
        model = RegisterUser
        # widgets = {
        #     'password1': forms.PasswordInput(),
        #     'password2': forms.PasswordInput(),
        #    }
        fields = ['username', 'name', 'email', 'contact_number', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        self.fields['contact_number'].widget.input_type = 'number'
        self.fields['date_of_birth'].widget.input_type = 'date'

class LoginForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = RegisterUser
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
        else:
            raise forms.ValidationError("Invalid Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = RegisterUser
        fields = {'email', 'username', 'name', 'contact_number', 'address', 'date_of_birth', 'nid', 'blood_group'}

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                registeruser = RegisterUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except RegisterUser.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use' % registeruser.email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                registeruser = RegisterUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except RegisterUser.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use' % registeruser.username)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field, in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        self.fields['date_of_birth'].widget.input_type = 'date'
        self.fields['contact_number'].widget.input_type = 'number'
        self.fields['nid'].widget.input_type = 'number'

