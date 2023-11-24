from datetime import datetime, timedelta
import time
import traceback
from typing import Dict, List
from database.redis.redis_database import compress_bar_data
from model.constant import CHINA_TZ, CN_EXCHANGES, CN_FUTURE_EXCHANGES, GM_LATEST_KLINE_KEY, GM_MINUTE_KLINE_KEY
from model.enum import Adjust, ExchangeMarket, Interval, V_Interval
from model.object import BarData, ContractData
from myquant.client import get_client
from util.converter import concat_vt_symbol_key, split_vt_symbol
from util.handle_time import when_to_trade
from util.logger import log

client = get_client()

def keep_current_bar():
        log.info('运行实时 K 线函数')
        vt_symbol_list: List[str] = []
        vt_symbols = ""
        try:
            for c in client.subscribe_list:
                vt_symbols += c.vt_symbol + ','
            vt_symbol_list.append(vt_symbols)

            while True:
                offset = when_to_trade(ExchangeMarket.Market_CFUTURE, False)
                if offset != 0:
                    log.info(f'当前非交易时间, {int(offset / 60)} 分钟后获取实时 K 线')
                    time.sleep(offset)
                    log.info(f'进入交易时间, 开始获取实时 K 线')

                now: datetime = datetime.now()

                if now.second != 5:
                    time.sleep(1)
                    continue

                for v in vt_symbol_list:
                    stocks = ''
                    futures = ''

                    for vt_symbol in v.split(','):
                        if vt_symbol == '':
                            continue

                        symbol, exchange = split_vt_symbol(vt_symbol)
                        if exchange in CN_EXCHANGES:
                            stocks += symbol + '.' + exchange.value + ','
                        else:
                            futures += symbol + '.' + exchange.value + ','

                    if stocks != '':
                        _fetch_current_bar(stocks[:-1], 1)

                    if futures != '':
                        _fetch_current_bar(futures[:-1], 1)
                log.info('finish')
                time.sleep(1)
        except Exception as e:
            log.error(f'获取实时 K 线异常: {e}\n{traceback.format_exc()}')


def _fetch_current_bar(vt_symbols: str, minutes: int):
        now: datetime = datetime.now(tz=CHINA_TZ).replace(second=0, microsecond=0)
        pre_min: datetime = now - timedelta(minutes=minutes)
        ready_to_cache: Dict[str, List[BarData]] = {}

        sample: ContractData = client.contract_dict[vt_symbols.split(',')[0]]
        if sample.exchange in CN_FUTURE_EXCHANGES:
            adjust = Adjust.NONE
        else:
            adjust = Adjust.POST

        for h in client.history(vt_symbols, pre_min, now, V_Interval.MINUTE, adjust):
            log.info(h)
            c: ContractData = client.contract_dict.get(h['symbol'], None)
            pre_bar: BarData = client.latest_bars.get(h['symbol'], None)

            if pre_bar:
                if (h['bob'] - pre_bar.datetime).seconds != 60:
                    log.warning(f'返回了不正确的时间: {h}')

            if not pre_bar:
                client.today_bars[h['symbol']] = []
            if not ready_to_cache.get(h['symbol'], None):
                ready_to_cache[h['symbol']] = []

            bar: BarData = BarData(
                gateway_name='GoldMiner',
                symbol=c.symbol,
                exchange=c.exchange,
                datetime=h['bob'],
                interval=Interval.MINUTE,
                volume=h['volume'],
                turnover=h['amount'],
                avg_price=h['amount'] / (h['volume'] * client.contract_dict[c.vt_symbol].multiplier),
                open_price=h['open'],
                high_price=h['high'],
                low_price=h['low'],
                close_price=h['close']
            )
            bar.datetime.replace(tzinfo=CHINA_TZ)
            append_bar(bar)
            ready_to_cache[bar.vt_symbol].append(bar)

        for symbol, bar in client.latest_bars.items():
            if bar.datetime + timedelta(minutes=1) != now:
                fix_bar: BarData = BarData(
                    gateway_name='GoldMiner',
                    symbol=bar.symbol,
                    exchange=bar.exchange,
                    datetime=now - timedelta(minutes=1),
                    interval=Interval.MINUTE,
                    volume=0,
                    turnover=0,
                    avg_price=0,
                    open_price=bar.close_price,
                    high_price=bar.close_price,
                    low_price=bar.close_price,
                    close_price=bar.close_price
                )
                append_bar(fix_bar, -1)
                try:
                    ready_to_cache[bar.vt_symbol] = []
                    ready_to_cache[bar.vt_symbol].append(bar)
                except Exception as e:
                    log.warn(f'获取实时 K 线异常: {e}\n{traceback.format_exc()}')

        # 写入缓存
        def get_minute_k_key(data: List[BarData]):
            cache_data = compress_bar_data(data[0]).SerializeToString()
            name = concat_vt_symbol_key(GM_MINUTE_KLINE_KEY, data[0].vt_symbol)
            return name, cache_data

        def get_latest_k_key(data: BarData):
            cache_data = compress_bar_data(data).SerializeToString()
            return concat_vt_symbol_key(GM_LATEST_KLINE_KEY, data.vt_symbol), cache_data

        client.rd.mlpush(name="", values=ready_to_cache.values(), handler=get_minute_k_key)
        client.rd.mset(name="", values=client.latest_bars.values(), handler=get_latest_k_key)


def append_bar(bar: BarData, index: int = 0):
    client.latest_bars[bar.vt_symbol] = bar
    if index != 0:
        client.today_bars[bar.vt_symbol].insert(index, bar)
    else:
        client.today_bars[bar.vt_symbol].append(bar)
