import time
from collections import defaultdict
from threading import Lock

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    def __init__(self, get_response, rate_limit=5, time_window=60):
        self.get_response = get_response
        self.visits = defaultdict(list)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.lock = Lock()

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time.time()

        with self.lock:
            # Remove timestamps older than the time window
            self.visits[ip] = [t for t in self.visits[ip]
                               if current_time - t < self.time_window]

            if len(self.visits[ip]) >= self.rate_limit:
                # logger.warning(f"Rate limit exceeded for IP address: {ip}")
                return HttpResponseForbidden("Rate limit exceeded. Please try again later.")

            self.visits[ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
