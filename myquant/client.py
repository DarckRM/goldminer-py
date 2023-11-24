from datetime import datetime, timedelta
from multiprocessing.dummy import Pool
from pydoc import cli
import traceback
from typing import Any, Dict, List, Union

import pytz
from conf.setting import SETTINGS
from database.redis.redis_database import depress_contract_data, get_redis
from gm.api.basic import _register_excepthook, _register_signal
from gm.enum import MODE_LIVE
from gm.api import (
    set_token, get_symbols, history, set_serv_addr, subscribe, get_trading_session, get_history_symbol,
    current, get_continuous_contracts, history_n
)
from gm.api._errors import check_gm_status
from gm.csdk.c_sdk import (
    py_gmi_set_apitoken, py_gmi_set_strategy_id, py_gmi_set_data_callback,
    gmi_poll, gmi_init
)
from gm.model.storage import context
from gm.callback import callback_controller
from model.constant import ALL_EXCHANGES, CONTRACT_KEY
from model.enum import Adjust, Interval, V_Interval
from model.object import BarData, ContractData, TickQuotes
from util.converter import gm_to_vt_symbols, parse_v_interval, vt_to_gm_symbols
from util.logger import log

class MyQuantApi():
    def __init__(self) -> None:
        self.contract_list: List[ContractData] = []
        self.contract_dict: Dict[str, ContractData] = {}
        self.subscribe_list: List[ContractData] = []
        self.latest_bars: Dict[str, BarData] = {}
        self.today_bars: Dict[str, List[BarData]] = {}
        self.token = SETTINGS['token']
        self.serv_addr = SETTINGS['serv_addr']
        self.strategy_id = "2EBNF3KAeGi@hnswxy.com"
        self.mode = MODE_LIVE

        self.rd = get_redis()
        self.pool = Pool(4)

        set_token(self.token)
        if self.serv_addr:
            set_serv_addr(self.serv_addr)
        py_gmi_set_apitoken(self.token)
        py_gmi_set_strategy_id(self.strategy_id)
        

    def connect(self, setting: Dict[str, Any] = {}):
        self._fetch_symbols()
    
        
    def subscribe(self, vt_symbols: str):
        self.subscribe_list.clear()
        
        for vt_symbol in vt_symbols.split(','):
            if vt_symbol == '':
                continue
            else:
                self.subscribe_list.append(self.contract_dict[vt_symbol])
        
        log.info(f'订阅数: {len(self.subscribe_list)}')

    def current(self, vt_symbols: str, fields: str = '') -> List[Dict]:
        gm_symbols = vt_to_gm_symbols(vt_symbols)
        log.debug(f'{gm_symbols}: {fields}')

        try:
            results = current(symbols=gm_symbols, fields=fields)

            for r in results:
                r['symbol'] = gm_to_vt_symbols(r['symbol'])
                quotes: List[TickQuotes] = []

                for q in r['quotes']:
                    quotes.append(TickQuotes(
                        bid_p=q['bid_p'],
                        bid_v=q['bid_v'],
                        ask_p=q['ask_p'],
                        ask_v=q['ask_v'],
                    ))

                r['quotes'] = quotes

        except Exception as e:
            log.error(f'获取历史数据异常: {e}\n{traceback.format_exc()}')
            return []

        return results

    def get_symbols(self, origin: int, sub_origin: int) -> List[Dict]:
        log.debug(f'{origin}')

        result: List[Dict] = get_symbols(sec_type1=origin, sec_type2=sub_origin, df=False)

        return result

    def history(self, vt_symbols: Union[str, List[str]], start: Union[str, datetime], end: [str, datetime],
                interval: V_Interval = V_Interval.DAILY, adjust: Adjust = Adjust.NONE, fill_missing: str = 'Last') -> List[Dict]:
        log.debug(f'{vt_symbols}')
        param_symbols = vt_to_gm_symbols(vt_symbols)

        try:
            results = history(symbol=param_symbols, frequency=parse_v_interval(interval).value, start_time=start,
                              end_time=end, adjust=adjust.value, fill_missing=fill_missing)

            for r in results:
                r['symbol'] = gm_to_vt_symbols(r['symbol'])

        except Exception as e:
            log.error(f'获取历史数据异常: {e}\n{traceback.format_exc()}')
            return []

        return results

    def history_n(self, vt_symbol: str, count: int = 1, interval: V_Interval= V_Interval.MINUTE, adjust: Adjust = Adjust.NONE, fill_missing: str = 'Last') -> List[Dict]:
        log.debug(f'{vt_symbol}')
        param_symbols = vt_to_gm_symbols(vt_symbol)

        try:
            results = history_n(symbol=param_symbols, count=count, frequency=parse_v_interval(interval).value, adjust=adjust.value, fill_missing=fill_missing)

            for r in results:
                r['symbol'] = gm_to_vt_symbols(r['symbol'])

        except Exception as e:
            log.error(f'获取历史数据异常: {e}\n{traceback.format_exc()}')
            return []

        return results
        pass

    def get_history_symbol(self, vt_symbol: str, start: str, end: str) -> List[Dict]:
        log.debug(f'{vt_symbol}: {start} - {end}')
        param_symbol = vt_to_gm_symbols(vt_symbol)

        if not param_symbol:
            return []
        try:
            result = get_history_symbol(symbol=param_symbol, start_date=start, end_date=end, df=False)
        except Exception as e:
            log.error(f'获取合约交易历史记录异常: {e}\n{traceback.format_exc()}')
            return []

        return result

    def get_trading_session(self, vt_symbols: str) -> List[Dict]:
        log.debug(f'{vt_symbols}')
        param = vt_to_gm_symbols(vt_symbols)

        try:
            result = get_trading_session(param)
        except Exception as e:
            log.error(f'获取合约交易时段异常: {e}\n{traceback.format_exc()}')
            return []

        return result

    def _fetch_symbols(self):
        log.info("获取合约列表")
        for exchange in ALL_EXCHANGES:
            result = self.rd.mget(CONTRACT_KEY + exchange.value, depress_contract_data)
            if not result:
                continue
            else:
                self.contract_list.extend(result)

        for contract_data in self.contract_list:
            self.contract_dict[contract_data.vt_symbol] = contract_data
        
        log.info(f"共获取 {len(self.contract_list)} 个合约信息")
    

    
    # def _connect_to_myquant(self):
    #     log.info('开始连接到掘金客户端')
    #     context.mode = self.mode
    #     context.strategy_id = self.strategy_id
    #     context.init_fun = self._init
    #     context.on_tick_fun = self._on_tick
    #     context.on_bar_fun = self._on_bar

    #     py_gmi_set_data_callback(callback_controller)
    #     # _register_signal()
    #     # _register_excepthook()
    #     status = gmi_init()
    #     check_gm_status(status)

    #     context._set_accounts()
    #     log.debug(f'连接状态: {status}')
    #     while True:
    #         gmi_poll()
    
client: MyQuantApi = None

def get_client() -> MyQuantApi:
    global client
    if not client:
        client = MyQuantApi()
        client.connect({})

    return client

