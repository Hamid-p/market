from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError
from django import forms

from account.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email=forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ["email", "password", "is_active", "is_admin"]

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password", "fullname", "phone" ,"address" , "image"]


class RegisterForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your username'}),
        validators=[
            validators.MaxLengthValidator(limit_value=20, message='نام کاربری نباید بیش از 20 کاراکتر باشد!')
        ]
    )

    email = forms.EmailField(required=False,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'enter your email'}),
                             validators=[
                                 validators.EmailValidator('ایمیل نامعتبر است!')
                             ]
                             )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your passowrd'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 're-enter your passowrd'})
    )

    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        query = User.objects.filter(username=userName)

        if query.exists():
            raise forms.ValidationError('this username is not available')
        return userName

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            query = User.objects.filter(email=email)

            if query.exists():
                raise forms.ValidationError('this email is already exist')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('passwords do not match')

        return data
