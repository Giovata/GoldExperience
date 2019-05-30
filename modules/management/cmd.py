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

# modules/management/cmd.py

# Still not finished creating this


import asyncio
from tools import get_json, set_json


def get_properties():
    return {
        "aliases": ["command", "cmd"],  
        "description": "[INCOMPLETE] Manage server-specific custom commands.",
        "syntax": "`{PREFIX}cmd add|remove <name>`\n`{PREFIX}cmd options <option> <value>`\n`{PREFIX}cmd list`",
        "min_perm_level": 90,
        "required_roles": [],
        "listed": False
    }


# !cmdname
#  Invalid command.
# !cmd add cmdname
#  Added command.
# !cmdname
#  This command does not have an output set.
# !cmd options cmdname output a b c
#  Set option for command.
# !cmdname
#  a b c
# !cmd options cmdname addalias a
#  Set option for command.
# !a
#  a b c
# !cmd options cmdname removealias a
#  Set option for command.
# !a
#  Invalid command.
# !cmd options cmdname addalias helo
#  Alias is already used.
# !cmd options cmdname addalias b
#  Set option for command.
# !cmd remove b
#  Removed command.
# !cmdname
#  Invalid command.

#cmd add <command>
#cmd remove <command>
#cmd clone <command> <newcommand>
#cmd options <command> output <output>
#cmd options <command> addalias <alias>
#cmd options <command> removealias <alias>
#cmd options <command> description <description>
#cmd options <command> minpermlevel <alias>
#cmd options <command> listed <description>
#cmd list
#cmd info <command>
#return the formatted info text for a custom command
def command_info(custom_commands, alias):
    for command in custom_commands:
        if alias in command.aliases:
            output = ""
            output = "__**" + alias + "**__\nAliases:"
            for a in command.aliases:
                output = output + " `" + a + "`"
            output = output + "\nDescription: `" + command.description + "`"
            return output
    return "Invalid command."

#return the formatted command list text for all ustom commands in the server 
def list_commands(custom_commands):
    output = "__**Commands**__"
    for command in custom_commands: 
        if command.listed:
            output = output + "\n`" + command.aliases[0] + "` - " + command.description
    return output

#check if an alias is existing in custom_commands
def existing_alias(custom_commands, alias):
    for command in custom_commands:
        if cmd in command["aliases"]:
            return True
    return False

#get default/template command json with name added
def default_command(template_path, cmd_name):
    cmd = get_json(template_path)["custom_command_template"]
    cmd["aliases"].append(cmd_name)
    return cmd

#used to add a blank command to custom_commands
def add_command(server_json, server_id, default_command):
    server_json["servers"][server_id]["settings"]["custom_commands"][command] = default_command
    return server_json

#used to clone a command
def clone_command(server_json, server_id, previous_command, new_command):
    previous_command["name"] = new_command
    return add_command(server_json, server_id, previous_command)

#used to remove a command from custom-commands
def remove_command(server_json, server_id, command):
    output_commands = {}
    for custom_command in server_json["servers"][server_id]["settings"]["custom_commands"]:
        if command not in custom_command["aliases"]:
            output_commands[custom_command["aliases"][0]] = custom_comamnd
        server_json["servers"][server_id]["settings"]["custom_commands"] = output_commands
    return server_json
 
#used to edit a property for a command
def set_property(server_json, server_id, command, property, value):
    server_json["servers"][server_id]["settings"]["custom_commands"][command][property] = value
    return server_json

#add an alias to a command
def add_alias(server_json, server_id, command, alias):
    server_json["servers"][server_id]["settings"]["custom_commands"][command]["aliases"].append(alias)
    return server_json

#remove an alias from a command
def remove_alias(server_json, server_id, command, target_alias):
    for alias in server_json["servers"][server_id]["settings"]["custom_commands"][command]["aliases"]:
        if alias == target_alias:
            del alias
            return server_json

#add a role to a command
def add_role(server_json, server_id, command, role):
    server_json["servers"][server_id]["settings"]["custom_commands"][command]["required_roles"].append(role)
    return server_json

