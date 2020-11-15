from questradeist.types import QuestradeType
from .auth import QuestradeAuth
from .types import *
from typing import Optional
import datetime
import requests
from urllib.parse import urljoin


class Questrade(object):

    def __init__(self, access_token: str=None, refresh_token: str=None):
        qtauth = QuestradeAuth(access_token, refresh_token)
        self._setup(qtauth)

    def _setup(self, qtauth):
        """Setup embeds the questrade AUTH api results into this class."""
        setattr(self, "ACCESS_TOKEN", qtauth.AUTH.ACCESS_TOKEN)
        setattr(self, "REFRESH_TOKEN", qtauth.AUTH.REFRESH_TOKEN)
        setattr(self, "API_SERVER", qtauth.AUTH.API_SERVER)
        setattr(self, "EXPIRES", qtauth.AUTH.EXPIRES)

    @property
    def access_token(self):
        """Returns the access token"""
        return self.ACCESS_TOKEN

    @property
    def expires(self):
        """Returns the time the access token expires"""
        return self.EXPIRES

    @property
    def server(self):
        """Returns the API server to be used in Questrade calls"""
        return self.API_SERVER

    @property
    def refresh_token(self):
        """Returns the refresh token to be exchanged for an access token"""
        return self.REFRESH_TOKEN

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
                qtauth = QuestradeAuth(refresh_token=self.REFRESH_TOKEN)
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
            qt = qtype(o)
            qts.append(qt)
        return qts

    def symbols(self, ids: Optional[int]=None, symbols: Optional[str]=None, raw: Optional[bool]=False):
        """Retrieve detailed information about one or more symbol.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id

        ids - A list of one or more questrade stock symbol ids.
        symbols - A list of one or more stock symbols.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        if not ids and not symbols or ids is not None and symbols is not None:
            raise AttributeError("either a list of ids or symbols must be specified")
        
        if ids:
            qids = ','.join(str(i) for i in ids)
            url = urljoin(self.server, "/v1/symbols/?ids=%s" % qids)
        if symbols:
            qnames = ','.join(symbols)
            url = urljoin(self.server, "/v1/symbols/?names=%s" % qnames)

        return self._request(url, qtype=Symbol, key="symbols", raw=raw)

    def symbol_search(self, sym: str, raw: Optional[bool]=False):
        """Search questrade for a matching stock symbol.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-search
        sym: A string containing a stock symbol
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        url = urljoin(self.server, "/v1/symbols/search?prefix=%s" % sym)
        return self._request(url, qtype=SearchSymbol, key="symbols", raw=raw)

    def quotes(self, ids: list[int], raw: Optional[bool]=False):
        """Retrieves the most recent quote data for a list of stock symbols.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-id
        ids - A list of questrade IDs whose stock quote data is to be retrieved.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        qids = ','.join(str(i) for i in ids)
        url = urljoin(self.server, "/v1/markets/quotes?ids=%s" % qids)
        return self._request(url, qtype=Quote, key="quotes", raw=raw)

    def history(self, id: int, start: datetime.datetime, end: datetime.datetime, interval: str="OneDay", raw: Optional[bool]=False):
        """Returns historical market data in an OHLC candlesick, for the provided symbol.
        id - An integer containing the internal questrade ID.
        start - The start time of the candle.
        end - The end time of the candle.
        interval - The interval for the candle data.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        if start > end:
            start_date = end.strftime("%Y-%m-%dT00:00:00.000000-05:00")
            end_date = start.strftime("%Y-%m-%dT00:00:00.000000-05:00")
        else:
            start_date = start.strftime("%Y-%m-%dT00:00:00.000000-05:00")
            end_date = end.strftime("%Y-%m-%dT00:00:00.000000-05:00")

        url = urljoin(self.server, "/v1/markets/candles/%s?startTime=%s&endTime=%s&interval=%s" % (id, start_date, end_date, interval))
        return self._request(url, qtype=Candle, key="candles", raw=raw)