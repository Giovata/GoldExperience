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

# modules/base/calc.py

import math
import asyncio


def get_properties():
    return {
        "aliases": ["calculate", "calc", "c", "what's"],
        "description": "Does a basic calculation using 1 to 2 numbers.",
        "syntax": "`{PREFIX}calc <number1> <operator> [number2]`",
        "min_perm_level": 0,
        "required_roles": [],
        "listed": True
    }

def valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_number(value):
    if valid_float(value):
        return value
    value = value.lower()
    if value == "pi" or value == "π":
        return str(math.pi)
    elif value == "tau" or value == "τ":
        return str(math.tau)
    elif value == "e":
        return str(math.e)
    elif value == "phi" or value == "φ" or value == "gr" or value == "goldenratio":
        return "1.618033988749895"
    elif value == "γ" or value == "e-m":
        return "0.577215664901532"
    else:
        return "invalid"

def get_operator(value):
    value = value.lower()
    if value == "add" or value == "plus" or value =="+" or value == "and":
        return "+"
    elif value == "minus" or value == "subtract" or value =="-" or value == "−" or value == "takeaway":
        return "-"
    elif value == "times" or value == "multiply" or value =="multiplied-by" or value == "*" or value == "x" or value == "×" or value == "⋅":
        return "*"
    elif value == "divided-by" or value == "divide" or value == "÷" or value == "/":
        return "/"
    elif value == "pow" or value == "**" or value == "^":
        return "^"
    elif value == "mod" or value == "%":
        return "%"
    else:
        return "invalid"

async def run(cmd_context):
    msg = cmd_context.msg
    args = cmd_context.args
    prefix = cmd_context.settings["prefix"]
    syntax = get_properties()["syntax"].replace("{PREFIX}", prefix)
    ops = "Operators are `+` `-` `*` `/` `^` `%` and `!`"
    output = "Error."
    
    if len(args) == 2:
        if args[1] == "!" or args[1].lower() == "factorial":
            if valid_int(args[0]):
                if int(args[0]) < 0:
                    output = "Undefined"
                elif int(args[0]) > 500:
                    output = "Can't calculate factorials for numbers above 500."
                else:
                    output = math.factorial(int(args[0]))
            else:
                output = "Non-integer factorials are not supported."
        else:
            output = f"Invalid syntax.\n{syntax}"

    elif len(args) == 3:
        if get_number(args[0]) == "invalid":
            await msg.channel.send("The first argument is not a valid number.")
            return
        n1 = float(get_number(args[0]))

        if get_operator(args[1]) == "invalid":
            await msg.channel.send(f"The second argument is not a valid operator.\n{ops}")
            return
        op = get_operator(args[1])

        if get_number(args[2]) == "invalid":
            await msg.channel.send("The third argument is not a valid number.")
            return
        n2 = float(get_number(args[2]))

        if op == "+":
            if args[1].lower() == "plus" or args[1] == "+":
                if n1 == 9 and n2 == 10:
                    output = "21"
                else:
                    output = str(n1 + n2)
            else:
                output = str(n1 + n2)
        elif op == "-":
            output = str(n1 - n2)
        elif op == "*":
            output = str(n1 * n2)
        elif op == "/":
            if n2 == 0:
                output = "Undefined"
            else:
                output = str(n1 / n2)
        elif op == "^":
            if n1 == 0 and n2 == 0:
                output = "Undefined"
            elif "j" in str(n1 ** n2) or "i" in str(n1 ** n2):
                output = "Complex numbers are not supported."
            else:
                output = str(n1 ** n2)
        elif op == "%":
            if valid_int(n1) == False or valid_int(n2) == False:
                output = "Modular operations are only supported for integers."
            elif n2 == 0:
                output = "Undefined"
            else:
                output = str(n1 % n2)

        if output == "-0.0" or output == "-0":
            output = "0"
        elif output.endswith(".0"):
            output = output[:-2]
    else:
        output = f"Invalid syntax.\n{syntax}"

    await msg.channel.send(output)