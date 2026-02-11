class UserIpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            user_ip = request.META.get("REMOTE_ADDR")
            user.update_ip(user_ip)

        return self.get_response(request)
