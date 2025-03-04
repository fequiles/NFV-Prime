import hashlib
import os
import psycopg2

def createUser(conn, data):
    username = data['username']
    password = data['password']
    # Generate a random salt
    salt = os.urandom(32)
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    # Add the salt to the password and hash it
    hash_object.update(salt + password.encode())
    # Get the hex digest of the hash
    hash_password = hash_object.hexdigest()

    curs_obj = conn.cursor()
    curs_obj.execute("INSERT INTO users(username, password, salt) VALUES(%s, %s , %s)", (username, hash_password, psycopg2.Binary(salt)))
    conn.commit()
    curs_obj.close()

def getUserIdByUsername(conn, data):
    username = data['username']
    print(username)
    curs_obj = conn.cursor()

    curs_obj.execute("SELECT user_id FROM users WHERE username = '{}' LIMIT 1".format(username))
    rows = curs_obj.fetchall()
    id = rows[0][0]
    curs_obj.close()

    return id
