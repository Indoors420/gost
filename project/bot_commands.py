import discord, dotenv, os, random
from discord.ext import commands
import coinmarketcap_api


# Convert x amount base currency to quote currency
def price(**kwargs):
    base = kwargs["base"]
    quote = kwargs["quote"]
    amount = kwargs["amount"]

    price = coinmarketcap_api.get_price(base, quote, amount)

    if quote.upper() == "USD":
        return f"{amount} {base} = ${price}"
    else:
        return f"{amount} {base} = {price} {quote}"


def echo(message):
    return message.content


COMMAND_SYMBOL = "$"

greetings = ["hi", "hello", "hey", "yo", "whats up"]

# List of bot commands with attributes
commands = [
    {
        "price": {"function": price, "kwargs": ["amount", "base", "quote"]},
        "echo": {"function": echo},
    }
]

# Generate a messag greeting the author by name
def greet(message):
    greet = random.choice(greetings)
    return f"{greet} {message.author.mention}"


# Check message for valid commands
# Returns arguments and corresponding function
def check_command(message):
    message = message.content.lower()
    # Remove COMMAND_SYMBOL and lowercase the text and split into arguments
    args = message.split(COMMAND_SYMBOL)[1].split(" ")
    # First word in line refering to command in commands
    command_name = args[0]
    args.pop(0)
    for command in commands:
        if command_name in command:
            # Append keywords to chat arguments for function
            kwargs = {}
            i = 0
            for kwarg in command[command_name]["kwargs"]:
                kwargs[kwarg] = args[i]
                i += 1
            return (command[command_name]["function"], kwargs)


# Returns command function call with arguments
def handle_command(message, command):
    function = command[0]
    kwargs = command[1]
    return function(**kwargs)


# Evaluate the message content and hand response
def check_message(message):
    if message.content.startswith(COMMAND_SYMBOL):
        command = check_command(message)
        return handle_command(message, command)

    for greeting in greetings:
        low = message.content.lower()
        if greeting in low and "gost" in low:
            return greet(message)
