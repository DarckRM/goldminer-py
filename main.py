from typing import List, Union
from fastapi import FastAPI
from myquant.service import MyQuantApi
from pydantic import BaseModel
from util.converter import parse_myquant_vt_symbol
from util.logger import log

app = FastAPI()
api = MyQuantApi()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/parse/{vt_symbol}")
def read_root(vt_symbol: str):
    vt_symbol = parse_myquant_vt_symbol(vt_symbol)
    return {"Hello": vt_symbol}

@app.get("/symbols")
def symbols():
    symbols_info = api.get_symbol_infos()
    return symbols_info

@app.get("/history")
def history(vt_symbols: str, start: str, end: str, interval: str = '1d', adjust: int = 1, fill_missing: str = 'Last'):
    for vt_symbol in vt_symbols.split(','):
        vt_symbol = parse_myquant_vt_symbol(vt_symbol)        
        if vt_symbol == None:
            return {"code": 400, "data": None, "msg": "不合法的合约代码"}

    result = api.history(vt_symbols, start, end, interval, adjust, fill_missing)
    return {"code": 200, "data": result, "msg": "查询成功"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}