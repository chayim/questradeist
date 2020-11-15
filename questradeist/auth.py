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

    def __init__(self, access_token=None, refresh_token=None):
        """Constructor
        access_token - The token used to access the Questrade API.
        refresh_token - Upon expiration of the access token, this token is used to trigger a refresh
        """

        if refresh_token is not None:
            self.AUTH = self.refresh(refresh_token)

        # when only an access token exists
        if access_token is not None:
            if getattr(self, "AUTH", None) is None:
                self.AUTH = Auth()
            self.AUTH.ACCESS_TOKEN = access_token

    def refresh(self, refresh_token):
        """Refresh accesses the questrade API, refreshing the access_token 
        to be used in API calls.
        refresh_token - The token to be used, exchanging for an access token.
        """

        authapi = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=%s" % refresh_token
        now = datetime.datetime.now()
        r = requests.get(authapi)

        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.content.decode('utf-8'))
        
        self.AUTH = Auth(r.json())

        # rather than constantly recalculate the EXPIRY period for the token
        # we do it once, here.
        self.AUTH.EXPIRES = now + datetime.timedelta(seconds=self.AUTH.EXPIRES_IN)
        return self.AUTH