import csv
import sqlite3




def get_cursor_and_connection():
    con = sqlite3.connect("server/data/db.db")
    return (con.cursor(), con)

def commit_and_close(con):
    con.commit()
    con.close()


def create_street(cur, address, coords, postalcode, number, area, fulladdress):
    cur.execute("REPLACE INTO Addresses VALUES (?, ?, ?, ?, ?, ?)", (address, coords, postalcode, number, area, fulladdress))


cur, con = get_cursor_and_connection()
with open('server/data/streetsnames.csv', mode ='r', encoding='UTF-8') as file:
  csvFile = csv.reader(file)
  for info in csvFile:
        line = info[0].split("\t")
        add = line[2]+" "+line[1]+', '+line[3]+', '+line[4]
        create_street(cur, line[2], str([line[5], line[6]]), line[4], line[1], line[3], add)

commit_and_close(con)
