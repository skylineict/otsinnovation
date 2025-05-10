from django.http import JsonResponse
from decimal import Decimal
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import logging
import re

from .models import PaymentDetail

logger = logging.getLogger(__name__)

@csrf_exempt
def verify_payment(request, payment_id):
    logger.debug(f"Received verify_payment request for payment_id: {payment_id}, user: {request.user}, method: {request.method}")

    # Validate payment_id format
    if not payment_id or not isinstance(payment_id, str) or not re.match(r'^[a-z0-9]{22}$', payment_id):
        logger.error(f"Invalid payment_id: {payment_id}, type={type(payment_id)}, length={len(payment_id) if isinstance(payment_id, str) else 'N/A'}")
        return JsonResponse({
            'error': 'Invalid payment ID format.',
            'status': 'error',
            'redirect_url': '/dashboard/'
        }, status=400)

    try:
        payment_detail = get_object_or_404(PaymentDetail, id=payment_id, registration__user=request.user)
        logger.debug(f"Found PaymentDetail: id={payment_detail.id}, registration={payment_detail.registration.id}")
        try:
            latest_transaction = payment_detail.transactions.latest('transaction_date')
            logger.debug(f"Latest transaction: ref={latest_transaction.transaction_reference}, method={latest_transaction.method}")
        except payment_detail.transactions.model.DoesNotExist:
            logger.error(f"No transactions found for PaymentDetail: {payment_id}")
            return JsonResponse({
                'error': 'No transaction associated with this payment.',
                'status': 'error',
                'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
            }, status=400)
    except PaymentDetail.DoesNotExist:
        logger.error(f"PaymentDetail not found for payment_id: {payment_id}, user: {request.user}")
        return JsonResponse({
            'error': 'Invalid payment reference or unauthorized access.',
            'status': 'error',
            'redirect_url': '/dashboard/'
        }, status=403)

    try:
        response = requests.get(
            f'https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={latest_transaction.transaction_reference}',
            headers={'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'}
        )

        logger.debug(f"Flutterwave API response: status={response.status_code}, body={response.text}")

        if response.status_code != 200:
            logger.error(f"Flutterwave API error: status={response.status_code}, response={response.text}")
            return JsonResponse({
                'error': f'Invalid response from payment gateway: {response.status_code} {response.text}',
                'status': 'failed',
                'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
            }, status=400)

        data = response.json().get('data', {})
        transaction_status = data.get('status', '').lower()

        if transaction_status == 'successful':
            payment_detail.update_payment(
                payment_amount=Decimal(data.get('amount', '0')),
                transaction_reference=latest_transaction.transaction_reference,
                method=latest_transaction.method,
                status='approved',
                notes=f"Verified {latest_transaction.method} payment"
            )
            return JsonResponse({
                'message': 'Payment verified successfully.',
                'status': 'success',
                'redirect_url': ''
            })

        elif transaction_status == 'pending':
            return JsonResponse({
                'message': 'Payment is still pending. Please check again later.',
                'status': 'pending',
                'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
            })

        else:
            logger.error(f"Payment verification failed: status={transaction_status}, data={data}")
            return JsonResponse({
                'error': f'Payment verification failed: {transaction_status or "Unknown status"}',
                'status': 'failed',
                'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
            }, status=400)

    except Exception as e:
        logger.error(f"Error verifying transaction {latest_transaction.transaction_reference}: {str(e)}")
        return JsonResponse({
            'error': f'Verification error: {str(e)}',
            'status': 'error',
            'redirect_url': f'/payment-form/{payment_detail.registration.id}/'
        }, status=500)