from typing import Union

from util.logger import log

def parse_myquant_vt_symbol(standard_vt_symbol: str) -> Union[str, None]:
    symbol_segment = standard_vt_symbol.split('.')
    if len(symbol_segment) < 2:
        log.error(f'传入的合约代码不合法, {standard_vt_symbol}')
        return None
    return f'{symbol_segment[1]}.{symbol_segment[0]}'