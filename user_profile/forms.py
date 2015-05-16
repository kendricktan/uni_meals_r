from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from models import *

# Form for registration
class register_form(forms.ModelForm):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Username', 'class': 'form-control input-sm'}))
    email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Email', 'class': 'form-control input-sm'}))
    re_email = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Re-enter email', 'class': 'form-control input-sm'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'required': '', 'placeholder': 'Password', 'class': 'form-control input-sm'}))
    re_password= forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'required': '', 'placeholder': 'Re-enter password', 'class': 'form-control input-sm'}))
    
    # Meta class
    class Meta:
        model = user_profile
        fields = ['username', 'email', 're_email', 'password', 're_password']
        
    # Checks if there's any account with similar username/email
    def check_exists(self, request):        
        # If it passes the check then there is an account with the same details
        # Checks if there's any account with a similar name
        try:
            user_profile.objects.get(username=request.POST['username'])
            return 'username'
            
        except Exception:
            pass
            
        # Checks if there's any account with a similar email
        try:
            user_profile.objects.get(email=request.POST['email'])
            return 'email'
        
        except Exception:
            pass                    
        
    # Saves form and creates a user
    def save(self):                   
        user = super(register_form, self).save()                        
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.save()                     

# Form to login        
class login_form(forms.ModelForm):
    identifier = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Username/Email', 'class': 'form-control input-sm'}))
    password = forms.CharField(max_length=100, label='', widget=forms.PasswordInput(attrs={'required': '', 'placeholder': 'Password', 'class': 'form-control input-sm'}))
    
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
                pass
            
        # Authenticate and Log user in
        _u = authenticate(username=username, password=password)
        
        if _u is not None:
            if _u.is_active:
                auth_login(request, _u)
                return True
        
        return False
        
# Form to edit profile display picture
class profile_edit_dp_form(forms.Form):
    new_dp = forms.ImageField(label='')
    
# Form to edit profile description
class profile_edit_info_form(forms.Form):
    new_location = forms.CharField(max_length=40, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter new location', 'class': 'profile-edit-input-textbox'}))
    new_description = forms.CharField(max_length=255, label='', widget=forms.Textarea(attrs={'placeholder': 'Enter new description', 'class': 'profile-edit-input-textarea'}))
    
# Form to edit user password
class profile_edit_password_form(forms.Form):
    new_password = forms.CharField(max_length=25, label='', widget=forms.PasswordInput(attrs={'required': '', 'placeholder': 'Password', 'class': 'profile-edit-input-textbox'}))
    new_re_password = forms.CharField(max_length=25, label='', widget=forms.PasswordInput(attrs={'required': '', 'placeholder': 'Re-enter Password', 'class': 'profile-edit-input-textbox'}))