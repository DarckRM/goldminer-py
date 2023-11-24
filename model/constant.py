from typing import Dict, List

import pytz

from model.enum import Exchange, ExchangeMarket, Interval

CN_EXCHANGES: List[Exchange] = [Exchange.SSE, Exchange.SZSE]
US_EXCHANGES: List[Exchange] = [Exchange.SMART]
HK_EXCHANGES: List[Exchange] = [Exchange.SEHK]
ALL_EXCHANGES: List[Exchange] = [Exchange.CFFEX, Exchange.SHFE, Exchange.DCE, Exchange.CZCE, Exchange.INE, Exchange.GFEX, Exchange.SSE, Exchange.SZSE, Exchange.SMART, Exchange.SEHK]
CN_FUTURE_EXCHANGES: List[Exchange] = [Exchange.CFFEX, Exchange.SHFE, Exchange.DCE, Exchange.CZCE, Exchange.INE, Exchange.GFEX]

MARKET_EXCHANGES: Dict[ExchangeMarket, List[Exchange]] = {
    ExchangeMarket.Market_CFUTURE: CN_FUTURE_EXCHANGES,
    ExchangeMarket.Market_CSE: CN_EXCHANGES,
    ExchangeMarket.Market_SEHK: HK_EXCHANGES,
    ExchangeMarket.Market_SMART: US_EXCHANGES
}

INTERVAL_MINUTES: Dict[Interval, int] = {
    Interval.MINUTE: 1,
    Interval.FIVE_MINUTES: 5,
    Interval.FIFTEEN_MINUTES: 15,
    Interval.DAILY: 1440
}


CHINA_TZ = pytz.timezone("Asia/Shanghai")


DATE_F = '%Y-%m-%d'
TIME_F = '%H:%M:%S'
D_TIME_F = '%Y-%m-%d %H:%M:%S'
HM_F = '%H:%M'

# GoldMiner Redis Key
CONTRACT_KEY: str = "GM:CONTRACT_INFO:"
GM_LATEST_QUOTE_KEY: str = "GM:LATEST:QUOTE:"
GM_LATEST_KLINE_KEY: str = "GM:LATEST:KLINE:"
GM_CONTRACT_INFO_KEY: str = "GM:CONTRACT_INFO:"
GM_MINUTE_KLINE_KEY: str = 'GM:MINUTE_KLINE:'
GM_SUBSCRIBE_LIST_KEY: str = 'GM:SUBSCRIBE_LIST:'
GM_DAILY_BARS_NUM_KEY: str = 'GM:BARS_NUM:'