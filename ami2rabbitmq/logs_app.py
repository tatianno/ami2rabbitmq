from datetime import datetime


class LogsApp:

    def __init__(self, DEBUG):
        self.debug = DEBUG

    def format_msg(self, msg: str) -> str:
        return f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {msg}'

    def register(self, msg: str) -> None:
        
        if self.debug:
            print(self.format_msg(msg))
