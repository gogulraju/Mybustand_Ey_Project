"""
Bus Route Search and Live Tracking Models
"""
from django.db import models
from django.utils import timezone


class BusRoute(models.Model):
    """Bus route information with live tracking"""
    
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('delayed', 'Delayed'),
        ('stopped', 'Stopped'),
        ('maintenance', 'Maintenance'),
        ('cancelled', 'Cancelled')
    ]
    
    id = models.AutoField(primary_key=True)
    from_city = models.CharField(max_length=100, db_index=True)
    to_city = models.CharField(max_length=100, db_index=True)
    bus_name = models.CharField(max_length=200)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bus_routes'
        ordering = ['from_city', 'to_city', 'departure_time']
        indexes = [
            models.Index(fields=['from_city', 'to_city']),
            models.Index(fields=['status']),
            models.Index(fields=['departure_time']),
        ]
    
    def __str__(self):
        return f"{self.bus_name} - {self.from_city} to {self.to_city}"
    
    @property
    def route_display(self):
        return f"{self.from_city} → {self.to_city}"


class BusLocationHistory(models.Model):
    """Track bus location history for live tracking"""
    
    id = models.AutoField(primary_key=True)
    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bus_location_history'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['bus', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.bus.bus_name} - {self.timestamp}"
