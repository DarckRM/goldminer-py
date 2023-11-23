from typing import Any, Dict, List, Union
from fastapi import FastAPI
from myquant.service import MyQuantApi
from pydantic import BaseModel
from util.converter import parse_myquant_vt_symbol
from util.logger import log
import uvicorn

app = FastAPI()
api = MyQuantApi()

def verify_symbols(vt_symbols) -> Union[Dict[str, Any], None]:
    # type: (str) -> Dict[str, Any]
    for vt_symbol in vt_symbols.split(','):
        vt_symbol = parse_myquant_vt_symbol(vt_symbol)        
        if vt_symbol == None:
            return {"code": 400, "data": None, "msg": "不合法的合约代码"}
    return None

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/csymbol")
def csymbol(csymbol: str):
    return api.get_continuous_contracts(csymbol)

@app.get("/current")
def current(vt_symbols: str, fields: str = ''):
    return api.current(vt_symbols, fields)

@app.get("/parse/{vt_symbol}")
def read_root(vt_symbol: str):
    vt_symbol = parse_myquant_vt_symbol(vt_symbol)
    return {"Hello": vt_symbol}

@app.get("/session")
def trade_session(vt_symbol: str):
    ok = verify_symbols(vt_symbol)
    if ok:
        return ok
    log.info('rua')
    result = api.get_trading_session(vt_symbol)
    return {"code": 200, "data": result, "msg": "查询成功"}

@app.get("/history_symbol")
def symbols(symbol: str, start: str, end: str):
    symbols_info = api.get_hisotry_symbol(symbol, start, end)
    return symbols_info

@app.get("/symbols")
def symbols(origin: int, sub_origin: int):
    symbols_info = api.get_symbol_infos(origin, sub_origin)
    return symbols_info

@app.get("/history")
def history(vt_symbols: str, start: str, end: str, interval: str = '1d', adjust: int = 1, fill_missing: str = 'Last'):
    ok = verify_symbols(vt_symbols)
    if ok:
        return ok
    result = api.history(vt_symbols, start, end, interval, adjust, fill_missing)
    return {"code": 200, "data": result, "msg": "查询成功"}

@app.get("/subscribe")
def subscribe(vt_symbols, interval, count = 2):
    # type: (str, str, int) -> None
    ok = verify_symbols(vt_symbols)
    if ok:
        return ok
    result = api.subscribe(vt_symbols, interval, count)
    return {"code": 200, "data": result, "msg": "订阅成功"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)