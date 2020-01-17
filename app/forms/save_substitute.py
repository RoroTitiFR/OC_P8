from django import forms


class SaveSubstituteForm(forms.Form):
    product_code = forms.CharField(required=True)
    substitute_code = forms.CharField(required=True)
