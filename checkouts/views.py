from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PaymentForm
import braintree


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


def index(request):
    return HttpResponseRedirect(reverse('new_checkout'))


def new_checkout(request):
    client_token = braintree.ClientToken.generate()
    return render(request, 'checkouts/new.html', {'client_token': client_token})


def create_checkout(request):
    # process the payment form data
    if request.method == 'POST':
        form = PaymentForm(request.POST)

        if form.is_valid():
            result = braintree.Transaction.sale({
                'amount': str(form.cleaned_data['amount']),
                'payment_method_nonce': str(form.cleaned_data['payment_method_nonce']),
                'options': {
                    "submit_for_settlement": True
                }
            })
            if result.is_success or result.transaction:
                url = reverse('show_checkout', kwargs={'transaction_id': result.transaction.id})
                return HttpResponseRedirect(url)
            else:
                for x in result.errors.deep_errors:
                    messages.add_message(request, messages.INFO, 'Error: %s: %s' % (x.code, x.message))
                return HttpResponseRedirect(reverse('new_checkout'))


def show_checkout(request, transaction_id):
    transaction = braintree.Transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render(request, 'checkouts/show.html', {'transaction': transaction, 'result': result})
