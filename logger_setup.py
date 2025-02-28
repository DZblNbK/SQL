from loguru import logger
import os
import sys


def setup_logger(log_dir, log_file, level="INFO"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Удаляем все предыдущие обработчики
    logger.remove()

    # Добавляем обработчик для записи логов в файл
    logger.add(os.path.join(log_dir, log_file), level=level, format="{time} - {name} - {level} - {message}")

    # Добавляем обработчик для вывода логов в консоль
    logger.add(sys.stdout, level=level, format="{time} - {name} - {level} - {message}")

    return logger
