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

# modules/base/rannum.py

import random
import asyncio


def get_properties():
    return {
        "aliases": ["randomnumber", "rannum", "rn"],
        "description": "Generates a random number in a given range.",
        "syntax": "`{PREFIX}rannum <number>` for a random number between 0 and the given number, or\n`{PREFIX}rannum <number> <number>` for a random number between the two given numbers.\nNumbers must be integers.",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

def valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    if len(args) == 1 and len(msg.content) >= (len(prefix) + len(cmd_context.cmd)):
        if valid_int(args[0]):
            if int(args[0]) > 0:
                await msg.channel.send(str(random.randint(0, int(args[0]))))
            else:
                await msg.channel.send(str(random.randint(int(args[0]), 0)))
        else:
            await msg.channel.send("Invalid integer.")
    elif len(args) == 2:
        if valid_int(args[0]) and valid_int(args[1]):
            if int(args[0]) > int(args[1]):
                await msg.channel.send(str(random.randint(int(args[1]), int(args[0]))))
            else:
                await msg.channel.send(str(random.randint(int(args[0]), int(args[1]))))
        else:
            await msg.channel.send("Invalid integer.")
    else:
        syntax = get_properties()["syntax"].replace("{PREFIX}", prefix)
        await msg.channel.send(f"Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
