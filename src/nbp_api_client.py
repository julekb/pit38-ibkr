from datetime import date

from src.core import Currency


class NBPClient:
    # see https://api.nbp.pl/
    API_URL = "https://api.nbp.pl/api/"

    @staticmethod
    def get_middle_exchange_rate_for_year(self, currency: Currency, year: int):
        if not 2020 < year <= date.today().year:
            raise ValueError(f"Cannot request rates for year {year}.")
        # exchangerates / rates / a / gbp / 2012 - 01 - 01 / 2012 - 12 - 31 /
