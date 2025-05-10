import logging
import requests
from django.conf import settings
logger = logging.getLogger(__name__)

def create_virtual_account(user, registration, amount, tx_ref, bank_code=None, payment_method='auto'):
    """
    Create a virtual account via Flutterwave API based on payment method.
    - For 'bank', use /v3/charges?type=bank_transfer with bank_code.
    - For 'auto', use /v3/virtual-account-numbers without bank_code.
    """
    logger.info(f"Creating virtual account for {payment_method} with bank_code: {bank_code}")
    try:
        if not user.email:
            return {'success': False, 'error': 'Email is missing from user profile.'}

        # NEW: Prepare payload with common fields
        payload = {
            "tx_ref": tx_ref,
            "amount": float(amount),
            "currency": "NGN",
            "email": user.email,
            "fullname": registration.full_name,
            "phone_number": user.phone,
            "narration": registration.full_name,
        }

        # NEW: Select endpoint based on payment_method
        endpoint = 'https://api.flutterwave.com/v3/virtual-account-numbers'
        if payment_method == 'bank':
            endpoint = 'https://api.flutterwave.com/v3/charges?type=bank_transfer'
            if bank_code:
                payload["bank_code"] = bank_code

        # NEW: Make API call to the selected endpoint
        logger.debug(f"Payload: {payload}")
        response = requests.post(
            endpoint,
            headers={
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload
        )

        print(response.json())  # For debugging
        logger.debug(f"Response: {response.status_code}, {response.text}")

        # NEW: Handle response, accounting for differences in endpoint response structures
        if response.status_code == 200 and response.json().get('status') == 'success':
            response_data = response.json()
            account_number = None
            bank_name = None
            account_name = f"OTS  {registration.full_name}"
            account_expiration = None 
            mode = None  

            if payment_method == 'bank':
                # NEW: Parse bank transfer response from meta.authorization
                authorization = response_data.get('meta', {}).get('authorization', {})
                account_number = authorization.get('transfer_account')
                bank_name = authorization.get('transfer_bank')
                account_name = authorization.get('full_name', account_name)
                account_expiration = authorization.get('account_expiration')
                mode = authorization.get('mode')
            else:
                # NEW: Parse virtual account response from data
                data = response_data.get('data', {})
                account_number = data.get('account_number')
                bank_name = data.get('bank_name', 'Flutterwave')
                account_name = data.get('account_name', account_name)
                account_expiration = data.get('expiry_date')
                mode = 'virtualaccount'

            if not account_number or not bank_name:
                return {
                    'success': False,
                    'error': 'Missing account number or bank name in response'
                }

            result = {
                'success': True,
                'account_number': account_number,
                'bank': bank_name,
                'account_name': account_name,
                'mode': mode
            }
            if account_expiration:
                result['account_expiration'] = account_expiration
            return result
        

        return {
            'success': False,
            'error': response_data.get('message', 'Failed to create virtual account')
        }
    except Exception as e:
        # NEW: Log exceptions for live mode
        # Purpose: Capture any errors during live API calls for troubleshooting.
        logger.error(f"Error creating virtual account in live mode: {str(e)}")
        return {'success': False, 'error': str(e)}