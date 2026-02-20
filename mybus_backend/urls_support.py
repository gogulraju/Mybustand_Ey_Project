"""
Support URLs - User Queries and Complaints
"""
from django.urls import path
from mybus_backend.support_views.views import submit_query, submit_complaint, get_user_queries, get_user_complaints, support_dashboard

urlpatterns = [
    # Support dashboard
    path('', support_dashboard, name='support_dashboard'),
    
    # API endpoints
    path('api/submit-query/', submit_query, name='submit_query'),
    path('api/submit-complaint/', submit_complaint, name='submit_complaint'),
    path('api/get-queries/', get_user_queries, name='get_user_queries'),
    path('api/get-complaints/', get_user_complaints, name='get_user_complaints'),
]
