# Gold Experience - Discord bot
# Copyright (C) 2019 Giovata
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

# modules/fun/eightball.py

import random
import asyncio


def get_properties():
    return {
        "aliases": ["8ball", "eightball", "8b"],
        "description": "Answers your questions very accurately.",
        "syntax": "`{PREFIX}8ball <question>`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

def get_responses(path):
    responses = []
    with open(path + "/data/eightball.txt") as f:
        for line in f:
            responses.append(line)
    return responses

async def run(cmd_context):
    msg = cmd_context.msg
    cmd = cmd_context.cmd
    prefix = cmd_context.settings["prefix"]
    if len(msg.content) <= (len(prefix) + len(cmd)):
        await msg.channel.send("Invalid question.")
    else:
        responses = get_responses(cmd_context.settings["path"])
        response = responses[random.randint(0, len(responses)-1)]
        response = response.replace("%q", msg.content[(len(prefix) + len(cmd) + 1):])
        response = response.replace("%n", str(msg.author.display_name))
        response = response.replace("@", "at")
        await msg.channel.send(response)