#remove an role from a command
def remove_role(server_json, server_id, command, target_role):
    for role in server_json["servers"][server_id]["settings"]["custom_commands"][command]["required_roles"]: 
        if role == target_role:
            del role
            return server_json

#called to output an error in the channel
async def error(msg, error_message):
    await msg.channel.send(error_message)

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    custom_commands = cmd_context.settings["custom_commands"]
    if len(args) == 1:
        if args[0] == "list":
            await msg.channel.send(list_commands(custom_commands))
        else:
            await error(msg, "Invalid syntax.")
    elif len(args) == 2:
        if args[0] == "info":
            await msg.channel.send(command_info(custom_commands, args[1].lower()))
        elif args[0] == "add":
            if existing_alias(custom_commands, args[1]):
                await error(msg, "Invalid command.")
            else:
                server_json = get_json(cmd_context.settings["server_path"])
                server_json = add_command(server_json, cmd_context.settings["id"], default_command(cmd_context.settings["template_path"], args[1].lower()))
                set_json(cmd_context.settings["server_path"], server_json)
                await msg.channel.send("Added new command. Remember: `{}cmd options {} output <output text>`".format(cmd_context.settings["prefix"], args[1].lower()))
        elif args[0] == "remove":
            if existing_alias(custom_commands, args[1]):
                server_json = get_json(cmd_context.settings["server_path"])
                for server in server_json:
                    if server["id"] == cmd_context.settings["id"]:
                        server_json = remove_command(server["settings"]["custom_commands"], default_command(cmd_context.settings["template_path"], args[1].lower()))
                        set_json(cmd_context.settings["server_path"], server_json)
                        await msg.channel.send("Removed command.")
                        return
            else:
                await error(msg, "Invalid command.")
        else:
            await error(msg, "Invalid syntax.")
    elif len(args) == 3:
        if args[0] == "clone":
            if existing_alias(custom_commands, args[1]) == False:
                await error(msg, "Invalid command.")
            elif existing_alias(custom_commands, args[2]):
                await error(msg, "Invalid command.")
            else:
                server_json = get_json(cmd_context.settings["server_path"])
                server_id = cmd_context.settings["id"]
                for custom_command in server_json["servers"][server_id]["settings"]["custom_commands"]:
                    if args[1] in custom_command["aliases"]:
                        previous_command = custom_command
                        new_command = args[2]
                        set_json(cmd_context.settings["server_path"], clone_command(server_json, server_id, previous_command, new_command)) 
                        await msg.channel.send("Cloned command.")
                        return
        elif args[0] == "options":
            command = args[1]
            option = args[2]
            if existing_alias(custom_commands, command):
                valid_options = ["output", "description", "minpermlevel", "listed"]
                valid_operations = ["addalias", "removealias", "addrole", "removerole"]
                if option in valid_options or option in valid_operations:

                    server_json = get_json(cmd_context.settings["server_path"])
                    server_id = cmd_context.settings["id"]
                    if command in valid_options:
                        server_json = set_property(server_json, server_id, command, option, args[3])
                    elif command in valid_operations:
                        if command == "addalias":
                            server_json = add_alias(server_json, server_id, command, args[3])
                        elif command == "removealias":
                            server_json = remove_alias(server_json, server_id, command, args[3])
                        if command == "addrole":
                            server_json = add_role(server_json, server_id, command, args[3])
                        elif command == "removealias":
                            server_json = remove_role(server_json, server_id, command, args[3])
                        else:
                            await error(msg, "Invalid option.")
                            return    
                    else:
                        await error(msg, "Invalid command.")
                        return
                    set_json(cmd_context.settings["server_path"], clone_command(server_json, server_id, previous_command, new_command)) 
                else:
                    await error(msg, "Invalid option.")
            else:
                await error(msg, "Invalid command.")
        else:
            await error(msg, "Invalid syntax.")
    else:
        await error(msg, "Invalid syntax.")
    await msg.channel.send("TODO.")