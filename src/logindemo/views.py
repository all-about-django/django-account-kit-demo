from django.conf import settings
from django.shortcuts import render


def render_login_page(request):
    template_name = 'logindemo/index.html'
    context = {}
    context['app_id'] = settings.ACCOUNT_KIT_APP_ID
    context['api_version'] = settings.ACCOUNT_KIT_API_VERSION
    return render(request, template_name, context)
