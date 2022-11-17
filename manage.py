#! /main.py
import logging
from app.app import ScienclyYarBot
from logging.handlers import RotatingFileHandler
from settings import TOKEN_TELEGRAM_BOT


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(
    'logs/main_logger.log',
    maxBytes=50000000,
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


def main():
    app = ScienclyYarBot(TOKEN_TELEGRAM_BOT)
    app.start()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        print("exit")
