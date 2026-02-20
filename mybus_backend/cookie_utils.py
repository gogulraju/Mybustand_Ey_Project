"""
Cookie Utilities - MyBusStand
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone


@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_cookies(request):
    """Get all cookies"""
    try:
        cookies = {}
        for key, value in request.COOKIES.items():
            cookies[key] = {
                'value': value,
                'secure': request.COOKIES.get(key, '').startswith('secure'),
                'httponly': True,  # All our cookies are HttpOnly
                'samesite': 'Lax'  # All our cookies use SameSite=Lax
            }
        
        return JsonResponse({
            'success': True,
            'cookies': cookies,
            'session_cookie': request.COOKIES.get('mybus_session'),
            'csrf_token': request.COOKIES.get('csrftoken')
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error getting cookies: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def set_custom_cookie(request):
    """Set custom cookie"""
    try:
        data = json.loads(request.body)
        cookie_name = data.get('name', '')
        cookie_value = data.get('value', '')
        max_age = data.get('max_age', 86400)  # 24 hours default
        
        if not cookie_name or not cookie_value:
            return JsonResponse({
                'success': False,
                'error': 'Cookie name and value are required'
            })
        
        response = JsonResponse({
            'success': True,
            'message': f'Cookie {cookie_name} set successfully'
        })
        
        # Set secure cookie
        response.set_cookie(
            cookie_name,
            cookie_value,
            max_age=max_age,
            secure=False,  # Set to True in production with HTTPS
            httponly=True,  # Prevent JavaScript access
            samesite='Lax',  # CSRF protection
            path='/'  # Available site-wide
        )
        
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error setting cookie: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def delete_cookie(request):
    """Delete specific cookie"""
    try:
        data = json.loads(request.body)
        cookie_name = data.get('name', '')
        
        if not cookie_name:
            return JsonResponse({
                'success': False,
                'error': 'Cookie name is required'
            })
        
        response = JsonResponse({
            'success': True,
            'message': f'Cookie {cookie_name} deleted successfully'
        })
        
        # Delete cookie by setting max_age=0
        response.delete_cookie(cookie_name, path='/')
        
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error deleting cookie: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def clear_all_cookies(request):
    """Clear all application cookies"""
    try:
        response = JsonResponse({
            'success': True,
            'message': 'All cookies cleared successfully'
        })
        
        # Clear common application cookies
        cookies_to_clear = [
            'mybus_session',
            'csrftoken',
            'user_preferences',
            'last_login',
            'theme_preference'
        ]
        
        for cookie_name in cookies_to_clear:
            response.delete_cookie(cookie_name, path='/')
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error clearing cookies: {str(e)}'
        })


def get_user_preferences(request):
    """Get user preferences from cookies"""
    try:
        preferences_cookie = request.COOKIES.get('user_preferences', '{}')
        return json.loads(preferences_cookie)
    except (json.JSONDecodeError, Exception):
        return {}


def set_user_preferences(response, preferences):
    """Set user preferences in cookie"""
    import json
    preferences_json = json.dumps(preferences)
    response.set_cookie(
        'user_preferences',
        preferences_json,
        max_age=86400 * 30,  # 30 days
        secure=False,
        httponly=True,
        samesite='Lax',
        path='/'
    )


def get_theme_preference(request):
    """Get theme preference from cookie"""
    return request.COOKIES.get('theme_preference', 'light')


def set_theme_preference(response, theme):
    """Set theme preference in cookie"""
    response.set_cookie(
        'theme_preference',
        theme,
        max_age=86400 * 30,  # 30 days
        secure=False,
        httponly=True,
        samesite='Lax',
        path='/'
    )


def get_last_login_time(request):
    """Get last login time from cookie"""
    last_login = request.COOKIES.get('last_login', '')
    if last_login:
        try:
            return timezone.datetime.fromisoformat(last_login)
        except:
            return None
    return None


def set_last_login_time(response):
    """Set last login time in cookie"""
    login_time = timezone.now().isoformat()
    response.set_cookie(
        'last_login',
        login_time,
        max_age=86400 * 7,  # 7 days
        secure=False,
        httponly=True,
        samesite='Lax',
        path='/'
    )
