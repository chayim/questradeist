import requests
from .types import Auth


class QuestradeAuth(object):

    def __init__(self, access_token=None, refresh_token=None):
        if refresh_token is not None:
            self.AUTH = self.refresh(refresh_token)

        if access_token is not None:
            if getattr(self, "AUTH", None) is None:
                self.AUTH = Auth()
            self.AUTH.ACCESS_TOKEN = access_token

    def refresh(self, refresh_token):

        authapi = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=%s" % refresh_token

        r = requests.get(authapi)
        if r.status_code >= 204:
            raise requests.exceptions.HTTPError(r.content.decode('utf-8'))
        
        self.AUTH = Auth(r.json())
        return self.AUTH