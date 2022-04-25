from django import forms
from .models import User, UserProfile


class RequestNewVerificationEmail(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(RequestNewVerificationEmail, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', ]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdate, self).__init__(*args, **kwargs)


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender']

    def __init__(self, *args, **kwargs):
        super(UserUpdate, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control input-rounded'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control input-rounded'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control input-rounded'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control input-rounded'})
