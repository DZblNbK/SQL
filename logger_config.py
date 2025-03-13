from loguru import logger
import sys
from pathlib import Path
from typing import Dict

class LoggerConfig:
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}"
    _loggers: Dict[str, logger] = {}

    @staticmethod
    def setup_logger(log_dir: str, log_file: str, log_level: str = DEFAULT_LOG_LEVEL) -> logger:
        log_path = Path(log_dir) / log_file
        log_key = str(log_path)
        if log_key not in LoggerConfig._loggers:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            LoggerConfig._loggers[log_key] = logger
            LoggerConfig._loggers[log_key].add(log_path, level=log_level, format=LoggerConfig.DEFAULT_LOG_FORMAT, rotation="10 MB", retention="7 days", compression="zip", encoding="utf-8")
            LoggerConfig._loggers[log_key].add(sys.stdout, level=log_level, format=LoggerConfig.DEFAULT_LOG_FORMAT)
        return LoggerConfig._loggers[log_key]

def get_logger(log_dir: str, log_file: str, log_level: str = "INFO") -> logger:
    return LoggerConfig.setup_logger(log_dir, log_file, log_level)