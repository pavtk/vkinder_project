import os

from dotenv import load_dotenv

load_dotenv()

VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')
VK_USER_TOKEN = os.getenv('VK_USER_TOKEN')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'vkinder')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

DATABASE_URL = (
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
