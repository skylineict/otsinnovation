# views.py
from django.conf import settings
from django.http import JsonResponse
import requests

def debug_banks(request):
    try:
        response = requests.get(
            f'{settings.FLUTTERWAVE_BASE_URL}/banks/NG',
            headers={'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'}
        )
        response_data = response.json()
        if response.status_code == 200 and response_data.get('status') == 'success':
            # Filter for three-digit bank codes
            filtered_banks = [
                bank for bank in response_data.get('data', [])
                if len(bank['code']) == 3 and bank['code'].isdigit()
            ]
            return JsonResponse({'banks': filtered_banks})
        return JsonResponse({'error': response_data.get('message', 'Failed to fetch banks')}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)