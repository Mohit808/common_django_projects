from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import DatingToken

class DatingTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            prefix, key = auth_header.split()
            if prefix.lower() != 'token':
                return None
        except ValueError:
            return None

        try:
            token = DatingToken.objects.get(key=key)
        except DatingToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (token.user, token)
