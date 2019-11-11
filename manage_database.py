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
            with open(photo, 'rb') as f:
                usrPhoto = f.read()
        else:
            print('Error: File {} does not exist'.format(photo))
        if os.path.isfile(traindata):
            with open(traindata, 'rb') as f:
                usrData = f.read()
        else:
            print('Error: File {} does not exist'.format(traindata))
        username = unicode(username, 'utf-8')
        passwd = unicode(passwd, 'utf-8')
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

def updateData(username):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        data = input('Which data you want to update? (1-password, 2-photo):')
        if data == 1:
            sql_update_query = """UPDATE users SET passwd = ? WHERE
                               username = ?
                               """
            while True:
                passwd = raw_input('Enter new user password:')
                retpasswd = raw_input('Retype new user password:')
                if passwd == retpasswd:
                    break
                print('Sorry, try again')
            username = unicode(username, 'utf-8')
            passwd = unicode(passwd, 'utf-8')
            columnValues = (passwd, username)
            c.execute(sql_update_query, columnValues)
            conn.commit()
            print('Password updated successfully')
        elif data == 2:
            sql_update_query = """UPDATE users SET photo = ? WHERE
                               username = ?
                               """
            photo = raw_input('Enter the path of file:')
            if os.path.isfile(photo):
                with open(photo, 'rb') as f:
                    usrPhoto = f.read()
                username = unicode(username, 'utf-8')
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

def getData(username, passwd):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        print('Connected to SQLite')
        sql_fetch_blob_query = """SELECT * FROM users where username = ?
                               AND passwd = ?
                               """
        username = unicode(username, 'utf-8')
        passwd = unicode(passwd, 'utf-8')
        data = (username, passwd)
        c.execute(sql_fetch_blob_query, data)
        record = c.fetchone()
        if record is not None:
            print('Data successfully obtained')
        else:
            print('Username or password are incorrect')
        return record
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
        username = unicode(username, 'utf-8')
        cursor.execute(sql_delete_query, (username,))
        conn.commit()
        print('Record deleted successfully')
    except sqlite3.Error as error:
        print('Failed to delete record from database', error)
    finally:
        conn.close()
        print('The SQLite connection is closed')
