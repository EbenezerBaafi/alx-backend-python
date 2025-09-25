# chats/middleware.py
import logging
from datetime import datetime, timedelta
import os
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
import json
from collections import defaultdict, deque

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
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_time = datetime.now().time()
        current_hour = current_time.hour
        
        allowed_start = 6
        allowed_end = 21
        
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
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST requests (messages) a user can send
    within a certain time window based on their IP address.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response
        # Dictionary to store request timestamps for each IP
        # Structure: {ip_address: deque([timestamp1, timestamp2, ...])}
        self.ip_requests = defaultdict(deque)
        
        # Configuration
        self.max_requests = 5  # Maximum requests allowed
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        """
        Track POST requests by IP address and enforce rate limits.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HTTP 429 Too Many Requests if limit exceeded,
            otherwise continues with normal response
        """
        # Only apply rate limiting to POST requests (message sending)
        if request.method == 'POST':
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = datetime.now()
            
            # Clean old requests outside the time window
            self.cleanup_old_requests(ip_address, current_time)
            
            # Check if user has exceeded the rate limit
            if len(self.ip_requests[ip_address]) >= self.max_requests:
                error_message = {
                    "error": "Rate limit exceeded",
                    "message": f"You have exceeded the maximum of {self.max_requests} messages per minute. Please wait before sending more messages.",
                    "limit": self.max_requests,
                    "time_window": "1 minute",
                    "retry_after": 60
                }
                
                return JsonResponse(
                    error_message,
                    status=429  # Too Many Requests
                )
            
            # Add current request timestamp
            self.ip_requests[ip_address].append(current_time)
        
        # Continue processing the request
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """
        Extract client IP address from request, considering proxy headers.
        
        Args:
            request: The HTTP request object
            
        Returns:
            str: Client IP address
        """
        # Check for IP address in proxy headers first
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Take the first IP if there are multiple (in case of multiple proxies)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fall back to REMOTE_ADDR
            ip = request.META.get('REMOTE_ADDR')
        
        return ip
    
    def cleanup_old_requests(self, ip_address, current_time):
        """
        Remove timestamps that are outside the time window.
        
        Args:
            ip_address (str): Client IP address
            current_time (datetime): Current timestamp
        """
        cutoff_time = current_time - timedelta(seconds=self.time_window)
        
        # Remove old timestamps
        while (self.ip_requests[ip_address] and 
               self.ip_requests[ip_address][0] < cutoff_time):
            self.ip_requests[ip_address].popleft()