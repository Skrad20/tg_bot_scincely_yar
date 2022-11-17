from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN_TELEGRAM_BOT: str = os.environ.get("TOKEN")

basname = os.path.basename(__file__)
abs_path = os.path.abspath(__file__).replace(basname, '')
PATH_STATIC = os.path.join(abs_path, "static")
