import discord
from discord.ext import commands
from discord import Forbidden
from main import infected
import asyncio
import requests
import json
import random
import time
import threading
from threading import Thread
import aiohttp
import os

class Wizz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_rate_limit = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.guild)
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        asyncio.create_task(self.session.close())
     
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return 

        await ctx.send(f'Error: {str(error)}')
        
    @commands.command()
    @infected()
    async def randomban(self, ctx, count: int):
        if count <= 0:
            await ctx.send("- Missing Number", delete_after=5)
            return

        guild = ctx.guild
        members = list(guild.members)
        random.shuffle(members)

        banned_count = 0
        async with aiohttp.ClientSession() as session:
            tasks = []
            for member in members[:count]:
                tasks.append(self.ban_member(session, guild, member))
            
            results = await asyncio.gather(*tasks)
            banned_count = sum(results)

        await ctx.send(f"Randomly banned {banned_count} mem\s", delete_after=30)

    async def ban_member(self, session, guild, member):
        try:
            await guild.ban(member, reason="Random ban")
            return 1
        except discord.Forbidden:
            return 0

    @commands.command(name='nukechannels', aliases=['wizzc'], brief="Nukes all channel", usage=".nukechannels")
    @infected()
    async def nukechannels(self, ctx):
        nuked_count = 0
        failed_count = 0

        confirmation_msg = await ctx.send("you sure ? type yes")
        try:
            response = await self.bot.wait_for('message', timeout=15.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        except asyncio.TimeoutError:
            await confirmation_msg.edit(content="Command timed out. wizzing channel canceled")
            return

        if response.content.lower() != 'yes':
            await confirmation_msg.edit(content="Wizzing channel canceled")
            return

        spinner_msg = await ctx.send("Nuking channels...")
        async with spinner_msg.channel.typing():
            for channel in ctx.guild.channels:
                if channel.permissions_for(ctx.me).manage_channels:
                    try:
                        await channel.delete()
                        nuked_count += 1
                    except:
                        failed_count += 1

        await spinner_msg.edit(content=f"Nuked {nuked_count} channels. Failed to delete {failed_count} channels", delete_after=5)

    @nukechannels.error
    async def nukechannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I donthave the required perms to initiate a channel delete", delete_after=30)
        else:
            await ctx.send("An error occurred while executing the channel delete", delete_after=30)

    @commands.command(name='servername', aliases=['sname'], brief="Changes server name", usage=".servername <new.name>")
    @infected()
    async def servername(self, ctx, new_name):
        try:
            await ctx.guild.edit(name=new_name)
            await ctx.send(f'Server name changed to {new_name}')
        except discord.Forbidden:
            await ctx.send('I do not have permission to change the server name', delete_after=5)
        except discord.HTTPException as e:
            await ctx.send(f'Failed to change server name: {str(e)}', delete_after=5)
          
    @commands.command(name='servericon', aliases=['spfp','sicon'], brief="Change server icon", usage=".servericon <image.url>")
    @infected()
    async def servericon(self, ctx, icon_url):
        try:
            async with self.session.get(icon_url) as response:
                if response.status == 200:
                    data = await response.read()
                    await ctx.guild.edit(icon=data)
                    await ctx.send('Server icon changed', delete_after=30)
                else:
                    await ctx.send('Failed to download the image.')
        except discord.Forbidden:
            await ctx.send('I do not have permission to change the server icon', delete_after=5)
        except discord.HTTPException as e:
            await ctx.send(f'Failed to change server icon: {str(e)}', delete_after=5)

    @commands.command()
    @infected()
    async def massban(self, ctx, delay: int = 5, *, reason: str = "Mass ban reason", member_ids: commands.Greedy[int]):
        guild = ctx.guild
        banned_count = 0
        failed_count = 0

        for member_id in member_ids:
            member = guild.get_member(member_id)
            if member:
                try:
                    await guild.ban(member, reason=reason)
                    banned_count += 1
                    await asyncio.sleep(delay)
                except discord.Forbidden:
                    failed_count += 1
                except discord.HTTPException as e:
                    print(f"An error occurred while banning {member_id}: {e}")
                    failed_count += 1
                    continue

        await ctx.send(f"- Banned {banned_count} mems \n - {failed_count} bans failed", delete_after=10)

    @commands.command()
    @infected()
    async def massunban(self, ctx, *member_ids: int):
        guild = ctx.guild
        unbanned_count = 0
        failed_count = 0

        for member_id in member_ids:
            try:
                await guild.unban(discord.Object(id=member_id))
                unbanned_count += 1
            except discord.Forbidden:
                failed_count += 1
            except discord.HTTPException as e:
                print(f"An error occurred while unbanning {member_id}: {e}")
                failed_count += 1

        await ctx.send(f"- Unbanned {unbanned_count} members \n- {failed_count} unbans failed", delete_after=10)

    @commands.command(name='massdm', aliases=['dmall'], brief="mass dm server members", usage=".massdm <context>")
    async def dmannounce(self, ctx, *, message):
            for member in ctx.guild.members:
                if not member.bot:
                    try:
                        await member.send(message)
                    except:
                        print(f"Couldn't send DM to {member.name}")

def setup(bot):
    bot.add_cog(Wizz(bot))