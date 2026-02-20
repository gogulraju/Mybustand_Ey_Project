"""
Support Models - User Queries and Complaints
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserQuery(models.Model):
    """User queries and support requests"""
    
    QUERY_TYPES = [
        ('general', 'General Query'),
        ('route', 'Route Information'),
        ('timing', 'Timing Query'),
        ('booking', 'Booking Issue'),
        ('payment', 'Payment Issue'),
        ('technical', 'Technical Issue'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    mobile_number = models.CharField(max_length=15, db_index=True)
    query_type = models.CharField(max_length=20, choices=QUERY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Response fields
    admin_response = models.TextField(null=True, blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responded_queries')
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_queries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['mobile_number']),
        ]
    
    def __str__(self):
        return f"Query #{self.id} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class UserComplaint(models.Model):
    """User complaints and issues"""
    
    COMPLAINT_TYPES = [
        ('service', 'Service Issue'),
        ('behavior', 'Staff Behavior'),
        ('bus_condition', 'Bus Condition'),
        ('safety', 'Safety Concern'),
        ('cleanliness', 'Cleanliness Issue'),
        ('delay', 'Delay Issue'),
        ('lost_found', 'Lost & Found'),
        ('other', 'Other Complaint')
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    
    STATUS_CHOICES = [
        ('filed', 'Filed'),
        ('investigating', 'Investigating'),
        ('action_taken', 'Action Taken'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed')
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    mobile_number = models.CharField(max_length=15, db_index=True)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES, default='other')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    bus_number = models.CharField(max_length=20, null=True, blank=True)
    route = models.CharField(max_length=100, null=True, blank=True)
    incident_date = models.DateTimeField(null=True, blank=True)
    incident_location = models.CharField(max_length=200, null=True, blank=True)
    
    # Status and resolution
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='filed')
    resolution_details = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Response fields
    admin_notes = models.TextField(null=True, blank=True)
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_complaints')
    handled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_complaints'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['complaint_type', 'severity']),
            models.Index(fields=['mobile_number']),
        ]
    
    def __str__(self):
        return f"Complaint #{self.id} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)
