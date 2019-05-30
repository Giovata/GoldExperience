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

# bot.py

if __name__ == "__main__":
    print("Initialising...")

import multiprocessing
import asyncio
import os
import discord
import msghandler
import importlib
from datetime import datetime
from tools import get_json, Module


def client_thread(pipe, queue):

    class Gold(discord.Client):

        # outputs a message to a log (by default, printing to the console)
        def log(self, text):
            print(text)

        # sets a marker whether modules have been imported
        def set_imported(self, value):
            self.has_imported_modules = value

        # gets whether modules have been imported
        def get_imported(self):
            return self.has_imported_modules

        # imports modules in the 'modules' directory and adds them to self.modules
        def import_modules(self, path):
            self.modules = []
            for module in os.listdir(path):
                module_path = path + "/" + module
                if os.path.isdir(module_path):
                    if len(os.listdir(module_path)) >= 1:
                        self.modules.append(Module(module_path, module))
        
        # imports commands for all modules in self.modules which are marked with an enabled attributed
        def import_commands(self):
            for module in self.modules:
                if module.enabled:
                    module.commands = []
                    module.import_commands()

        # returns the overall amount of command files for all enabled modules
        def count_commands(self):
            count = 0
            for module in self.modules:
                if module.enabled:
                    count += module.count_commands()
            return count

        # experimental

        # adds a new VoiceClient object to a list when it is created
        #def init_vc(self, value):
        #    self.vcs = value

        # adds a new VoiceClient object to a list when it is created
        #def add_vc(self, vc):
        #    self.vcs.append(vc)

        # removes a VoiceClient (when disconnecting)
        #def rem_vc(self, index):
        #    self.vcs.remove(index)


    # constant values
    VERSION = "1.0"
    PATH = os.path.dirname(os.path.abspath(__file__))
    KEYS_PATH = PATH + "/keys.json"
    MODULES_PATH = PATH + "/modules"
    SERVER_PATH = PATH + "/data/servers.json"
    TEMPLATE_PATH = PATH + "/data/template.json"
    DEFAULT_PERM_LEVEL = 0
   
    BASE_SETTINGS = {
    	"version": VERSION,
        "path": PATH,
        "server_path": SERVER_PATH,
        "template_path": TEMPLATE_PATH,
        "modules_path": MODULES_PATH,
        "default_perm_level": DEFAULT_PERM_LEVEL,
        "perm_level": DEFAULT_PERM_LEVEL,
        "keys_path": KEYS_PATH
    }

    ge = Gold()
    
    @ge.event
    async def on_ready():
        ge.set_imported(False)
        ge.import_modules(MODULES_PATH)
        CMD_COUNT = ge.count_commands()
        init_text = f"\nSuccessfully connected. Running:\nGold Experience v{VERSION}\nas user {ge.user.name} ({ge.user.id})\nin directory {PATH}\nwith {CMD_COUNT} commands present.\n-----\n"
        ge.log(init_text)
        
    @ge.event
    async def on_message(msg):
        await msghandler.handle(ge, msg, BASE_SETTINGS)

    TOKEN = get_json(KEYS_PATH)["bot_token"]

    try:
        ge.loop.run_until_complete(ge.start(TOKEN))
    except KeyboardInterrupt:
        ge.loop.run_until_complete(ge.logout())
    finally:
        ge.loop.close()

def start_bot():
    queue = multiprocessing.Queue()
    parent_pipe, child_pipe = multiprocessing.Pipe()
    thread = multiprocessing.Process(target=client_thread, args=(child_pipe, queue,))
    try:
        thread.start()
    except KeyboardInterrupt:
        os.kill(thread.pid, signal.SIGINT)


if __name__ == "__main__":
    print("Finished initialisation. Connecting...")
    start_bot()