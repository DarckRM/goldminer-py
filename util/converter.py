import re
from typing import List, Tuple, Union
from model.enum import Exchange

from util.logger import log

def parse_myquant_vt_symbol(standard_vt_symbol: str) -> Union[str, None]:
    symbol_segment = standard_vt_symbol.split('.')
    if len(symbol_segment) < 2:
        log.error(f'传入的合约代码不合法, {standard_vt_symbol}')
        return None
    return f'{symbol_segment[1]}.{symbol_segment[0]}'

def vt_to_gm_symbol(vt_symbol: str) -> Union[str, None]:
    symbol_segment: List[str] = []
    
    symbol_segment = vt_symbol.split('.')
    if len(symbol_segment) < 2:
        log.error(f'传入的合约代码不合法, {vt_symbol}')
        return None

    if '9999' in symbol_segment[0]:
        symbol_segment[0] = symbol_segment[0][:-4]
    
    if Exchange(symbol_segment[1]) == Exchange.CZCE:
        code, exchange = extract_future_vt_symbol(vt_symbol)
        symbol_segment[0] = code + symbol_segment[0][len(code) + 1:]

    if symbol_segment[1] == 'SSE':
        symbol_segment[1] = 'SHSE'
    
    return f'{symbol_segment[1]}.{symbol_segment[0]}'

def extract_future_vt_symbol(vt_symbol: str) -> Tuple[str, Exchange]:
    symbol, exchange = extract_vt_symbol(vt_symbol)

    if exchange == Exchange.CFFEX and 'LX' in symbol:
        code = symbol.split('LX')[0]
    else:
        start, end = re.search('\D\d', symbol).span()
        code = symbol[:(end - 1)]
    return code, exchange

def extract_vt_symbol(vt_symbol: str) -> Tuple[str, Exchange]:
    """
    :return: (symbol, exchange)
    """
    if vt_symbol.startswith(".") and vt_symbol.count(".") == 2:
        _, symbol, exchange_str = vt_symbol.split(".")
        return "." + symbol, Exchange(exchange_str)
    else:
        symbol, exchange_str = vt_symbol.split(".")
        return symbol, Exchange(exchange_str)
    
def extract_symbol(vt_symbols: str) -> str:
    param_symbols: str = ""

    for vt_symbol in (vt_symbols + ',').split(','):
        if vt_symbol == "":
            continue

        vt_symbol = vt_to_gm_symbol(vt_symbol)
        if not vt_symbol:
            continue
        param_symbols += vt_symbol + ','

    param_symbols = param_symbols[:-1]

    return param_symbols