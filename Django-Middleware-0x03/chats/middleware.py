import logging
from datetime import datetime
import os
from django.conf import settings

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