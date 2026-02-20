"""
Simple Console-based Chatbot for MyBusStand
Works without external API keys
"""

def get_bot_response(user_message):
    """
    Get bot response based on user message
    Simple rule-based responses for bus-related queries
    """
    user_message = user_message.lower().strip()
    
    # Bus route queries - enhanced patterns
    if any(keyword in user_message for keyword in ['route', 'routes', 'bus route', 'which routes', 'available routes']):
        return "🚌 Available Routes:\n1. Melmaruvathur → Vandavasi\n2. Chennai → Kanchipuram\n3. Kanchipuram → Vellore\n4. Vellore → Tiruvannamalai\n5. Tiruvannamalai → Villupuram\n6. Villupuram → Puducherry\n7. Puducherry → Cuddalore\n8. Cuddalore → Chidambaram\n9. Chidambaram → Mayiladuthurai\n10. Mayiladuthurai → Kumbakonam\n11. Kumbakonam → Thanjavur\n\nUse bus search page to find buses for any route!"
    
    # Specific route queries - enhanced patterns
    elif any(keyword in user_message for keyword in ['chennai to kanchipuram', 'chennai kanchipuram', 'kanchipuram from chennai']):
        return "🚌 Chennai → Kanchipuram Route:\n\n🚍 **TNSTC Express**\n⏰ Departure: 07:00 AM\n⏰ Arrival: 09:30 AM\n📍 Status: Running\n\n🔍 Use bus search page to book tickets!\n📍 Track this bus live on tracking page!"
    
    elif any(keyword in user_message for keyword in ['melmaruvathur to vandavasi', 'melmaruvathur vandavasi', 'vandavasi from melmaruvathur']):
        return "🚌 Melmaruvathur → Vandavasi Route:\n\n🚍 **TNSTC Express**\n⏰ Departure: 06:00 AM\n⏰ Arrival: 08:30 AM\n📍 Status: Running\n\n🔍 Use bus search page to book tickets!\n📍 Track this bus live on tracking page!"
    
    elif any(keyword in user_message for keyword in ['kanchipuram to vellore', 'kanchipuram vellore', 'vellore from kanchipuram']):
        return "🚌 Kanchipuram → Vellore Route:\n\n🚍 **TNSTC Express**\n⏰ Departure: 08:00 AM\n⏰ Arrival: 10:30 AM\n📍 Status: Running\n\n🔍 Use bus search page to book tickets!\n📍 Track this bus live on tracking page!"
    
    # Check for any city-to-city pattern
    elif ' to ' in user_message or any(city in user_message for city in ['chennai', 'kanchipuram', 'vellore', 'tiruvannamalai', 'villupuram', 'puducherry', 'cuddalore', 'chidambaram', 'mayiladuthurai', 'kumbakonam', 'thanjavur', 'melmaruvathur', 'vandavasi']):
        return "🚌 Route Information:\n\nI found route information! Use the **Bus Search** page to:\n• Find buses for any route\n• Check departure/arrival times\n• See bus status\n• Book tickets online\n• Track buses live\n\n🔍 Try: 'what routes are available?' for complete list"
    
    # Bus timing queries
    elif any(keyword in user_message for keyword in ['timing', 'time', 'schedule', 'departure', 'arrival']):
        return "🕐 Bus Timings:\n• TNSTC Express buses run from 6:00 AM to 9:00 PM\n• Departure and arrival times vary by route\n• Use bus search to check specific route timings"
    
    # Bus tracking queries
    elif any(keyword in user_message for keyword in ['track', 'tracking', 'location', 'where is', 'live']):
        return "📍 Bus Tracking:\n• Go to Bus Tracking page to track buses in real-time\n• Click on any bus to see its current location\n• Updates every 5 seconds automatically"
    
    # Login/OTP queries
    elif any(keyword in user_message for keyword in ['login', 'otp', 'mobile', 'account']):
        return "🔐 Login Help:\n• Use mobile number to login with OTP\n• Enter your mobile number and click 'Send OTP'\n• Enter received OTP to access your account"
    
    # Booking queries
    elif any(keyword in user_message for keyword in ['book', 'booking', 'ticket', 'reserve']):
        return "🎫 Bus Booking:\n• Search for your desired route\n• Select your preferred bus\n• Choose your seat and complete booking\n• Payment options available online"
    
    # Fare queries
    elif any(keyword in user_message for keyword in ['fare', 'price', 'cost', 'ticket price']):
        return "💰 Bus Fares:\n• Fares vary by route and bus type\n• TNSTC Express offers competitive pricing\n• Check specific route for exact fare details"
    
    # Support queries
    elif any(keyword in user_message for keyword in ['help', 'support', 'contact', 'issue', 'problem']):
        return "🛠️ Support Options:\n• Use Support Dashboard for queries and complaints\n• Contact customer service for urgent issues\n• Available 24/7 for emergency support"
    
    # General greeting
    elif any(keyword in user_message for keyword in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
        return "👋 Hello! Welcome to MyBusStand!\n\nI can help you with:\n• Bus routes and schedules\n• Live bus tracking\n• Booking information\n• Login and OTP support\n• Fare details\n• Technical support\n\nWhat would you like to know about?"
    
    # Thank you responses
    elif any(keyword in user_message for keyword in ['thank', 'thanks', 'bye', 'goodbye']):
        return "🙏 You're welcome! Have a safe journey with MyBusStand!"
    
    # Website features
    elif any(keyword in user_message for keyword in ['features', 'what can you do', 'services']):
        return "🌟 MyBusStand Features:\n\n🔍 **Route Search** - Find buses between cities\n🚌 **Available Buses** - View all buses with status\n📍 **Live Tracking** - Track buses in real-time\n🎫 **Bus Booking** - Reserve seats online\n🔐 **Mobile Login** - OTP-based authentication\n🛠️ **24/7 Support** - Help whenever you need it\n\nTry asking about any of these features!"
    
    # Default response
    else:
        return "💡 I'm here to help with MyBusStand services!\n\nYou can ask me about:\n• Bus routes and schedules\n• Live bus tracking\n• Booking information\n• Login and OTP support\n• Fares and pricing\n• Technical support\n\nType 'help' for more information or ask a specific question!"


def console_chatbot():
    """
    Console-based chatbot for testing
    """
    print("🤖 MYBUSSTAND CHATBOT CONSOLE")
    print("=" * 50)
    print("Type 'quit' to exit the chatbot")
    print("Type 'help' for available commands")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using MyBusStand Chatbot!")
                break
            
            if not user_input:
                continue
            
            # Get bot response
            bot_response = get_bot_response(user_input)
            
            print(f"\n🤖 Bot: {bot_response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chatbot session ended. Thank you!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    console_chatbot()
