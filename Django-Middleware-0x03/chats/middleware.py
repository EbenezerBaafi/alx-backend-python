import logging
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden
import json

# Create logs directory if it doesn't exist
logs_dir = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Create file handler
log_file = os.path.join(logs_dir, 'user_requests.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger if not already added
if not logger.handlers:
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file.
    Logs timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process the request and log user information.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HTTP response from the next middleware/view
        """
        # Get user information
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access outside of 6AM to 9PM (18:00 to 21:00).
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Check current server time and restrict access outside allowed hours.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HTTP 403 Forbidden response if outside allowed hours,
            otherwise continues with normal response
        """
        current_time = datetime.now().time()
        current_hour = current_time.hour
        
        # Define allowed hours: 6AM (06:00) to 9PM (21:00)
        allowed_start = 6  # 6AM
        allowed_end = 21   # 9PM
        
        # Check if current time is outside allowed hours
        if current_hour < allowed_start or current_hour >= allowed_end:
            error_message = {
                "error": "Access denied",
                "message": f"Chat access is restricted. Please try again between 6:00 AM and 9:00 PM. Current time: {current_time.strftime('%H:%M:%S')}",
                "allowed_hours": "6:00 AM - 9:00 PM",
                "current_time": current_time.strftime('%H:%M:%S')
            }
            
            return HttpResponseForbidden(
                json.dumps(error_message),
                content_type='application/json'
            )
        
        # Continue processing the request if within allowed hours
        response = self.get_response(request)
        return response