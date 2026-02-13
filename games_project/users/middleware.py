from .models import UserIp


class UserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            ip_address = request.META.get("REMOTE_ADDR")
            UserIp.save_ip_if_new(user, ip_address)

        return self.get_response(request)
