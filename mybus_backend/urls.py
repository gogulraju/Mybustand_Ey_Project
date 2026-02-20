from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from . import urls_support
from . import urls_chatbot
from . import cookie_utils
from . import urls_bus
from . import visitor_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    # OTP Authentication APIs
    path('api/send-otp/', views.send_otp, name='send_otp'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    # Bus Search Frontend
    path('bus-search/', views.bus_search_frontend, name='bus_search_frontend'),
    # Bus Routes & Available Buses
    path('route-search/', views.route_search, name='route_search'),
    path('bus-list/', views.bus_list, name='bus_list'),
    path('available-buses/', views.bus_list, name='available_buses'),
    # Enhanced Bus Tracking
    path('bus-tracking/', views.live_tracking, name='bus_tracking'),
    path('bus-tracking-enhanced/', views.live_tracking, name='bus_tracking_enhanced'),
    # Simplified feature pages (coming soon)
    path('api/bus-location/', views.get_bus_location, name='get_bus_location'),
    path('api/all-buses/', views.get_all_buses, name='get_all_buses'),
    path('api/route-stops/', views.get_route_stops, name='get_route_stops'),
    # Support System
    path('support/', include('mybus_backend.urls_support')),
    # Chatbot System
    path('chatbot/', include('mybus_backend.urls_chatbot')),
    # Cookie Management
    path('cookies/', views.cookie_dashboard, name='cookie_dashboard'),
    path('api/cookies/', cookie_utils.get_cookies, name='get_cookies'),
    path('api/set-cookie/', cookie_utils.set_custom_cookie, name='set_cookie'),
    path('api/delete-cookie/', cookie_utils.delete_cookie, name='delete_cookie'),
    path('api/clear-cookies/', cookie_utils.clear_all_cookies, name='clear_cookies'),
    # Bus Route Search and Live Tracking
    path('bus/', include('mybus_backend.urls_bus')),
    # Visitor Cookie Management
    path('visitor-info/', visitor_views.visitor_info_view, name='visitor_info'),
    path('visitor-api-info/', visitor_views.visitor_api_info, name='visitor_api_info'),
    path('test-visitor-cookie/', visitor_views.test_visitor_cookie, name='test_visitor_cookie'),
    # Admin
    path('admin/', admin.site.urls),
]
