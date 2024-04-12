import discord
from discord.ext import commands
import aiohttp
import io
import requests
import json
from decouple import config
from colorama import Fore
from main import infected, infectpre

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(name="stealav", usage="<@member>", description="Steal the avatar")
    @infected()
    async def stealav(self, ctx, user: discord.Member):

        url = user.avatar_url
        prefix = infectpre
        password = config("tokenpass", default="")
        if password == "":
            await ctx.send(f"You didnt configure your password yet, use {prefix}password <password>")
        else:
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=password, avatar=f.read())
            await ctx.send(f"Stole {user}'s avatar")
        except discord.HTTPException as e:
            await ctx.send(str(e))

    @commands.command(name="setavatar",aliases=["setav"], usage="<url>",  description="Set your avatar")
    @infected()
    async def setavatar(self, ctx, url: str):
        prefix = infectpre
        password = config("tokenpass", default="")
        if password == "":
            await ctx.send(f"You didn't configure your password yet, use {prefix}password <password>")
        else:
            password
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=password, avatar=f.read())
            await ctx.send("Changed avatar")
        except discord.HTTPException as e:
            await ctx.send(str(e))

    @commands.command(name="invisav", usage="", description="Invisible avatar")
    @infected()
    async def invisav(self, ctx):
        prefix = infectpre
        url = "https://i.ibb.co/Wgn91T7/Infected-Invisible.png"
        password = config("tokenpass", default="")
        if password == "":
            await ctx.send(f"You didnt configure your password yet, use {prefix}setpass <password>")
        else:
            password
            with open('PFP-1.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
        try:
            with open('PFP-1.png', 'rb') as f:
                await self.bot.user.edit(password=password, avatar=f.read())
            await ctx.send("Changed to an invisible avatar")
        except discord.HTTPException as e:
            await ctx.send(str(e))
            
    @commands.command(name="setpass",usage="<password>", description="Set selfbot password")
    @infected()
    async def setpassword(self, ctx, password: str):
        with open(".env", "w") as f:
            f.write(f"tokenpass={password}")
        await ctx.send("Password set successfully")            

def setup(bot):
    bot.add_cog(Image(bot))
