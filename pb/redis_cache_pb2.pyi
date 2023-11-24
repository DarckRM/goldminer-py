from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BarDataCache(_message.Message):
    __slots__ = ["avg_price", "close_price", "datetime", "exchange", "high_price", "interval", "low_price", "open_interest", "open_price", "symbol", "turnover", "volume"]
    AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRICE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    LOW_PRICE_FIELD_NUMBER: _ClassVar[int]
    OPEN_INTEREST_FIELD_NUMBER: _ClassVar[int]
    OPEN_PRICE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TURNOVER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    avg_price: float
    close_price: float
    datetime: str
    exchange: str
    high_price: float
    interval: str
    low_price: float
    open_interest: float
    open_price: float
    symbol: str
    turnover: float
    volume: float
    def __init__(self, symbol: _Optional[str] = ..., exchange: _Optional[str] = ..., datetime: _Optional[str] = ..., interval: _Optional[str] = ..., volume: _Optional[float] = ..., turnover: _Optional[float] = ..., avg_price: _Optional[float] = ..., open_interest: _Optional[float] = ..., open_price: _Optional[float] = ..., high_price: _Optional[float] = ..., low_price: _Optional[float] = ..., close_price: _Optional[float] = ...) -> None: ...

class ContractDataCache(_message.Message):
    __slots__ = ["exchange", "name", "symbol"]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    exchange: str
    name: str
    symbol: str
    def __init__(self, symbol: _Optional[str] = ..., exchange: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class DbBarDataCache(_message.Message):
    __slots__ = ["avg_price", "close_price", "datetime", "high_price", "low_price", "open_interest", "open_price", "turnover", "volume"]
    AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRICE_FIELD_NUMBER: _ClassVar[int]
    LOW_PRICE_FIELD_NUMBER: _ClassVar[int]
    OPEN_INTEREST_FIELD_NUMBER: _ClassVar[int]
    OPEN_PRICE_FIELD_NUMBER: _ClassVar[int]
    TURNOVER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    avg_price: float
    close_price: float
    datetime: int
    high_price: float
    low_price: float
    open_interest: float
    open_price: float
    turnover: float
    volume: float
    def __init__(self, datetime: _Optional[int] = ..., volume: _Optional[float] = ..., turnover: _Optional[float] = ..., avg_price: _Optional[float] = ..., open_interest: _Optional[float] = ..., open_price: _Optional[float] = ..., high_price: _Optional[float] = ..., low_price: _Optional[float] = ..., close_price: _Optional[float] = ...) -> None: ...

class DbBarDataCacheList(_message.Message):
    __slots__ = ["bar_datas"]
    BAR_DATAS_FIELD_NUMBER: _ClassVar[int]
    bar_datas: _containers.RepeatedCompositeFieldContainer[DbBarDataCache]
    def __init__(self, bar_datas: _Optional[_Iterable[_Union[DbBarDataCache, _Mapping]]] = ...) -> None: ...

class DbOptionBarCache(_message.Message):
    __slots__ = ["close_price", "datetime", "high_price", "low_price", "open_interest", "open_price", "volume"]
    CLOSE_PRICE_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRICE_FIELD_NUMBER: _ClassVar[int]
    LOW_PRICE_FIELD_NUMBER: _ClassVar[int]
    OPEN_INTEREST_FIELD_NUMBER: _ClassVar[int]
    OPEN_PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    close_price: float
    datetime: int
    high_price: float
    low_price: float
    open_interest: float
    open_price: float
    volume: float
    def __init__(self, datetime: _Optional[int] = ..., volume: _Optional[float] = ..., open_interest: _Optional[float] = ..., open_price: _Optional[float] = ..., high_price: _Optional[float] = ..., low_price: _Optional[float] = ..., close_price: _Optional[float] = ...) -> None: ...

class DbOptionBarCacheList(_message.Message):
    __slots__ = ["option_bars"]
    OPTION_BARS_FIELD_NUMBER: _ClassVar[int]
    option_bars: _containers.RepeatedCompositeFieldContainer[DbOptionBarCache]
    def __init__(self, option_bars: _Optional[_Iterable[_Union[DbOptionBarCache, _Mapping]]] = ...) -> None: ...

class QuotesCache(_message.Message):
    __slots__ = ["ask_p", "ask_v", "bid_p", "bid_v"]
    ASK_P_FIELD_NUMBER: _ClassVar[int]
    ASK_V_FIELD_NUMBER: _ClassVar[int]
    BID_P_FIELD_NUMBER: _ClassVar[int]
    BID_V_FIELD_NUMBER: _ClassVar[int]
    ask_p: float
    ask_v: int
    bid_p: float
    bid_v: int
    def __init__(self, bid_p: _Optional[float] = ..., bid_v: _Optional[int] = ..., ask_p: _Optional[float] = ..., ask_v: _Optional[int] = ...) -> None: ...

class TickDataCache(_message.Message):
    __slots__ = ["create_time", "latest_price", "name", "pre_close", "quotes", "symbol", "update_time"]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    LATEST_PRICE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRE_CLOSE_FIELD_NUMBER: _ClassVar[int]
    QUOTES_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    create_time: int
    latest_price: float
    name: str
    pre_close: float
    quotes: _containers.RepeatedCompositeFieldContainer[QuotesCache]
    symbol: str
    update_time: int
    def __init__(self, symbol: _Optional[str] = ..., name: _Optional[str] = ..., create_time: _Optional[int] = ..., update_time: _Optional[int] = ..., latest_price: _Optional[float] = ..., pre_close: _Optional[float] = ..., quotes: _Optional[_Iterable[_Union[QuotesCache, _Mapping]]] = ...) -> None: ...
