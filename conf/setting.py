from typing import Any, Dict

from conf.setting_dev import SETTINGS_DEV


SETTINGS: Dict[str, Any] = {
    "setting.env": "dev",
    "token": ""
}

if SETTINGS['setting.env'] == 'dev':
    SETTINGS = SETTINGS_DEV