class GuestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/manage/' and not request.user.is_authenticated:
            if request.session.get('is_guest'):
                request.user = AnonymousUser()
                return self.get_response(request)
        
        return self.get_response(request)
    
from django.contrib.auth import login
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.functional import SimpleLazyObject

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем для статики и некоторых URL
        if request.path.startswith('/static/') or request.path in ['/login/', '/register/']:
            return self.get_response(request)
            
        # Если уже аутентифицирован через сессию - пропускаем
        if request.user.is_authenticated:
            return self.get_response(request)
            
        # Пробуем аутентифицировать через JWT
        try:
            jwt_auth = JWTAuthentication()
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                user, _ = auth_result
                request.user = user
                login(request, user)  # Создаём сессию
        except Exception:
            pass
            
        return self.get_response(request)