import logging
import time
from django.core.mail import send_mail
from django.conf import settings

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

# This middleware monitors the performance of requests
class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()  #Start timing when request comes in

        response = self.get_response(request)

        end_time = time.time()  # this will stop timing 
        duration = end_time - start_time

        # Log how long did it takes
        logger.info(
            f"{request.method} {request.path} took {duration:.3f} seconds"
        )

        #  Alert if too slow maybe more than 5 seconds
        if duration > 5.0:
            logger.warning(
                f"SLOW REQUEST: {request.path} took {duration:.3f} seconds!"
            )
            send_mail(
                subject='VERY SLOW REQUEST DETECTED',
                message=f"Endpoint: {request.path}\nMethod: {request.method}\nDuration: {duration:.3f} seconds",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['Thatoselepe53@gmail.com'],
                fail_silently=True,
            )

        return response
