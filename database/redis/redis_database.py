from datetime import datetime
import json
import traceback
from enum import Enum
from typing import Any, List, Callable, Dict, Optional

import redis
from pb import redis_cache_pb2

from util.logger import log

from model.enum import Exchange, Interval, Product
from model.object import BarData, ContractData, TickData
from conf.setting import SETTINGS

class RedisClient:
    def __init__(self):
        self.rd = redis.Redis(host=SETTINGS['redis_host'], port=SETTINGS['redis_port'], password=SETTINGS['redis_pwd'],
                              decode_responses=False)

    def to_dict(self, obj: Any) -> Any:
        try:
            # 枚举类型以及 datetime 类型特殊处理
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, datetime):
                try:
                    return obj.strftime('%Y%m%d %H:%M')
                except Exception as e:
                    log.warning(f'秒级 datetime 序列化: {e}')
                    return obj.strftime('%Y%m%d %H:%M:S')
            else:
                return obj.__dict__
        except Exception as e:
            log.warning(f"序列化对象 {obj} 失败: {e}")

    def mlpush(self, name: str, values: [Any], handler: Callable = None):
        try:
            pipeline = self.rd.pipeline()
            for value in values:
                if handler:
                    name, value = handler(value)
                if isinstance(value, List):
                    # todo 由于每次写入的是一个 List 会造成重复写入的问题，暂时采取先清空之前的 value 后再写入
                    # self.delete(name)
                    for inner in value:
                        pipeline.lpush(name, inner)
                else:
                    pipeline.lpush(name, value)
                log.debug(f"追加 Redis 缓存: {name} -> {value}")
            pipeline.execute()
        except Exception as e:
            log.warning(f"批量追加 Redis 缓存失败: {e}")

    def lpush(self, name: str, value: Any):
        try:
            value = json.dumps(value, default=self.to_dict, sort_keys=True)
            self.rd.lpush(name, value)
            log.debug(f"追加 Redis 缓存: {name} -> {value}")
        except Exception as e:
            log.warning(f"追加 Redis 缓存失败: {e}")

    def mset(self, name: str, values: [Any], ex: int = None, px: int = None, nx: bool = False, xx: bool = False,
             handler: Callable = None):
        try:
            pipeline = self.rd.pipeline()
            for value in values:
                if handler:
                    name, value = handler(value)
                pipeline.set(name, value, ex, px, nx, xx)
                log.debug(f"写入 Redis 缓存: {name} -> {value}")
            pipeline.execute()
        except Exception as e:
            log.warning(f"批量写入 Redis 缓存失败: {e}")

    def set(self, name: str, value: Any, ex: int = None, px: int = None, nx: bool = False, xx: bool = False,
            handler: Callable = None) -> bool:
        # todo 目前是将需要序列化的类型固定处理
        try:
            if handler:
                name, value = handler(value)
            self.rd.set(name, value, ex, px, nx, xx)
            log.debug(f"写入 Redis 缓存: {name} -> {value}")
        except Exception as e:
            log.warning(f"写入 Redis 缓存失败: {e}")

    def get(self, name: str, handler: Callable = None) -> Any:
        try:
            result = self.rd.get(name=name)
            if result is None:
                log.info(f"Redis 缓存不存在 Key: {name}")
                return None
            if handler:
                return handler(result)
            else:
                return result
        except Exception as e:
            log.error(f"读取 Redis 缓存失败: {e}\n{traceback.format_exc()}")
            return None

    def mget(self, namespace: str, handler: Callable = None) -> List[Any]:
        results: List[Any] = []
        stop = False
        cursor = 0
        try:
            pipeline = self.rd.pipeline()
            while not stop:
                # 使用 SCAN 遍历 Redis, count 的值使其控制在大约 50 次迭代遍历
                result = self.rd.scan(cursor=cursor, match=namespace + '*', count=100)
                cursor = result[0]
                for record_bytes in result[1]:
                    pipeline.get(record_bytes.decode())
                if cursor == 0:
                    stop = True
            results: List[Any] = pipeline.execute()
            if results and handler:
                return_list: [Any] = []
                for result in results:
                    return_list.append(handler(result))
                log.info(f"获取命名空间 {namespace} 成功: 共 {len(results)} 条数据")
                return return_list
        except Exception as e:
            log.error(f"批量获取 [{namespace}*] Redis 缓存失败: {e}\n{traceback.format_exc()}")
            return []
        return results

    def range(self, name: str, handler: Callable, start: int = 0, end: int = 1, ) -> List[Any]:
        try:
            caches = self.rd.lrange(name, start, end)
            results: [bytes] = []
            for result in caches:
                results.append(handler(result))
            return results
        except Exception as e:
            log.warning(f"读取 Redis 缓存 List 失败: {e}")
            return []

    def len(self, name: str) -> int:
        try:
            length = self.rd.llen(name)
            return length
        except Exception as e:
            log.warning(f"读取 Redis 缓存 List 长度失败: {e}")
            return 0

    def delete(self, names: str) -> int:
        return self.rd.delete(names)

    def delete_group(self, namespace: str) -> int:
        namespace = namespace + '*'
        log.debug(f"准备删除命名空间 {namespace}")
        cursor: int = 0
        stop: bool = False
        try:
            pipeline = self.rd.pipeline()
            while not stop:
                # 使用 SCAN 遍历 Redis, count 的值使其控制在大约 50 次迭代遍历
                result = self.rd.scan(cursor=cursor, match=namespace + '*', count=100)
                cursor = result[0]
                for key in result[1]:
                    pipeline.delete(bytes(key).decode())
                if cursor == 0:
                    stop = True
            result = pipeline.execute()
            log.info(f"删除命名空间 {namespace} 成功: 共 {len(result)} 条数据")
            return len(result)
        except Exception as e:
            log.error(f"删除命名空间 {namespace} 失败: {e}\n{traceback.format_exc()}")


