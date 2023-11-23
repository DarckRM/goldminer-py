from datetime import datetime, timedelta
from multiprocessing.dummy import Pool
from typing import Dict, List, Union

import pytz
from conf.setting import SETTINGS
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
from model.enum import Adjust, Interval
from util.converter import extract_symbol, vt_to_gm_symbol
from util.logger import log

class MyQuantApi():
    def __init__(self) -> None:
        self.token = SETTINGS['token']
        self.serv_addr = SETTINGS['serv_addr']
        self.strategy_id = "2EBNF3KAeGi@hnswxy.com"
        self.mode = MODE_LIVE
        self.pool = Pool(4)

        set_token(self.token)
        if self.serv_addr:
            set_serv_addr(self.serv_addr)
        py_gmi_set_apitoken(self.token)
        py_gmi_set_strategy_id(self.strategy_id)
        # self.pool.apply_async(self._connect_to_myquant)
    
    def current(self, vt_symbols: str, fields: str = '') -> List[Dict]:
        log.info(f'{vt_symbols}')
        result: List[Dict] = current(symbols=extract_symbol(vt_symbols), fields=fields)
        return result

    def get_continuous_contracts(self, csymbol: str) -> List[Dict]:
        log.info(f'{csymbol}')
        now: datetime = datetime.now()
        result: List[Dict] = get_continuous_contracts(csymbol, '2018-01-01', '2018-10-10')
        log.info(result)
        return result
    
    def get_trading_session(self, vt_symbols: str) -> List[Dict]:
        log.info(f'{vt_symbols}')
        result: List[Dict] = get_trading_session(vt_symbols)
        return result
    
    def get_hisotry_symbol(self, vt_symbol: str, start: str, end: str) -> List[Dict]:
        log.debug(f'{vt_symbol} {start} - {end}')
        result: List[Dict] = get_history_symbol(symbol=vt_symbol, start_date=start, end_date=end)
        return result

    def get_symbol_infos(self, origin: int, sub_origin: int) -> List[Dict]:
        log.debug(f'{origin}')
        now: datetime = datetime.now(tz=pytz.timezone("Asia/Shanghai")).replace(hour=0, minute=0, second=0, microsecond=0)
        result: List[Dict] = get_symbols(sec_type1=origin, sec_type2=sub_origin, df=False)
        # TODO 暂时过滤
        index = 0
        while index < len(result):
            r = result[index]
            if '连' in r['sec_name'] or '次主' in r['sec_name']:
                result.pop(index)
                continue
            if '主力' in r['sec_name']:
                r['sec_id'] += '9999'

            if r.get('delisted_date', None) < now - timedelta(days=25):
                result.pop(index)
                continue
            index += 1
            # else:
            #     code, ashe = extract_future_vt_symbol(f"{r['sec_id']}.{exchange.value}")
            #     r['sec_id'] = code + r['delisted_date'].strftime('%Y%m')[2:]
        return result
    
    def history(self, vt_symbols: Union[str, List[str]], start: str, end: str, interval: Interval = Interval.DAILY, adjust: Adjust = Adjust.NONE, fill_missing: str ='Last') -> List[Dict]:
        log.debug(f'{vt_symbols}')
        result: List[Dict] = history(symbol=vt_symbols, frequency=interval, start_time=start, end_time=end, adjust=adjust, fill_missing=fill_missing)
        return result
    
    def history_n(self, symbol: str, count: int = 1):
        pass
    
    def subscribe(self, vt_symbols, interval, count = 2) -> None:
        # type: (Union[str, List[str]], str, int) -> None
        log.debug(f'{vt_symbols} {interval}')
        subscribe(symbols=vt_symbols, frequency=interval, count=count)
    
    def _connect_to_myquant(self):
        log.info('开始连接到掘金客户端')
        context.mode = self.mode
        context.strategy_id = self.strategy_id
        context.init_fun = self._init
        context.on_tick_fun = self._on_tick
        context.on_bar_fun = self._on_bar

        py_gmi_set_data_callback(callback_controller)
        # _register_signal()
        # _register_excepthook()
        status = gmi_init()
        check_gm_status(status)

        context._set_accounts()
        log.debug(f'连接状态: {status}')
        while True:
            gmi_poll()
    
    def _init(self, context):
        pass 

    def _on_bar(self, context, bar):
        print('收到bar行情---', bar)
        data = context.data(symbol='SHSE.600519', frequency='60s', count=2)
        print('bar数据滑窗---', data)

    def _on_tick(self, context, tick):
        print('收到tick行情---', tick)
    
if __name__ == '__main__':
    api = MyQuantApi()
    result = api.get_symbol_infos()
    print(result)