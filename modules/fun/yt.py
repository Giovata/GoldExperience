# modules/fun/yt.py

import asyncio
import urllib
from bs4 import BeautifulSoup


def get_properties():
    return {
        "aliases": ["youtube", "yt"],
        "description": "Finds a YT video and sends a link to it. Note: This command is slow to execute.",
        "syntax": "`{PREFIX}yt <search target>`.",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }


def search(target):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(target)
    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response.read())
    results = soup.findAll(attrs={"class":"yt-uix-tile-link"})
    return ("https://www.youtube.com" + results[0]["href"])


async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    cmd = cmd_context.cmd
    if len(msg.content) <= (len(prefix) + len(cmd)):
        await msg.channel.send("Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
    else:
        target = msg.content[(len(prefix) + len(cmd) + 1):].replace("<@", "<")
        await msg.channel.send(search(target))
