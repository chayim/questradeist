import os
import datetime
from questradeist import Questrade


class TestClass():

    SYMBOL = "ENB"
    SYMBOL_ID = 17356

    def setup_class(self):
        refresh_token = os.getenv("QUESTRADE_TOKEN", None)
        assert refresh_token is not None

        qt = Questrade(refresh_token=refresh_token)
        assert qt.access_token is not None
        self.QT = qt

    def test_symbol_search(self):
        """Searching for stock ticker symbols"""
        symbols = self.QT.symbol_search(self.SYMBOL)
        assert len(symbols) > 1
        assert symbols[0].SYMBOL == self.SYMBOL
        assert symbols[0].SYMBOLID == self.SYMBOL_ID

        symbols = self.QT.symbol_search("ENB", raw=True)
        assert isinstance(symbols, dict)

    def test_symbols(self):
        """Retrieving symbol data"""
        symbols = self.QT.symbols(symbols=[self.SYMBOL,])
        assert(symbols[0].SYMBOL == self.SYMBOL)

        symbols = self.QT.symbols(ids=[self.SYMBOL_ID,])
        assert(symbols[0].SYMBOL == self.SYMBOL)

        symbols = self.QT.symbols(ids=[self.SYMBOL_ID,], raw=True)
        assert isinstance(symbols, dict)

        symbols = self.QT.symbols(symbols=[self.SYMBOL,], raw=True)
        assert isinstance(symbols, dict)

    def test_history(self):
        """Retrieving EOD data"""
        end_time = datetime.datetime.today()
        start_time = end_time - datetime.timedelta(days=30)
        prices = self.QT.history(self.SYMBOL_ID, start_time, end_time)
        assert len(prices) > 10
        for p in prices:
            assert p.VOLUME != 0

        prices = self.QT.history(self.SYMBOL_ID, start_time, end_time, raw=True)
        assert isinstance(prices, dict)

    def test_quotes(self):
        """Fetching latest prices for a ticker symbol"""
        quotes = self.QT.quotes([self.SYMBOL_ID, ])
        assert(quotes[0].SYMBOL == self.SYMBOL)

        quotes = self.QT.quotes([self.SYMBOL_ID], raw=True)
        assert isinstance(quotes, dict)