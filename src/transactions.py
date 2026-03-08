from src.core import Currency, Transaction

from strictly_typed_pandas import DataSet


class ReportDFSchema:
    symbol: str
    currency: Currency
    transaction_type: Transaction
    size: float
    price: float


ReportDFFType = DataSet[ReportDFSchema]






