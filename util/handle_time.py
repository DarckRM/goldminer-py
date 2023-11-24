from datetime import datetime, timedelta
from typing import Dict, List
from model.constant import CN_EXCHANGES, D_TIME_F, DATE_F, HM_F
from model.enum import Exchange, ExchangeMarket, Interval
from model.object import BarData



def when_to_trade(market: ExchangeMarket, quote: bool = False) -> int:
    """判断当前是否开盘时间 并返回距离开盘时间差多少秒 如果为 0 则说明是开盘时间"""
    offset = timedelta()
    now = datetime.now()
    now_date_str = now.strftime(DATE_F)

    noon_start = datetime.strptime(f'{now_date_str} 09:01:00', D_TIME_F)
    noon_end = datetime.strptime(f'{now_date_str} 11:31:00', D_TIME_F)
    afternoon_start = datetime.strptime(f'{now_date_str} 13:00:00', D_TIME_F)
    afternoon_end = datetime.strptime(f'{now_date_str} 15:15:00', D_TIME_F)
    night_start = datetime.strptime(f'{now_date_str} 21:01:00', D_TIME_F)
    night_end = datetime.strptime(f'{now_date_str} 02:30:00', D_TIME_F)

    if quote:
        noon_start -= timedelta(minutes=1)
        afternoon_start -= timedelta(minutes=1)
        night_start -= timedelta(minutes=1)

    if market == ExchangeMarket.Market_CSE:
        # 周末时间
        if now.isoweekday() in [6, 7] and market != ExchangeMarket.Market_CFUTURE:
            monday = now + timedelta(days=8 - now.isoweekday())
            offset = monday.replace(hour=9, minute=31, second=0, microsecond=0) - now
        # 非开盘时间不进行维护
        elif noon_end < now < afternoon_start:
            offset = afternoon_start - now
        elif now < noon_start:
            offset = noon_start - now
        elif now > afternoon_end:
            offset = noon_start + timedelta(days=1) - now

    if market == ExchangeMarket.Market_CFUTURE:
        if noon_end < now < afternoon_start:
            offset = afternoon_start - now
        elif night_end < now < noon_start:
            offset = noon_start - now
        elif afternoon_end < now < night_start:
            offset = night_start - now
    return offset.seconds


def list_time_gap(start: str, end: str) -> List[str]:
    time_list: List[str] = []
    start_time: datetime = datetime.strptime(start, "%H:%M")
    end_time: datetime = datetime.strptime(end, '%H:%M')
    time_gap = (end_time - start_time).seconds / 60

    while time_gap != 0:
        time_list.append(start_time.strftime('%H:%M'))
        start_time += timedelta(minutes=1)
        time_gap -= 1

    return time_list


def when_monday_trim_bar_dict(start: datetime, bar_dict: Dict[str, BarData]) -> Dict[str, BarData]:
    if start.isoweekday() != 1:
        return bar_dict

    trimmed_bar_dict: Dict[str, BarData] = {}
    for slot in bar_dict.keys():
        slot_time = datetime.strptime(slot, HM_F)
        if slot_time.hour < 9:
            continue
        trimmed_bar_dict[slot] = {}
    return trimmed_bar_dict


def generate_bar_dict(time_trading: List[Dict], exchange: Exchange, interval: Interval = Interval.MINUTE) -> (
        Dict[str, BarData], str):
    if interval == Interval.DAILY:
        return {'00:00': {}}, '00:00'

    bar_dict: Dict[str, BarData] = {}
    time_list: List[str] = []
    index = 0

    while index < len(time_trading):
        part = time_trading[index]
        start = part['start']
        end = part['end']

        if start == '21:00':
            s_h = int(start.split(':')[0])
            e_h = int(end.split(':')[0])

            if e_h < s_h and index == 0:
                part['start'] = '00:00'
                start = part['start']

                time_trading.append({
                    'start': '21:00',
                    'end': '00:00'
                })
            elif e_h > s_h and index == 0:
                time_trading.append(part)
                time_trading.pop(0)
                continue

        time_list.extend(list_time_gap(start, end))
        for dot in time_list:
            bar_dict[dot] = {}
        index += 1

    if exchange in CN_EXCHANGES:
        bar_dict['14:57'] = {}
        bar_dict['14:58'] = {}
        bar_dict['14:59'] = {}
        time_list.extend(['14:57', '14:58', '14:59'])

    return bar_dict, time_list[0]