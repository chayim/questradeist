import requests
import datetime
from .types import Auth


class QuestradeAuth(object):
    """This class implements Questrade authentication.
    During the first time authorization, the access token must be exchanged
    for a full set of tokens. This means that this class must be initialized
    as QuestradeAuth(refresh_token=XXX) during first time initializtion.
    https://www.questrade.com/api/documentation/authorization
    """

    def __init__(self, access_token=None, refresh_token=None, expires=None):
        """Constructor
        access_token - The token used to access the Questrade API.
        refresh_token - Upon expiration of the access token, this token is used to trigger a refresh
        """
        if expires is not None and refresh_token is not None:
            if expires <= datetime.datetime.now():
                self.refresh(refresh_token)
                return

        if access_token is None and refresh_token is None:
            raise AttributeError("either access_token or refresh_token must be specified.")

        if access_token is not None:
            self.AUTH = Auth()
            self.AUTH.ACCESS_TOKEN = access_token
            return

        if refresh_token is not None:
            self.refresh(refresh_token)

    def refresh(self, refresh_token):
        """Refresh accesses the questrade API, refreshing the access_token
        to be used in API calls.
        refresh_token - The token to be used, exchanging for an access token.
        """

        authapi = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=%s" % refresh_token
        now = datetime.datetime.now()
        r = requests.get(authapi)

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.content)

        self.AUTH = Auth(r.json())

        # rather than constantly recalculate the EXPIRY period for the token
        # we do it once, here.
        self.AUTH.EXPIRES = now + datetime.timedelta(seconds=self.AUTH.EXPIRES_IN)
        return self.AUTH
