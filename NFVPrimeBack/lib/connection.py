import psycopg2

conn = psycopg2.connect(
    host="192.168.15.120",
    database="postgres",
    user="postgres",
    password="postgres",
    port="5433")