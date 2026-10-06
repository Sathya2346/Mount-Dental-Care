from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class OptionalJWTAuthentication(JWTAuthentication):
    """JWT authentication that never breaks public endpoints.

    DRF resolves authentication *before* permission classes run. With the plain
    ``JWTAuthentication``, a browser holding an expired/old access token (for
    example after ``SECRET_KEY`` changed) makes every request 401 — even on
    public routes such as ``/api/site/`` and the booking/OTP endpoints that use
    ``AllowAny``. That is what blocked the CMS refresh and the appointment flow.

    Returning ``None`` here simply means "no authenticated user". Protected
    views still answer 401 because ``IsAuthenticated`` is evaluated afterwards
    and ``JWTAuthentication`` supplies the ``WWW-Authenticate`` header.
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, AuthenticationFailed):
            return None
