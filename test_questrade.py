import os
import datetime
from questradeist.account import Account
from questradeist.symbol import Symbol


class TestClass():

    SYMBOL = "ENB"
    SYMBOL_ID = 17356

    def _configure(self, klass):
        refresh_token = os.getenv("QUESTRADE_TOKEN", None)
        assert refresh_token is not None

        qt = klass(refresh_token=refresh_token)
        assert qt.access_token is not None
        self.QT = qt

    def test_symbol_search(self):
        """Searching for stock ticker symbols"""
        self._configure(Symbol)
        symbols = self.QT.search(self.SYMBOL)
        assert len(symbols) > 1
        assert symbols[0].SYMBOL == self.SYMBOL
        assert symbols[0].SYMBOLID == self.SYMBOL_ID

        symbols = self.QT.search("ENB", raw=True)
        assert isinstance(symbols, dict)

    def test_symbols(self):
        """Retrieving symbol data"""
        self._configure(Symbol)
        symbols = self.QT.get(symbols=[self.SYMBOL, ])
        assert(symbols[0].SYMBOL == self.SYMBOL)

        symbols = self.QT.get(ids=[self.SYMBOL_ID, ])
        assert(symbols[0].SYMBOL == self.SYMBOL)

        symbols = self.QT.get(ids=[self.SYMBOL_ID, ], raw=True)
        assert isinstance(symbols, dict)

        symbols = self.QT.get(symbols=[self.SYMBOL, ], raw=True)
        assert isinstance(symbols, dict)

    def test_history(self):
        """Retrieving EOD data"""
        self._configure(Symbol)
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
        self._configure(Symbol)
        quotes = self.QT.quotes([self.SYMBOL_ID, ])
        assert(quotes[0].SYMBOL == self.SYMBOL)

        quotes = self.QT.quotes([self.SYMBOL_ID], raw=True)
        assert isinstance(quotes, dict)

    def test_accounts(self):
        """Test fetching accounts"""
        self._configure(Account)
        accounts = self.QT.get_all()
        assert (len(accounts) != 0)
        for ac in accounts:
            assert(int(ac.NUMBER) > 0)

    def test_account_positions(self):
        """Fetching account positions"""
        self._configure(Account)
        accounts = self.QT.get_all()
        positions = self.QT.positions(int(accounts[0].NUMBER))
        assert(len(positions) > 0)
        for p in positions:
            assert(int(p.SYMBOLID) > 0)

    def test_account_activities(self):
        """Fetch the account activities"""
        self._configure(Account)
        accounts = self.QT.get_all()
        today = datetime.datetime.today()
        month_ago = today - datetime.timedelta(days=30)
        activities = self.QT.activities(int(accounts[0].NUMBER), today, month_ago)
        assert(len(activities) > 0)
        for ac in activities:
            print(ac.__dict__)
            assert(ac.SYMBOLID != '')

    def test_account_executions(self):
        """Fetch the account executions"""
        self._configure(Account)
        accounts = self.QT.get_all()
        executions = self.QT.executions(int(accounts[0].NUMBER))
        assert(len(executions) > 0)
        for e in executions:
            assert(e.SYMBOLID != '')

        # now with dates
        today = datetime.datetime.today()
        month_ago = today - datetime.timedelta(days=30)
        executions = self.QT.executions(int(accounts[0].NUMBER), month_ago, today)
        assert(len(executions) > 0)
        for e in executions:
            assert(e.SYMBOLID != '')

    def test_account_currency_balances(self):
        """Fetch the account balances"""
        self._configure(Account)
        accounts = self.QT.get_all()
        executions = self.QT.balances(int(accounts[0].NUMBER))
        assert(len(executions) > 0)
        for e in executions:
            assert(e.CURRENCY != '')

    def test_account_orders(self):
        """Test fetching orders for an account."""
        self._configure(Account)
        accounts = self.QT.get_all()
        today = datetime.datetime.today()
        month_ago = today - datetime.timedelta(days=30)
        orders = self.QT.orders(int(accounts[0].NUMBER), today, month_ago, state='Closed')
        print(orders)
        assert(len(orders) > 0)
        for o in orders:
            assert(o.TOTALQUANTITY > 0)