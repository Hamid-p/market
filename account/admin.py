from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from account.models import User
from django import forms


class UserCreationForm(forms.ModelForm):
    """فرم ساخت کاربر جدید در ادمین"""
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تأیید رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'phone', 'address', 'image')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("رمز عبور و تأیید آن یکسان نیستند.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """فرم ویرایش کاربر در ادمین"""

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username', 'fullname', 'email', 'phone', 'address', 'is_admin']
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        ("Personal info", {"fields": ['fullname', 'email', 'phone', 'address', 'image']}),
        ("Permissions", {"fields": ['is_admin', 'is_active']}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ['username', 'fullname', 'email', 'phone', 'address', 'image', 'password1', 'password2', 'is_admin', 'is_active'],
            },
        ),
    ]
    search_fields = ['username', 'email', 'phone']
    ordering = ['username', ]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
