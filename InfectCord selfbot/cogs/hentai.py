import discord
from discord.ext import commands
from main import infected
import requests

class Hentai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="hrandom",
        usage="",
        description="Random hentai"
    )
    @infected()
    async def hrandom(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/hentai")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="hass",
        usage="",
        description="Random hentai ass"
    )
    @infected()
    async def hass(self, ctx):
        try:
            r = requests.get("https://nekobot.xyz/api/image?type=hass")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['message'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="ass",
        usage="",
        description="Random ass"
    )
    @infected()
    async def ass(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/ass")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="boobs",
        usage="",
        description="Real breasts"
    )
    @infected()
    async def boobs(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/boobs")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="pussy",
        usage="",
        description="Random pussy"
    )
    @infected()
    async def pussy(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/pussy")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="4k",
        usage="",
        description="4k NSFW"
    )
    @infected()
    async def fk(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/4k")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="cumm",
        usage="",
        description="Baby gravy!"
    )
    @infected()
    async def cumm(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/cum")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="hblowjob",
        usage="",
        description="Self explainable"
    )
    @infected()
    async def blowjob(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/blowjob")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="ahegao",
        usage="",
        description="Ahegao"
    )
    @infected()
    async def ahegao(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/gasm")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="lewd",
        usage="",
        description="Lewd loli"
    )
    @infected()
    async def lewd(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/lewd")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="feet",
        usage="",
        description="Random feet"
    )
    @infected()
    async def feet(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/feet")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(
        name="lesbian",
        usage="",
        description="Girls rule!"
    )
    @infected()
    async def lesbian(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/lesbian")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(name="spank",usage="", description="NSFW for butts")
    @infected()
    async def spank(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/spank")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

    @commands.command(name="hwallpaper", usage="", description="99% SFW")
    @infected()
    async def hwallpaper(self, ctx):
        try:
            r = requests.get("http://api.nekos.fun:8080/api/wallpaper")
            r.raise_for_status()
            data = r.json()
            await ctx.send(data['image'])
        except requests.RequestException:
            await ctx.send("An error occurred while fetching the image.")

def setup(bot):
    bot.add_cog(Hentai(bot))