from discord.ext import commands
from coinmarketcapapi import CoinMarketCapAPIError
from coinmarketcap_api import get_price
from datetime import datetime
import dotenv, os, random, math, re

# Initialize Discord Client
dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CMD_PREFIX = "!"
client = commands.Bot(command_prefix="!", case_insensitive=True)


# Add timestamps and flush to print statements
def stamped_print(x):
    print(f"{datetime.now().isoformat(' ', 'seconds')}  {x}", flush=True)


@client.event
async def on_ready():
    stamped_print(f"Logged in as {client.user.display_name}")


@client.event
async def on_message(message):
    content = message.content.lower()
    # on_message event interrupts commands
    await client.process_commands(message)


@client.command()  # Get crypto/fiat price conversions
async def price(ctx):
    # numbers/words in message following the command
    cmd = ctx.message.content.lower().replace("!price", "")
    args = re.split("\s+", cmd)
    args.pop(0)  # re.split leaves empty item at front

    # zo smokes mid
    if ctx.author.id == 802693615260270622:
        if random.randint(0, 10) > 5:
            ctx.message.reply("this guy smokes mid😂")
            return

    if len(args) < 1:
        try:
            await ctx.message.reply("?")
        except Exception as err:
            stamped_print(f"ERROR: {err}")
        return
    for arg in args:
        try:
            # First (and only first) number in args is ammount
            amount = float(arg)
            args.remove(arg)
            break
        except:
            # Exception for if theres no number in args
            amount = 1
    if len(args) > 1:
        base = args[0]
        quote = args[1]
    else:
        try:
            float(args[0])
            try:
                await ctx.message.reply("?")
            except Exception as err:
                stamped_print(f"ERROR: {err}")
        except:
            base = args[0]
            quote = "USD"

    # PUNCH EXCTRACTS (CRUCIAL)
    if base in ["punchextracts", "punch_extracts", "punch-extracts"]:
        # Every 5th gram is 1 cent
        discount = math.trunc(amount / 5) * 34.31

        # Pluralizing the "gram(s)" for multiple
        if amount > 1:
            s = "s"
        else:
            s = ""

        if quote.upper() == "USD":
            price = 34.32 * amount - discount
            msg = f"{amount} gram{s} {base} = ${round(price, 2)} with tax"
        else:
            try:
                price = get_price("usd", quote, 34.32 * amount - discount)
            except CoinMarketCapAPIError:
                stamped_print("CoinMarketCapAPIError")
                return
            msg = f"{amount} gram{s} {base} = {round(price, 2)} {quote} with tax"
    elif quote in ["punchextracts", "punch_extracts", "punch-extracts"]:
        try:
            price = get_price(base, "usd", amount) / 34.32
        except CoinMarketCapAPIError:
            stamped_print("CoinMarketCapAPIError")
            return
        msg = f"{amount} {base} = {round(price, 2)} grams {quote}"
    else:
        try:
            price = get_price(base, quote, amount)
        except CoinMarketCapAPIError:
            stamped_print("CoinMarketCapAPIError")
            return
        if quote.upper() == "USD":
            msg = f"{amount} {base} = ${price}"
        else:
            msg = f"{amount} {base} = {price} {quote}"
    try:
        await ctx.channel.send(msg)
    except Exception as err:
        stamped_print(f"ERROR: {err}")


client.run(TOKEN)
