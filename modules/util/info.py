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

# modules/util/info.py

import asyncio


def get_properties():
    return {
        "aliases": ["info", "i"],
        "description": "Gives bot info.",
        "syntax": "`{PREFIX}info`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

def get_info(V, P): 
    return f"__**Gold Experience v{V}**__\n\nCreated by *Giovata#0001*\nWritten in Python 3.6 using discord.py API\nFor a list of commands, write `{P}help`.\nIf you have any questions about the bot, or suggestions, contact the creator.\nSource code is available at <https://github.com/giovata/GoldExperience>."

async def run(cmd_context):
    await cmd_context.msg.channel.send(get_info(cmd_context.settings["version"], cmd_context.settings["prefix"]))
