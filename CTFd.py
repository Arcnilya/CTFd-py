#!/usr/bin/env python3

import os
import sys
import requests
import argparse
from pprint import pprint

DEBUG=True

def read_file(fname):
    with open(fname, "r") as fp:
        return fp.read().splitlines()


def get_chall_id(url, token, chall_name):
    if isinstance(chall_name, int):
        return chall_name
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    challenges = session.get(
        f"{url}/api/v1/challenges", 
        headers={"Content-Type": "application/json"}
        ).json()
    for chall in challenges["data"]:
        if chall["name"] == chall_name:
            return chall["id"]


def get_flag_id(url, token, flag, chall_id):
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    flags = session.get(
        f"{url}/api/v1/flags", 
        headers={"Content-Type": "application/json"}
        ).json()
    for f in flags["data"]:
        if f["content"].startswith(flag) and f["challenge_id"] == chall_id:
            return f["id"]


def get_hint_ids(url, token, chall_id):
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    hints = session.get(
        f"{url}/api/v1/hints", 
        headers={"Content-Type": "application/json"}
        ).json()
    return [h["id"] for h in hints["data"] if h["challenge_id"] == chall_id]


def get_player_id(url, token, player_name):
    if isinstance(player_name, int):
        return player_name
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    players = session.get(
        f"{url}/api/v1/users", 
        headers={"Content-Type": "application/json"}
        ).json()
    for p in players["data"]:
        if p["name"] == player_name:
            return p["id"]


def parse(foo, bar):
    if foo == "hints":
        return f"{foo},{bar.split()[-1]}"
    return f"{foo},{bar}"


def get_awards(url, token, player_name=None):
    if player_name:
        pid = get_player_id(url, token, player_name)
        if not pid:
            print(f"[GET AWARDS]: Could not find player: {player_name}.")
            return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    awards = session.get(
        f"{url}/api/v1/awards", 
        headers={"Content-Type": "application/json"}
        ).json()
    if player_name:
        return [f"{a['date']},{pid},{parse(a['category'],a['description'])},{a['value']}" 
                for a in awards["data"] if a['user_id'] == pid]
    return [f"{a['date']},{a['user_id']},{parse(a['category'],a['description'])},{a['value']}" 
                for a in awards["data"]]


def get_submissions(url, token, player_name=None):
    if player_name:
        pid = get_player_id(url, token, player_name)
        if not pid:
            print(f"[GET AWARDS]: Could not find player: {player_name}.")
            return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    awards = session.get(
        f"{url}/api/v1/submissions", 
        headers={"Content-Type": "application/json"}
        ).json()
    if player_name:
        return [f"{a['date']},{pid},{a['type']},{a['challenge']['name']},{a['provided']}" 
                for a in awards["data"] if a['user_id'] == pid]
    return [f"{a['date']},{a['user_id']},{a['type']},{a['challenge']['name']},{a['provided']}" 
                for a in awards["data"]]


