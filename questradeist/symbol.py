from .questrade import Questrade, to_datestring
import datetime
from typing import Optional
from urllib.parse import urljoin
from .types import Candle, Quote, SymbolData, SearchSymbol


class Symbol(Questrade):
    """This class communicates with the various symbol APIs in order to provide
    symbol data such as price history and current quotes.
    """

    def __init__(self, **kwargs):
        Questrade.__init__(self, **kwargs)

    def get(self, ids: Optional[int]=None, symbols: Optional[str]=None, raw: Optional[bool]=False):
        """Retrieve detailed information about one or more symbol.
        https://www.questrade.com/api/documentation/rest-operations/market-calls/symbols-id

        ids - A list of one or more questrade stock symbol ids.
        symbols - A list of one or more stock symbols.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        if not ids and not symbols or ids is not None and symbols is not None:
            raise AttributeError("either a list of ids or symbols must be specified")

        url = None
        if ids:
            qids = ','.join(str(i) for i in ids)
            url = urljoin(self.server, "/v1/symbols/?ids=%s" % qids)

        if symbols:
            qnames = ','.join(symbols)
            url = urljoin(self.server, "/v1/symbols/?names=%s" % qnames)

        return self._request(url, qtype=SymbolData, key="symbols", raw=raw)

    def search(self, sym: str, raw: Optional[bool]=False):
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
        https://www.questrade.com/api/documentation/rest-operations/market-calls/markets-candles-id

        id - An integer containing the internal questrade ID.
        start - The start time of the candle.
        end - The end time of the candle.
        interval - The interval for the candle data.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        if start > end:
            start_date = to_datestring(end)
            end_date = to_datestring(start)
        else:
            start_date = to_datestring(start)
            end_date = to_datestring(end)

        url = urljoin(self.server, "/v1/markets/candles/%s?startTime=%s&endTime=%s&interval=%s" % (id, start_date, end_date, interval))
        return self._request(url, qtype=Candle, key="candles", raw=raw)