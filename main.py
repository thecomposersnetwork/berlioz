import discord
import datetime
from discord.ext import commands
import random
import logging
from scaler.scaler import (Key, Modes)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

# Setting up logger
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='berlioz.log', encoding='utf-8',
        mode='w')
log.addHandler(handler)

extensions = [
]

def wrapCode(text: str):
    return '```' + text + '```'

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

@bot.command()
async def scale(key: int, mode: str):
    m = ''
    if mode == 'M':
        m = Modes.Major
    elif mode == 'nm':
        m = Modes.NaturalMinor
    elif mode == 'hm':
        m = Modes.HarmonicMinor
    elif mode == 'mm':
        m = Modes.MelodicMinor

    k = Key(key, m)

    await bot.say(wrapCode(k.ppChordScale()))

@bot.command(pass_context=True)
async def collab(ctx, url):
    print('=====')
    print(ctx.message.channel)
    await bot.say(ctx.message.channel.id)


if __name__ == '__main__':
    with open('token', 'r') as f:
        for extension in extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension,
                            type(e).__name__, e))
        token = f.readline().strip()
        bot.run(token)
