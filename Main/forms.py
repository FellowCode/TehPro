from django import forms
from Main.models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        exclude = ['id']
        model = Material
