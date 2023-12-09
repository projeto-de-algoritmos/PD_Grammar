from django import forms


class TextCheckForm(forms.Form):
    word = forms.RegexField(regex=r'\b[A-Za-z]+\b',
                            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                            label='',
                            required=True,
                            error_messages={'invalid': 'Por favor, insira apenas letras'})

    gap_cost = forms.IntegerField(min_value=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                  max_value=100,
                                  label='',
                                  required=True,
                                  initial=4,
                                  error_messages={'invalid': 'O custo do gap deve ser maior ou igual a 1'})

    max_diff = forms.IntegerField(min_value=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                  max_value=100,
                                  label='',
                                  required=True,
                                  initial=12,
                                  error_messages={'invalid': 'A distância máxima entre as palavras deve ser maior ou igual a 1'})


class AddWordForm(forms.Form):
    new_word = forms.RegexField(regex=r'[A-Za-z]+$',
                            widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
                            label='',
                            required=False,
                            error_messages={'invalid': 'Por favor, insira apenas letras'},)