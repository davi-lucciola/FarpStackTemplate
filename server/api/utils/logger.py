from enum import Enum, auto
from dataclasses import dataclass


class LoggerType(Enum):
    INFO = auto()
    DEBUG = auto()
    ERROR = auto()


@dataclass
class ILogger:
    LOGGING_TYPE_MAP = {
        LoggerType.INFO: {'color': '\033[0;32m', 'space': 5},
        LoggerType.DEBUG: {'color': '\033[0;34m', 'space': 4},
        LoggerType.ERROR: {'color': '\033[0;31m', 'space': 4},
    }

    def info(self, object: object):
        log_type_map = self.LOGGING_TYPE_MAP.get(LoggerType.INFO)
        print(
            f"{log_type_map.get('color')}INFO\033[0m:{log_type_map.get('space') * ' '}{object}"
        )

    def debug(self, object: object):
        log_type_map = self.LOGGING_TYPE_MAP.get(LoggerType.DEBUG)
        print(
            f"{log_type_map.get('color')}DEBUG\033[0m:{log_type_map.get('space') * ' '}{object}"
        )

    def error(self, object: object):
        log_type_map = self.LOGGING_TYPE_MAP.get(LoggerType.ERROR)
        print(
            f"{log_type_map.get('color')}ERROR\033[0m:{log_type_map.get('space') * ' '}{object}"
        )


ilogger = ILogger()
