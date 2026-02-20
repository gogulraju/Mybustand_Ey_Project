"""
Simple Chatbot Module - MyBusStand Assistant
Works without external API keys
"""
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .chatbot_simple import get_bot_response


@csrf_exempt
@require_http_methods(["POST"])
def chatbot_view(request):
    """
    Simple Chatbot API endpoint
    Accepts POST request with user message and returns AI response
    """
    try:
        # Parse request data
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message is required'
            })
        
        # Get bot response using simple rule-based system
        bot_reply = get_bot_response(user_message)
        
        # Log to console for debugging
        print(f"🤖 Chatbot Console:")
        print(f"   User: {user_message}")
        print(f"   Bot: {bot_reply}")
        print("-" * 50)
        
        return JsonResponse({
            'success': True,
            'reply': bot_reply
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        })
    except Exception as e:
        print(f"❌ Chatbot Error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Chatbot error: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["GET"])
def chatbot_widget_page(request):
    """
    Standalone chatbot widget page for testing
    """
    return render(request, 'mybus/chatbot_widget.html')
