from datetime import datetime
import time
import traceback
from typing import Dict, List
from database.redis.redis_database import compress_tick_data
from model.constant import CN_EXCHANGES, GM_LATEST_QUOTE_KEY
from model.enum import ExchangeMarket
from model.object import StockBriefData, TickData
from myquant.client import get_client
from util.converter import concat_vt_symbol_key
from util.handle_time import when_to_trade
from util.logger import log

client = get_client()

def keep_current_quote():
    log.info(f'运行实时行情维护函数')
    
    stocks: List[str] = []
    futures: List[str] = []

    while True:
        offset = when_to_trade(ExchangeMarket.Market_CFUTURE, True)
        if offset != 0:
            log.info(f'当前非交易时间, {int(offset / 60)} 分钟后获取实时行情')
            time.sleep(offset)
            log.info(f'进入交易时间, 开始获取实时行情')
        for c in client.subscribe_list:
            if c.exchange in CN_EXCHANGES:
                stocks.append(c.vt_symbol)
            else:
                futures.append(c.vt_symbol)
        try:
            if len(stocks) != 0:
                _fetch_current_quote(stocks)
            if len(futures) != 0:
                _fetch_current_quote(futures)

            time.sleep(1)
            stocks.clear()
            futures.clear()
        except Exception as e:
            log.error(f'获取行情异常: {e}\n{traceback.format_exc()}')


def _fetch_current_quote(vt_symbols: List[str]):
    now: datetime = datetime.now()
    param_symbols: str = ''

    def get_tick_key(data: TickData):
        cache_data = compress_tick_data(data).SerializeToString()
        return concat_vt_symbol_key(GM_LATEST_QUOTE_KEY, data.symbol), cache_data

    for s in vt_symbols:
        param_symbols += s + ','

    ticks: List[Dict] = client.current(param_symbols, 'symbol,open,price,quotes,created_at')
    tick_caches: List[TickData] = []
    for t in ticks:
        tick: TickData = TickData(
            name=client.contract_dict[t['symbol']].name,
            symbol=t['symbol'],
            pre_close=t.get('open', 0),
            latest_price=t['price'],
            create_time=int(now.timestamp()),
            update_time=int(t['created_at'].timestamp()),
            quotes=t['quotes'],
        )
        tick_caches.append(tick)
    client.rd.mset(name="", values=tick_caches, handler=get_tick_key)