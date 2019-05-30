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

# modules/base/avatar.py

import asyncio

def get_properties():
    return {
        "aliases": ["avatar", "getavatar", "av"],
        "description": "Returns the URL for your avatar.",
        "syntax": "`{PREFIX}avatar`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

async def run(cmd_context):
    await cmd_context.msg.channel.send(str(cmd_context.msg.author.avatar_url))