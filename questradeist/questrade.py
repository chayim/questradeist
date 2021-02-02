from questradeist.types import QuestradeType
from urllib.parse import urljoin
from .auth import QuestradeAuth
import datetime
import requests


def to_datetime(date):
    """A uniform function for parsing a questrade date and returning a datetime object."""
    return datetime.datetime.strptime(date, "%Y-%m-%dT00:00:00.000000-%H:%M")


def to_datestring(date):
    """A uniform function for formatting datetime objects like the strings Questrade expects."""
    return datetime.datetime.strftime(date, "%Y-%m-%dT00:00:00.00-05:00")


class Questrade(object):
    """This is the base call for all questrade operations."""

    def __init__(self, access_token: str=None, refresh_token: str=None, f: callable=None, expires: datetime.datetime=None):
        qtauth = QuestradeAuth(access_token, refresh_token, expires)
        self._setup(qtauth, f)

    def _setup(self, qtauth, f: callable=None):
        """Setup embeds the questrade AUTH api results into this class."""
        setattr(self, "ACCESS_TOKEN", qtauth.AUTH.ACCESS_TOKEN)
        setattr(self, "REFRESH_TOKEN", qtauth.AUTH.REFRESH_TOKEN)
        setattr(self, "API_SERVER", qtauth.AUTH.API_SERVER)
        setattr(self, "EXPIRES", qtauth.AUTH.EXPIRES)

        if f:
            f(qtauth.AUTH)

    @property
    def access_token(self):
        """Returns the access token"""
        return self.ACCESS_TOKEN

    @property
    def refresh_token(self):
        """Returns the refresh token"""
        return self.REFRESH_TOKEN

    @property
    def expires(self):
        """Returns the time the access token expires"""
        return self.EXPIRES

    @property
    def server(self):
        """Returns the API server to be used in Questrade calls"""
        return self.API_SERVER

    def time(self):
        """Call the Questrade time api, and return the time associated
        with the service.
        """
        url = urljoin(self.server, "/v1/time")
        return self._request(url, qtype=None, raw=True)

    def _request(self, url: str, qtype: QuestradeType, key: str=None, raw: bool=False):
        """This is a request wrapper. It's meant to be called by other functions.
        qtype - The types.Questrade object that should be used for deserializing data.
        key - A string, containing the key within the Questrade API response, that contains the response elements.
        raw - If set, return the raw JSON rather than objects of qtype.
        """

        header = {"Authorization": "Bearer %s" % self.access_token}
        r = requests.get(url, headers=header)
        if r.status_code != 200:

            # at least try to trigger a refresh if authentication fails.
            if datetime.datetime.now() > self.expires:
                qtauth = QuestradeAuth(refresh_token=self.refresh_token)
                self._setup(qtauth)
                r = requests.get(url, headers=header)
                if r.status_code != 200:
                    raise OSError(r.content.decode('utf-8'))
            else:
                raise OSError(r.content.decode('utf-8'))

        if raw:
            return r.json()

        if key is not None:
            objs = r.json()[key]
        else:
            objs = r.json()

        qts = []
        for o in objs:
            qt = qtype(d=o)
            qts.append(qt)
        return qts
