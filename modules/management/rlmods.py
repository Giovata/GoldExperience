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

# modules/management/rlmods.py

import asyncio


def get_properties():
    return {
        "aliases": ["rlmods", "reloadmodules", "reloadmods"],
        "description": "Reloads the modules. [Not functional]",
        "syntax": "`{PREFIX}rlmods`",
        "min_perm_level": 110,
        "required_roles": [],
        "listed": False
    }

async def run(cmd_context):
    await cmd_context.msg.channel.send("Reloading...")
    cmd_context.ge.log("[Modules not imported, importing now...]")
    cmd_context.ge.import_modules(cmd_context.settings["modules_path"])
    cmd_context.ge.import_commands()
    