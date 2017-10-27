import md5
import requests
from requests.auth import HTTPBasicAuth

url  = "http://localhost:5000/computing/api/v1.0/students"

username = None
password = None

while True:

    username = raw_input("username to connect server: ")

    password = raw_input("password to connect server: ")

    if username and password:

        md = md5.new()
        md.update(password)

        password = md.hexdigest()
        res = requests.get(url, auth = HTTPBasicAuth(username,password))
        if res.ok:
            res = requests.get("http://localhost:5000/", auth = HTTPBasicAuth(username,password))
            print "---> " + res.json() +" <---"

            res = requests.get(url, auth=HTTPBasicAuth(username, password))
            print res.json()

            break
        else:

            print "---> "+res.json()["error"]+" <---"
    else:
        print ("\n---> Fill in correctly <---\n")

