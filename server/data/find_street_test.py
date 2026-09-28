import csv
import sqlite3
from thefuzz import fuzz
from thefuzz import process
import time


def get_cursor_and_connection():
    con = sqlite3.connect("server/data/db.db")
    con.row_factory = lambda cursor, row: row[0]
    return (con.cursor(), con)

def commit_and_close(con):
    con.commit()
    con.close()


def get_streets(cur):
    return cur.execute("SELECT DISTINCT address FROM Addresses")

def get_streets_area(cur, area):
    return cur.execute("SELECT DISTINCT address FROM Addresses WHERE area = ?", (area,))

def get_areas(cur):
    return cur.execute("SELECT DISTINCT area FROM Addresses")


cur, con = get_cursor_and_connection()

areas = get_areas(cur).fetchall()

ti = time.time()
streets = get_streets(cur).fetchall()
streets = streets[1:]
print(ti-time.time())
ti = time.time()
suggestions = process.extract("Theodore poorsvelts vej 17", streets, scorer=fuzz.ratio, limit=10)
print(ti-time.time())
print(suggestions)

for area in areas:
    print(area)

    ti = time.time()
    streets = get_streets_area(cur, area).fetchall()
    streets = streets[1:]
    print(ti-time.time())
    print(len(streets))
    ti = time.time()
    suggestions = process.extract("Theodore poorsvelts vej 17", streets, scorer=fuzz.ratio, limit=10)
    print(ti-time.time())
    #print(suggestions)


commit_and_close(con)



