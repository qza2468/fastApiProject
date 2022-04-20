import requests
import json

host = "http://localhost:8000/"
body = {"name": "qza2468", "password": "123456"}

res = None

for i in range(5):
    print("=========================================")
    print("test login with ", body)
    res = requests.post(host + "api/login", json=body)
    print("received result: ")

    print(res.content)
    print("==========================================")

cookie = json.loads(res.content)["token"]
res = requests.post(host + "api/removeOtherCookies", headers={"token": cookie})
print(res.content)

res = requests.post(host + "api/createuser", headers={"token": cookie}, json={"name": "better", "password": "usedto"})
print(res.content)

res = requests.post(host + "api/logout", headers={"token": cookie})
print(res.content)

res = requests.post(host + "api/login", json={"name": "better", "password": "usedto"})
print(res.content)

res = requests.post(host + "api/createuser", headers={"token": json.loads(res.content)["token"]}, json={"name": "best", "password": "no"})

print(res.content)

