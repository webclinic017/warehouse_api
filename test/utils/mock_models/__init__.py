"""Entry point for all mock models"""

from .config import Base

# nomics
from .nomics.currencies import Currencies
from .nomics.currencies_ticker import CurrenciesTicker

# tokyo_commodities_exchange
from .tokyo_commodities_exchange.quotes_by_day_session import QuotesByDaySession
from .tokyo_commodities_exchange.quotes_by_night_session import QuotesByNightSession
from .tokyo_commodities_exchange.quotes_by_trade_date import QuotesByTradeDate

