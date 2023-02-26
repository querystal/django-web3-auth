import logging

from django.contrib.auth import get_user_model, backends

from web3auth.settings import app_settings
from web3auth.utils import recover_to_addr

LOG = logging.getLogger(__name__)


class Web3Backend(backends.ModelBackend):
    def authenticate(self, request, address=None, token=None, signature=None):
        # get user model
        User = get_user_model()
        # check if the address the user has provided matches the signature
        if not address == recover_to_addr(token, signature):
            LOG.info(
                "Address {address} doesn't match signature {signature}".format(address=address, signature=signature))
            return None
        else:
            LOG.info("Address {address} matches signature {signature}".format(address=address, signature=signature))
            # get address field for the user model
            address_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
            kwargs = {
                f"{address_field}__iexact": address
            }
            # try to get user with provided data
            user = User.objects.filter(**kwargs).first()
            return user
