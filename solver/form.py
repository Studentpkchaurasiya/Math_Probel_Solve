from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import All_account


class Account_creation_form(UserCreationForm):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=12, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    STANDARD_CHOICES = All_account.STANDARD_CHOICES
    standard = forms.ChoiceField(choices=STANDARD_CHOICES)
    
    class Meta:
        model = User
        fields =  ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            All_account.objects.create(
                user=user,
                name = self.cleaned_data['name'],
                address = self.cleaned_data['address'],
                standard = self.cleaned_data['standard'],
                mobile_number=self.cleaned_data['mobile_number']
            )
        return user
        