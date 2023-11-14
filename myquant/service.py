from typing import Dict, List, Union
from conf.setting import SETTINGS
from gm.enum import MODE_LIVE
from gm.api import (
    set_token, get_symbol_infos, history
)
from gm.csdk.c_sdk import (
    py_gmi_set_apitoken, py_gmi_set_strategy_id
)
from model.enum import Adjust, Interval
from util.logger import log

class MyQuantApi():
    def __init__(self) -> None:
        self.token = SETTINGS['token']
        self.strategy_id = "2EBNF3KAeGi@hnswxy.com"
        self.mode = MODE_LIVE

        set_token(self.token)
        py_gmi_set_apitoken(self.token)
        py_gmi_set_strategy_id(self.strategy_id)

    def get_symbol_infos(self) -> List[Dict]:
        result: List[Dict] = get_symbol_infos(sec_type1=1010, df=False)
        return result
    
    def history(self, vt_symbols: Union[str, List[str]], start: str, end: str, interval: Interval = Interval.DAILY, adjust: Adjust = Adjust.NONE, fill_missing: str ='Last') -> List[Dict]:
        log.debug(f'{vt_symbols}')
        result: List[Dict] = history(symbol=vt_symbols, frequency=interval, start_time=start, end_time=end, adjust=adjust, fill_missing=fill_missing)
        return result

if __name__ == '__main__':
    api = MyQuantApi()
    result = api.get_symbol_infos()
    print(result)