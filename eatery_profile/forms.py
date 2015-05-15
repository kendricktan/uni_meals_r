from django import forms

# Search query form
class search_form(forms.Form):
    query = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'What?', 'class': 'form-control'}))
    nearby = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Where?', 'class': 'form-control'}))
    
    