from enum import StrEnum


class Currency(StrEnum):
    PLN = "pln"
    EUR = "eur"
    USD = "usd"


class Transaction(StrEnum):
    BUY = "buy"
    SELL = "sell"



