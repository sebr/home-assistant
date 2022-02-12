"""Define package errors."""


class BHyveError(Exception):
    """Define a base error."""


class RequestError(BHyveError):
    """Define an error related to invalid requests."""


class WebsocketError(BHyveError):
    """Define an error related to generic websocket errors."""
