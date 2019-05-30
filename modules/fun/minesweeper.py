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

# modules/fun/minesweeper.py

import random
from .notcmd.minesweeper import generate
import asyncio

def get_properties():
    return {
        "aliases": ["minesweeper", "ms"],
        "description": "Generates a Minesweeper board using Discord spoilers.",
        "syntax": "`{PREFIX}minesweeper <rows> <columns> <bombs>` for a regular board, or `{PREFIX}minesweeper <rows> <columns> <bombs> dm` for it to be sent to you in a DM, if it's able to.\n Numbers must be integers.",
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

async def error(msg, error_message):
    await msg.channel.send(error_message)

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    if len(args) == 3 or len(args) == 4:
        if valid_int(args[0]) and valid_int(args[1]) and valid_int(args[2]):
            rows = int(args[0])
            columns = int(args[1])
            bombs = int(args[2])
            if rows < 1 or columns < 1 or rows > 15 or columns > 15:
                await error(msg, "Width and height of board must be between 1 and 15, though large sizes might not be able to generate.")
            elif bombs < 1 or bombs > (rows*columns)-1:
                await error(msg, "Bombs must cover between 1 square and the full board.")
            elif len(args) == 4:
                if args[3] != "dm":
                    await error(msg, "Invalid syntax.")
                else:
                    board = generate(rows, columns, bombs)
                    await msg.author.send(board)
            else:
                board = generate(rows, columns, bombs)
                await msg.channel.send(board)
        else:
            await error(msg, "Invalid integer.")
    else:
        syntax = get_properties()["syntax"].replace("{PREFIX}", prefix)
        await msg.channel.send(f"Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
