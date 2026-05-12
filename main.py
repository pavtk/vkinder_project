import logging

from dotenv import load_dotenv

from bot.bot import bot
from database.models import Base
from database.service import engine


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('mylog.log', encoding='utf-8'),
        logging.StreamHandler(),
    ],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
)


Base.metadata.create_all(engine)

if __name__ == "__main__":
    logging.info("Бот запускается...")
    load_dotenv()
    bot.run_forever()
