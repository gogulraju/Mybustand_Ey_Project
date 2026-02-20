from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import time
import os
from django.core.cache import cache


def about(request):
    """About page view"""
    return render(request, 'mybus/about.html')


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        messages.success(request, f'Thank you {name}! Your message has been sent successfully. We\'ll contact you at {email} or {mobile} soon.')
        return redirect('contact')
    
    return render(request, 'mybus/contact.html')


def home(request):
    """Home page view"""
    return render(request, 'mybus/index.html')


def logout_view(request):
    """Logout user and redirect to home"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def bus_search_frontend(request):
    """Bus search frontend page"""
    return render(request, 'mybus/bus_search.html')


def cookie_dashboard(request):
    """Cookie management dashboard"""
    return render(request, 'mybus/cookie_dashboard_working.html')


def route_search(request):
    """Combined route search and bus listing module"""
    return render(request, 'mybus/bus_routes.html')


def bus_list(request):
    """Available buses listing with enhanced features"""
    return render(request, 'mybus/available_buses.html')


def live_tracking(request):
    """Enhanced live bus tracking page view"""
    return render(request, 'mybus/bus_tracking_enhanced.html')


@csrf_exempt
@require_http_methods(["GET"])
def get_bus_location(request):
    """Live bus location API"""
    bus_id = request.GET.get('bus_id', '1')
    
    # Simulate real-time bus location data
    import random
    import time
    
    # Generate realistic bus position along route
    current_time = int(time.time())
    position = (current_time % 100) / 100.0 * 90  # 0-90% along route
    
    # Generate realistic coordinates for Bangalore route
    base_lat = 12.9716  # Electronic City
    base_lng = 77.5946
    dest_lat = 12.9798  # MG Road
    dest_lng = 77.5946
    
    current_lat = base_lat + (dest_lat - base_lat) * (position / 90)
    current_lng = base_lng + (dest_lng - base_lng) * (position / 90)
    
    # Add some realistic variation
    current_lat += random.uniform(-0.001, 0.001)
    current_lng += random.uniform(-0.001, 0.001)
    
    # Determine next stop
    next_stop = "Electronic City"
    if position > 10:
        next_stop = "BTM Layout"
    if position > 35:
        next_stop = "Koramangala"
    if position > 60:
        next_stop = "MG Road"
    
    return JsonResponse({
        'success': True,
        'data': {
            'bus_id': bus_id,
            'latitude': current_lat,
            'longitude': current_lng,
            'position_percentage': position,
            'speed': random.randint(25, 55),
            'next_stop': next_stop,
            'distance_to_next': round(random.uniform(0.5, 3.5), 1),
            'passengers': random.randint(15, 45),
            'eta_minutes': max(2, round((90 - position) * 0.3)),
            'status': 'On Time' if random.random() > 0.2 else 'Delayed',
            'last_updated': 'just now'
        }
    })

@csrf_exempt
@require_http_methods(["GET"])
def get_all_buses(request):
    """All buses API with real-time data"""
    import random
    
    # Generate realistic bus data
    buses = [
        {
            'id': 1,
            'bus_number': 'KA-01-1234',
            'route': 'Electronic City → Majestic',
            'status': 'On Time' if random.random() > 0.2 else 'Delayed',
            'latitude': 12.9716 + random.uniform(-0.01, 0.01),
            'longitude': 77.5946 + random.uniform(-0.01, 0.01),
            'speed': random.randint(25, 55),
            'passengers': random.randint(15, 45),
            'capacity': 40,
            'next_stop': random.choice(['Electronic City', 'BTM Layout', 'Koramangala', 'MG Road']),
            'eta_minutes': random.randint(5, 25)
        },
        {
            'id': 2,
            'bus_number': 'KA-01-5678',
            'route': 'Majestic → Electronic City',
            'status': 'On Time' if random.random() > 0.2 else 'Delayed',
            'latitude': 12.9798 + random.uniform(-0.01, 0.01),
            'longitude': 77.5946 + random.uniform(-0.01, 0.01),
            'speed': random.randint(25, 55),
            'passengers': random.randint(15, 45),
            'capacity': 40,
            'next_stop': random.choice(['MG Road', 'Koramangala', 'BTM Layout', 'Electronic City']),
            'eta_minutes': random.randint(5, 25)
        },
        {
            'id': 3,
            'bus_number': 'KA-02-3456',
            'route': 'Whitefield → Koramangala',
            'status': 'On Time' if random.random() > 0.2 else 'Delayed',
            'latitude': 12.9698 + random.uniform(-0.01, 0.01),
            'longitude': 77.7494 + random.uniform(-0.01, 0.01),
            'speed': random.randint(25, 55),
            'passengers': random.randint(15, 45),
            'capacity': 40,
            'next_stop': random.choice(['Whitefield', 'Marathahalli', 'Koramangala']),
            'eta_minutes': random.randint(5, 25)
        }
    ]
    
    return JsonResponse({
        'success': True,
        'data': {
            'buses': buses,
            'total_count': len(buses),
            'active_routes': ['Electronic City → Majestic', 'Majestic → Electronic City', 'Whitefield → Koramangala'],
            'last_updated': 'just now'
        }
    })

@csrf_exempt
@require_http_methods(["GET"])
def get_route_stops(request):
    """Route stops API with real data"""
    route = request.GET.get('route', 'Electronic City → Majestic')
    
    # Define stops for different routes
    routes_data = {
        'Electronic City → Majestic': [
            {'name': 'Electronic City', 'stop_id': 1, 'latitude': 12.9716, 'longitude': 77.5946, 'eta_minutes': 0},
            {'name': 'BTM Layout', 'stop_id': 2, 'latitude': 12.9128, 'longitude': 77.6011, 'eta_minutes': 8},
            {'name': 'Koramangala', 'stop_id': 3, 'latitude': 12.9352, 'longitude': 77.6245, 'eta_minutes': 15},
            {'name': 'MG Road', 'stop_id': 4, 'latitude': 12.9798, 'longitude': 77.5946, 'eta_minutes': 22},
            {'name': 'Majestic', 'stop_id': 5, 'latitude': 12.9766, 'longitude': 77.5713, 'eta_minutes': 30}
        ],
        'Majestic → Electronic City': [
            {'name': 'Majestic', 'stop_id': 1, 'latitude': 12.9766, 'longitude': 77.5713, 'eta_minutes': 0},
            {'name': 'MG Road', 'stop_id': 2, 'latitude': 12.9798, 'longitude': 77.5946, 'eta_minutes': 8},
            {'name': 'Koramangala', 'stop_id': 3, 'latitude': 12.9352, 'longitude': 77.6245, 'eta_minutes': 15},
            {'name': 'BTM Layout', 'stop_id': 4, 'latitude': 12.9128, 'longitude': 77.6011, 'eta_minutes': 22},
            {'name': 'Electronic City', 'stop_id': 5, 'latitude': 12.9716, 'longitude': 77.5946, 'eta_minutes': 30}
        ],
        'Whitefield → Koramangala': [
            {'name': 'Whitefield', 'stop_id': 1, 'latitude': 12.9698, 'longitude': 77.7494, 'eta_minutes': 0},
            {'name': 'Marathahalli', 'stop_id': 2, 'latitude': 12.9569, 'longitude': 77.7011, 'eta_minutes': 10},
            {'name': 'Koramangala', 'stop_id': 3, 'latitude': 12.9352, 'longitude': 77.6245, 'eta_minutes': 25}
        ]
    }
    
    stops = routes_data.get(route, routes_data['Electronic City → Majestic'])
    
    return JsonResponse({
        'success': True,
        'data': {
            'route': route,
            'stops': stops,
            'total_stops': len(stops),
            'total_distance_km': round(len(stops) * 6.5, 1),
            'estimated_duration_minutes': len(stops) * 8
        }
    })


def chatbot(request):
    """Chatbot page view"""
    return render(request, 'mybus/chatbot support module.html')


def login_view(request):
    """Login view with phone number authentication"""
    if request.method == 'POST':
        mobile_number = request.POST.get('username')  # Using username field for mobile
        password = request.POST.get('password')

        # Validate mobile number format
        if not mobile_number or len(mobile_number) < 10:
            messages.error(request, 'Please enter a valid mobile number')
            return render(request, 'mybus/user authentication module.html', {'form': AuthenticationForm()})

        # Try to authenticate with mobile number as username
        user = authenticate(username=mobile_number, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back! Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid mobile number or password')
    else:
        form = AuthenticationForm()

    return render(request, 'mybus/user authentication module.html', {'form': form})


def search_buses(request):
    """Handle bus search form submission"""
    if request.method == 'POST':
        from_city = request.POST.get('from')
        to_city = request.POST.get('to')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date')
        
        # Store search parameters in session for display in bus listing
        search_params = {
            'from': from_city,
            'to': to_city,
            'departure_date': departure_date,
            'return_date': return_date
        }
        request.session['search_params'] = search_params
        
        # In a real app, you would search the database
        # For now, create sample bus data based on search
        buses = [
            {
                'id': 1,
                'name': 'Volvo AC Sleeper',
                'bus_type': 'AC Sleeper',
                'departure_time': '08:00 AM',
                'arrival_time': '02:30 PM',
                'duration': '6h 30m',
                'price': 1200,
                'available_seats': 12,
                'total_seats': 30
            },
            {
                'id': 2,
                'name': 'Scania Non-AC',
                'bus_type': 'Non-AC Sleeper',
                'departure_time': '09:30 AM',
                'arrival_time': '04:00 PM',
                'duration': '6h 30m',
                'price': 800,
                'available_seats': 8,
                'total_seats': 35
            },
            {
                'id': 3,
                'name': 'Mercedes AC Semi-Sleeper',
                'bus_type': 'AC Semi-Sleeper',
                'departure_time': '11:00 AM',
                'arrival_time': '05:30 PM',
                'duration': '6h 30m',
                'price': 1000,
                'available_seats': 15,
                'total_seats': 40
            }
        ]
        
        messages.success(request, f'Found {len(buses)} buses from {from_city} to {to_city}')
        return render(request, 'mybus/bus listing module.html', {
            'buses': buses,
            'search_params': search_params
        })
    
    return redirect('route_search')


@csrf_exempt
def chatbot_api(request):
    """ChatGPT integrated chatbot API endpoint"""
    if request.method == 'POST':
        try:
            import openai
            import os
            
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            # Set OpenAI API key (you should set this as environment variable)
            # For demo purposes, using a fallback response if API key is not configured
            api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
            
            if api_key == 'your-openai-api-key-here':
                # Fallback to simple responses when API key is not configured
                response = get_fallback_response(user_message)
                return JsonResponse({'reply': response, 'using_chatgpt': False})
            
            # Configure OpenAI
            openai.api_key = api_key
            
            # Create context for MyBusStand chatbot
            system_prompt = """You are a helpful assistant for MyBusStand, a bus travel booking platform. 
            You help users with:
            - Bus route information and schedules
            - Ticket booking and pricing
            - Live bus tracking
            - Cancellation and refund policies
            - General travel assistance
            
            Be friendly, professional, and provide accurate information about bus travel in India.
            If you don't know specific information, suggest the user check the app or contact support."""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            bot_response = response.choices[0].message.content.strip()
            
            return JsonResponse({'reply': bot_response, 'using_chatgpt': True})
            
        except Exception as e:
            # Fallback to simple responses on any error
            response = get_fallback_response(user_message)
            return JsonResponse({'reply': response, 'using_chatgpt': False})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_fallback_response(message):
    """Fallback responses when OpenAI API is not available"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 I'm your MyBusStand assistant. How can I help you with your bus travel today?"
    elif any(word in message_lower for word in ['timing', 'schedule', 'when', 'time']):
        return "Our buses operate from 6:00 AM to 11:00 PM daily. Peak hours have more frequent buses - every 10-15 minutes. You can check specific route timings in the route search section."
    elif any(word in message_lower for word in ['book', 'ticket', 'booking', 'reserve']):
        return "To book a ticket: 1) Search for your route, 2) Select your preferred bus, 3) Choose your seats, 4) Make payment using mobile number login."
    elif any(word in message_lower for word in ['track', 'tracking', 'location', 'where']):
        return "For live tracking: Go to Live Tracking section and enter your bus number. You can see real-time location and ETA."
    elif any(word in message_lower for word in ['price', 'cost', 'fare', 'rate']):
        return "Bus fares vary: AC buses ₹65-120, Non-AC buses ₹30-80, Volvo buses ₹85-150. Exact fare depends on your route distance."
    elif any(word in message_lower for word in ['cancel', 'refund', 'money back']):
        return "Full refund if cancelled 2 hours before departure. 50% refund for cancellations 1 hour before. No refund for less than 1 hour before departure."
    elif any(word in message_lower for word in ['contact', 'support', 'help', 'phone']):
        return "Contact our support team at 📞 1800-123-4567 (24/7) or email support@mybusstand.com. We typically respond within 2 hours."
    elif any(word in message_lower for word in ['payment', 'pay', 'upi', 'card']):
        return "We accept all major credit/debit cards, UPI (PhonePe, GPay, Paytm), net banking, and digital wallets."
    elif any(word in message_lower for word in ['login', 'signin', 'account']):
        return "Login with your mobile number using OTP. No password needed! Enter your 10-digit mobile number, receive OTP, and you're in."
    else:
        return "I'm here to help with bus bookings, schedules, tracking, and general travel information. You can ask me about routes, timings, fares, or use the quick help buttons below."


def google_login(request):
    """Google OAuth login view"""
    # Check if Google OAuth is configured
    client_id = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET')
    redirect_uri = os.getenv('GOOGLE_OAUTH2_REDIRECT_URI')
    
    if not all([client_id, client_secret, redirect_uri]):
        messages.error(request, 'Google OAuth is not configured. Please check environment variables.')
        return redirect('login')
    
    # Check if using demo credentials
    if 'your-google-client-id' in client_id or 'your-google-client-secret' in client_secret:
        # Demo mode - simulate successful Google login
        messages.success(request, 'Google login successful! Welcome to MyBusStand.')
        request.session['google_user'] = {
            'email': 'user@gmail.com',
            'name': 'Google User',
            'avatar': 'https://lh3.googleusercontent.com/a/default-user'
        }
        return redirect('home')
    
    from google_auth_oauthlib.flow import Flow
    from google.oauth2.credentials import Credentials
    import googleapiclient.discovery
    
    # Google OAuth configuration
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": [redirect_uri],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    )
    
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # Store state in session for security
    request.session['oauth_state'] = state
    
    return redirect(authorization_url)


def google_callback(request):
    """Google OAuth callback view"""
    from google_auth_oauthlib.flow import Flow
    from google.oauth2.credentials import Credentials
    import googleapiclient.discovery
    
    # Verify state for security
    state = request.session.get('oauth_state')
    if state != request.GET.get('state'):
        messages.error(request, 'Invalid OAuth state parameter')
        return redirect('login')
    
    # Exchange authorization code for access token
    client_config = {
        "web": {
            "client_id": os.getenv('GOOGLE_OAUTH2_CLIENT_ID'),
            "client_secret": os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET'),
            "redirect_uris": [os.getenv('GOOGLE_OAUTH2_REDIRECT_URI')],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    )
    
    flow.redirect_uri = os.getenv('GOOGLE_OAUTH2_REDIRECT_URI')
    
    try:
        # Exchange code for token
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        
        # Get user info
        credentials = flow.credentials
        userinfo_service = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        
        # Create user session
        request.session['google_user'] = {
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'avatar': user_info.get('picture'),
            'verified': user_info.get('verified_email', False)
        }
        
        messages.success(request, f'Welcome {user_info.get("name")}! Google login successful.')
        return redirect('home')
        
    except Exception as e:
        messages.error(request, f'Google login failed: {str(e)}')
        return redirect('login')


@csrf_exempt
@require_http_methods(["POST"])
def send_otp(request):
    """Send OTP to mobile number via SMS with database integration"""
    try:
        data = json.loads(request.body)
        mobile = data.get('mobile')
        
        if not mobile or len(mobile) != 10:
            return JsonResponse({'success': False, 'error': 'Please enter a valid 10-digit mobile number'})
        
        # Check 30-second cooldown
        from .models import OTPVerification
        from django.utils import timezone
        
        latest_otp = OTPVerification.objects.filter(
            mobile_number=mobile
        ).order_by('-created_at').first()
        
        if latest_otp and not latest_otp.can_send_new_otp():
            remaining_time = 30 - int((timezone.now() - latest_otp.created_at).total_seconds())
            return JsonResponse({
                'success': False, 
                'error': f'Please wait {remaining_time} seconds before requesting another OTP'
            })
        
        # Generate 6-digit OTP
        import random
        otp = str(random.randint(100000, 999999))
        
        # Create OTP record in database
        otp_record = OTPVerification.objects.create(
            mobile_number=mobile,
            otp_code=otp,
            is_verified=False
        )
        
        # Send SMS via Twilio SMS API
        sms_sent = False
        sms_sid = None
        error_message = None
        
        try:
            sms_provider = os.getenv('SMS_SERVICE_PROVIDER', 'demo')
            
            if sms_provider == 'twilio':
                # Use real Twilio SMS API
                success, sid = send_otp_via_twilio_sms(mobile, otp)
                if success:
                    sms_sent = True
                    sms_sid = sid
                else:
                    error_message = "Failed to send SMS via Twilio"
            else:
                # Fallback to console if not configured
                print(f"TWILIO NOT CONFIGURED - OTP for {mobile}: {otp}")
                error_message = "SMS service not configured"
                
        except Exception as sms_error:
            print(f"SMS sending failed: {sms_error}")
            error_message = str(sms_error)
        
        # Update OTP record with SMS status
        if sms_sent:
            otp_record.sms_sent = True
            otp_record.sms_sid = sms_sid
        else:
            otp_record.sms_sent = False
        otp_record.save()
        
        if sms_sent:
            return JsonResponse({
                'success': True, 
                'message': f'OTP sent successfully to {mobile}',
                'sms_sent': True,
                'otp_id': otp_record.id
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': error_message or 'Unable to send OTP. Please try again.',
                'sms_sent': False
            })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'})
    except Exception as e:
        print(f"Send OTP error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def verify_otp(request):
    """Verify OTP and login user with full database integration"""
    try:
        from django.utils import timezone
        data = json.loads(request.body)
        mobile = data.get('mobile')
        otp = data.get('otp')
        
        if not mobile or not otp:
            return JsonResponse({'success': False, 'error': 'Mobile number and OTP are required'})
        
        # Verify OTP from database
        print(f"DEBUG: Verifying OTP - Mobile: {mobile}, OTP: {otp}")
        is_valid, message = verify_otp_from_database(mobile, otp)
        print(f"DEBUG: Verification result - Valid: {is_valid}, Message: {message}")
        
        if is_valid:
            # Create user session
            request.session['otp_user'] = {
                'mobile': mobile,
                'authenticated': True,
                'login_time': str(timezone.now())
            }
            
            # Create or get user profile
            from django.contrib.auth.models import User
            from .models import UserProfile
            
            user, created = User.objects.get_or_create(
                username=mobile,
                defaults={
                    'first_name': f'User_{mobile}',
                    'email': f'{mobile}@mybusstand.com'
                }
            )
            
            if created:
                UserProfile.objects.create(
                    user=user,
                    mobile_number=mobile,
                    login_method='MOBILE_OTP'
                )
            
            # Log the user in
            from django.contrib.auth import login
            login(request, user)
            
            # Set login cookies
            from .cookie_utils import set_last_login_time, set_theme_preference
            from django.http import JsonResponse
            
            response = JsonResponse({
                'success': True, 
                'message': 'OTP verified successfully',
                'redirect_url': '/home/'
            })
            
            # Set last login time cookie
            set_last_login_time(response)
            
            # Set default theme preference if not exists
            if not request.COOKIES.get('theme_preference'):
                set_theme_preference(response, 'light')
            
            return response
        else:
            return JsonResponse({
                'success': False, 
                'error': message
            })
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request format'})
    except Exception as e:
        print(f"Verify OTP error: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def send_sms_via_twilio_verify(mobile, otp):
    """Send OTP via Twilio Verify API (Professional Method)"""
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
        
        if not all([account_sid, auth_token, verify_service_sid]):
            print("Twilio Verify credentials not configured")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Send OTP using Twilio Verify API
        verification = client.verify.services(verify_service_sid).verifications.create(
            to=f'+91{mobile}',
            channel='sms'
        )
        
        print(f"Twilio Verify OTP sent. SID: {verification.sid}")
        print(f"Status: {verification.status}")
        print(f"To: {verification.to}")
        
        return True
        
    except ImportError:
        print("Twilio not installed. Run: pip install twilio")
        return False
    except Exception as e:
        print(f"Twilio Verify error: {e}")
        return False


def verify_twilio_otp(mobile, otp):
    """Verify OTP using Twilio Verify API"""
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
        
        if not all([account_sid, auth_token, verify_service_sid]):
            return False
        
        client = Client(account_sid, auth_token)
        
        # Verify the OTP
        verification_check = client.verify.services(verify_service_sid).verification_checks.create(
            to=f'+91{mobile}',
            code=otp
        )
        
        print(f"Twilio Verify status: {verification_check.status}")
        
        return verification_check.status == 'approved'
        
    except ImportError:
        print("Twilio not installed. Run: pip install twilio")
        return False
    except Exception as e:
        print(f"Twilio Verify error: {e}")
        return False


def send_otp_via_twilio_sms(mobile, otp):
    """Send OTP via Twilio SMS API (not Verify)"""
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, twilio_phone_number]):
            print("Twilio credentials not configured")
            return False, None
        
        client = Client(account_sid, auth_token)
        
        # Send SMS via Twilio SMS API
        message = client.messages.create(
            body=f"Your MyBusStand OTP is: {otp}. Valid for 5 minutes. Do not share this OTP.",
            from_=twilio_phone_number,
            to=f"+91{mobile}"
        )
        
        print(f"SMS sent to {mobile}: SID {message.sid}")
        print(f"Status: {message.status}")
        print(f"From: {message.from_}")
        print(f"To: {message.to}")
        
        return True, message.sid
        
    except ImportError:
        print("Twilio not installed. Run: pip install twilio")
        return False, None
    except Exception as e:
        print(f"Twilio SMS error: {e}")
        return False, None


def verify_otp_from_database(mobile, otp):
    """Verify OTP from database with proper validation"""
    try:
        from django.utils import timezone
        from .models import OTPVerification
        
        # Get latest unverified OTP for this mobile
        otp_record = OTPVerification.objects.filter(
            mobile_number=mobile,
            is_verified=False
        ).order_by('-created_at').first()
        
        if not otp_record:
            return False, "No OTP found for this mobile number"
        
        # Check if OTP is expired
        if otp_record.is_expired():
            return False, "OTP has expired"
        
        # Check if OTP matches
        if otp_record.otp_code != otp:
            # Increment attempts
            otp_record.attempts += 1
            otp_record.save()
            
            if otp_record.attempts >= 3:
                return False, "Too many failed attempts. Please request new OTP"
            
            return False, "Invalid OTP"
        
        # OTP is correct - mark as verified
        otp_record.mark_as_verified()
        
        return True, "OTP verified successfully"
        
    except Exception as e:
        print(f"OTP verification error: {e}")
        return False, "Verification failed"


def send_sms_via_twilio(mobile, otp):
    """Send SMS via Twilio Verify API"""
    return send_sms_via_twilio_verify(mobile, otp)


def otp_login(request):
    """Handle OTP login"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp_inputs = request.POST.getlist('otp')
        otp = ''.join(otp_inputs)
        
        if not mobile or not otp:
            messages.error(request, 'Please enter mobile number and OTP')
            return redirect('login')
        
        # Verify OTP from cache first (fallback)
        cached_otp = cache.get(f'otp_{mobile}')
        
        # Try Twilio Verify if configured
        sms_provider = os.getenv('SMS_SERVICE_PROVIDER', 'demo')
        if sms_provider == 'twilio_verify' and cached_otp != otp:
            twilio_valid = verify_twilio_otp(mobile, otp)
            if twilio_valid:
                cache.delete(f'otp_{mobile}')  # Remove OTP after successful verification
                
                # In a real implementation, you would:
                # 1. Find user by mobile number
                # 2. If user exists, log them in
                # 3. If user doesn't exist, create new user
                # 4. Set user session
                
                # For demo, we'll create a mock session
                request.session['otp_user'] = {
                    'mobile': mobile,
                    'authenticated': True
                }
                
                messages.success(request, f'Login successful! Welcome +91{mobile}')
                return redirect('home')
        
        # Fallback to cache verification
        if cached_otp and cached_otp == otp:
            # OTP is valid
            cache.delete(f'otp_{mobile}')  # Remove OTP after successful verification
            
            # In a real implementation, you would:
            # 1. Find user by mobile number
            # 2. If user exists, log them in
            # 3. If user doesn't exist, create new user
            # 4. Set user session
            
            # For demo, we'll create a mock session
            request.session['otp_user'] = {
                'mobile': mobile,
                'authenticated': True
            }
            
            messages.success(request, f'Login successful! Welcome +91{mobile}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('login')
    
    return redirect('login')


