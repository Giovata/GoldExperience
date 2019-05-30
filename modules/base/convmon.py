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

# modules/base/convmon.py

import asyncio
import json
import requests
import decimal
from tools import get_json


def get_properties():
    return {
        "aliases": ["convertmoney", "convertcurrency", "convmon", "convert", "cm"],
        "description": "Converts between currencies.",
        "syntax": "`{PREFIX}cm <amount> <from> <to>` - ISO Currency codes only.",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

async def run(cmd_context):
    #This uses "fixer" key in keys.json to access exchange rate API. Contact Giovata if you want to know how to get one.
    base = "http://data.fixer.io/api/latest?access_key=" + get_json(cmd_context.settings["keys_path"])["fixer"]
    msg = cmd_context.msg
    args = cmd_context.args
    if len(args) != 3:
        await msg.channel.send("Invalid syntax.\n" + get_properties()["syntax"].replace("{PREFIX}", cmd_context.settings["prefix"]))
    else:
        try:
            amount = float(args[0])
        except:
            await msg.channel.send("Invalid amount.")
            return
        cur_from = args[1].upper()
        cur_to = args[2].upper()
        amount_string = args[0]
        url = f"{base}&from={cur_from}&to={cur_to}&amount={amount_string}"
        try:
            response = requests.get(url)
        except:
            await msg.channel.send("An error occurred.")
            return
        data = response.json()
        rates = data["rates"]
        try:
            in_euro = amount / rates[cur_from]
            converted = in_euro * rates[cur_to]
        except:
            await msg.channel.send("Invalid currency code.")
            return
        conv_decimal = decimal.Decimal(converted)
        conv_rounded = round(conv_decimal, 2)
        conv_string = str(conv_rounded)
        await msg.channel.send(f"{amount_string} {cur_from} = {conv_string} {cur_to}")