def post_flag(url, token, flag, challenge):
    cid = get_chall_id(url, token, challenge)
    if not cid:
        print(f"[POST FLAG]: Could not find challenge: {challenge}.")
        return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.post(
        f"{url}/api/v1/flags", 
        json={
            "content": flag,
            "data":"",
            "type":"static",
            "challenge": cid
        },
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[POST FLAG]:")
        pprint(r.json())


def delete_flag(url, token, flag, challenge):
    cid = get_chall_id(url, token, challenge)
    if not cid:
        print(f"[DELETE FLAG]: Could not find challenge: {chall_name}.")
        return
    fid = get_flag_id(url, token, flag, cid)
    if not fid:
        print(f"[DELETE FLAG]: Could not find flag: {flag}.")
        return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.delete(
        f"{url}/api/v1/flags/{fid}",
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[DELETE FLAG]:")
        pprint(r.json())


def patch_flag(url, token, new_flag, challenge, old_flag):
    cid = get_chall_id(url, token, challenge)
    if not cid:
        print(f"[PATCH FLAG]: Could not find challenge: {chall_name}.")
        return
    ofid = get_flag_id(url, token, old_flag, cid)
    if not ofid:
        print(f"[PATCH FLAG]: Could not find flag: {old_flag}.")
        return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.patch(
        f"{url}/api/v1/flags/{ofid}",
        json={
            "content": new_flag,
            "data":"",
            "type":"static",
            "challenge": cid
        },
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[PATCH FLAG]:")
        pprint(r.json())


def post_challenge(url, token, name, category, description, score, prereq=None):
    cid = get_chall_id(url, token, name)
    if cid:
        print(f"[POST CHALLENGE]: Challenge {name} already exists.")
        return
    preq = [get_chall_id(url, token, prereq)] if prereq else []
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.post(
        f"{url}/api/v1/challenges", 
        json={
            "name": name,
            "category": category,
            "description": description,
            "value": score,
            "state":"visible",
            "type":"standard",
            "requirements": {
                "prerequisites": preq
            },
        },
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[POST CHALLENGE]:")
        pprint(r.json())


def post_hint(url, token, challenge, content, cost, prereqs):
    cid = get_chall_id(url, token, challenge)
    if not cid:
        print(f"[POST HINT]: Could not find challenge: {challenge}.")
        return
    hints = get_hint_ids(url, token, cid) if len(prereqs) > 0 else []
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.post(
        f"{url}/api/v1/hints", 
        json={
            "challenge_id": cid,
            "content": content,
            "cost": cost,
            "requirements": {
                "prerequisites": [hints[i] for i in prereqs]
            },
        },
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[POST HINT]:")
        pprint(r.json())


def get_players(url, token):
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    players = session.get(
        f"{url}/api/v1/users", 
        headers={"Content-Type": "application/json"}
    ).json()
    return [p["name"] for p in players["data"]]


def post_player(url, token, name, email, password, registration_code):
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.post(
        f"{url}/api/v1/users", 
        json={
            "name": name,
            "email": email,
            "password": password,
            "registration_code": registration_code
        },
        headers={"Content-Type": "application/json"}
    )
    if DEBUG:
        print("[POST PLAYER]:")
        pprint(r.json())


def post_attempt(url, token, challenge, flag):
    cid = get_chall_id(url, token, challenge)
    if not cid:
        print(f"[POST ATTEMPT]: Could not find challenge: {challenge}.")
        return
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    r = session.post(
        f"{url}/api/v1/challenges/attempt", 
        json={
            "challenge_id": cid,
            "submission": flag
        },
        headers={"Content-Type": "application/json"}
    )
    pprint(r.json()['data']['message'])


def get_scoreboard(url, token):
    session = requests.Session()    
    session.headers.update({
        "Authorization": f"Token {read_file(token)[0]}"
    })    
    scoreboard = session.get(
        f"{url}/api/v1/scoreboard", 
        headers={"Content-Type": "application/json"}
    ).json()
    return [(row['account_id'], row['name'], row['score']) for row in scoreboard['data']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-d', default="https://dvad25.kauotic.se", 
            help="CTFd URL")
    parser.add_argument('--challenge', '-c', default="", 
            help="Challenge name")
    parser.add_argument('--flag', '-f', 
            help="Flag to post")
    parser.add_argument('--old', '-o', default="", 
            help="Old flag to patch")
    parser.add_argument('--token', '-t', 
            help="Admin API access token")
    parser.add_argument('--post', action='store_true')
    parser.add_argument('--delete', action='store_true')
    parser.add_argument('--patch', action='store_true')
    args = parser.parse_args()

    if args.post:
        post_flag(args.url, args.token, args.flag, args.challenge)
    elif args.delete:
        delete_flag(args.url, args.token, args.flag, args.challenge)
    elif args.patch:
        patch_flag(args.url, args.token, args.flag, args.challenge, args.old)
    else:
        exit("[MAIN]: No valid action.")

if __name__== "__main__":
    main()
