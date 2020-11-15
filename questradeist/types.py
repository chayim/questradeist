class QuestradeType:

    def __init__(self, dict=None):
        if dict is not None:
            self._set(dict)

    def _set(self, dict):
        """Given that Questrade returns JSON items, all returns result in a dictionary.
        This function takes the dictionary and sets variables on the class object, for
        each key in the dictionary.
        """
        for k, v in dict.items():
            if k.upper() not in self.fields:
                raise AttributeError("Invalid questrade field response. Missing %s. Received fields: %s" % (k, dict.keys()))
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

class Symbol(QuestradeType):
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