import sqlite3
import json
import ast
from thefuzz import fuzz
from thefuzz import process
from datetime import datetime
from operator import itemgetter

try:
    from sallinggroup.server.data.tools.tools import stores_in_radius
except:
    from tools.tools import stores_in_radius

def get_cursor_and_connection(return_directly=False):
    con = sqlite3.connect("server/data/db.db")
    if return_directly:
        con.row_factory = lambda cursor, row: row[0]
    return (con.cursor(), con)

def commit_and_close(con):
    con.commit()
    con.close()


def create_product(cur, ean, cateogriesEn, categoriesDa, description, image, timestamp):
    cur.execute("REPLACE INTO Products VALUES (?, ?, ?, ?, ?, ?)", (ean, cateogriesEn, categoriesDa, description, image, timestamp))

def create_store(cur, id, phone, address, name, brand, coordinates, timestamp):
    cur.execute("REPLACE INTO Stores VALUES (?, ?, ?, ?, ?, ?, ?)", (id, phone, address, name, brand, coordinates, timestamp))

def create_offer(cur, ean, store, currency, end, newPrice, originalPrice, start, stock, stockUnit, timestamp):
      cur.execute("REPLACE INTO Offers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ean, store, currency, end, newPrice, originalPrice, start, stock, stockUnit, timestamp))


# Custom methods
def get_product(cur, ean):
    return cur.execute("SELECT * FROM Products WHERE ean = ?", ean)

def get_store_offers(cur, store):
    return cur.execute("SELECT * FROM Offers INNER JOIN Products ON Products.ean = Offers.ean WHERE store = ?", (store,))

def get_store_positions(cur):
    return cur.execute("SELECT id, coordinates FROM Stores")


def get_store_position(cur, store_id):
    return cur.execute("SELECT id, coordinates FROM Stores WHERE id = ?", (store_id,))


def get_coords(cur, address):
    return cur.execute("SELECT coords FROM Addresses WHERE (fulladdress LIKE ?)", ('%'+address+'%',))

def get_streets(cur):
    return cur.execute("SELECT DISTINCT address FROM Addresses")

def get_streets_area(cur, area):
    return cur.execute("SELECT DISTINCT address FROM Addresses WHERE area = ?", (area,))


def get_closeby(location):
    cur, con = get_cursor_and_connection()

    stores_locations = get_store_positions(cur)

    stores = [] 
    for store in stores_locations.fetchall(): 
        stores.append((store[0], ast.literal_eval(store[1])))
    close_stores = stores_in_radius(location, stores, 1)
    close_stores.sort(key=itemgetter(1))
    
    info = []
    for store in close_stores:
       info.append(((read_store(cur, store[0]).fetchall(), float(store[1])), get_store_offers(cur, store[0]).fetchall()))

    commit_and_close(con)
    return info



def get_store_page(address):
    cur, con = get_cursor_and_connection()

    stores_locations = get_store_position(cur, address).fetchall()


    stores = [] 
    for store in stores_locations: 
        stores.append((store[0], ast.literal_eval(store[1])))

    stores = stores_in_radius(stores[0][1], stores, 1)

    info = []
    for store in stores:
       info.append(((read_store(cur, store[0]).fetchall(), store[1]), get_store_offers(cur, store[0]).fetchall()))

    commit_and_close(con)
    return info



def get_closeby_address(address):
    cur, con = get_cursor_and_connection()

    location = get_coords(cur, address).fetchall()
    location = ast.literal_eval(location[0][0])
    location = [float(location[1]),float(location[0])]

    stores_locations = get_store_positions(cur).fetchall()


    stores = [] 
    for store in stores_locations: 
        stores.append((store[0], ast.literal_eval(store[1])))
    
    close_stores = stores_in_radius(location, stores, 1)
    close_stores.sort(key=itemgetter(1))
    
    info = []
    for store in close_stores:
       info.append(((read_store(cur, store[0]).fetchall(), store[1]), get_store_offers(cur, store[0]).fetchall()))

    commit_and_close(con)
    return info




def get_store_page_data(store_id):  
    print(store_id)
    cur, con = get_cursor_and_connection()  
    info = [read_store(cur, store_id).fetchall(), get_store_offers(cur, store_id).fetchall()]
    commit_and_close(con)
    return info



def addresses_from_area(area, address):
    cur, con = get_cursor_and_connection(return_directly=True)
    to_return = None

    if area != "":
        streets = get_streets_area(cur, area).fetchall()
    else:
        streets = get_streets(cur).fetchall()
    streets = streets[1:]

    suggestions = process.extract(address, streets, scorer=fuzz.ratio, limit=10)
    to_return = ["<option value=\""+area[0]+"\">"+address+"</option>" for area in suggestions]
    #to_return = [area[0] for area in suggestions]

    commit_and_close(con)
    return  " ".join(to_return)
    #return to_return




# Update methods
def update_product(cur, ean, categoriesEn, categoriesDa, description, image, timestamp):
    cur.execute("UPDATE Products SET categoriesEn = ?, categoriesDa = ?, description = ?, Image = ?, timestamp = ? WHERE ean = ?", (categoriesEn, categoriesDa, description, image, timestamp, ean))

def update_store(cur, id, phone, address, name, brand, coordinates, timestamp):
    cur.execute("UPDATE Stores SET phone = ?, address = ?, name = ?, brand = ?, coordinates = ?, timestamp = ? WHERE id = ?", (phone, address, name, brand, coordinates, timestamp, id))

def update_offer(cur, ean, store, currency, end, newPrice, originalPrice, start, stock, stockUnit, timestamp):
    cur.execute("UPDATE Offers SET store = ?, currency = ?, end = ?, newPrice = ?, originalPrice = ?, start = ?, stock = ?, stockUnit = ?, timestamp = ? WHERE ean = ?", (store, currency, end, newPrice, originalPrice, start, stock, stockUnit, timestamp, ean))



# Read methods
def read_product(cur, ean):
    return cur.execute("SELECT * FROM Products WHERE ean = ?", (ean,))

def read_store(cur, id):
    return cur.execute("SELECT * FROM Stores WHERE id = ?", (id,))

def read_offer(cur, ean):
    return cur.execute("SELECT * FROM Offers WHERE ean = ?", (ean,))



# Delete methods
def delete_product(cur, ean):
    cur.execute("DELETE FROM Products WHERE ean = ?", (ean,))

def delete_store(cur, id):
    cur.execute("DELETE FROM Stores WHERE id = ?", (id,))

def delete_offer(cur, ean):
    cur.execute("DELETE FROM Offers WHERE ean = ?", (ean,))

def delete_past_offers(cur, timestamp):
    cur.execute("DELETE FROM Offers WHERE DATE(end) < ? OR timestamp < ?", (datetime.today().strftime('%Y-%m-%d'), timestamp))