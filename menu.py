import json
from typing import Dict, Any, Callable
from users import UserDatabase
from config import settings


class ConfigurableMenu:
    def __init__(self, db_instance, config_path: str, section: str):
        self.db = db_instance
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)[section]
        self.table_name = self.config["table_name"]

    def get_action(self, key: str) -> Callable[[], None]:
        """Создаёт функцию для выполнения действия на основе конфигурации."""
        action_config = self.config["actions"].get(key, {})
        method_name = action_config.get("method")
        if not method_name:
            return None

        method = getattr(self.db, method_name)
        args = action_config.get("args", [])
        defaults = action_config.get("defaults", {})
        prompts = action_config.get("prompt", {})

        def action():
            # Собираем аргументы для вызова метода
            resolved_args = []
            for arg in args:
                if arg == "table_name":
                    resolved_args.append(self.table_name)
                elif arg in prompts:
                    # Запрашиваем ввод у пользователя, если есть prompt
                    value = input(prompts[arg])
                    # Преобразуем тип для чисел (например, age)
                    if arg == "age":
                        value = int(value) if value else defaults.get(arg)
                    resolved_args.append(value or defaults.get(arg))
                else:
                    # Используем значение по умолчанию, если нет prompt
                    resolved_args.append(defaults.get(arg))
            
            # Выполняем метод с собранными аргументами
            method(*resolved_args)

        return action

    def display(self) -> None:
        """Отображает меню."""
        print(f"Таблица: {self.table_name}")
        for key, info in self.config["actions"].items():
            print(f"{key} - {info['description']}")
        print("0 - Выйти")

    def run(self) -> None:
        """Запускает цикл меню."""
        while True:
            self.display()
            choice = input("Введите номер действия: ")
            if choice == "0":
                break
            action = self.get_action(choice)
            if action:
                try:
                    action()
                except Exception as e:
                    self.db.logger.error(f"Error executing action {choice}: {e}")
                    print(f"Ошибка: {e}")
            else:
                print("Некорректный выбор, попробуйте снова.")

if __name__ == "__main__":
    try:
        with UserDatabase(settings, log_dir="custom_logs") as user_db:
            user_menu = ConfigurableMenu(user_db, "menu_config.json", "users")
            user_menu.run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")