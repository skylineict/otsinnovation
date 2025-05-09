from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import uuid
import requests
from django.views import View
from .models import PaymentDetail, CourseRegistration, Transaction


@csrf_exempt
def flutterwave_webhook(request):
    """
    Handle Flutterwave webhook for payment completion.
    """
    if request.method == 'POST':
        try:
            payload = request.json()
            if payload.get('event') == 'charge.completed' and payload['data']['status'] == 'successful':
                tx_ref = payload['data']['tx_ref']
                payment_detail = PaymentDetail.objects.get(flutterwave_ref=tx_ref)
                payment_detail.update_payment(
                    payment_amount=Decimal(payload['data']['amount']),
                    transaction_reference=tx_ref,
                    method=payload['data']['payment_type'],
                    status='approved',
                    notes=f"Webhook-verified {payload['data']['payment_type']} payment"
                )
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=400)
    return HttpResponse(status=405)