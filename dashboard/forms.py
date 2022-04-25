from django import forms
from .models import Withdraws, Deposits


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraws
        fields = ['wallet_address', 'amount']

    def __init__(self, *args, **kwargs):
        super(WithdrawForm, self).__init__(*args, **kwargs)
        self.fields['wallet_address'].widget.attrs.update({'class': 'form-control input-rounded'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control input-rounded'})


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposits
        fields = ['wallet_address', 'amount']

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['wallet_address'].widget.attrs.update({'class': 'form-control input-rounded'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control input-rounded'})
