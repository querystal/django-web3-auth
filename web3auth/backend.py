from django.contrib.auth import get_user_model

from web3auth.utils import recover_to_addr


class Web3Backend:
    def authenticate(self, request, token=None, signature=None):
        User = get_user_model()
        try:
            addr = recover_to_addr(token, signature)
            return User.objects.get(username=addr)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
