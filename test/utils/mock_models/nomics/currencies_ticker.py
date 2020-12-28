"""
Database model from the currencies_ticker table in the nomics live database
i.e. nomics_live_db in case nothing was changed
"""

import sqlalchemy as orm
from test.utils.mock_models.config import Base


class CurrenciesTicker(Base):
    """
    Database model for all currencies_ticker realtime data by the nomics API from the /nomics/currencies-ticker endpoint
    """
    __tablename__ = 'currencies_ticker'
    __table_args__ = {'schema': 'currencies'}

    id = orm.Column(orm.Text, primary_key=True)
    price_timestamp = orm.Column(orm.DateTime(timezone=True), primary_key=True)
    interval = orm.Column(orm.VARCHAR(30), primary_key=True)

    currency = orm.Column(orm.Text)
    symbol = orm.Column(orm.Text)
    name = orm.Column(orm.Text)
    logo_url = orm.Column(orm.Text)
    status = orm.Column(orm.Text)
    price = orm.Column(orm.FLOAT(decimal_return_scale=8, precision=20))
    price_date = orm.Column(orm.Date)
    circulating_supply = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    max_supply = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    market_cap = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    num_exchanges = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    num_pairs = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    num_pairs_unmapped = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    first_candle = orm.Column(orm.DateTime(timezone=True))
    first_order_book = orm.Column(orm.DateTime(timezone=True))
    first_trade = orm.Column(orm.DateTime(timezone=True))
    first_priced_at = orm.Column(orm.DateTime(timezone=True))
    rank = orm.Column(orm.Integer)
    rank_delta = orm.Column(orm.Integer)
    high = orm.Column(orm.FLOAT(precision=20, decimal_return_scale=8))
    high_timestamp = orm.Column(orm.DateTime(timezone=True))
    volume = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    price_change = orm.Column(orm.FLOAT(precision=20, decimal_return_scale=8))
    price_change_pct = orm.Column(orm.FLOAT(precision=20, decimal_return_scale=8))
    volume_change = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    volume_change_pct = orm.Column(orm.FLOAT(precision=20, decimal_return_scale=8))
    market_cap_change = orm.Column(orm.FLOAT(precision=15, decimal_return_scale=2))
    market_cap_change_pct = orm.Column(orm.FLOAT(precision=20, decimal_return_scale=8))
    created_at = orm.Column(orm.DateTime(timezone=True))
    updated_at = orm.Column(orm.DateTime(timezone=True))
