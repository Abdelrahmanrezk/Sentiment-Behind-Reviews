from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact_us


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
    # def clean(self):
    # 	email = self.cleaned_data.get('username')
    # 	current_emails = User.objects.filter(email=email)
    # 	if current_emails.exists():
    # 		raise forms.ValidationError("That email is taken")

class Contact_us_form(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = ['first_name', 'mail', 'phonenumber', 'message']
