from environs import Env
import random

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

photo_start = "https://i.imgur.com/Di5160N.png"
photo_wooden_wall = "https://rustlabs.com/img/screenshots/wall1.png"

f = open('C:\\Users\\farca\\Desktop\\Rust_bot\\tokens.txt', 'r')
tokens = f.read().split("\n")
f.close()

