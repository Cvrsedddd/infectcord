import discord
from discord.ext import commands
import requests
import os
from main import infected

class Dump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="alldump", usage="<channel>", description="Dump all from a channel")
    @infected()
    async def alldump(self, ctx, channel: discord.TextChannel):
        if not os.path.exists(f"data/dumping/all/{channel.guild.name}/{channel.name}"):
            os.makedirs(f"data/dumping/all/{channel.guild.name}/{channel.name}")

        try:
            async for message in channel.history(limit=None):
                for attachment in message.attachments:
                    r = requests.get(attachment.url, stream=True)
                    with open(f'data/dumping/all/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb') as f:
                        f.write(r.content)
            await ctx.send("Dumped all content.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="imgdump", usage="<channel>", description="Dump images from a channel")
    @infected()
    async def imgdump(self, ctx, channel: discord.TextChannel):
        if not os.path.exists(f"data/dumping/images/{channel.guild.name}/{channel.name}"):
            os.makedirs(f"data/dumping/images/{channel.guild.name}/{channel.name}")

        try:
            async for message in channel.history(limit=None):
                for attachment in message.attachments:
                    if attachment.url.endswith((".png", ".jpg", ".jpeg", ".gif")):
                        r = requests.get(attachment.url, stream=True)
                        with open(f'data/dumping/images/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb') as f:
                            f.write(r.content)
            await ctx.send("Dumped images.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="audiodump", usage="<channel>", description="Dump audio from a channel")
    @infected()
    async def audiodump(self, ctx, channel: discord.TextChannel):
        if not os.path.exists(f"data/dumping/audio/{channel.guild.name}/{channel.name}"):
            os.makedirs(f"data/dumping/audio/{channel.guild.name}/{channel.name}")

        try:
            async for message in channel.history(limit=None):
                for attachment in message.attachments:
                    if attachment.url.endswith(".mp3"):
                        r = requests.get(attachment.url, stream=True)
                        with open(f'data/dumping/audio/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb') as f:
                            f.write(r.content)
            await ctx.send("Dumped audio.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="videodump", usage="<channel>", description="Dump videos from a channel")
    @infected()
    async def videodump(self, ctx, channel: discord.TextChannel):
        if not os.path.exists(f"data/dumping/videos/{channel.guild.name}/{channel.name}"):
            os.makedirs(f"data/dumping/videos/{channel.guild.name}/{channel.name}")

        try:
            async for message in channel.history(limit=None):
                for attachment in message.attachments:
                    if attachment.url.endswith((".mp4", ".mov")):
                        r = requests.get(attachment.url, stream=True)
                        with open(f'data/dumping/videos/{channel.guild.name}/{channel.name}/{attachment.filename}', 'wb') as f:
                            f.write(r.content)
            await ctx.send("Dumped videos.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="textdump", usage="<channel>", description="Dump text from a channel")
    @infected()
    async def textdump(self, ctx, channel: discord.TextChannel):
        if not os.path.exists(f"data/dumping/text/{channel.guild.name}/{channel.name}"):
            os.makedirs(f"data/dumping/text/{channel.guild.name}/{channel.name}")

        try:
            async for message in channel.history(limit=1000):
                text = f"{message.author.name}#{message.author.discriminator}: {message.content}\n"
                with open(f'data/dumping/text/{channel.guild.name}/{channel.name}/{channel.name}.txt', 'a', encoding='utf-8') as f:
                    f.write(text)
            await ctx.send("Dumped text.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="emojidump", usage="<guild>", description="Dump all emojis from a guild")
    @infected()
    async def emojidump(self, ctx, guild: discord.Guild):
        if not os.path.exists(f"data/dumping/emojis/{guild.name}"):
            os.makedirs(f"data/dumping/emojis/{guild.name}")

        try:
            for emoji in guild.emojis:
                url = str(emoji.url)
                name = str(emoji.name)
                r = requests.get(url, stream=True)
                if '.png' in url:
                    with open(f'data/dumping/emojis/{guild.name}/{name}.png', 'wb') as f:
                        f.write(r.content)
                elif '.gif' in url:
                    with open(f'data/dumping/emojis/{guild.name}/{name}.gif', 'wb') as f:
                        f.write(r.content)
            await ctx.send("Dumped emojis.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="emojidownload", usage="<guild> <emoji>", description="Download an emoji")
    @infected()
    async def emojidownload(self, ctx, guild: discord.Guild, emoji: discord.Emoji):
        if not os.path.exists(f"data/dumping/emojis/{guild.name}"):
            os.makedirs(f"data/dumping/emojis/{guild.name}")

        try:
            url = str(emoji.url)
            name = str(emoji.name)
            r = requests.get(url, stream=True)
            if '.png' in url:
                with open(f'data/dumping/emojis/{guild.name}/{name}.png', 'wb') as f:
                    f.write(r.content)
            elif '.gif' in url:
                with open(f'data/dumping/emojis/{guild.name}/{name}.gif', 'wb') as f:
                    f.write(r.content)
            await ctx.send("Downloaded emoji.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="avatardump", usage="<guild>", description="Dump avatars from a guild")
    @infected()
    async def avatardump(self, ctx, guild: discord.Guild):
        if not os.path.exists(f"data/dumping/avatars/{guild.name}"):
            os.makedirs(f"data/dumping/avatars/{guild.name}")

        try:
            for member in guild.members:
                url = str(member.avatar_url)
                name = str(member.name)
                r = requests.get(url, stream=True)
                if '.png' in url:
                    with open(f'data/dumping/avatars/{guild.name}/{name}.png', 'wb') as f:
                        f.write(r.content)
                elif '.gif' in url:
                    with open(f'data/dumping/avatars/{guild.name}/{name}.gif', 'wb') as f:
                        f.write(r.content)
            await ctx.send("Dumped avatars.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="channeldump", usage="<guild>", description="Dump channels from a guild")
    @infected()
    async def channeldump(self, ctx, guild: discord.Guild):
        if not os.path.exists(f"data/dumping/channels/{guild.name}"):
            os.makedirs(f"data/dumping/channels/{guild.name}")

        try:
            for channel in guild.channels:
                name = str(channel.name)
                with open(f'data/dumping/channels/{guild.name}/{name}.txt', 'w') as f:
                    f.write(name)
            await ctx.send("Dumped channel names.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Dump(bot))
