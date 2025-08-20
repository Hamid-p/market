from django import forms
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ["fullName", "email", "message"]
        widgets = {
            "fullName": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "پیام شما"}),
        }
