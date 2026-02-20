"""
Visitor Cookie Views
Views to demonstrate and test visitor cookie functionality
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .visitor_utils import get_visitor_info


def visitor_info_view(request):
    """
    View to display visitor information
    Useful for testing and debugging
    """
    visitor_info = get_visitor_info(request)
    
    return render(request, 'mybus/visitor_info.html', {
        'visitor_info': visitor_info,
        'all_cookies': request.COOKIES
    })


@require_http_methods(["GET"])
def visitor_api_info(request):
    """
    API endpoint to get visitor information
    Returns JSON response with visitor details
    """
    visitor_info = get_visitor_info(request)
    
    return JsonResponse({
        'success': True,
        'visitor_info': visitor_info,
        'total_cookies': len(request.COOKIES),
        'cookie_names': list(request.COOKIES.keys())
    })


@csrf_exempt
@require_http_methods(["POST"])
def test_visitor_cookie(request):
    """
    Test endpoint to manually set visitor cookie
    Useful for testing purposes
    """
    from django.http import HttpResponse
    from .visitor_utils import set_visitor_cookie
    
    response = HttpResponse("Visitor cookie set successfully!")
    response = set_visitor_cookie(response)
    
    return response
