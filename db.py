import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

#def execute(sql, params=[]):
#    con = get_connection()
#    result = con.execute(sql, params)
#    con.commit()
#    g.last_insert_id = result.lastrowid
#    con.close()
def execute(sql, params=[]):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(sql, params)
    con.commit()
    
    # Fetch the last inserted ID using last_insert_rowid()
    cursor.execute("SELECT last_insert_rowid()")
    last_insert_id = cursor.fetchone()[0]  # Fetch the row and get the first element
    
    g.last_insert_id = last_insert_id  # Store the integer ID
    
    cursor.close()
    con.close()

def last_insert_id(): 
    return g.last_insert_id    
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def execute_batch_insert(sql, params_list):
    con = get_connection()
    cursor = con.cursor()
    cursor.executemany(sql, params_list)
    con.commit()
    con.close()