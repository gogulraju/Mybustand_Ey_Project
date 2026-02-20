"""
Visitor Cookie Utilities
Helper functions for visitor cookie management
"""
import uuid
from django.http import HttpResponse


def get_visitor_id(request):
    """
    Get visitor ID from request cookies
    Returns None if no visitor cookie exists
    """
    return request.COOKIES.get('site_visitor')


def is_new_visitor(request):
    """
    Check if user is a new visitor
    Returns True if no visitor cookie exists
    """
    return 'site_visitor' not in request.COOKIES


def set_visitor_cookie(response, visitor_id=None):
    """
    Set visitor cookie on response
    If visitor_id is None, generates a new UUID
    """
    from django.conf import settings
    
    if visitor_id is None:
        visitor_id = str(uuid.uuid4())
    
    response.set_cookie(
        'site_visitor',
        visitor_id,
        max_age=24 * 60 * 60,  # 24 hours in seconds
        httponly=True,
        samesite='Lax',
        secure=getattr(settings, 'VISITOR_COOKIE_SECURE', False),
        path='/'
    )
    
    return response


def get_visitor_info(request):
    """
    Get complete visitor information
    Returns dictionary with visitor details
    """
    visitor_id = get_visitor_id(request)
    is_new = is_new_visitor(request)
    
    return {
        'visitor_id': visitor_id,
        'is_new_visitor': is_new,
        'has_visitor_cookie': visitor_id is not None
    }
