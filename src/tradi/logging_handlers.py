import logging
from logging import Handler, LogRecord, getLogger
from os import getenv

import sqlparse
from telebot import TeleBot
from telebot.util import antiflood

log_bot = TeleBot(getenv('TELEGRAM_TOKEN', ''))
ERROR_CHAT_ID = getenv('ERROR_CHAT_ID', '')
MAX_MESSAGE_LENGTH = 4096

tg_logger = getLogger('telegram')
main_logger = getLogger('main')


class TelegramHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.bot = log_bot
        self.chat_id = ERROR_CHAT_ID
        self.MAX_MESSAGE_LENGTH = MAX_MESSAGE_LENGTH

    def emit(self, record: LogRecord) -> None:
        log_entry = self.format(record)
        for i in range(0, len(log_entry), self.MAX_MESSAGE_LENGTH):
            antiflood(
                self.bot.send_message,
                self.chat_id,
                log_entry[i : i + self.MAX_MESSAGE_LENGTH],
            )


class SQLFormatterFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        formatted_message = record.getMessage()
        record.msg = sqlparse.format(
            formatted_message,
            reindent=True,
            keyword_case='upper',
            indent_width=4,
        )
        record.args = ()
        return True
