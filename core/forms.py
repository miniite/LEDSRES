from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    region = forms.ChoiceField(choices=[('North Malabar', 'North Malabar'), ('North', 'North'), ('Central', 'Central'), ('South', 'South')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'region')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user, region=self.cleaned_data['region'])
            user_profile.save()
        return user
    

# forms.py in your 'core' app


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # This fetches the custom user model
        fields = ('email', 'name', 'password1', 'password2', 'region', 'parent_company')

    def save(self, commit=True):
        user = super().save(commit=False)
                                                        # FOR FUTURE USE ONLY :Where to do any additional processing, like saving the user to the database                      
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
                                                        # FOR FUTURE USE ONLY :Post-save operations can be done here, like sending a welcome email
        return user
