# ------ Imports

import json
import logging
from datetime import datetime

import discord

# Reading config.json

def get_config():
    """
    READ /config.json and return it's content as a dictionary
    """
    with open("config.json", "r") as f:
        data = f.read()
    return json.loads(data)

def get_discord_config():
    """
    Returns discord configs in /config.json as (TOKEN, PREFIX)
    """
    config = get_config()

    try:
        discord_configs = config["discord"]
        return discord_configs["token"], discord_configs["prefix"]
    except:
        # TODO: add option to create config.json
        raise Exception("Couldn't find discord configs in /config.json")

def get_spotify_config():
    """
    Returns cliend id and secret as (ID, SECRET)
    """
    config = get_config()
    try:
        discord_configs = config["spotify"]
        return discord_configs["id"], discord_configs["secret"]
    except:
        # TODO: add option to create config.json
        raise Exception("Couldn't find Spotify configs in /config.json")

def ms_to_minsec(ms: int):
    """
    Convert milliseconds to minutes and seconds in m.ss format
    """

    mssec = round(ms/1000, 0)
    mins = int(mssec/60)
    secs = mssec - mins * 60

    if(secs < 10):
        return f"{mins}.0{secs}"
    return f"{mins}.{secs}"

def minsec_to_ms(minsec: str):
    """
    Convert m.ss format string to milliseconds
    """

    mins = int(minsec.split(".")[0])
    secs = int(minsec.split(".")[1])

    return float((mins * 60 + secs) * 1000)
