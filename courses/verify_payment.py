from django.http import JsonResponse
from decimal import Decimal
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import PaymentDetail

@csrf_exempt
def verify_payment(request, payment_id):
    """
    Verify payment via Flutterwave API and return JSON response only.
    """
    payment_detail = get_object_or_404(PaymentDetail, id=payment_id)
    latest_transaction = payment_detail.transactions.latest('transaction_date')

    try:
        response = requests.get(
            f'https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={latest_transaction.transaction_reference}',
            headers={'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'}
        )

        if response.status_code == 200:
            data = response.json().get('data', {})
            if data.get('status') == 'successful':
                payment_detail.update_payment(
                    payment_amount=Decimal(data.get('amount')),
                    transaction_reference=latest_transaction.transaction_reference,
                    method=latest_transaction.method,
                    status='approved',
                    notes=f"Verified {latest_transaction.method} payment"
                )
                return JsonResponse({
                    'message': 'Payment verified successfully.',
                    'status': 'success',
                    'redirect_url': '/my-courses/'  # change this to your actual URL or use reverse()
                })

            return JsonResponse({
                'error': 'Payment verification failed.',
                'status': 'failed',
                'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
            }, status=400)

        return JsonResponse({
            'error': 'Invalid response from payment gateway.',
            'status': 'failed',
            'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'error': f'Verification error: {str(e)}',
            'status': 'error',
            'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
        }, status=500)
