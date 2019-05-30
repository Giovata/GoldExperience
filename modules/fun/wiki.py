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

# modules/fun/wiki.py

import asyncio
import wikipedia


def get_properties():
    return {
        "aliases": ["wikipedia", "wiki", "wp", "w"],
        "description": "Finds a Wikipedia article.",
        "syntax": "`{PREFIX}wiki <article name>` or `{PREFIX}wiki -r` for a random article.",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }


def summary(page_name):
    try:
        return [page_name, wikipedia.page(page_name).summary]
    except wikipedia.exceptions.DisambiguationError as e:
        return [e.options[0], wikipedia.page(e.options[0]).summary]

def random_summary():
    return summary(wikipedia.random(1))

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    cmd = cmd_context.cmd
    if len(msg.content) <= (len(prefix) + len(cmd)):
        await msg.channel.send("Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", prefix))
    else:
        target = msg.content[(len(prefix) + len(cmd) + 1):].replace("<@", "<")
        if target == "special:randompage" or target == "-random" or target == "-r":
            try:
                page = random_summary()
                output_text = f"__**{page[0]}**__\n{page[1]}"
                if len(output_text) >= 1996:
                    output_text = output_text[:1995] + "..."
                await msg.channel.send(output_text)
            except (IndexError, wikipedia.exceptions.PageError) as e:
                await msg.channel.send("An error occurred.")
                cmd_context.ge.log(e)
        else:
            cmd_context.ge.log("[!=] Target = " + target)
            results = wikipedia.search(target)
            output = "Error finding Wikipedia page."
            selected_page = target
            try:
                selected_page = str(results[0])
                try:
                    output = wikipedia.summary(selected_page)
                except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                    output = wikipedia.summary(e.options[0])
                    cmd_context.ge.log(e)
            except (IndexError, wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
                output = "Error finding Wikipedia page."
                cmd_context.ge.log(e)

            output_text = f"__**{selected_page}**__\n{output}"
            if len(output_text) >= 1996:
                output_text = output_text[:1995] + "..."
            await msg.channel.send(output_text)
