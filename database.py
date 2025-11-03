import sqlite3

def get_connection():
    conn = sqlite3.connect("accounts.db")
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS accounts(summoner_name TEXT, rank TEXT, redcarpet INT, bluecarpet INT)")

def create_player(summoner_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts(summoner_name, rank, redcarpet, bluecarpet) VALUES(?,?,?,?)", (summoner_name, None, None, None))
    conn.commit()
    conn.close()

def insert_bluecarpet_to_database(name, bluecarpet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET bluecarpet = ?, redcarpet = ? WHERE summoner_name = ?", (bluecarpet, 0, name))
    conn.commit()
    conn.close()

def insert_redcarpet_to_database(name, redcarpet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET redcarpet = ?, bluecarpet = ? WHERE summoner_name = ?", (redcarpet, 0, name))
    conn.commit()
    conn.close()

def insert_rank_to_databse(name, rank):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET rank = ? WHERE summoner_name = ?", (rank, name))
    conn.commit()
    conn.close()

def get_rank_from_database(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rank FROM accounts WHERE summoner_name = ?", (name))
    result = cursor.fetchone()
    if(result):
        return result[0]
    else:
        return None
    
def get_bluecarpet_from_database(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT bluecarpet FROM accounts WHERE summoner_name = ?", (name))
    result = cursor.fetchone()
    if(result):
        return result[0]
    else:
        return None
    
def get_redcarpet_from_database(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT redcarpet FROM accounts WHERE summoner_name = ?", (name))
    result = cursor.fetchone()
    if(result):
        return result[0]
    else:
        return None
    
def check_database_for_account(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM accounts WHERE summoner_name = ?", (name))
    result = cursor.fetchone()
    if(result):
        return result[0]
    else:
        return None


