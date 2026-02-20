from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for MyBusStand"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mybus_profile')
    mobile_number = models.CharField(max_length=10, unique=True, help_text="10-digit mobile number")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, 
        choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')],
        null=True, 
        blank=True
    )
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    
    # Login tracking
    login_method = models.CharField(
        max_length=20,
        choices=[
            ('MOBILE_OTP', 'Mobile OTP'),
            ('GOOGLE', 'Google OAuth'),
            ('EMAIL', 'Email Password')
        ],
        default='MOBILE_OTP'
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='EN')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"
    
    class Meta:
        db_table = 'mybus_user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class OTPVerification(models.Model):
    """Store OTP verification records for real-time authentication"""
    mobile_number = models.CharField(max_length=10, db_index=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"OTP for {self.mobile_number} - {self.created_at}"
    
    def is_expired(self):
        """Check if OTP is expired (5 minutes)"""
        from django.utils import timezone
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
    def can_send_new_otp(self):
        """Check if new OTP can be sent (30-second cooldown)"""
        from django.utils import timezone
        latest_otp = OTPVerification.objects.filter(
            mobile_number=self.mobile_number
        ).order_by('-created_at').first()
        
        if not latest_otp:
            return True
            
        return timezone.now() > latest_otp.created_at + timezone.timedelta(seconds=30)
    
    def mark_as_verified(self):
        """Mark OTP as verified"""
        from django.utils import timezone
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = 'otp_verification'
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mobile_number', 'created_at']),
            models.Index(fields=['is_verified']),
        ]


class OTPLog(models.Model):
    """Log all OTP requests for tracking and analytics"""
    mobile_number = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(
        max_length=20,
        choices=[
            ('LOGIN', 'Login'),
            ('REGISTER', 'Registration'),
            ('RESET', 'Password Reset'),
            ('VERIFY', 'Mobile Verification')
        ],
        default='LOGIN'
    )
    is_used = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    sms_sid = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"OTP for {self.mobile_number} - {self.purpose}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def mark_as_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = 'mybus_otp_logs'
        verbose_name = 'OTP Log'
        verbose_name_plural = 'OTP Logs'
        ordering = ['-created_at']


class LoginHistory(models.Model):
    """Track user login history for security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    login_method = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"
    
    class Meta:
        db_table = 'mybus_login_histories'
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'
        ordering = ['-login_time']
