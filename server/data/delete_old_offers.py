from db_connection import *
import requests
import numpy as np
import time
import json
from constants import salling_token
from datetime import datetime

cur, con = get_cursor_and_connection()

timestamp = datetime.now().strftime("%Y-%m-%d (%H:%M:%S.%f)")
print(timestamp)
delete_past_offers(cur, timestamp)

commit_and_close(con)