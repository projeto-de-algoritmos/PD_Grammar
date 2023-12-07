from django import forms
from django.core.validators import RegexValidator


class TextCheckForm(forms.Form):
    word = forms.RegexField(
                            regex=r"\b[A-Za-z]+\b",
                            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), 
                            label='', 
                            required=False, 
                            error_messages={'invalid': 'Por favor, insira apenas letras'})
