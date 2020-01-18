import requests

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .utils import genAppSecretProof


def render_login_page(request):
    template_name = 'logindemo/index.html'
    context = {}
    context['app_id'] = settings.ACCOUNT_KIT_APP_ID
    context['api_version'] = settings.ACCOUNT_KIT_API_VERSION
    return render(request, template_name, context)


@csrf_protect
def process_login(request):
    template_name = 'logindemo/success.html'
    context = {}
    if request.method == 'POST':
        app_access_token = '|'.join([
            'AA', settings.ACCOUNT_KIT_APP_ID,
            settings.ACCOUNT_KIT_APP_SECRET])
        params = {
            'grant_type': 'authorization_code',
            'code': request.POST.get('code'),
            'access_token': app_access_token,
        }
        try:
            response = requests.get(settings.ACCOUNT_KIT_TOKEN_EXCHANGE_BASE_URL,
                                    params=params)
        except Exception as e:
            print ('Failed to request token exchange api', e)
            response = None

        if response and response.status_code == 200:
            data = response.json()
            appsecret_proof = genAppSecretProof(settings.ACCOUNT_KIT_APP_SECRET,
                                                data['access_token'])
            context['user_access_token'] = data['access_token']
            context['user_id'] = data['id']
            params = {
                'access_token': data['access_token'],
                'appsecret_proof': appsecret_proof,
            }
            try:
                me_response = requests.get(settings.ACCOUNT_KIT_ME_ENDPOINT_BASE_URL,
                                           params=params)
            except Exception as e:
                me_response = None
                print ('Failed to request user access api', e)

            if me_response and me_response.status_code == 200:
                me_data = me_response.json()
                if me_data.get('phone'):
                    context['method'] = 'SMS'
                    context['identity'] = me_data['phone']['number']
                elif me_data.get('email'):
                    context['method'] = 'Email'
                    context['identity'] = me_data['email']['address']
    return render(request, template_name, context)
