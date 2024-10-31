from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        requests = cache.get(f'requests_{ip}', 0)
        
        if requests > 100:  # Лимит запросов
            return HttpResponseForbidden('Too many requests')
            
        cache.set(f'requests_{ip}', requests + 1, 60)  # Время в секундах
        return self.get_response(request) 