"""
Bus Route Search and Live Tracking URLs
"""
from django.urls import path
from mybus_backend.bus_views.views import (
    search_bus, get_supported_routes, get_all_buses,
    track_bus, update_bus_location, bus_tracking_map
)

urlpatterns = [
    # Bus Search APIs
    path('api/search-bus/', search_bus, name='search_bus'),
    path('api/supported-routes/', get_supported_routes, name='get_supported_routes'),
    path('api/all-buses/', get_all_buses, name='get_all_buses'),
    
    # Bus Tracking APIs
    path('api/track-bus/<int:bus_id>/', track_bus, name='track_bus'),
    path('api/update-bus-location/<int:bus_id>/', update_bus_location, name='update_bus_location'),
    
    # Bus Tracking Map
    path('bus-tracking-map/', bus_tracking_map, name='bus_tracking_map'),
]
