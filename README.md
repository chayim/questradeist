# Questradeist

Questradeist is a python library for dealing with the [Questrade API](https://api.quesrade.com). This API was built to make it as pythonic as possible to retrieve data from Questrade.

To access Questrade via the API, you will need to [generate an API key](https://www.questrade.com/api/documentation/getting-started). From that point on, all interactions take place, as documented in the [unit tests](blob/master/test_questrade.py).

## Contributing

If you'd like to contribute a change, please create an issue, and make a pull request. If your pull request contains code, but not a unit test, it will be rejected.

## Why another library?

*More pythonic*

Other libraries return the raw JSON. Primarily I want Python objects - except for when I want raw JSON. This library provides both, as needed.

*No local storage*

Other implementations store the questrade token on local disk. This doesn't.

*Passing a callable in questradeist.Questrade*

I use this library by authenticating, and then storing the resulting tokens in an encrypted key value store. By passing a function to the varying Questrade one can cache the resulting output.