import logging
import time

logger = logging.getLogger(__name__)
"""
# this class is a middleware that logs incoming requests and their response times
# it can be used to monitor the performance of the API and track any issues that may arise
"""
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Log incoming request
        logger.info(f"[REQUEST] {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)

        duration = time.time() - start_time
        # Log response info
        logger.info(f"[RESPONSE] Status: {response.status_code} | Duration: {duration:.2f}s")

        return response
