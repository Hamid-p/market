from django import forms



class ContactUsForm(forms.Form):
    fullName = forms.CharField(
        label= 'نام کامل',
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'})
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='پیام شما',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )