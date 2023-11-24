from typing import Any, Dict

from conf.setting_dev import SETTINGS_DEV


SETTINGS: Dict[str, Any] = {
    "setting.env": "dev",
    "token": "",

    "serv_addr": "",

    # 开发
    "redis_host": "127.0.0.1",
    "redis_pwd": "",
    "redis_port": 6379,

}

if SETTINGS['setting.env'] == 'dev':
    SETTINGS = SETTINGS_DEV