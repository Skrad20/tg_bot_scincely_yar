import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from typing import Callable
from settings import PATH_STATIC
from app.parsing import ParserProgram


class Answer:
    """
    Возвращает функцию ответа на вопрос.
    """
    def __init__(self) -> None:
        self.answer_dict: dict[str, Callable] = {}

    def get_function_answer(self, text: str) -> Callable:
        return self.answer_dict.get(text, self.default_answer)

    def default_answer(self, update: Update, context: CallbackContext):
        chat = update.effective_chat
        name_user = update.message.chat.first_name
        text = (
            f"К сожалению я Вас не понял, {name_user}." +
            "Пожалуйста, переформулируйте Ваш вопрос."
        )

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
            text=text,
            reply_markup=buttons
        )


class AnswerText(Answer):
    """
    Возвращает функцию ответа на текстовый вопрос.
    """
    def __init__(self) -> None:
        super().__init__()
        self.answer_dict = {
            'Ближайшие программы': self.upcoming_programs,
            'О проекте': self.about,
            'Место проведения программ': self.location_of_the_programs,
            "Где купить билеты": self.where_to_buy_tickets,
            'Частые вопросы': self.frequent_questions,
        }
        self.url_site = "https://smartyar.timepad.ru/events/"

    def upcoming_programs(self, update: Update, context: CallbackContext):
        chat = update.effective_chat
        buttons = ReplyKeyboardMarkup(
            [
                ['Ближайшие программы', 'О проекте'],
                ['Место проведения программ', "Где купить билеты"],
                ['Частые вопросы'],
            ],
            resize_keyboard=True
        )

        pp = ParserProgram()
        data = pp.get_data()
        for prog in data:
            text = (
                "Название программы: " + prog.name + "\n" +
                "Когда: " + prog.period + "\n" +
                "Через сколько: " + prog.time_data + "\n" +
                "О чём: " + prog.description + "\n" +
                f'<a href="{prog.link}">Подробнее</a>'
            )
            context.bot.send_message(
                chat_id=chat.id,
                text=text,
                reply_markup=buttons,
                parse_mode="HTML"
            )

    def about(self, update: Update, context: CallbackContext):
        text = (
            "Проект «Умный Ярославль» — научные программы" +
            " для детей 7-14 лет.\n" + " 🔬Интерактивные научные программы" +
            " для детей 5-14 лет. 🧑🏻‍🔬Наша команда молодых учёных уже" +
            " больше 3 лет " +
            " влюбляет детей в естественные науки. \n" +
            f'<a href="{self.url_site}">Наш сайт</a>\n' +
            "Телефон для связи: +7 (980) 747-21-72\n" +
            "Также доступны в WhatsApp."
        )

        chat = update.effective_chat
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
            text=text,
            reply_markup=buttons,
            parse_mode="HTML"
        )

    def location_of_the_programs(
        self, update: Update,
        context: CallbackContext
    ):
        text = "Угличская улица, 24, Ярославль, 150054"
        chat = update.effective_chat
        buttons = ReplyKeyboardMarkup(
            [
                ['Ближайшие программы', 'О проекте'],
                ['Место проведения программ', "Где купить билеты"],
                ['Частые вопросы'],
            ],
            resize_keyboard=True
        )
        context.bot.send_photo(
            chat_id=chat.id,
            photo=open(
                os.path.join(PATH_STATIC, "map.png"),
                'rb'
            )
        )
        context.bot.send_message(
            chat_id=chat.id,
            text=text,
            reply_markup=buttons,
            parse_mode="HTML"
        )

    def where_to_buy_tickets(self, update: Update, context: CallbackContext):
        text = (
            "Билеты можно приобрести по" +
            f' <a href="{self.url_site}">ссылке</a>.' +
            " Или по телефону: +7 (980) 747-21-72"
        )

        chat = update.effective_chat
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
            text=text,
            reply_markup=buttons,
            parse_mode="HTML"
        )

    def frequent_questions(self, update: Update, context: CallbackContext):
        pass


class AnswerCommand(Answer):
    """
    Возвращает функцию ответа на вопрос-команду.
    """
    pass
