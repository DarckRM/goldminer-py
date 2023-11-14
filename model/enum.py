from enum import Enum


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "60s"
    FIVE_MINUTES = "300s"
    FIFTEEN_MINUTES = "900s"
    HOUR = "3600s"
    DAILY = "1d"
    WEEKLY = "1w"
    TICK = "tick"

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

class Adjust(Enum):
    NONE: int = 0 # 不复权
    PREV: int = 1 # 前复权
    POST: int = 2 # 后复权