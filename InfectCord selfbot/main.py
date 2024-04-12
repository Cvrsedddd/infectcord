'''
TO RUN THE SELFBOT IN REPLIT
--------------------------------
- UPLOAD THE PROJECT AS ZIP

- MOVE TO SHELL,and Type

- unzip zipfilename.zip 

(rename zip file name to `infected.zip`, it can be anything because sellapp randomise the name)

- MAKE 4 SECRETS

1 token
2 userid
3 prefix 
4 tokenpass

- Fill these with it values
- Now tap on run
'''
import os
os.system('pip uninstall discord.py -y')
os.system('pip install -r infreq.txt')
os.system('pip uninstall decouple')
os.system('pip install python-decouple')
import discord
import asyncio
from discord.ext import commands
from decouple import config
from colorama import Fore, Style

infectpre = config('prefix')
bot = commands.Bot(command_prefix=infectpre, self_bot=True, help_command=None)

authorized_user = int(config("userid")) 
        
@bot.event
async def on_message(message):
    if message.author != bot.user:
        return

    await bot.process_commands(message)    
  
def infected():
    def predicate(ctx):
        return ctx.author.id == authorized_user
    return commands.check(predicate)
    
@bot.command()
@infected()
async def help(ctx, *, query=None):
    prefix = infectpre
    await ctx.message.delete()

    if not query:
        cogs = bot.cogs.keys()

        helpinfected = f"# **Infect Cord**\n"
        helpinfected += "- " + prefix + "help <modules> to see cmds\n\n"

        for cog in cogs:
            helpinfected += f"_{cog}_, "

        await ctx.send(helpinfected, delete_after=30)
    else:
        query = query.lower()

        found_cog = None

        for cog in bot.cogs:
            if query == cog.lower():
                found_cog = bot.get_cog(cog)
                break

        if not found_cog:
            await ctx.send("Module Not Found", delete_after=5)
            return

        cog_commands = found_cog.get_commands()

        helpinfected = f"**## Infect Cord {found_cog.qualified_name} Cmds**\n\n"

        for command in cog_commands:
            helpinfected += f"_{command.name}_, "

        await ctx.send(helpinfected, delete_after=30)    
        
@bot.command()
@infected()
async def allcmds(ctx):
    command_list = bot.commands
    sorted_commands = sorted(command_list, key=lambda x: x.name)

    response = "# **InfectedCord Cmds**\n\n"
    for command in sorted_commands:
        response += f"_{command.name}_, " 
        
    await ctx.send(response, delete_after=30)


infection = config('token')

@bot.event
async def on_ready():
    infbanner = """
.___        _____              __    _________                  .___         ____ 
|   | _____/ ____\____   _____/  |_  \_   ___ \  ___________  __| _/ ___  __/_   |
|   |/    \   __\/ __ \_/ ___\   __\ /    \  \/ /  _ \_  __ \/ __ |  \  \/  /|   |
|   |   |  \  | \  ___/\  \___|  |   \     \___(  <_> )  | \/ /_/ |   >    < |   |
|___|___|  /__|  \___  >\___  >__|    \______  /\____/|__|  \____ |  /__/\_ \|___|
         \/          \/     \/               \/                  \/        \/             
"""

    print(Fore.RED + infbanner + Style.RESET_ALL)
    print(f"{'='*30}")
    print(f"        Logged in as: {bot.user.name}")
    print(f"        Selfbot ID: {bot.user.id}")
    print(f"{'='*30}\n")
    print("InfectCord is connected")
    print(f"{'-'*30}")
    print(f"   Username: {bot.user.name}")
    print(f"   Guilds: {len(bot.guilds)}")
    print(f"   Members: {sum([guild.member_count for guild in bot.guilds])}")
    print(f"{'-'*30}")
    print("Developer - I N F E C T E D")
    
def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            bot.load_extension(f'cogs.{cog_name}')

load_cogs()  
                                  
bot.run(infection, reconnect=True)