#!/usr/bin/env python3
import os
import json
import CTFd
from pprint import pprint

def read_json(fname):
    with open(fname, "r") as fp:
        return json.load(fp)


def add_ctf(auth):
    foo = {}
    foo["url"] = input("CTFd url> ")
    foo["token"] = input("CTFd token> ")
    auth.append(foo)
    return auth 


def details(challenge):
    print("Connection:", challenge["connection_info"])
    print("Description:", 
            "".join(challenge["description"]))
    print("Solved:", challenge["solved_by_me"])
    print("Value:", challenge["value"])
    print("Hints:", challenge["hints"])


auth = []
if not os.path.exists(".auth.json"):
    auth = add_ctf(auth)
else:
    auth = read_json(".auth.json")
    for i,ctf in enumerate(auth):
        print(i, ctf["url"])
    print(len(auth), "new")
    idx = int(input("Which to play? "))

    if idx < len(auth):
        ctf = auth[idx] 
    else:
        auth = add_ctf(auth)
        ctf = auth[-1]
    #print(foo)
    challs = CTFd.get_challenges(ctf["url"], ctf["token"])
    for i,chall in enumerate(challs):
        print(i, chall)
    idx = int(input(">"))
    print(challs[idx])
    chall = CTFd.get_challenge_details(ctf["url"], ctf["token"], challs[idx])
    #pprint(chall)
    details(chall)

    

# get_players()
# post_attempt()
# get_scoreboard()

with open(".auth.json", "w") as fp:
    json.dump(auth, fp)

