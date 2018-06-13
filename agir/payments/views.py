from django.http import Http404, HttpResponseServerError
from django.template.response import TemplateResponse
from django.views.generic import DetailView


from .models import Payment
from .types import PAYMENT_TYPES
from .payment_modes import PAYMENT_MODES


PAYMENT_ID_SESSION_KEY = '_payment_id'


def payment_view(request, ):
    pass


class PaymentView(DetailView):
    queryset = Payment.objects.filter(status=Payment.STATUS_WAITING)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment_mode = PAYMENT_MODES.get(self.object.mode)

        if payment_mode is None:
            return HttpResponseServerError()

        return payment_mode.payment_view(request, payment=self.object, *args, **kwargs)


def return_view(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        raise Http404('Ce paiement n\'existe pas')

    return handle_return(request, payment)


def handle_return(request, payment):
    if payment.type in PAYMENT_TYPES and PAYMENT_TYPES[payment.type].success_view:
        return PAYMENT_TYPES[payment.type].success_view(request, payment=payment)
    else:
        return TemplateResponse(
            request,
            'payments/success.html' if payment.status == payment.STATUS_COMPLETED else 'payments/failure.html',
        )
