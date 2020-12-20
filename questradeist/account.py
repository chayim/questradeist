from .questrade import Questrade, to_datestring
import datetime
from typing import Optional
from urllib.parse import urljoin
from .types import AccountActivity, AccountExecution, AccountPosition, TradingAccount


class Account(Questrade):
    """This class communicates with the Questrade Account APIs, in order to retrieve
    accunt-specific data.
    """

    def __init__(self, **kwargs):
        Questrade.__init__(self, **kwargs)

    def get_all(self, raw: Optional[bool]=False):
        """Returns the list of accounts associated.
        https://www.questrade.com/api/documentation/rest-operations/account-calls/accounts

        raw - If set, return the raw JSON rather than objects of qtype.
        """
        url = urljoin(self.server, "/v1/accounts")
        return self._request(url, qtype=TradingAccount, key="accounts", raw=raw)

    def positions(self, id: int, raw: Optional[bool]=False):
        """Return positions held by the specified account.
        https://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-positions

        id - An integer containing the account ID.
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        url = urljoin(self.server, "/v1/accounts/%d/positions" % id)
        return self._request(url, qtype=AccountPosition, key="positions", raw=raw)

    def activities(self, id: int, start: datetime.datetime, end: datetime.datetime, raw: Optional[bool]=False):
        """Return the account activities - actions including buys, sells, and dividends, amongst other things.
        https://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-activities

        id - An integer containing the account ID.
        start - The start time of transactions
        end - The end time of the transactons
        raw - If set, return the raw JSON rather than objects of qtype.
        """
        if start > end:
            start_date = to_datestring(end)
            end_date = to_datestring(start)
        else:
            start_date = to_datestring(start)
            end_date = to_datestring(end)

        url = urljoin(self.server, "/v1/accounts/%d/activities/?startTime=%s&endTime=%s" % (id, start_date, end_date))
        return self._request(url, qtype=AccountActivity, key="activities", raw=raw)

    def executions(self, id: int, start: Optional[datetime.datetime]=None, end: Optional[datetime.datetime]=None, raw: Optional[bool]=False):
        """Return the account executions - actions including buys, sells, and dividends, amongst other things.
        https://www.questrade.com/api/documentation/rest-operations/account-calls/accounts-id-executions

        id - An integer containing the account ID.
        start - The start time of transactions
        end - The end time of the transactons
        raw - If set, return the raw JSON rather than objects of qtype.
        """

        if start is None:
            url = urljoin(self.server, "/v1/accounts/%d/executions" % id)
            return self._request(url, qtype=AccountExecution, key="executions", raw=raw)

        start_date, end_date = None, None
        if start > end:
            start_date = to_datestring(end)
            end_date = to_datestring(start)
        else:
            start_date = to_datestring(start)
            end_date = to_datestring(end)

        url = urljoin(self.server, "/v1/accounts/%d/executions?startTime=%s&endTime=%s" % (id, start_date, end_date))
        return self._request(url, qtype=AccountExecution, key="executions", raw=raw)