import logging

logger = logging.getLogger("role_access")


class RoleAccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            logger.info(
                "%s [%s] -> %s %s (%s)",
                user, getattr(user, "role", "-"), request.method, request.path, response.status_code,
            )
        return response
