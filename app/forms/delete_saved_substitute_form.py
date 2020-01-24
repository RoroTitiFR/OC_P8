from django import forms


class DeleteSavedSubstituteForm(forms.Form):
    product_substitute_id = forms.IntegerField(required=True)
