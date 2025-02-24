import random
import sqlite3
from data import config as cfg
from datetime import datetime
from loader import bot
conn = sqlite3.connect(r"utils\db_api\database.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id PRIMARY KEY,
    username TEXT,
    date INT)
""")
cur.execute("""CREATE TABLE IF NOT EXISTS chat(
    user_id INT,
    role TEXT,
    content TEXT)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS adv_chats(
    id INT PRIMARY KEY,
    user_count INT,
    url TEXT,
    name TEXT
)""")


#Users
def create_user(userId,username):
    try:
        date = str(datetime.now())[:19]
        cur.execute("INSERT INTO users VALUES(?,?,?)",(userId,username,date))
        conn.commit()
    except Exception as e:
        pass

def parse_user_data(data):
    return {'id':data[0],'username':data[1],'date':data[2]}

def get_all_users():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(parse_user_data(crtj))
    return result

def get_user_ids():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(int(crtj[0]))
    return result

def get_user(userId):
    try:
        user_data = cur.execute("SELECT * FROM users WHERE id = ?",(userId,)).fetchone()
        pass
    except:
        pass

def update_userfield(user_id,field,update):
    cur.execute(f"UPDATE users SET {field} = ? WHERE id = ?",(update,user_id))
    conn.commit()

def plus_userfield(user_id,field,plus_value):
    old = cur.execute(f"SELECT {field} FROM users WHERE id = ?", (user_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_userfield(user_id,field,new)

def create_adv_chat(id,url,name):
    try:
        cur.execute("INSERT INTO adv_chats VALUES(?,?,?,?)",(id,0,url,name))
        conn.commit()
    except:
        pass
def get_adv_chat(id):
    x = cur.execute("SELECT * FROM adv_chats WHERE id = ?",(id,)).fetchone()
    return parse_adv_chat_data(x)
def get_all_adv_chats():
    res = []
    datas = cur.execute("SELECT * FROM adv_chats").fetchall()
    for data in datas:
        res.append(parse_adv_chat_data(data))
    return res
def get_all_adv_chats_id():
    res = []
    datas = cur.execute("SELECT * FROM adv_chats").fetchall()
    for data in datas:
        res.append(data[0])
    return res
def parse_adv_chat_data(data):
    return {'id':data[0],'user_count':data[1],'url':data[2],'name':data[3]}

def delete_adv_chat(id):
    cur.execute("DELETE FROM adv_chats WHERE id = ?",(id,))
    conn.commit()

def update_adv_chat_field(chat_id,field,update):
    cur.execute(f"UPDATE adv_chats SET {field} = ? WHERE id = ?",(update,chat_id))
    conn.commit()

def plus_adv_chat_field(chat_id,field,plus_value):
    old = cur.execute(f"SELECT {field} FROM adv_chats WHERE id = ?", (chat_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_adv_chat_field(chat_id,field,new)

def plus_user_count_to_all():
    ids = get_all_adv_chats_id()
    for id in ids:
        plus_adv_chat_field(id,'user_count',1)

def delete_users_for_ids(ids: list):
    for id in ids:
        cur.execute(f"DELETE FROM users WHERE id = ?", (id,))
        conn.commit()


