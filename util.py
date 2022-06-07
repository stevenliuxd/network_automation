import json
from time import sleep

def getcreds(name):

    with open('credentials.json', 'r') as f:
        userdata = json.load(f)

    cred = userdata["data"]

    for x in cred:
        if name == x["name"]:
            cred_dict = {'hostname': x["hostname"], 'port': '22', 'username': x["username"], 'password': x["password"]}
            return cred_dict
                

def wait(duration=2):
    
    sleep(duration)

