class QuestradeType:
    """This class maps the questrade type data back to python objects. An active choice has been made to raise
    an AttributeError when the Questrade API no longer contains a field, or contains new fields.
    """

    def __init__(self, d=None):
        """Given that Questrade returns JSON items, all returns result in a dictionary.
        This function takes the dictionary and sets variables on the class object, for
        each key in the dictionary.
        """
        if d is None:
            return

        for k, v in d.items():

            # sometimes fields are uppercase, sometimes they aren't
            if k.upper() not in self.fields:
                raise AttributeError("Invalid questrade field response. Missing %s. Received fields: %s" % (k, d.keys()))
            setattr(self, k.upper(), v)


class Auth(QuestradeType):
    """This type contains the results of a questrade auth request"""

    @property
    def fields(self):
        return [
            "ACCESS_TOKEN",
            "REFRESH_TOKEN",
            "EXPIRES_IN",
            "TOKEN_TYPE",
            "API_SERVER",
        ]


class OptionQuote(QuestradeType):
    """This type returns option types"""

    @property
    def fields(self):
        return [
            "UNDERLYING",
            "UNDERLYINGID",
            "SYMBOL",
            "SYMBOLID",
            "BIDPRICE",
            "BIDSIZE",
            "ASKPRICE",
            "ASKSIZE",
            "LASTTRADEPRICETRHRS",
            "LASTTRADEPRICE",
            "LASTTRADESIZE",
            "LASTTRADETICK",
            "LASTTRADETIME",
            "VOLUME",
            "OPENPRICE",
            "HIGHPRICEHIGHPRICE",
            "LOWPRICE",
            "VOLATILITY",
            "DELTA",
            "GAMMA",
            "THETA",
            "VEGA",
            "RHO",
            "OPENINTEREST",
            "DELAY",
            "ISHALTED",
            "VWAP",
        ]


class Quote(QuestradeType):
    """This type contains the results of a stock quote"""

    @property
    def fields(self):
        return [
            "SYMBOL",
            "SYMBOLID",
            "TIER",
            "BIDPRICE",
            "BIDSIZE",
            "ASKPRICE",
            "ASKSIZE",
            "LASTTRADEPRICETRHRS",
            "LASTTRADEPRICE",
            "LASTTRADESIZE",
            "LASTTRADETICK",
            "LASTTRADETIME",
            "VOLUME",
            "OPENPRICE",
            "HIGHPRICE",
            "LOWPRICE",
            "DELAY",
            "ISHALTED",
            "HIGH52W",
            "LOW52W",
            "VWAP",
        ]


class SearchSymbol(QuestradeType):
    """This type contains the results of a stock symbol search"""

    @property
    def fields(self):
        return [
            "SYMBOL",
            "SYMBOLID",
            "DESCRIPTION",
            "SECURITYTYPE",
            "LISTINGEXCHANGE",
            "ISTRADABLE",
            "ISQUOTABLE",
            "CURRENCY",
        ]


class SymbolData(QuestradeType):
    """This type contains the results of a stock symbol fetch"""

    @property
    def fields(self):
        return [
            "SYMBOL",
            "SYMBOLID",
            "PREVDAYCLOSEPRICE",
            "HIGHPRICE52",
            "LOWPRICE52",
            "AVERAGEVOL3MONTHS",
            "AVERAGEVOL20DAYS",
            "OUTSTANDINGSHARES",
            "EPS",
            "PE",
            "DIVIDEND",
            "YIELD",
            "EXDATE",
            "MARKETCAP",
            "TRADEUNIT",
            "OPTIONTYPE",
            "OPTIONDURATIONTYPE",
            "OPTIONROOT",
            "OPTIONCONTRACTDELIVERABLES",
            "OPTIONEXERCISETYPE",
            "LISTINGEXCHANGE",
            "DESCRIPTION",
            "SECURITYTYPE",
            "OPTIONEXPIRYDATE",
            "DIVIDENDDATE",
            "OPTIONSTRIKEPRICE",
            "ISTRADABLE",
            "ISQUOTABLE",
            "HASOPTIONS",
            "CURRENCY",
            "MINTICKS",
            "INDUSTRYSECTOR",
            "INDUSTRYGROUP",
            "INDUSTRYSUBGROUP",
        ]


class Candle(QuestradeType):
    """Historic end of day data"""

    @property
    def fields(self):
        return [
            "START",
            "END",
            "LOW",
            "HIGH",
            "OPEN",
            "CLOSE",
            "VOLUME",
            "VWAP",
        ]


class TradingAccount(QuestradeType):
    """Trading accounts, as held in questrade"""

    @property
    def fields(self):
        return [
            "TYPE",
            "NUMBER",
            "STATUS",
            "ISPRIMARY",
            "ISBILLING",
            "CLIENTACCOUNTTYPE"
        ]


class AccountPosition(QuestradeType):
    """The positions, i.e shares held by a trading account"""

    @property
    def fields(self):
        return [
            "SYMBOL",
            "SYMBOLID",
            "OPENQUANTITY",
            "CLOSEDQUANTITY",
            "CURRENTMARKETVALUE",
            "CURRENTPRICE",
            "AVERAGEENTRYPRICE",
            "DAYPNL",
            "CLOSEDPNL",
            "OPENPNL",
            "TOTALCOST",
            "ISREALTIME",
            "ISUNDERREORG"
        ]


class AccountActivity(QuestradeType):
    """Account activities - the actions (dividends, buy, sell, etc) that took place in a trading account"""

    @property
    def fields(self):
        return [
            "TRADEDATE",
            "TRANSACTIONDATE",
            "SETTLEMENTDATE",
            "ACTION",
            "SYMBOL",
            "SYMBOLID",
            "DESCRIPTION",
            "CURRENCY",
            "QUANTITY",
            "PRICE",
            "GROSSAMOUNT",
            "COMMISSION",
            "NETAMOUNT",
            "TYPE",
        ]


class AccountExecution(QuestradeType):
    """Executions - The individual actions that took place within an account, to close trades."""

    @property
    def fields(self):
        return [
            "SYMBOL",
            "SYMBOLID",
            "QUANTITY",
            "SIDE",
            "PRICE",
            "ID",
            "ORDERID",
            "ORDERCHAINID",
            "EXCHANGEEXECID",
            "TIMESTAMP",
            "NOTES",
            "VENUE",
            "TOTALCOST",
            "ORDERPLACEMENTCOMMISSION",
            "COMMISSION",
            "EXECUTIONFEE",
            "SECFEE",
            "LEGID",
            "CANADIANEXECUTIONFEE",
            "PARENTID",
        ]