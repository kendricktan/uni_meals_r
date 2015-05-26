from django import forms

# Search query form
class search_form(forms.Form):
    query = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'What? (Restaurant, food, specials...)', 'class': 'form-control'}))
    location = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'required': '', 'placeholder': 'Where? (Postal code, city, suburb...)', 'class': 'form-control'}))
    
    