# LibraryProject/middleware.py
class CSPHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self';"
        )
        return response
