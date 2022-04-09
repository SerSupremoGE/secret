import sqlite3
import asyncio
import config
from SimpleQIWI import *
async def add_user(id,ref_id=None):
    with sqlite3.connect("piramid.db") as c:
        info = c.execute("SELECT id FROM users WHERE id = ?",(ref_id,)).fetchone()
        info_user = c.execute("SELECT id FROM users WHERE id =?",(id,)).fetchone()
        print(info)
        print(info_user)
        print("slito v https://t.me/Slivki_Logs")
        if info == None and info_user == None:
            c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)",(id,0,0,0,None,0,))
        elif info != None and info_user == None:
            c.execute("INSERT INTO users VALUES(?,?,?,?,?,?)",(id,0,0,0,ref_id,0,))
            c.execute("UPDATE users SET purchases_ref = purchases_ref+1 WHERE id = ?",(info[0],))

async def take_info_user(id):
    with sqlite3.connect("piramid.db") as c:
        info = c.execute("SELECT * FROM users WHERE id = ?",(id,)).fetchone()
        return info

async def replace(id):
    with sqlite3.connect("piramid.db") as c:
        c.execute("UPDATE users SET status = 1,level = 1 WHERE id = ?",(id,))
    
    with sqlite3.connect("piramid.db") as c:
        
        info = c.execute("SELECT * FROM users WHERE id = ?",(id,)).fetchone()
        print(info)
        information = c.execute("SELECT * FROM users WHERE id = ?",(info[4],)).fetchone()
        print(information)
        print("# слито https://t.me/Slivki_Logs")
        if info[4] != None:
        
        	if information[-1] == 1:
        		balance = config.access_cost * config.PERCENT_1
        		c.execute("UPDATE users SET balance = balance+? WHERE id = ?",(balance,information[0],))
        		c.execute("UPDATE users SET level =level+1 WHERE id = ?",(information[0],))
        
        	elif information[-1] == 2:
        		balance = config.access_cost * config.PERCENT_2
        		c.execute("UPDATE users SET balance =balance+? WHERE id = ?",(balance,information[0],))
        		c.execute("UPDATE users SET level =level+1 WHERE id = ?",(information[0],))
        
        	elif information[-1] == 3:
        		balance = config.access_cost * config.PERCENT_3
        		c.execute("UPDATE users SET balance =balance+? WHERE id = ?",(balance,information[0],))
        elif info[4] == None:
            pass

async def info_users():
    with sqlite3.connect("piramid.db") as c:
        vip_users = c.execute("SELECT id FROM users WHERE status = 1").fetchall()
    with sqlite3.connect("piramid.db") as c:
        all_users = c.execute("SELECT id FROM users").fetchall()
    return len(vip_users),len(all_users)

async def check_pay(id,price):
    with sqlite3.connect("piramid.db") as c:
        balance = c.execute("SELECT balance FROM users WHERE id =?",(id,)).fetchone()
        print(balance)
        if int(price)<= int(balance[0]) and config.MIN_PAYOUT <= int(balance[0]) and config.MIN_PAYOUT<= int(price):
            c.execute("UPDATE users SET balance = balance-? WHERE id =?", (price, id,)) 
            return True
        else:
            return False

"""async def pay(price,number,id):
    
    api = QApi(token=config.QIWI_TOKEN, phone=config.QIWI_NUMBER)
    try:
    	api.pay(account=number, amount=price, comment='Привет мир!')
    	with sqlite3.connect("piramid.db") as c:
            bal = c.execute("SELECT balance FROM users WHERE id = ?",(id,)).fetchone()[0]
            balance = int(bal)- int(price)
            c.execute("UPDATE users SET balance= ? WHERE id = ?",(balance,id,))
            return True
    except Exception as e:
        print(e)
        return False"""


async def add_application(id,username,price,number):
    username =f"@{username}"
    with sqlite3.connect("piramid.db") as c:
        c.execute("INSERT INTO application VALUES(?,?,?,?)",(id,username,price,number,))

async def take_application():
    with sqlite3.connect("piramid.db") as c:
        info = c.execute("SELECT * FROM application").fetchall()
        return info

async def delete_application(id, price=0):
    with sqlite3.connect("piramid.db") as c:
        c.execute("UPDATE users SET balance = balance+? WHERE id = ?",(price, id,)) 
        
        c.execute("DELETE FROM application WHERE id = ?",(id,))

async def delete_app(id):
    with sqlite3.connect("piramid.db") as c:
       
        
        c.execute("DELETE FROM application WHERE id = ?",(id,))