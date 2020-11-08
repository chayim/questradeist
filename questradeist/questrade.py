from questradeist.types import QuestradeType
from .auth import QuestradeAuth
from .types import *
from typing import Optional
import datetime
import requests
from urllib.parse import urljoin


class Questrade(object):

    def __init__(self, access_token=None, refresh_token=None):
        self._QTAUTH_ = QuestradeAuth(access_token, refresh_token)

    @property
    def token(self):
        return self._QTAUTH_.AUTH.ACCESS_TOKEN

    @property
    def expiry(self):
        return self._QTAUTH_.AUTH.EXPIRES_IN

    @property
    def server(self):
        return self._QTAUTH_.AUTH.API_SERVER

    def _request(self, url: str, qtype: QuestradeType, key: str=None, raw: bool=False):
        header = {"Authorization": "Bearer %s" % self.token}
        r = requests.get(url, headers=header)
        if r.status_code != 200:
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

    def symbols(self, ids: Optional[int], symbols: Optional[str], raw: Optional[bool]=False):
        """
        Retrieves detailed information about one or more symbol.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id

        ids - A list of one or more questrade stock symbol ids.
        symbols - A list of one or more stock symbols.
        """
        if not ids and not symbols:
            raise AttributeError("either a list of ids or symbols must be specified")
        
        if ids:
            qids = ','.join(str(i) for i in ids)
            url = urljoin(self.server, "/v1/symbols/?ids=%s" % qids)
        if symbols:
            qnames = ','.join(symbols)
            url = "%s/v1/symbols/?names=%s" % (self.server, qnames)

        return self._request(url, qtype=Symbol, key="symbols", raw=raw)

    def symbol_options(self, id: int, raw: Optional[bool]=False):
        """
        Retrieves an option chain for a particular underlying symbol.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id-options

        id - The questrade id for a stock ticker.
        """
        url = urljoin(self.server, "/v1/symbols/%d/options" % id)

    def symbol_search(self, sym: str, raw: Optional[bool]=False):
        """
        Searches for stock symbols
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-search
        sym: A string containing a stock symbol
        """
        url = urljoin(self.server, "/v1/symbols/search?prefix=%s" % sym)
        return self._request(url, qtype=SearchSymbol, key="symbols", raw=raw)

    def quotes(self, ids: list[int], raw: Optional[bool]=False):
        qids = ','.join(str(i) for i in ids)
        url = urljoin(self.server, "/v1/markets/quotes?ids=%s" % qids)
        return self._request(url, qtype=Quote, key="quotes", raw=raw)

    def history(self, id: int, start: datetime.datetime, end: datetime.datetime, interval: str="OneDay", raw: Optional[bool]=False):
        start_date = start.strftime("%Y-%m-%dT00:00:00.000000-05:00")
        end_date = end.strftime("%Y-%m-%dT00:00:00.000000-05:00")
        url = urljoin(self.server, "/v1/markets/candles/%s?startTime=%s&endTime=%s&interval=%s" % (id, start_date, end_date, interval))
        return self._request(url, qtype=Candle, key="candles", raw=raw)

    def options_quotes(self, filters: list[dict], ids: list[int], raw: Optional[bool]=False):
        """Retrieves a single Level 1 market data quote and Greek data for one or more option symbols.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/markets-quotes-options

        filters: A list of dictinaries containing the fields:
            {optionType: Call|Put,
             underlyingId: symbol_id [REQUIRED],
             expiryDate: datetime [REQUIRED],
             minstrikePrice: float,
             maxstrikePrice: float
            }

        ids: A list of questrade option ids
        """
        # POST
        payload = {}
        payload["optionIds"] = ids
        payload["filters"] = filters

        # url = "%s/v1/markets/quotes/options" % self.server
        # return self._request(url, qtype=Candle, key="optionQuotes", raw=raw)