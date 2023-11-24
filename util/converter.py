import re
from typing import Any, Dict, List, Tuple, Union
from model.constant import ALL_EXCHANGES, CN_EXCHANGES
from model.enum import Exchange, Interval, V_Interval

from util.logger import log

def verify_symbols(vt_symbols) -> Union[Dict[str, Any], None]:
    # type: (str) -> Dict[str, Any]
    for vt_symbol in vt_symbols.split(','):
        vt_symbol = vt_to_gm_symbols(vt_symbol)        
        if vt_symbol == None:
            return {"code": 400, "data": None, "msg": "不合法的合约代码"}
    return None

def split_vt_symbol(vt_symbol: str) -> (str, Exchange):
    seg: List[str] = vt_symbol.split('.')
    return seg[0], Exchange(seg[1])

def parse_v_interval(interval: V_Interval) -> Interval:
    if interval == V_Interval.MINUTE:
        return Interval.MINUTE

    if interval == V_Interval.DAILY:
        return Interval.DAILY


def concat_vt_symbol_key(key: str, vt_symbol: str) -> str:
  symbol, exchange = split_vt_symbol(vt_symbol)
  return key + exchange.value + ":" + symbol


def extract_future_vt_symbol(vt_symbol: str) -> Tuple[str, Exchange]:
    symbol, exchange = split_vt_symbol(vt_symbol)

    if exchange == Exchange.CFFEX and 'LX' in symbol:
        code = symbol.split('LX')[0]
    else:
        result = re.search('\D\d', symbol)
        if not result:
            return symbol, exchange
        else:
            start, end = result.span()
        code = symbol[:(end - 1)]
    return code, exchange


def gm_to_vt_symbols(gm_symbols: str) -> str:
    vt_symbols: str = ""

    for gm_symbol in (gm_symbols + ',').split(','):
        if gm_symbol == "":
            continue

        vt_symbol = extract_gm_symbol(gm_symbol)
        vt_symbols += vt_symbol + ','

    return vt_symbols[:-1]


def vt_to_gm_symbols(vt_symbols: str) -> str:
    param_symbols: str = ""

    for vt_symbol in (vt_symbols + ',').split(','):
        if vt_symbol == "":
            continue

        vt_symbol = extract_vt_symbol(vt_symbol)
        if not vt_symbol:
            continue
        param_symbols += vt_symbol + ','

    param_symbols = param_symbols[:-1]

    return param_symbols


def extract_vt_symbol(vt_symbol: str) -> Union[str, None]:
    seg = vt_symbol.split('.')
    if len(seg) < 2:
        log.error(f'传入的合约代码不合法, {vt_symbol}')
        return None

    if seg[0] in ALL_EXCHANGES:
        log.warning(f'传入的合约代码已经满足条件')
        return vt_symbol

    if '9999' in seg[0]:
        seg[0] = seg[0][:-4]
        if Exchange(seg[1]) == Exchange.SHFE:
            seg[0] = seg[0].upper()

    if '8888' in seg[0]:
        seg[0] = f'{seg[0][:-4]}99'
        if Exchange(seg[1]) == Exchange.SHFE:
            seg[0] = seg[0].upper()

    if Exchange(seg[1]) == Exchange.CZCE:
        code, exchange = extract_future_vt_symbol(vt_symbol)
        seg[0] = code + seg[0][len(code) + 1:]

    if seg[1] == 'SSE':
        seg[1] = 'SHSE'
    return f'{seg[1]}.{seg[0]}'


def extract_gm_symbol(gm_symbol: str) -> Union[str, None]:
    gm_seg = gm_symbol.split('.')

    if gm_seg[0] == 'SHSE':
        gm_seg[0] = 'SSE'

    code, exchange = extract_future_vt_symbol(f'{gm_seg[1]}.{gm_seg[0]}')
    main = True

    for c in gm_seg[1]:
        if c.isdigit():
            main = False
            break

    if '99' in gm_seg[1] and exchange not in CN_EXCHANGES:
        gm_seg[1] = f'{code}8888'

    if main:
        code += '9999'
    else:
        code = gm_seg[1]

    if exchange == Exchange.CZCE:
        if '9999' not in code and '8888' not in code:
            code = f'{code[:2]}2{code[2:]}'

    if exchange == Exchange.SHFE:
        code = code.lower()

    return f'{code}.{gm_seg[0]}'
