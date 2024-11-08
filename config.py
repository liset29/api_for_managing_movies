
import os
from dotenv import load_dotenv
from crypto_utils import load_private_key, load_public_key

load_dotenv()


# Настройки базы данных
DB_HOST = os.getenv("HOST")
DB_USER = os.getenv("USER")
DB_PASS = os.getenv("PASSWORD")
DB_NAME = os.getenv("DATABASE")
DB_PORT = os.getenv("PORT")
data_base_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"



# Настройки аутентификации и JWT
algorithm = os.getenv("algorithm")
access_token_expire = os.getenv("access_token_expire")


# Пути к публичному и приватному ключам из переменных окружения
public_path = os.getenv("public_path")
private_path = os.getenv("private_path")



private_key = load_private_key(private_path)
public_key = load_public_key(public_path)

