from django.shortcuts import redirect
from django.urls import reverse

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'userprofile') and request.user.userprofile.is_blocked:
                # Разрешим выйти на страницу выхода или logout
                if request.path not in [reverse('login_user'), reverse('blocked')]:
                    return redirect('blocked')
        response = self.get_response(request)
        return response

