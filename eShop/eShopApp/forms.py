from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, Product
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
