from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from models import *

# Form for registration
class register_form(forms.ModelForm):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    re_email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Re-enter email'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    re_password= forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password'}))
    
    # Meta class
    class Meta:
        model = user_profile
        fields = ['username', 'email', 're_email', 'password', 're_password']
        
    # Saves form and creates a user
    def save(self):
        user = super(register_form, self).save()
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()                     
            
        return user
        
class login_form(forms.ModelForm):
    identifier = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username/Email'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = user_profile
        fields = ['identifier', 'password']            
        
    def login(self, request):
        username = self.cleaned_data['identifier']
        identifier = self.cleaned_data['identifier']
        password = self.cleaned_data['password']
        
        # If user used Email to log in
        # we need to extract username and login using username and email combo
        if '@' in identifier:
            try:
                _u = user.objects.get(email=identifier)
                username = _u.get_username()
                
            except Exception as e:
                return False
            
        # Authenticate and Log user in
        _u = authenticate(username=username, password=password)
        
        if _u is not None:
            if _u.is_active:
                auth_login(request, _u)
                return True
        
        return False