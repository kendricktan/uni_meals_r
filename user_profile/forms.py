from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from models import *

# Form for registration
class register_form(forms.ModelForm):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control input-sm'}))
    email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control input-sm'}))
    re_email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Re-enter email', 'class': 'form-control input-sm'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control input-sm'}))
    re_password= forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter password', 'class': 'form-control input-sm'}))
    
    # Meta class
    class Meta:
        model = user_profile
        fields = ['username', 'email', 're_email', 'password', 're_password']
        
    # Saves form and creates a user
    def save(self):
        # Checks if there's any account with similar email
        # If it passes the check then there is an account with the same details
        try:
            user.objects.get(email=self.cleaned_data['email'])
            return 'email'
        
        except Exception:
            pass
            
        # Checks if there's any account with a similar name
        try:
            user.objects.get(username=self.cleaned_data['username'])
            return 'username'
            
        except Exception:
            pass
    
        # If it passes that test then it saves the user to the database
        user = super(register_form, self).save()                        
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()                     
            
        return None
        
class login_form(forms.ModelForm):
    identifier = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username/Email', 'class': 'form-control input-sm'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control input-sm'}))
    
    class Meta:
        model = user_profile
        fields = ['identifier', 'password']            
        
    def login(self, request):
        username = self.cleaned_data['identifier']
        identifier = self.cleaned_data['identifier']
        password = self.cleaned_data['password']                
        
        # If user used Email to log in
        # we need to extract username and login using username and email combo
        if '@' in username:
            try:
                # Get email's username
                _u = user_profile.objects.get(email=identifier)
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