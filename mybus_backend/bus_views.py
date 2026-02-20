"""
Bus Route Search and Live Tracking Views
"""
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from .bus_models import BusRoute, BusLocationHistory


# Predefined supported routes
SUPPORTED_ROUTES = [
    ("Melmaruvathur", "Vandavasi"),
    ("Chennai", "Kanchipuram"),
    ("Kanchipuram", "Vellore"),
    ("Vellore", "Tiruvannamalai"),
    ("Tiruvannamalai", "Villupuram"),
    ("Villupuram", "Puducherry"),
    ("Puducherry", "Cuddalore"),
    ("Cuddalore", "Chidambaram"),
    ("Chidambaram", "Mayiladuthurai"),
    ("Mayiladuthurai", "Kumbakonam"),
    ("Kumbakonam", "Thanjavur"),
]


def normalize_city_name(city):
    """Normalize city name for matching with variations"""
    if not city:
        return ""
    
    # Common variations and corrections
    variations = {
        'chennai': 'Chennai',
        'chenai': 'Chennai',
        'madras': 'Chennai',
        'kanchipuram': 'Kanchipuram',
        'kanchi': 'Kanchipuram',
        'vellore': 'Vellore',
        'tiruvannamalai': 'Tiruvannamalai',
        'thiruvannamalai': 'Tiruvannamalai',
        'villupuram': 'Villupuram',
        'pondicherry': 'Puducherry',
        'pondy': 'Puducherry',
        'cuddalore': 'Cuddalore',
        'chidambaram': 'Chidambaram',
        'mayiladuthurai': 'Mayiladuthurai',
        'mayavaram': 'Mayiladuthurai',
        'kumbakonam': 'Kumbakonam',
        'kumbam': 'Kumbakonam',
        'thanjavur': 'Thanjavur',
        'thanjore': 'Thanjavur',
        'melmaruvathur': 'Melmaruvathur',
        'melmaruvathur': 'Melmaruvathur',
        'vandavasi': 'Vandavasi',
        'vandavashi': 'Vandavasi',
    }
    
    # Normalize: lowercase, remove spaces/special chars
    normalized = city.lower().strip().replace(' ', '').replace('-', '')
    
    # Return the correct city name if found in variations
    return variations.get(normalized, city.title())


@csrf_exempt
@require_http_methods(["POST"])
def search_bus(request):
    """Search buses between two cities"""
    try:
        data = json.loads(request.body)
        from_city = normalize_city_name(data.get('from', ''))
        to_city = normalize_city_name(data.get('to', ''))
        
        if not from_city or not to_city:
            return JsonResponse({
                'success': False,
                'error': 'Both from and to locations are required'
            })
        
        # Check if route is supported
        route_supported = False
        for supported_from, supported_to in SUPPORTED_ROUTES:
            if (from_city == supported_from and to_city == supported_to) or \
               (from_city == supported_to and to_city == supported_from):
                route_supported = True
                break
        
        if not route_supported:
            return JsonResponse({
                'success': False,
                'error': 'No buses available for this route',
                'message': 'This route is not supported. Please check supported routes.'
            })
        
        # Get buses for this route
        buses = BusRoute.objects.filter(
            Q(from_city=from_city, to_city=to_city) |
            Q(from_city=to_city, to_city=from_city)
        ).order_by('departure_time')
        
        if not buses.exists():
            return JsonResponse({
                'success': False,
                'error': 'No buses available for this route',
                'message': 'No buses found for this route at the moment.'
            })
        
        # Format response
        bus_list = []
        for bus in buses:
            bus_list.append({
                'id': bus.id,
                'bus_name': bus.bus_name,
                'departure_time': bus.departure_time.strftime('%I:%M %p'),
                'arrival_time': bus.arrival_time.strftime('%I:%M %p'),
                'status': bus.status,
                'route': bus.route_display
            })
        
        return JsonResponse({
            'success': True,
            'route': f"{from_city} to {to_city}",
            'buses': bus_list,
            'total_buses': len(bus_list)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Search error: {str(e)}'
        })


@require_http_methods(["GET"])
def get_supported_routes(request):
    """Get list of supported routes"""
    try:
        routes = []
        for from_city, to_city in SUPPORTED_ROUTES:
            routes.append({
                'from': from_city,
                'to': to_city,
                'route_display': f"{from_city} → {to_city}"
            })
        
        return JsonResponse({
            'success': True,
            'routes': routes,
            'total_routes': len(routes)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error getting routes: {str(e)}'
        })


@require_http_methods(["GET"])
def track_bus(request, bus_id):
    """Get live bus location for tracking"""
    try:
        bus = get_object_or_404(BusRoute, id=bus_id)
        
        # Get latest location
        latest_location = bus.location_history.first()
        
        response_data = {
            'success': True,
            'bus_id': bus.id,
            'bus_name': bus.bus_name,
            'route': bus.route_display,
            'from_city': bus.from_city,
            'to_city': bus.to_city,
            'departure_time': bus.departure_time.strftime('%I:%M %p'),
            'arrival_time': bus.arrival_time.strftime('%I:%M %p'),
            'status': bus.status,
            'latitude': float(bus.latitude) if bus.latitude else None,
            'longitude': float(bus.longitude) if bus.longitude else None,
            'last_updated': bus.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Add latest location if available
        if latest_location:
            response_data.update({
                'latitude': float(latest_location.latitude),
                'longitude': float(latest_location.longitude),
                'location_timestamp': latest_location.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Tracking error: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
def update_bus_location(request, bus_id):
    """Update bus location (for testing/demo)"""
    try:
        bus = get_object_or_404(BusRoute, id=bus_id)
        data = json.loads(request.body)
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        status = data.get('status')
        
        if latitude is not None and longitude is not None:
            # Update bus current location
            bus.latitude = latitude
            bus.longitude = longitude
            
            # Add to location history
            BusLocationHistory.objects.create(
                bus=bus,
                latitude=latitude,
                longitude=longitude
            )
        
        if status:
            bus.status = status
        
        bus.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Bus location updated for {bus.bus_name}',
            'latitude': float(bus.latitude),
            'longitude': float(bus.longitude),
            'status': bus.status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Update error: {str(e)}'
        })


@require_http_methods(["GET"])
def get_all_buses(request):
    """Get all buses for display"""
    try:
        buses = BusRoute.objects.all().order_by('from_city', 'to_city')
        
        bus_list = []
        for bus in buses:
            bus_list.append({
                'id': bus.id,
                'bus_name': bus.bus_name,
                'route': bus.route_display,
                'from_city': bus.from_city,
                'to_city': bus.to_city,
                'departure_time': bus.departure_time.strftime('%I:%M %p'),
                'arrival_time': bus.arrival_time.strftime('%I:%M %p'),
                'status': bus.status,
                'latitude': float(bus.latitude) if bus.latitude else None,
                'longitude': float(bus.longitude) if bus.longitude else None,
            })
        
        return JsonResponse({
            'success': True,
            'buses': bus_list,
            'total_buses': len(bus_list)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error getting buses: {str(e)}'
        })


def bus_tracking_map(request):
    """Simple bus tracking map page"""
    return render(request, 'mybus/bus_tracking_map.html')
