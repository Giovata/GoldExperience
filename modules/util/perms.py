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

# modules/util/perms.py

import asyncio


def get_properties():
    return {
        "aliases": ["permissions", "perms"],
        "description": "Debug command - list your perms.",
        "syntax": "`{PREFIX}perms`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": False
    }

async def run(cmd_context):
    output_text = "__*Permissions*__:"
    for perm in cmd_context.msg.author.guild_permissions:
        output_text += f"\n{str(perm)}"
    await cmd_context.msg.channel.send(output_text)