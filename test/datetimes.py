from datetime import datetime
import time

x = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
print(x)
time.sleep(1)
print(datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
print(datetime.strptime(x, "%d-%b-%Y (%H:%M:%S.%f)"))