import json
from server.data.db_connection import *
import ast
from tools.tools import stores_in_radius


cur, con = get_cursor_and_connection()

stores_locations = get_store_positions(cur)

stores = [] 
for store in stores_locations.fetchall(): 
    stores.append((store[0], ast.literal_eval(store[1])))

close_stores = stores_in_radius((12.5597394, 55.65842379999999), stores, 1)

print(close_stores)
print(len(close_stores))

for store in close_stores:
    print(get_store_offers(cur, store[0]).fetchall())
    print()
commit_and_close(con)
            
