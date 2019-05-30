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

# tools.py

import json
import re
import os
import importlib


emojis = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🥔🅾"
letters = "abcdefghijklmnopqrstuvwxyzPO"

# used for command context passed from the msghandler to individual command files when executed, containing a reference to the client, msg, settings, etc
class Context:
    pass

# used for handling modules composed of command files in a directory
class Module:

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.enabled = True
        self.commands = []
        self.info = ""

    # imports command files from the module's directory and add them to self.commands
    def import_commands(self):
        for file in os.listdir(self.path):
            if file.endswith(".py"):
                file_path = "modules." + self.name + "." + file[:-3]
                self.commands.append(importlib.import_module(file_path))

    # returns the amount of command files in the module's directory
    def count_commands(self):
        count = 0
        for file in os.listdir(self.path):
            if file.endswith(".py"):
                count += 1
        return count
        
# returns a json object from a json file
def get_json(file_path):
    with open(file_path, "r") as file:
        return json.loads(file.read())

# write a json object to a json file
def set_json(file_path, json_obj):
    with open(file_path, "w") as file:
        file.write(json.dumps(json_obj))
def get_settings(server_json, server_id):
    return server_json["servers"][server_id]["settings"]

# returns a servers object with a setting for a server set
def set_setting(server_json, server_id, key, value):
    server_json["servers"][server_id]["settings"][key] = value
    return server_json

# returns a servers object with the full settings for a server set
def set_settings(server_json, server_id, settings):
    server_json["servers"][server_id]["settings"] = settings
    return server_json

# returns a servers object with a server added
def add_server(server_json, server_template, new_id, new_name):
    server_json["servers"][new_id] = server_template
    server_json["servers"][new_id]["id"] = new_id
    server_json["servers"][new_id]["name"] = new_name
    return server_json

def get_emoji(char):
    return str(emojis[letters.index(char)])