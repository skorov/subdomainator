#!/usr/bin/python
# Sqlite database connector
# Author: skorov

import sqlite3

DATABASE = ""


def connect(database):
    global DATABASE
    DATABASE = database


def createdb():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS domains (domain text primary key)''')
        c.execute('''CREATE TABLE IF NOT EXISTS subdomains (subdomain text, domain text, primary key(subdomain, domain))''')
        c.execute('''CREATE TABLE IF NOT EXISTS pushkeys (key text primary key)''')
        conn.commit()
    except Exception as e:
        print(str(e))


def destroydb():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS domains''')
        c.execute('''DROP TABLE IF EXISTS subdomains''')
        c.execute('''DROP TABLE IF EXISTS pushkeys''')
        conn.commit()
    except Exception as e:
        print(str(e))


def dbexists():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM domains")
        c.execute("SELECT * FROM subdomains")
        c.execute("SELECT * FROM pushkeys")
        return True
    except Exception:
        return False


def getDomains():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''SELECT domain FROM domains''')
        domains = c.fetchall()
        conn.commit()
        return [x[0] for x in domains]
    except Exception as e:
        print(str(e))


def addDomain(domain):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO domains values(?)", [domain])
        conn.commit()
    except sqlite3.IntegrityError:
        print("Domain already added: %s" % domain)
        return False
    except Exception as e:
        print(str(e))
        return False


def deleteDomain(domain):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM domains WHERE domain = ''?''', [domain])
        c.execute('DELETE FROM subdomains WHERE domain = ''?''', [domain])
        conn.commit()
    except Exception as e:
        print(str(e))
        return False


def getPushkeys():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''SELECT key FROM pushkeys''')
        keys = c.fetchall()
        conn.commit()
        return [x[0] for x in keys]
    except Exception as e:
        print(str(e))


def addPushkey(key):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO pushkeys values(?)", [key])
        conn.commit()
    except sqlite3.IntegrityError:
        print("Key already added: %s" % key)
        return False
    except Exception as e:
        print(str(e))
        return False


def deletePushkey(key):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM pushkeys WHERE key = ''?''', [key])
        conn.commit()
    except Exception as e:
        print(str(e))
        return False


def getSubdomains(domain):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM subdomains WHERE domain = ''?''', [domain])
        subdomains = c.fetchall()
        conn.commit()
        return [x[0] for x in subdomains]
    except Exception as e:
        print(str(e))


def addSubdomain(subdomain, domain):
    if (domain not in getDomains()):
        print("Domain is not being tracked: %s" % domain)
        return False

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO subdomains values(?,?)", [subdomain, domain])
        conn.commit()
    except sqlite3.IntegrityError:
        print("Subdomain already added: %s.%s" % (subdomain, domain))
        return False
    except Exception as e:
        print(str(e))
        return False
