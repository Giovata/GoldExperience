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

# modules/test/join.py

# This one is temporary-ish as a means of experimenting with voice channels

import asyncio

vcs = []

def get_properties():
    return {
        "aliases": ["join", "connect"],
        "description": "Joins a voice channel.",
        "syntax": "`{PREFIX}join [id]`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": False
    }

async def get_vc(ge, msg, channel_id):
    try:
        vc = msg.guild.get_channel(channel_id)
        return vc
    except BaseException as e:
        ge.log(f"Error getting channel;\n{e}")
        return None

async def connect(ge, channel):
    await vcs.append(channel.connect())


async def run(cmd_context):
    ge = cmd_context.ge
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    if len(msg.content) == (len(prefix) + len("join")):
        found = False
        for channel in msg.guild.channels:
            if msg.author in channel.voice_members:
                found = True
                try:
                    await connect(ge, vc)
                    await ge.msg.channel.send("Should have joined... maybe?")
                except BaseException as e:
                    ge.log(f"Error connecting to channel;\n{e}")
                    await ge.msg.channel.send("Unable to connect to channel.")    
                break
        if found == False:
            await ge.msg.channel.send("You don't appear to be in any channels for me.")
    elif len(args) > 1:
        await ge.msg.channel.send(f"Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
    else:
        channel_id = args[0]
        vc = await get_vc(ge, msg, channel_id)
        if vc == None:
            await ge.msg.channel.send("Unable to get channel from that ID.")
        else:
            try:
                await connect(ge, vc)
                await ge.msg.channel.send("I can't guarantee it but I should have joined the voice channel.")
            except BaseException as e:
                ge.log(f"Error connecting to voice channel;\n{e}")
                await ge.msg.channel.send("Unable to connect to channel.")