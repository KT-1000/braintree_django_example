from django import forms


class PaymentForm(forms.Form):
    amount = forms.FloatField(label='Amount', max_value=9999999.99)
    payment_method_nonce = forms.CharField(max_length=100)
