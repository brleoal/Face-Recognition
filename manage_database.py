""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sqlite3
import os

def createDatabase():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        sql_create_table_query = """CREATE TABLE users (id INTEGER PRIMARY
                                 KEY, username TEXT NOT NULL, passwd TEXT
                                 NOT NULL, photo BLOB NOT NULL, traindata
                                 BLOB NOT NULL)
                                 """
        c.executescript(sql_create_table_query)
        conn.commit()
        print('Database created successfully')
    except sqlite3.Error as error:
        print('Failed to create database', error)    
    finally:
        conn.close()
        print('The SQLite connection is closed')

def insertData(ID, username, passwd, photo, traindata):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        sql_insert_blob_query = """INSERT INTO users (id, username, passwd,
                                photo, traindata) VALUES (?, ?, ?, ?, ?)
                                """
        if os.path.isfile(photo):
            with open(photo, 'rb') as f1:
                usrPhoto = f1.read()
        else:
            print('Error: File {} does not exist'.format(photo))
        if os.path.isfile(traindata):
            with open(traindata, 'rb') as f2:
                usrData = f2.read()
        else:
            print('Error: File {} does not exist'.format(traindata))
        #username = unicode(username, 'utf-8')
        #passwd = unicode(passwd, 'utf-8')
        data = (ID, username, passwd, sqlite3.Binary(usrPhoto),
                sqlite3.Binary(usrData))
        c.execute(sql_insert_blob_query, data)
        conn.commit()
        print('Data inserted successfully')
    except IOError as error:
        print(error)
    except sqlite3.Error as error:
        print('Failed to insert data', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')

def updateData(param, username, passwd, photo):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        query = {
            0: "UPDATE users SET passwd = ? WHERE username = ?",
            1: "UPDATE users SET photo = ? WHERE username = ?"
        }
        sql_update_query = query.get(param, 'Invalid parameter')
        if param == 0:
            #username = unicode(username, 'utf-8')
            #passwd = unicode(passwd, 'utf-8')
            columnValues = (passwd, username)
            c.execute(sql_update_query, columnValues)
            conn.commit()
            print('Password updated successfully')
        elif param == 1:
            if os.path.isfile(photo):
                with open(photo, 'rb') as f:
                    usrPhoto = f.read()
                #username = unicode(username, 'utf-8')
                columnValues = (sqlite3.Binary(usrPhoto), username)
                c.execute(sql_update_query, columnValues)
                conn.commit()
                print('Photo updated successfully')
            else:
                print('Error: File {} does not exist'.format(photo))
    except IOError as error:
        print(error)
    except sqlite3.Error as error:
        print('Failed to update database', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')

def getData(param, id, user, passwd):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        query = {
            0: "SELECT * FROM users WHERE id = ? AND passwd = ?",
            1: "SELECT * FROM users WHERE username = ? AND passwd = ?"
        }
        sql_fetch_blob_query = query.get(param, 'Invalid parameter')
        #username = unicode(user, 'utf-8')
        #passwd = unicode(passwd, 'utf-8')
        tablelist = {
            0: (id, passwd),
            1: (user, passwd)
        }
        data = tablelist.get(param, 'Invalid parameter')
        c.execute(sql_fetch_blob_query, data)
        record = c.fetchone()
        if record is not None:
            print('Data successfully obtained')
        else:
            print('Inserted data are incorrect')
        return record
    except sqlite3.Error as error:
        print('Failed to read data from database', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')

def getLastID():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        sql_lastid_query = "SELECT COUNT(id) FROM users"
        c.execute(sql_lastid_query)
        return c.fetchone()[0]
    except sqlite3.Error as error:
        print('Failed to read data from database', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')

def deleteData(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        sql_delete_query = """DELETE FROM users WHERE username = ?"""
        #username = unicode(username, 'utf-8')
        c.execute(sql_delete_query, (username,))
        conn.commit()
        print('Record deleted successfully')
    except sqlite3.Error as error:
        print('Failed to delete record from database', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')
