"""
Support Views - User Queries and Complaints
"""
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .support_models import UserQuery, UserComplaint
from django.core.paginator import Paginator


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def submit_query(request):
    """Submit user query"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Get user profile for mobile number
        mobile_number = getattr(user.userprofile, 'mobile_number', '')
        
        # Create query
        query = UserQuery.objects.create(
            user=user,
            mobile_number=mobile_number,
            query_type=data.get('query_type', 'general'),
            subject=data.get('subject', ''),
            message=data.get('message', ''),
            priority=data.get('priority', 'medium')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Query submitted successfully',
            'query_id': query.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error submitting query: {str(e)}'
        })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def submit_complaint(request):
    """Submit user complaint"""
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Get user profile for mobile number
        mobile_number = getattr(user.userprofile, 'mobile_number', '')
        
        # Parse incident date if provided
        incident_date = None
        if data.get('incident_date'):
            try:
                incident_date = timezone.datetime.strptime(data['incident_date'], '%Y-%m-%d %H:%M')
            except:
                pass
        
        # Create complaint
        complaint = UserComplaint.objects.create(
            user=user,
            mobile_number=mobile_number,
            complaint_type=data.get('complaint_type', 'other'),
            severity=data.get('severity', 'medium'),
            subject=data.get('subject', ''),
            description=data.get('description', ''),
            bus_number=data.get('bus_number', ''),
            route=data.get('route', ''),
            incident_date=incident_date,
            incident_location=data.get('incident_location', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Complaint submitted successfully',
            'complaint_id': complaint.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error submitting complaint: {str(e)}'
        })


@login_required
@require_http_methods(["GET"])
def get_user_queries(request):
    """Get user's queries"""
    try:
        user = request.user
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queries = UserQuery.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(queries, per_page)
        page_obj = paginator.get_page(page)
        
        queries_data = []
        for query in page_obj:
            queries_data.append({
                'id': query.id,
                'query_type': query.query_type,
                'subject': query.subject,
                'message': query.message,
                'status': query.status,
                'priority': query.priority,
                'created_at': query.created_at.strftime('%Y-%m-%d %H:%M'),
                'admin_response': query.admin_response,
                'responded_at': query.responded_at.strftime('%Y-%m-%d %H:%M') if query.responded_at else None
            })
        
        return JsonResponse({
            'success': True,
            'queries': queries_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error fetching queries: {str(e)}'
        })


@login_required
@require_http_methods(["GET"])
def get_user_complaints(request):
    """Get user's complaints"""
    try:
        user = request.user
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        complaints = UserComplaint.objects.filter(user=user).order_by('-created_at')
        paginator = Paginator(complaints, per_page)
        page_obj = paginator.get_page(page)
        
        complaints_data = []
        for complaint in page_obj:
            complaints_data.append({
                'id': complaint.id,
                'complaint_type': complaint.complaint_type,
                'severity': complaint.severity,
                'subject': complaint.subject,
                'description': complaint.description,
                'bus_number': complaint.bus_number,
                'route': complaint.route,
                'status': complaint.status,
                'created_at': complaint.created_at.strftime('%Y-%m-%d %H:%M'),
                'incident_date': complaint.incident_date.strftime('%Y-%m-%d %H:%M') if complaint.incident_date else None,
                'incident_location': complaint.incident_location,
                'resolution_details': complaint.resolution_details,
                'resolved_at': complaint.resolved_at.strftime('%Y-%m-%d %H:%M') if complaint.resolved_at else None
            })
        
        return JsonResponse({
            'success': True,
            'complaints': complaints_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error fetching complaints: {str(e)}'
        })


@login_required
def support_dashboard(request):
    """Support dashboard page"""
    return render(request, 'mybus/support_dashboard.html')