def compress_contract_data(contract: ContractData) -> redis_cache_pb2.ContractDataCache:
    contract_data_cache = redis_cache_pb2.ContractDataCache(
        symbol=contract.symbol,
        name=contract.name,
        exchange=contract.exchange.value
    )
    return contract_data_cache


def depress_contract_data(cache: bytes) -> Optional[ContractData]:
    cache_data = redis_cache_pb2.ContractDataCache()
    try:
        cache_data.ParseFromString(cache)
        contract_data = ContractData(
            symbol=cache_data.symbol,
            name=cache_data.name,
            gateway_name="Gateway Name",
            exchange=Exchange(cache_data.exchange),
            product=Product.EQUITY,
            size=0,
            pricetick=0.2
        )
        return contract_data
    except Exception as e:
        log.error(f"解压 Redis 缓存 [contract_data] 数据异常: {e}\n{traceback.format_exc()}")
        return None


def compress_tick_data(tick: TickData) -> redis_cache_pb2.TickDataCache:
    quotes_caches: List[redis_cache_pb2.QuotesCache] = []
    for q in tick.quotes:
        quotes_caches.append(
            redis_cache_pb2.QuotesCache(
                bid_p=q.bid_p,
                bid_v=q.bid_v,
                ask_p=q.ask_p,
                ask_v=q.ask_v
            )
        )

    tick_data_cache = redis_cache_pb2.TickDataCache(
        symbol=tick.symbol,
        name=tick.name,
        create_time=tick.create_time,
        update_time=tick.update_time,
        latest_price=tick.latest_price,
        pre_close=tick.pre_close,
        quotes=quotes_caches
    )
    return tick_data_cache


def depress_tick_data(cache: bytes) -> Optional[TickData]:
    try:
        cache_data = redis_cache_pb2.TickDataCache()
        cache_data.ParseFromString(cache)
        tick_data = TickData(
            symbol=cache_data.symbol,
            name=cache_data.name,
            create_time=cache_data.create_time,
            update_time=cache_data.update_time,
            latest_price=cache_data.latest_price,
            pre_close=cache_data.pre_close,
            quotes=cache_data.quotes
        )
        return tick_data
    except Exception as e:
        log.error(f"解压 Redis 缓存 [tick_data] 数据异常: {e}\n{traceback.format_exc()}")
        return None


def compress_bar_data(bar: BarData) -> redis_cache_pb2.BarDataCache:
    bar_data_cache = redis_cache_pb2.BarDataCache(
        symbol=bar.symbol,
        exchange=bar.exchange.value,
        datetime=bar.datetime.strftime('%Y%m%d %H:%M'),
        interval=bar.interval.value,
        volume=bar.volume,
        turnover=bar.turnover,
        avg_price=bar.avg_price,
        open_interest=bar.open_interest,
        open_price=bar.open_price,
        high_price=bar.high_price,
        low_price=bar.low_price,
        close_price=bar.close_price,
    )
    return bar_data_cache


def depress_bar_data(cache: bytes) -> Optional[BarData]:
    try:
        cache_data = redis_cache_pb2.BarDataCache()
        cache_data.ParseFromString(cache)

        bar_data = BarData(
            gateway_name="",
            symbol=cache_data.symbol,
            exchange=Exchange(cache_data.exchange),
            datetime=datetime.strptime(cache_data.datetime, '%Y%m%d %H:%M'),
            interval=Interval(cache_data.interval),
            volume=cache_data.volume,
            turnover=cache_data.turnover,
            avg_price=cache_data.avg_price,
            open_interest=cache_data.open_interest,
            open_price=cache_data.open_price,
            high_price=cache_data.high_price,
            low_price=cache_data.low_price,
            close_price=cache_data.close_price,
        )
        return bar_data
    except Exception as e:
        log.error(f"解压 Redis 缓存 [bar_data] 数据异常: {e}\n{traceback.format_exc()}")
        return None


redis_client: RedisClient = None


def get_redis() -> RedisClient:
    global redis_client
    if redis_client:
        return redis_client
    redis_client = RedisClient()
    return redis_client


if __name__ == '__main__':
    rd = get_redis()
    count = rd.range()
    print(count)
