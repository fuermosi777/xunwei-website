#-*- coding: UTF-8 -*- 
from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import uuid, os

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("用户名已经存在"),
        'duplicate_email': _("Email已经存在"),
        'password_mismatch': _("两次输入的密码不一致"),
    }
    username = forms.RegexField(label=_("Username"), max_length=30, min_length=6,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
            widget=forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':'用户名（英文字符、数字或下划线）',}))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control','required':'required','placeholder':'请输入密码',}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control','required':'required','placeholder':'请再次输入密码',}),
        help_text=_("Enter the same password as above, for verification."))
    email = forms.CharField(label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control','required':'required','placeholder':'Email',}))
    # the nickname field will go into userprofile table....
    nickname = forms.CharField(label=_("Nickname"),
        widget=forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':'昵称（可填中文）',}))

    class Meta:
        model = User
        fields = ("username","email",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EatenForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'5', 'id':'review','placeholder':'你什么都没写，我看着你呐~','required':'required',}))
    star = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rating','data-max':'5', 'data-min':'1',}))
    CHOICES = [('1','低于$10'),('2','$10-$30'),('3','$30-$50'),('4','$50-$80'),('5','$80+')]
    price = forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'price','value':'',}))

#upload user avatar form-------------------------------------------
class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField()

#settings----------------------------------------------------------
class ChangeBasicForm(forms.Form):
    nickname = forms.CharField(max_length=9,label=_("Nickname"),widget=forms.TextInput(attrs={'class': 'form-control','required':'required','placeholder':'昵称',}))
    introduction = forms.CharField(max_length=50,required=False,widget=forms.Textarea(attrs={'class': 'form-control','rows':'5', 'placeholder':'介绍一下自己',}))

class ChangeAvatarForm(forms.Form):
    avatar = forms.ImageField()

from collections import OrderedDict

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': _("两次输入密码不一致"),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control','required':'required','placeholder':'请输入新密码',}))
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control','required':'required','placeholder':'请再输入一次新密码',}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control','required':'required','placeholder':'请输入旧密码',}))

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)
