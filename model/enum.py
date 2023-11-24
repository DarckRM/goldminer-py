from enum import Enum

class V_Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    HOUR = "1h"
    DAILY = "1d"
    WEEKLY = "1w"
    TICK = "tick"

class Interval(Enum):
    """
    CAUTIOUS: This enum class is for GoldMiner it's not exactly same with VVTR.Interval
    Interval of bar data.
    """
    MINUTE = "60s"
    FIVE_MINUTES = "300s"
    FIFTEEN_MINUTES = "900s"
    HOUR = "3600s"
    DAILY = "1d"
    WEEKLY = "1w"
    TICK = "tick"

class ExchangeMarket(Enum):
    """
    Exchange market.
    """
    Market_CSE = "CSE"
    Market_SEHK = "SEHK"
    Market_CFUTURE = "CFUTURE"
    Market_SMART = "SMART"


class Exchange(Enum):
    """
    Exchange.
    """
    # Chinese
    CSE = "CSE"  # China Stock Exchange
    SSE = "SSE"  # Shanghai Stock Exchange
    SZSE = "SZSE"  # Shenzhen Stock Exchange
    SEHK = "SEHK"  # Stock Exchange of Hong Kong

    # CN futures
    CFUTURE = "CFUTURE"  # China Futures Exchange
    CFFEX = "CFFEX"  # China Financial Futures
    SHFE = "SHFE"  # Shanghai Futures Exchange
    CZCE = "CZCE"  # Zhengzhou Commodity
    DCE = "DCE"  # Dalian Commodity Exchange
    INE = "INE" # Shanghai International Energy Exchange
    GFEX = "GFEX" # Guangzhou Futures Exchange

    # Global
    SMART = "SMART"  # Smart Router for US stocks

class Product(Enum):
    """
    Product class.
    """
    EQUITY = "股票"
    OPTION = "期权"
    FUTURES = "期货"
    INDEX = "指数"
    FOREX = "外汇"
    SPOT = "现货"
    ETF = "ETF"
    BOND = "债券"
    WARRANT = "权证"
    SPREAD = "价差"
    FUND = "基金"


class OptionType(Enum):
    """
    Option type.
    """
    CALL = "看涨期权"
    PUT = "看跌期权"


class Adjust(Enum):
    NONE: int = 0 # 不复权
    PREV: int = 1 # 前复权
    POST: int = 2 # 后复权