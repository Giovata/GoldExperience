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

# modules/management/echof.py

import asyncio


def get_properties():
    return {
        "aliases": ["echof", "echofor", "ef"],
        "description": "Echos the input for a given amount of times. Use \"{current-number}\" for the current number between 1 and <times>.",
        "syntax": "`{PREFIX}echof <times> <message>`",
        "min_perm_level": 90,
        "required_roles": [],
        "listed": False
    }

async def run(cmd_context):
    to_echo = cmd_context.msg.content[len(cmd_context.cmd)+len(cmd_context.args[0])+2:]
    times = int(cmd_context.args[0])
    for t in range(1, times+1):
        output = to_echo.replace("{current-number}", str(t))
        await cmd_context.msg.channel.send(output)