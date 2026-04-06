import datetime as dt

from strictly_typed_pandas import DataSet

from core import Currency, Transaction


class ReportDFSchema:
    symbol: str
    currency: Currency
    transaction_type: Transaction
    size: float
    price: float
    settlement_date: dt.date


type ReportDFFType = DataSet[ReportDFSchema]
