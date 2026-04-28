from django import forms
from .models import CustomUser
from departments.models import Department


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','department','password']

    def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
                raise forms.ValidationError("Password do not match")
            return cleaned_data
