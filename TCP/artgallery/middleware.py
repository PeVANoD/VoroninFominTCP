class GuestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/manage/' and not request.user.is_authenticated:
            if request.session.get('is_guest'):
                request.user = AnonymousUser()
                return self.get_response(request)
        
        return self.get_response(request)