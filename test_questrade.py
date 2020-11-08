import os
import datetime
from questradeist import Questrade
# TvEaAarTVlULGeB3xx5Tw3vZhw22bBSW0


class TestClass():

    def setup_class(self):
        refresh_token = os.getenv("QUESTRADE_TOKEN", None)
        assert refresh_token is not None

        qt = Questrade(refresh_token=refresh_token)
        assert qt.token is not None
        self.QT = qt

    def test_symbol_search(self):
        symbols = self.QT.symbol_search("ENB")
        assert len(symbols) > 1
        assert symbols[0].SYMBOL == "ENB"
        assert symbols[0].SYMBOLID == 17356

        symbols = self.QT.symbol_search("ENB", raw=True)
        assert isinstance(symbols, dict)

# def test_symbols():
#     qt = Questrade(refresh_token=refresh_token)
#     symbols = qt.symbols("ENB")

# def test_history():
#     qt = Questrade(refresh_token=refresh_token)

    def test_quotes(self):
        quotes = self.QT.quotes([17356, ])
        assert(quotes[0].SYMBOL == "ENB")

        quotes = self.QT.quotes([17356], raw=True)
        assert isinstance(quotes, dict)

# def test_options_quotes():
#     qt = Questrade(refresh_token=refresh_token)

# def test_symbol_options():
#     qt = Questrade(refresh_token=refresh_token)