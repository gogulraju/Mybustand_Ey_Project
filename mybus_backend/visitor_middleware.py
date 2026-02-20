"""
Visitor Cookie Middleware
Automatically sets site_visitor cookie for first-time visitors
"""
import uuid
from django.conf import settings
from django.http import HttpResponse


class VisitorCookieMiddleware:
    """
    Middleware to automatically set site_visitor cookie for first-time visitors
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if site_visitor cookie already exists
        if 'site_visitor' not in request.COOKIES:
            # Generate unique visitor ID
            visitor_id = str(uuid.uuid4())
            
            # Set cookie with specified settings
            response.set_cookie(
                'site_visitor',
                visitor_id,
                max_age=24 * 60 * 60,  # 24 hours in seconds
                httponly=True,
                samesite='Lax',
                secure=getattr(settings, 'VISITOR_COOKIE_SECURE', False),
                path='/'
            )
            
            # Optional: Add visitor info to request for debugging
            request.is_new_visitor = True
            request.visitor_id = visitor_id
        else:
            # Existing visitor
            request.is_new_visitor = False
            request.visitor_id = request.COOKIES['site_visitor']
        
        return response
