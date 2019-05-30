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

# modules/management/settings.py

import asyncio
from tools import get_json, set_json, get_settings, set_setting


def get_properties():
    return {
        "aliases": ["settings", "options", "s"],
        "description": "Sets a bot-setting for the server. (Requires 'Manage Server' permission)",
        "syntax": "`{PREFIX}settings set <settings> <value>`\n`{PREFIX}settings list`",
        "min_perm_level": 10,
        "required_roles": [],
        "listed": False
    }

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    if len(args) == 3:

        if args[0] == "set":
            key = args[1].lower()
            template_json = get_json(cmd_context.settings["template_path"])
            valid_setting = False
            for setting in template_json["server_template"]["settings"]:
                if key == setting:
                    valid_setting = True
            if not valid_setting:
                await msg.channel.send("Invalid setting.")
                return
            maximum = template_json["server_maximum_settings"][key]
            if maximum == None:
                await msg.channel.send("Invalid setting.")
            else:
                raw_value = args[2]
                server_json = get_json(cmd_context.settings["server_path"])
                server_id = str(cmd_context.msg.guild.id)
                server_settings = get_settings(server_json, server_id)
                t = type(server_settings[key])
                if t == type(""):
                    if len(raw_value) > maximum and maximum != 0:
                        await msg.channel.send("Invalid value.")
                        return
                    server_json = set_setting(server_json, server_id, key, raw_value)
                    set_json(cmd_context.settings["server_path"], server_json)
                    await msg.channel.send("Setting has been changed.")
                elif t == type(1):
                    try:
                        value = int(raw_value)
                        if value > maximum and maximum != 0:
                            await msg.channel.send("Invalid value.")
                            return
                        server_json = set_setting(server_json, server_id, key, value)
                        set_json(cmd_context.settings["server_path"], server_json)
                        await msg.channel.send("Setting has been changed.")
                    except ValueError:
                        await msg.channel.send("Integer expected.")
                elif t == type(1.0):
                    try:
                        value = float(raw_value)
                        if value > maximum and maximum != 0:
                            await msg.channel.send("Invalid value.")
                            return
                        server_json = set_setting(server_json, server_id, key, value)
                        set_json(cmd_context.settings["server_path"], server_json)
                        await msg.channel.send("Setting has been changed.")
                    except ValueError:
                        await msg.channel.send("Floating point expected.")
                elif t == type(True):
                    if str(raw_value).lower() == "true":
                        value = True
                    elif str(raw_value).lower() == "false":
                        value = False
                    else:
                        await msg.channel.send("Boolean expected.")
                        return
                    server_json = set_setting(server_json, server_id, key, value)
                    set_json(cmd_context.settings["server_path"], server_json)
                    await msg.channel.send("Setting has been changed.")
                else:
                    await msg.channel.send("Invalid setting.")

    elif len(args) == 1:
        if args[0] == "list":
            template_json = get_json(cmd_context.settings["template_path"])
            server_json = get_json(cmd_context.settings["server_path"])
            server_id = str(cmd_context.msg.guild.id)
            server_settings = get_settings(server_json, server_id)
            output = "__**Settings:**__\n"
            for setting in server_settings:
                if template_json["server_maximum_settings"][setting] != None:
                    output = output + "\n" + setting + ": " + str(server_settings[setting])
            await msg.channel.send(output)
    else:
        await msg.channel.send("Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", cmd_context.settings["prefix"]))