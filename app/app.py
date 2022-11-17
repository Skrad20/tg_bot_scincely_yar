#! /app.py
import logging
from logging.handlers import RotatingFileHandler
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, Filters, MessageHandler, CallbackContext, CommandHandler
)
from .answer import AnswerText
from typing import Callable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'logs/app_logger.log',
    maxBytes=50000000,
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


class ScienclyYarBot:
    def __init__(self, token: str) -> None:
        self._token: str = token

    def start(self) -> None:
        self.creater_updater()
        self._updater.start_polling(poll_interval=20.0)
        self._updater.idle()

    def creater_updater(self) -> None:
        self._updater: Updater = Updater(token=self._token)
        self.create_handler_command()
        self.create_handler_messanger()

    def create_handler_command(self) -> None:
        self._updater.dispatcher.add_handler(
            CommandHandler(
                'start',
                FunctoolsBot.start
            )
        )

    def create_handler_messanger(self) -> None:
        self._updater.dispatcher.add_handler(
            MessageHandler(
                Filters.text,
                FunctoolsBot.answer_by_text
            )
        )


class FunctoolsBot:
    @staticmethod
    def answer_by_text(update: Update, context: CallbackContext):
        text_update: str = update.message.text
        answer = AnswerText()
        func: Callable = answer.get_function_answer(text_update)
        func(update, context)

    @staticmethod
    def start(update: Update, context: CallbackContext):
        chat = update.effective_chat
        name_user = update.message.chat.first_name

        buttons = ReplyKeyboardMarkup(
            [
                ['Ближайшие программы', 'О проекте'],
                ['Место проведения программ', "Где купить билеты"],
                ['Частые вопросы'],
            ],
            resize_keyboard=True
        )

        context.bot.send_message(
            chat_id=chat.id,
            text=f'Спасибо, что включили меня, {name_user}',
            reply_markup=buttons
        )
