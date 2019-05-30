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

# msghandler.py

import asyncio
import sys
import os
import time
import random
from tools import get_json, set_json, set_setting, add_server, get_emoji, Context


async def invalid_cmd(cmd_context):
    
    prefix = cmd_context.settings["prefix"]
    await cmd_context.msg.channel.send(f"That is not a valid command. For a list of commands, use `{prefix}help`.")
 
async def run_cmd(cmd_context):

    # sets up modules and command variables
    ge = cmd_context.ge
    settings = cmd_context.settings
    if not ge.get_imported():
        ge.log("[Modules not imported, importing now...]")
        ge.import_modules(settings["modules_path"])
        ge.import_commands()
        ge.set_imported(True)
    msg = cmd_context.msg
    msg_text = msg.content[len(settings["prefix"]):]
    cmd = msg_text.split(" ")[0].lower()
    cmd_context.cmd = cmd
    cmd_context.args = msg_text[len(cmd)+1:].split(" ")
    valid_cmd = False


    # sets permissions (default=0, manage_server=10, administrator=20, PotatoBot=90, Potato=100)
    cmd_context.settings["perm_level"] = 0

    for perm in msg.author.guild_permissions:
        if perm[0] == "administrator" and perm[1]:
            cmd_context.settings["perm_level"] = 20
            break
    if cmd_context.settings["perm_level"] == 0:
        for perm in msg.author.guild_permissions:
            if perm[0] == "manage_server" and perm[1]:
                cmd_context.settings["perm_level"] = 10
                break
    if str(msg.author.id) == str(ge.user.id):
        cmd_context.settings["perm_level"] = 90
    elif str(msg.author.id) == "163997823245746177":
        cmd_context.settings["perm_level"] = 100

    # looks for command in modules
    for module in ge.modules:
        if module.enabled:
            for command in module.commands:
                if cmd in command.get_properties()["aliases"]:
                    valid_cmd = True
                    if command.get_properties()["min_perm_level"] > cmd_context.settings["perm_level"]:
                        await msg.channel.send("You don't have valid permissions to run this command.")
                    else:
                        has_all_roles = True
                        for required_role in command.get_properties()["required_roles"]:
                            has_role = False
                            for role in msg.author.roles:
                                if role.name == required_role:
                                    has_role = True
                            if has_role == False:
                                has_all_roles = False
                                break
                        if has_all_roles == False:
                            await msg.channel.send("You don't have valid permissions to runt his command.")
                        else:
                            await command.run(cmd_context)

    # looks for command in server-specific custom commands
    if not valid_cmd:
        for command in settings["custom_commands"]:
            if cmd in command["aliases"]:
                valid_cmd = True
                if command["min_perm_level"] > cmd_context.settings["perm_level"]:
                    await cmd_context.msg.channel.send("You don't have valid permissions to run this command.")
                else:
                    for required_role in command.get_properties()["required_roles"]:
                        has_role = False
                        for role in msg.author.roles:
                            if role.name == required_role:
                                has_role = True
                        if has_role == False:
                            await msg.channel.send("You don't have valid permissions to runt his command.")
                        else:
                            if command["output"] == "":
                                await cmd_context.msg.channel.send("This command does not have an output set.")
                            else:
                                await cmd_context.msg.channel.send(command["output"])

    if not valid_cmd:
        await invalid_cmd(cmd_context)

async def reaction(ge, msg, reactions_path, reaction_rarity):

    if reaction_rarity < 0:
        return
    x = random.randint(0, reaction_rarity)
    if x == 0:
        with open(reactions_path, "r") as f:
            reaction_words = []
            for line in f:
                reaction_words.append(line.replace("\n", ""))
            word = reaction_words[random.randint(0, len(reaction_words)-1)]
            for c in word:
                await ge.add_reaction(msg, get_emoji(c))

async def handle(ge, msg, base_settings):

    author = msg.author
    msg_text = str(msg.content)
    server_id = str(msg.guild.id)
    channel_id = str(msg.channel.id)
    server_name = str(msg.guild.name) 
    channel_name = str(msg.channel.name)
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    log_text = "[" + msg_time + "] " + server_id + ", " + channel_id + " (" + server_name + ", " + channel_name + "), " + str(author) + ": " + msg_text
    settings = base_settings
    template_json = get_json(settings["template_path"])
    for template_setting in template_json["server_template"]["settings"]:
        settings[template_setting] = template_json["server_template"]["settings"][template_setting]

    in_list = True
    servers = get_json(settings["server_path"])
    try:
        server = servers["servers"][server_id]
        for setting in server["settings"]:
            settings[setting] = server["settings"][setting]
    except KeyError:
        in_list = False
 
    if in_list == False:
        ge.log("[Server json not found, creating copy of server json template...]")
        server_list = add_server(servers, template_json["server_template"], server_id, server_name)
        set_json(settings["server_path"], server_list)

    # executed if the message is a command
    if msg_text.startswith(settings["prefix"]):
        ge.log(log_text)
        cmd_context = Context()
        cmd_context.ge = ge
        cmd_context.msg = msg
        cmd_context.settings = settings
        await run_cmd(cmd_context)
    else:
        if settings["log"] == True:
            ge.log(log_text)
        elif str(author.id) in [str(ge.user.id), "163997823245746177"]:
            ge.log(log_text)

        if settings["reaction_rarity"] >= 0:
            await reaction(ge, msg, settings["path"] + "/data/reaction_words.txt", settings["reaction_rarity"])