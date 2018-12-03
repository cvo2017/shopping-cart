import sys
import os
import sqlite3
from contextlib import closing

from business import Product
from business import LineItem

conn = None

def connectDB():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "C:\\Users\\Chau Vo\\Desktop\\shoppingCart\\shopping_cart1.sqlite"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "C:\\Users\\Chau Vo\\Desktop\\shoppingCart\\shopping_cart1.sqlite"
            
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
    enableForeignKey()

def closeDB():
    if conn:
        conn.closeDB()

def enableForeignKey():
    sql = '''PRAGMA foreign_keys = ON'''
    with closing(conn.cursor()) as c:
        c.execute(sql)
    conn.commit()


def createItemObject(row):
    return Product(row["name"], row["price"], row["discount"])

def showInventory():
    query = '''SELECT * FROM Inventory'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    item = []
    for row in results:
        item.append(createItemObject(row))
    return item

def userRegister(username,password):
    if checkUsername(username) == 0:
        sql = '''INSERT INTO User(username, password, role) VALUES (?, ?, ?)'''
        with closing(conn.cursor()) as c:
            c.execute(sql, (username, password, "reg"))
        conn.commit()
        return 1
    else:
        return 0


def checkUsername(username):
    query = '''SELECT * FROM User WHERE username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        row = c.fetchone()
        if row:
            return 1
        else:
            return 0

def userLogin(username,password):
    query = '''SELECT * FROM User WHERE username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
        
        if result:
            if result["password"]== password:
               return 2
            else:
               return 1 
        else:
            return 0

def selectItemCount (username):
    query = '''SELECT count()
                FROM Cart ct
                INNER JOIN User ut ON ut.userid = ct.userid
                LEFT OUTER JOIN Inventory it ON it.itemid = ct.itemid
                WHERE ut.username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
        if result:
               return result["count()"]
        else:
            return 0

    
def createLineItem(row):
    return LineItem(row["itemid"],row["quantity"])

def getCart(username):
    query = '''SELECT  it.itemid , ct.quantity
            FROM Cart ct
            INNER JOIN User ut ON ut.userid = ct.userid
            LEFT OUTER JOIN Inventory it ON it.itemid = ct.itemid
            WHERE ut.username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        results = c.fetchall()

    item = []
    for row in results:
        item.append(createLineItem(row))
    return item

def getProductDetail(itemid):
    query = '''SELECT * FROM Inventory Where itemid = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (itemid,))
        result = c.fetchone()

    return Product(result["name"], result["price"], result["discount"])

def getItemid(name):
    query = '''SELECT * FROM Inventory Where name = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (name,))
        result = c.fetchone()
    return result["itemid"]

def getUserid(username):
    query = '''SELECT * FROM User Where username = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (username,))
        result = c.fetchone()
    return result["userid"]


def addItemtoCart(username,name,quantity):
    itemid = getItemid(name)
    userid = getUserid(username)
    sql = '''INSERT INTO Cart(itemid, userid, quantity) VALUES (?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (itemid, userid, quantity))
    conn.commit()

def deleteItemCart(username,itemid,quantity):
    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Cart WHERE userid = ? AND itemid = ? AND quantity = ?",
          (getUserid(username), itemid, quantity))
    conn.commit()
    
def modifyItemCart(username,itemid,quantity, mod):
    with closing(conn.cursor()) as c:
        c.execute("UPDATE Cart set quantity = ? WHERE userid = ? AND itemid = ? AND quantity = ?",
          (mod, getUserid(username), itemid, quantity))
    conn.commit()

def checkOut(username):
    with closing(conn.cursor()) as c:
        c.execute("DELETE FROM Cart WHERE userid = ?",
          (getUserid(username),))
    conn.commit()

