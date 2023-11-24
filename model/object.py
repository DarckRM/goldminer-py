from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from model.enum import Exchange, Interval, OptionType, Product


class TickQuotes:
    def __init__(self, bid_p: float = 0, bid_v: int = 0, ask_p: float = 0, ask_v: int = 0):
        self.bid_p: float = bid_p
        self.bid_v: int = bid_v
        self.ask_p: float = ask_p
        self.ask_v: int = ask_v


class TickData:
    def __init__(
            self,
            symbol: str,
            name: str,
            create_time: int,
            update_time: int,
            latest_price: float,
            pre_close: float,
            quotes: List[TickQuotes] = []
    ):
        self.symbol: str = symbol  # 股票代码
        self.name: str = name  # 股票名称

        self.create_time: int = create_time  # 行情对应时间
        self.update_time: int = update_time  # 记录更新时间

        self.latest_price: float = latest_price  # 最新价
        self.pre_close: float = pre_close  # 昨日收盘价
        self.quotes: List[TickQuotes] = quotes # 五档价格


@dataclass
class BaseData:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    gateway_name: str

    extra: dict = field(default=None, init=False)


@dataclass
class ContractData(BaseData):
    """
    Contract data contains basic information about each contract traded.
    """

    symbol: str
    exchange: Exchange
    name: str
    product: Product
    size: float
    pricetick: float

    pre_settle: float = 0
    pre_close: float = 0
    multiplier: int = 1
    margin_ratio: float = 1
    min_volume: float = 1  # minimum trading volume of the contract
    stop_supported: bool = False  # whether server supports stop order
    net_position: bool = False  # whether gateway uses net position volume
    history_data: bool = False  # whether gateway provides bar history data

    option_strike: float = 0
    option_underlying: str = ""  # vt_symbol of underlying contract
    option_type: OptionType = None
    option_listed: datetime = None
    option_expiry: datetime = None
    option_portfolio: str = ""
    option_index: str = ""  # for identifying options with same strike price
    option_latest_price: float = 0

    option_delta: float = 0
    option_gamma: float = 0
    option_vega: float = 0
    option_theta: float = 0
    option_rho: float = 0
    option_open_interest: float = 0
    option_implied_volatility: float = 0
    option_pre_close: float = 0

    is_st: bool = False
    is_suspended: bool = False
    listed_date: datetime = datetime.fromtimestamp(86400)
    delisted_date: datetime = datetime.fromtimestamp(2524579200)

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"


@dataclass
class BarData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """

    symbol: str
    exchange: Exchange
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    avg_price: float = 0
    open_interest: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"


class StockBriefData:
    def __init__(self, vt_symbol:str, pre_close: float = 0, latest_price: float = 0, quotes: List[TickQuotes] = []):
        self.vt_symbol: str = vt_symbol
        self.pre_close: float = pre_close
        self.latest_price: float = latest_price
        self.quotes: List[TickQuotes] = quotes