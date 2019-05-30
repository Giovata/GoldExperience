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

# modules/fun/ransen.py

import asyncio
from .notcmd.sentencegen import get_sentence


def get_properties():
    return {
        "aliases": ["randomsentence", "ransen", "rs"],
        "description": "Generates a random sentence.",
        "syntax": "`{PREFIX}ransen [amount]`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }
def valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

async def run(cmd_context):
    arg = cmd_context.args[0]
    msg = cmd_context.msg
    max_sentences = cmd_context.settings["max_sentences"]
    dict_path = cmd_context.settings["path"] + "/data/dictionary"
    if valid_int(arg):
        if int(arg) <= max_sentences and int(arg) >= 1:
            sentences = ""
            for i in range(int(arg)):
                if i < int(arg):
                    sentences = sentences + get_sentence(dict_path) + "\n\n"
                else:
                    sentences = sentences + get_sentence(dict_path)
            await msg.channel.send(sentences)
        else:
            sentence = get_sentence(dict_path)
            await msg.channel.send(sentence)
    else:
        sentence = get_sentence(dict_path)
        await msg.channel.send(sentence)
