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

# modules/fun/potatoes.py

import asyncio


def get_properties():
    return {
        "aliases": ["potatoes", "potato", "p"],
        "description": "Generates potatoes.",
        "syntax": "`{PREFIX}potatoes <amount>`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

def validint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    max_potatoes = cmd_context.settings["max_potatoes"]

    if len(msg.content) == (len(prefix) + len("potatoes")) or len(args) != 1:
        await msg.channel.send(f"Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
    else:
        if validint(args[0]) == False:
            await msg.channel.send("Invalid integer.")
        else:
            potatoes = int(args[0])
            if potatoes >= 1 and potatoes <= max_potatoes:
                potatoes_string = ""
                for potato in range(0, potatoes):
                    potatoes_string = potatoes_string + ":potato: "
                await msg.channel.send(potatoes_string)
            elif potatoes > 9000:
                await msg.channel.send("That's too many potatoes to post. You wanna know why it's too many? Because IT'S OVER 9000! Bet you didn't see that reference coming, did you?")
            else:
                max_potatoes_string = str(max_potatoes)
                await msg.channel.send(f"Invalid integer; must be between 1 and {max_potatoes_string}.")