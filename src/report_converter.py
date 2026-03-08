import abc
import dataclasses
from enum import StrEnum
from typing import Iterable

from src.transactions import ReportDFFType


class RowType(StrEnum):
    HEADER = "HEADER"
    DATA = "DATA"


class ColEnum(StrEnum, abc.ABC):
    ...


class ColConfig(StrEnum, abc.ABC):
    ...


class SectionMeta(abc.ABC):
    section_name: str
    columns: ColEnum


class TradeCols(ColEnum):
    TRADE_CURRENCY = "CurrencyPrimary"
    ASSET_TYPE = "AssetClass"
    ASSET_SUBTYPE = "SubCategory"
    SYMBOL = "Symbol"
    TRANSACTION_DATE = "TradeDate"
    TRANSACTION_TYPE = "TransactionType"
    TRANSACTION_SIZE = "Quantity"
    COMMISSION_IB = "IBCommission"
    COMMISSION_IB_CUR = "IBCommissionCurrency"


@dataclasses.dataclass
class ReportExtractor:
    ROW_TYPE = RowType

    sections: list[SectionMeta]

    _files_read: list = dataclasses.field(default_factory=list)

    def _validate_csv(self, f) -> None:
        """
        Check that a file f has all sections
        if not, raise ReportExtractionValidationError
        """

    def extract_file(self, f) -> ReportDFFType:
        """Extract data from a file, add to _files_read"""

    def extract_files(self, files) -> ReportDFFType:
        """Extract from multiple files and merge to one dataset object"""


