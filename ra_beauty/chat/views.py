import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .bot import get_bot_response, greet, MAIN_MENU_OPTIONS


def chat_page(request):
    return render(request, 'chat/chat.html')


@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '')
        is_init = data.get('init', False)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid request body'}, status=400)

    if is_init:
        request.session['state'] = {'flow': 'main'}
        return JsonResponse({'reply': greet(), 'options': MAIN_MENU_OPTIONS})

    if not user_message.strip():
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)

    reply, options = get_bot_response(request.session, user_message)
    request.session.modified = True
    return JsonResponse({'reply': reply, 'options': options})
