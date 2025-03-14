from loguru import logger
import sys
from pathlib import Path
from typing import Dict

class LoggerConfig:
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}"
    _loggers: Dict[str, 'logger'] = {}
    _configured_paths: Dict[str, int] = {}  # Храним ID обработчиков для каждого пути

    @staticmethod
    def setup_logger(log_dir: str, log_file: str, log_level: str = DEFAULT_LOG_LEVEL) -> 'logger':
        log_path = Path(log_dir) / log_file
        log_key = str(log_path)
        
        if log_key not in LoggerConfig._loggers:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            # Добавляем обработчик для файла с фильтром по имени файла
            file_handler_id = logger.add(
                log_path,
                level=log_level,
                format=LoggerConfig.DEFAULT_LOG_FORMAT,
                rotation="10 MB",
                retention="7 days",
                compression="zip",
                encoding="utf-8",
                filter=lambda record: record["extra"].get("log_file") == log_file
            )
            # Добавляем обработчик для stdout с фильтром по имени файла
            stdout_handler_id = logger.add(
                sys.stdout,
                level=log_level,
                format=LoggerConfig.DEFAULT_LOG_FORMAT,
                filter=lambda record: record["extra"].get("log_file") == log_file
            )
            # Привязываем логгер к конкретному имени файла через extra
            LoggerConfig._loggers[log_key] = logger.bind(log_file=log_file)
            LoggerConfig._configured_paths[log_key] = file_handler_id  # Сохраняем ID обработчика (если нужно удалять)
        
        return LoggerConfig._loggers[log_key]

def get_logger(log_dir: str, log_file: str, log_level: str = "INFO") -> 'logger':
    return LoggerConfig.setup_logger(log_dir, log_file, log_level)