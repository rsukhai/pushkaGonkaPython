import os
from datetime import datetime
import shutil

class LoggingError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class Logger:
    def __init__(self, log_file_prefix='consolidated_logs'):
        self.log_file = self._generate_log_file_name(log_file_prefix)
        self.old_logs = []
        

        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except PermissionError:
                raise LoggingError(f"Немає прав для створення директорії: {log_dir}")
            except Exception as e:
                raise LoggingError(f"Помилка при створенні директорії: {e}")

    def _generate_log_file_name(self, log_file_prefix):
        """Генерує ім'я файлу логу на основі поточної дати."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        return f"{log_file_prefix}_{current_date}.txt"

    def log(self, level, message):
        """Запис повідомлення в лог."""
        log_entry = f"{datetime.now()} - {level.upper()} - {message}"
        self.old_logs.append(log_entry)
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(log_entry + "\n")
        except PermissionError:
            raise LoggingError(f"Немає прав на запис у файл: {self.log_file}")
        except Exception as e:
            raise LoggingError(f"Помилка запису в файл логу: {e}")

    def info(self, message):
        self.log('info', message)

    def warning(self, message):
        self.log('warning', message)

    def error(self, message):
        self.log('error', message)

    def critical(self, message):
        self.log('critical', message)

    def save_old_logs_to_file(self, output_file='old_logs.txt'):
        """Запис усіх старих логів в окремий файл."""
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                for log in self.old_logs:
                    file.write(log + "\n")
            print(f"Старі логи були успішно збережені в {output_file}")
        except PermissionError:
            raise LoggingError(f"Немає прав на запис у файл: {output_file}")
        except Exception as e:
            raise LoggingError(f"Помилка запису старих логів: {e}")
    
    def move_old_logs_to_all_logs(self, old_logs_file='old_logs.txt', all_logs_file='all_logs.txt'):
        """Переміщення даних з old_logs.txt в all_logs.txt з підписом дати та очищення old_logs.txt."""
        try:
            with open(old_logs_file, 'r', encoding='utf-8') as file:
                logs = file.readlines()
            with open(all_logs_file, 'a', encoding='utf-8') as file:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for log in logs:
                    file.write(f"{current_date} - {log.strip()}\n")
            
            open(old_logs_file, 'w', encoding='utf-8').close()
            
            print(f"Логи з {old_logs_file} успішно переміщені в {all_logs_file} і {old_logs_file} очищено.")
        
        except FileNotFoundError:
            raise LoggingError(f"Файл {old_logs_file} не знайдено.")
        except PermissionError:
            raise LoggingError(f"Немає прав на запис у файл: {all_logs_file}")
        except Exception as e:
            raise LoggingError(f"Помилка під час переміщення логів: {e}")

    def archive_logs(self, log_files, archive_dir='logs_archive'):
        """Архівація старих лог-файлів з обробкою можливих помилок."""
        if not os.path.exists(archive_dir):
            try:
                os.makedirs(archive_dir)
            except PermissionError:
                raise LoggingError(f"Немає прав для створення директорії архіву: {archive_dir}")
            except Exception as e:
                raise LoggingError(f"Помилка при створенні директорії архіву: {e}")
        
        for log_file in log_files:
            try:
                if os.path.exists(log_file):
                    shutil.move(log_file, os.path.join(archive_dir, os.path.basename(log_file)))
                    print(f"Лог файл {log_file} було успішно архівовано.")
                else:
                    raise LoggingError(f"Файл {log_file} не знайдено.")
            except PermissionError:
                raise LoggingError(f"Немає прав для переміщення файлу {log_file} до архіву.")
            except Exception as e:
                raise LoggingError(f"Помилка архівації файлу {log_file}: {e}")

logger = Logger('logs')

logger.info("Інформаційне повідомлення")
logger.warning("Це попередження")
logger.error("Це помилка")
logger.critical("Це критична помилка")

logger.save_old_logs_to_file('old_logs.txt')


logger.move_old_logs_to_all_logs('old_logs.txt', 'all_logs.txt')

logger.archive_logs(['old_logs.txt', logger.log_file], archive_dir='logs_archive')
