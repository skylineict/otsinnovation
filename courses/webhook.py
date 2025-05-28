from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import logging
import json
from decimal import Decimal
from .models import PaymentDetail, Transaction

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def flutterwave_webhook(request):
 
    # Verify webhook signature
    webhook_secret = 'f93kf0293kd!@#LFSJLsdkfj'
    signature = request.headers.get('verif-hash')

    if not signature:
        return JsonResponse({'error': 'Missing verif-hash header'}, status=403)

    if signature != webhook_secret:
        return JsonResponse({'error': 'Invalid signature'}, status=403)

    try:
        # Parse webhook payload
        payload = json.loads(request.body.decode('utf-8'))
      

        # Extract relevant data
        event = payload.get('event')
        data = payload.get('data', {})
        tx_ref = data.get('tx_ref')
        status = data.get('status', '').lower()
        amount = Decimal(str(data.get('amount', '0')))
        payment_type = data.get('payment_type', 'unknown').lower()

        
        if event != 'charge.completed' or status != 'successful':
            return HttpResponse(status=200)

        # Find PaymentDetail by transaction reference
        payment_detail = get_object_or_404(
            PaymentDetail,
            transactions__transaction_reference=tx_ref
        )

        # Update PaymentDetail
        payment_detail.update_payment(
            payment_amount=amount,
            transaction_reference=tx_ref,
            method='bank_transfer' if payment_type == 'banktransfer' else 'flutterwave',
            status='approved',
            notes=f"Webhook confirmed {payment_type} payment"
        )

        
        return HttpResponse(status=200)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid webhook payload: {e}")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
  
