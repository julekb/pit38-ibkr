import csv
import dataclasses
import datetime as dt
from enum import StrEnum
from typing import Iterable, TextIO, cast

from strictly_typed_pandas import DataSet

from core import Currency, Transaction
from exceptions import ReportExtractionValidationError
from transactions import ReportDFFType, ReportDFSchema


class RowType(StrEnum):
    HEADER = "HEADER"
    DATA = "DATA"


class ColEnum(StrEnum): ...


class ColConfig(StrEnum): ...


@dataclasses.dataclass(frozen=True)
class SectionMeta:
    section_name: str
    columns: type[ColEnum]


class TradeCols(ColEnum):
    TRADE_CURRENCY = "CurrencyPrimary"
    ASSET_TYPE = "AssetClass"
    ASSET_SUBTYPE = "SubCategory"
    SYMBOL = "Symbol"
    TRANSACTION_DATE = "TradeDate"
    TRANSACTION_SETTLEMENT_DATE = "SettleDateTarget"
    TRANSACTION_TYPE = "TransactionType"
    BUY_SELL = "Buy/Sell"
    TRANSACTION_SIZE = "Quantity"
    TRADE_PRICE = "TradePrice"
    COMMISSION_IB = "IBCommission"
    COMMISSION_IB_CUR = "IBCommissionCurrency"


@dataclasses.dataclass
class ReportExtractor:
    ROW_TYPE = RowType

    sections: list[SectionMeta]

    _files_read: list[str] = dataclasses.field(default_factory=list)

    @staticmethod
    def _required_columns(columns: type[ColEnum]) -> set[str]:
        return {
            column.value for column in columns if column != TradeCols.TRANSACTION_SETTLEMENT_DATE
        }

    @staticmethod
    def _rewind_file(f: TextIO) -> None:
        f.seek(0)

    def _validate_csv(self, f: TextIO) -> None:
        """
        Check that a file f has all sections
        if not, raise ReportExtractionValidationError
        """
        self._rewind_file(f)
        reader = csv.reader(f)

        found_sections: dict[str, set[str]] = {}
        for row in reader:
            if len(row) < 3:
                continue
            if row[0] != self.ROW_TYPE.HEADER:
                continue

            section_name = row[1]
            found_sections[section_name] = set(row[2:])

        missing_sections: list[str] = []
        missing_columns: dict[str, list[str]] = {}

        for section in self.sections:
            if section.section_name not in found_sections:
                missing_sections.append(section.section_name)
                continue

            required = self._required_columns(section.columns)
            available = found_sections[section.section_name]
            diff = sorted(required - available)
            if diff:
                missing_columns[section.section_name] = diff

        errors: list[str] = []
        if missing_sections:
            errors.append(f"missing sections: {', '.join(sorted(missing_sections))}")
        if missing_columns:
            details = "; ".join(
                f"{name}: {', '.join(cols)}" for name, cols in sorted(missing_columns.items())
            )
            errors.append(f"missing columns: {details}")

        self._rewind_file(f)
        if errors:
            raise ReportExtractionValidationError(" | ".join(errors))

    def extract_file(self, f: TextIO) -> ReportDFFType:
        """Extract data from a file, add to _files_read"""
        self._validate_csv(f)
        reader = csv.DictReader(f)

        rows: list[dict[str, str | float | dt.date | Currency | Transaction]] = []
        for row in reader:
            if row.get(self.ROW_TYPE.HEADER) != self.ROW_TYPE.DATA:
                continue
            if row.get("TRNT") != "TRNT":
                continue

            symbol = row.get(TradeCols.SYMBOL.value)
            currency_raw = row.get(TradeCols.TRADE_CURRENCY.value)
            side_raw = row.get(TradeCols.BUY_SELL.value)
            size_raw = row.get(TradeCols.TRANSACTION_SIZE.value)
            price_raw = row.get(TradeCols.TRADE_PRICE.value)
            settlement_date_raw = row.get(TradeCols.TRANSACTION_SETTLEMENT_DATE.value) or row.get(
                TradeCols.TRANSACTION_DATE.value
            )

            if not symbol or not currency_raw or not side_raw:
                continue
            if size_raw is None or price_raw is None or settlement_date_raw is None:
                continue

            rows.append(
                {
                    "symbol": symbol,
                    "currency": Currency(currency_raw.lower()),
                    "transaction_type": Transaction(side_raw.lower()),
                    "size": float(size_raw),
                    "price": float(price_raw),
                    "settlement_date": dt.date.fromisoformat(settlement_date_raw),
                }
            )

        dataset = DataSet[ReportDFSchema].from_records(rows)

        file_name = getattr(f, "name", "<in-memory>")
        self._files_read.append(str(file_name))
        self._rewind_file(f)
        return dataset

    def extract_files(self, files: Iterable[TextIO]) -> ReportDFFType:
        """Extract from multiple files and merge to one dataset object"""
        extracted_rows: list[dict[str, str | float | dt.date | Currency | Transaction]] = []

        for f in files:
            data = self.extract_file(f)
            extracted_rows.extend(
                cast(
                    list[dict[str, str | float | dt.date | Currency | Transaction]],
                    data.to_dict("records"),
                )
            )

        extracted_rows.sort(key=lambda row: cast(dt.date, row["settlement_date"]))

        return DataSet[ReportDFSchema].from_records(extracted_rows)
