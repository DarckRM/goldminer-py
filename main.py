from multiprocessing.dummy import Pool
from typing import Any, Dict, List, Union
from fastapi import FastAPI
from myquant.client import get_client
from pydantic import BaseModel
from service.keep_current_bar import keep_current_bar
from service.keep_current_quote import keep_current_quote
from util.converter import vt_to_gm_symbols
from util.logger import log
import uvicorn


pool = Pool(4)
log.info('初始化任务线程池')

# 初始化掘金客户端
client = get_client()

# 添加任务函数
pool.apply_async(keep_current_quote)
pool.apply_async(keep_current_bar)

# 启动 HTTP 服务
app = FastAPI()


@app.get("/subscribe")
def subscribe(vt_symbols: str = ''):
    client.subscribe(vt_symbols)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)