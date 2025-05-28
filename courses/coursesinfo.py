from venv import logger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from decimal import Decimal
import uuid
import requests
from .virtual_account import create_virtual_account


from django.views import View
from .models import PaymentDetail, CourseRegistration, Transaction

  # Valid bank codes for Flutterwave's /v3/charges?type=bank_transfer in test mode
# VALID_BANK_CODES = ['035', '232', '101', '057', '070', '090360']

class PaymentDetailView(LoginRequiredMixin, View):
    login_url = 'login'
  

    def get(self, request, registration_id):
        """
        Render the payment form with course and payment details, filtering banks to three-digit codes.
        """
        registration = get_object_or_404(CourseRegistration, id=registration_id, user=request.user)
        payment_detail, created = PaymentDetail.objects.get_or_create(registration=registration)

        remaining_amount = payment_detail.remaining_amount
        total_amount = registration.course.amount  
        first_payment_amount = total_amount * Decimal('0.5')
        formatted_amount = first_payment_amount.quantize(Decimal('0.00'))

        # Fetch supported banks from Flutterwave
        banks = []
        try:
            response = requests.get(
                'https://api.flutterwave.com/v3/banks/NG',
                headers={'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'}
            )
           
                # Filter banks to include only those with three-digit codes
            banks = [
                bank for bank in response.json().get('data', [])
                if bank['code'] == '035'
            ]
            additional_banks = [
                {'code': '232', 'name': 'Sterling Bank'},
                {'code': '101', 'name': 'Providus Bank'},
                {'code': '057', 'name': 'Zenith Bank'},
                {'code': '070', 'name': 'Fidelity Bank'},
                {'code': '090360', 'name': 'VFD Microfinance Bank'}
            ]
            banks.extend(additional_banks)
            logger.debug(f"Supported bank codes for bank transfer: {banks}")
            print(f"Supported bank codes for bank transfer: {banks}")
                

            logger.debug(f"Filtered banks with three-digit codes: {[f'{bank['code']}: {bank['name']}' for bank in banks]}")
            if not banks:
                    logger.warning("No banks with three-digit codes found.")
                    messages.error(request, 'No supported banks available. Please try another payment method.')
            else:
                logger.error(f"Failed to fetch banks: {response.json().get('message', 'Unknown error')}")
                messages.error(request, 'Failed to fetch bank list. Please try again later.')
        except Exception as e:
            logger.error(f"Error fetching banks: {str(e)}")
            messages.error(request, f'Failed to fetch bank list: {str(e)}')

        context = {
            'registration': registration,
            'payment_detail': payment_detail,
            'remaining_amount': remaining_amount,
            'flutterwave_public_key': settings.FLUTTERWAVE_PUBLIC_KEY,
            'customer_email': request.user.email,
            'first_payment_amount': formatted_amount,
            'banks': banks,
        }



        return render(request, 'dashboard/coursespage/cousesinfo.html', context=context)
    def post(self, request, registration_id):
        """
        Process payment form submission.
        """
        registration = get_object_or_404(CourseRegistration, id=registration_id, user=request.user)
        payment_detail = PaymentDetail.objects.get(registration=registration)

        payment_option = request.POST.get('paymentOption')
        payment_method = request.POST.get('paymentMethod')
        bank_code = request.POST.get('bankCode')  # For bank transfer
        amount_to_pay_str = request.POST.get('amountToPay', '').replace('₦', '').replace(',', '').strip()
        print(f"welcome this is my bank code: {bank_code}")
      

        if not payment_option or not payment_method or not amount_to_pay_str:
            return JsonResponse({'error': "All fields are required."}, status=400)
      
        # Validate payment method

        if payment_method == 'bank' and not bank_code:
            return JsonResponse({'error': "Bank selection is required for bank transfer."}, status=400)
        
        # # Validate bank_code for bank transfer
        # if payment_method == 'bank' and bank_code not in VALID_BANK_CODES:
        #     return JsonResponse({'error': f"Invalid bank code. Please select a supported bank."}, status=400)

        try:
            payment_option_raw = float(payment_option)
        except ValueError:
            return JsonResponse({'error': "Invalid payment option format."}, status=400)

        full_amount = float(registration.course.amount)
        half_amount = round(full_amount * 0.5, 2)

        if round(payment_option_raw, 2) not in [round(full_amount, 2), round(half_amount, 2)]:
            return JsonResponse({'error': "Invalid payment option selected."}, status=400)

        if payment_method not in ['bank', 'auto']:
            return JsonResponse({'error': "Invalid payment method selected."}, status=400)

        try:
            amount_to_pay = Decimal(amount_to_pay_str)
            if amount_to_pay <= 0:
                raise ValueError("Amount to pay must be greater than zero.")
        except (ValueError, TypeError):
            return JsonResponse({'error': "Invalid amount entered."}, status=400)

        model_payment_option = 'installment' if payment_option_raw == half_amount else 'full'
        model_payment_method = 'bank_transfer' if payment_method == 'bank' else 'flutterwave'

        try:
            if not payment_detail.payment_option:
                payment_detail.set_payment_option(model_payment_option)

            if model_payment_option == 'full':
                if amount_to_pay != payment_detail.remaining_amount:
                    raise ValidationError("Full payment must cover the entire remaining amount.")
            elif model_payment_option == 'installment':
                expected_amount = (registration.course.amount * Decimal('0.5')).quantize(Decimal('0.01'))
                if amount_to_pay != expected_amount:
                    raise ValidationError(f"Installment payment must be ₦{expected_amount}.")

            tx_ref = f"TXN-{uuid.uuid4().hex[:10]}"
            virtual_account_result = create_virtual_account(
                request.user, registration, amount_to_pay, tx_ref, bank_code, payment_method
            )
            if not virtual_account_result['success']:
                return JsonResponse({'error': f"Failed to create virtual account: {virtual_account_result['error']}"}, status=400)

            payment_detail.virtual_account_number = virtual_account_result['account_number']
            payment_detail.virtual_account_bank = virtual_account_result['bank']
            payment_detail.virtual_account_name = virtual_account_result['account_name']
            payment_detail.save()

            payment_detail.update_payment(
                payment_amount=amount_to_pay,
                transaction_reference=tx_ref,
                method=model_payment_method,
                status='pending',
                notes=f"{model_payment_method.title()} payment for {model_payment_option} payment"
            )

            if model_payment_method == 'bank_transfer':
                return JsonResponse({
                    'success': True,
                    'data': {
                        'payment_id': payment_detail.id,
                        'amount': float(amount_to_pay),
                        'account_number': payment_detail.virtual_account_number,
                        'account_bank': payment_detail.virtual_account_bank,
                        'account_name': payment_detail.virtual_account_name,
                        'account_expiration': virtual_account_result.get('account_expiration'),
                        'mode': virtual_account_result.get('mode', 'banktransfer')
                    }
                })
            else:  # flutterwave
                return JsonResponse({
                    'success': True,
                    'data': {
                        'payment_id': payment_detail.id,
                        'amount': float(amount_to_pay),
                        'tx_ref': tx_ref,
                        'public_key': settings.FLUTTERWAVE_PUBLIC_KEY,
                        'customer_email': request.user.email,
                        'customer_name': registration.full_name,
                        'course_name': registration.course.name,
                        'virtual_account_number': payment_detail.virtual_account_number,
                        'virtual_account_bank': payment_detail.virtual_account_bank,
                        'virtual_account_name': payment_detail.virtual_account_name,
                        'account_expiration': virtual_account_result.get('account_expiration'),
                        'mode': virtual_account_result.get('mode', 'virtualaccount')

                    }
                })

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        
    

        