
class OldLogger:
    def log(self, message):
        print(f"OldLogger: {message}")


class NewLogger:
    def write_log(self, msg):
        print(f"NewLogger: {msg}")


class LoggerAdapter(OldLogger):
    def __init__(self, new_logger):
        self.new_logger = new_logger
    
    def log(self, message):
        self.new_logger.write_log(message)


if __name__ == "__main__":
    old_logger = OldLogger()
    old_logger.log("Повідомлення від старого логера")

    # Новий логер через адаптер
    new_logger = NewLogger()
    adapter = LoggerAdapter(new_logger)
    adapter.log("Повідомлення від нового логера через адаптер")
