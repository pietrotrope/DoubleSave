import requests

x = requests.get('https://pietrotrope.pythonanywhere.com/updateoffers?p1=dhg30e83jbofu30jg79e2202KJGD0dG')
print(x.status_code)