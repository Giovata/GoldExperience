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

# modules/util/help.py

import asyncio

def get_properties():
    return {
        "aliases": ["help", "h"],
        "description": "Provides command help.",
        "syntax": "`{PREFIX}help [command]`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }


async def run(cmd_context):
    prefix = cmd_context.settings["prefix"]
    help_text = "Invalid command."
    if len(cmd_context.args[0]) >= 1:
        for module in cmd_context.ge.modules:
            if module.enabled:
                for command in module.commands:
                    if cmd_context.args[0] in command.get_properties()["aliases"]:
                        if cmd_context.settings["perm_level"] >= command.get_properties()["min_perm_level"]:
                            aliases = command.get_properties()["aliases"]
                            alias_text = "Aliases:"
                            for alias in aliases:
                                alias_text = alias_text + " `" + alias + "`,"
                            help_text = "__**" + aliases[0] + "**__\n" + alias_text[:-1] + "\nModule: " + module.name + "\nDescription: " + command.get_properties()["description"] + "\nSyntax: " + command.get_properties()["syntax"].replace("{PREFIX}", prefix)
                            await cmd_context.msg.channel.send(help_text)
                            return
    else:
        help_text = "__**Commands:**__\n"
        for module in cmd_context.ge.modules:
            if module.enabled:
                for command in module.commands:
                    if command.get_properties()["listed"]:
                        command_help = "`" + prefix + command.get_properties()["aliases"][0] + "`: " + command.get_properties()["description"]
                        help_text = help_text + "\n" + command_help
        help_text = f"{help_text}\n*To view individual command syntax, use* `{prefix}help <command>`*.*"
    await cmd_context.msg.channel.send(help_text)