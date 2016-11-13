from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
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
    template = loader.get_template('checkouts/new.html')
    context = RequestContext(
        request, {
            'client_token': client_token,
        }
    )
    return HttpResponse(template.render(context))
