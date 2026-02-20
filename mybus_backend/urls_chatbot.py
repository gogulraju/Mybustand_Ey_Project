"""
Chatbot URL Configuration
"""
from django.urls import path
from . import chatbot_views

urlpatterns = [
    # Chatbot API endpoint - matches the frontend call
    path('chatbot-api/', chatbot_views.chatbot_view, name='chatbot_api'),
    
    # Chatbot widget page (optional - for standalone testing)
    path('chatbot-widget/', chatbot_views.chatbot_widget_page, name='chatbot_widget'),
]
