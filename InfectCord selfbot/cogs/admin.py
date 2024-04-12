import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp
import requests
from decouple import config
from datetime import datetime, timedelta
from main import infected

rate_limits = {}

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forced_nicks = {}
        self.infectoken = config("token")

    @commands.command(name='savebans', aliases=['saveban'], brief="Save bans list", usage=".saveban <any.name>")
    @infected()
    async def savebans(self, ctx, file_name):
        try:
            ban_list = await ctx.guild.bans()
            data = []
            for entry in ban_list:
                data.append({"id": entry.user.id, "reason": str(entry.reason)})
            with open(f'{file_name}.json', 'w') as f:
                json.dump(data, f)
            await ctx.send(f'Ban list has been saved to {file_name}.json')
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')

    @commands.command(name='exportbans', aliases=['exportban'], brief="Export bans list", usage=".exportban <filename>")
    @commands.has_permissions(ban_members=True)
    @infected()
    async def exportbans(self, ctx, file_name):
        try:
            if not os.path.isfile(f'{file_name}.json'):
                await ctx.send(f'File {file_name}.json does not exist.')
                return

            with open(f'{file_name}.json', 'r') as f:
                ban_list = json.load(f)

            async with aiohttp.ClientSession() as session:
                for ban_entry in ban_list:
                    user_id = ban_entry["id"]
                    if user_id in rate_limits and rate_limits[user_id] > datetime.now():
                        await asyncio.sleep((rate_limits[user_id] - datetime.now()).total_seconds())

                    try:
                        async with session.get(f"https://discord.com/api/v10/users/{user_id}") as response:
                            if response.status == 429:
                                retry_after = int(response.headers.get("Retry-After"))

                                rate_limits[user_id] = datetime.now() + timedelta(seconds=retry_after)

                                await asyncio.sleep(retry_after)
                                continue 

                            user_data = await response.json()

                        user = self.bot.get_user(user_id)
                        if user is None:
                            user = await self.bot.fetch_user(user_id)

                        await ctx.guild.ban(user, reason=ban_entry["reason"])

                    except Exception as e:
                        await ctx.send(f'An unexpected error occurred: {e}', delete_after=30)

            await ctx.send(f'Ban list has been imported from {file_name}.json', delete_after=30)

        except Exception as e:
            await ctx.send(f'An unexpected error occurred: {e}')

    @commands.command(name='nuke', aliases=['fuckchannel'], brief="Instant nuke the channel", usage=".nuke")
    @infected()
    async def nuke(self, ctx):
        old_channel = ctx.channel
        try:
            new_channel = await old_channel.clone(reason="Channel clone created by admin")
            await new_channel.edit(position=old_channel.position)
            await old_channel.delete()

            await new_channel.send(f"`Channel nuked by {ctx.author.mention}`")
        except Forbidden:
            await ctx.send("I don't have permissions to nuke channels")
        except HTTPException:
            await ctx.send("Failed to clone")

    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You dont have perms')
        else:
            await ctx.send('An unexpected error occurred')


    @commands.command(name='forcenick', aliases=['fucknick','fn'], brief="Force a users nickname", usage=".forcenick <mention.user> <nick.name>")
    @infected()
    async def forcenick(self, ctx, user: discord.Member, *, nickname: str):
        self.forced_nicks[user.id] = nickname
        try:
            await user.edit(nick=nickname)
            await ctx.send(f"Fucked nickname '{nickname}' on {user.display_name}.")
        except discord.Forbidden:
            await ctx.send("I dont have perms to edit nn")

    @commands.command(name='stopforcenick', aliases=['sfn','stopfucknick'], brief="Stop force kicking the user", usage=".stopforcenick <mention.user>")
    @infected()
    async def stopforcenick(self, ctx, user: discord.Member):
        if user.id in self.forced_nicks:
            del self.forced_nicks[user.id]
            try:
                await user.edit(nick=None)
                await ctx.send(f"Stopped fucking nickname on {user.display_name}.")
            except discord.Forbidden:
                await ctx.send("I dont have perms to edit nn")
        else:
            await ctx.send(f"No forced nickname found for {user.display_name}.")
            
    @commands.command(name="kick", usage="<@member> [reason]", description="Kick a user")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @infected()
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        await user.kick(reason=reason)
        await ctx.send(f"- {user.name} has been kicked.\nReason~ {reason}")

    @commands.command(name="softban", usage="<@member> [reason]", description="Softban a user")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @infected()
    async def softban(self, ctx, user: discord.Member, *, reason: str = None):
        await user.ban(reason=reason)
        await user.unban()
        await ctx.send(f"- {user.name} has been softbanned.\nReason~ {reason}", delete_after=30)

    @commands.command(name="ban", aliases=['machuda','nikal'], usage="<@member> [reason]", description="Ban a user")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @infected()
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        await user.ban(reason=reason)
        await ctx.send(f"- {user.name} has been banned.\nReason~ {reason}", delete_after=30)

    @commands.command(name="unban", usage="<user_id>", description="Unban a user")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @infected()
    async def unban(self, ctx, user_id: int):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.id == user_id:
                await ctx.guild.unban(user)
                await ctx.send(f"- {user.name} has been unbanned", delete_after=30)
                return
        await ctx.send(f"No banned user with the ID {user_id} was found", delete_after=30)
        
    @commands.command(name="mute", usage="<user> <time>", description="Mute a user")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @infected()
    async def mute(self, ctx, user: discord.Member, time: int):
        payload = {
            'user_id': user.id,
            'duration': time
        }
        response = requests.post(
            f'https://discord.com/api/v10/guilds/{ctx.guild.id}/bans',
            json=payload,
            headers={
                'authorization': self.infectoken,
                'user-agent': 'Mozilla/5.0'
            }
        )
        if response.status_code == 200:
            await ctx.send(f"Muted for {time} sec", delete_after=30)
        else:
            await ctx.send("Failed to time out the user", delete_after=30)       

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.id in self.forced_nicks and after.nick != self.forced_nicks[after.id]:
            try:
                await after.edit(nick=self.forced_nicks[after.id])
            except discord.Forbidden:
                pass

    @forcenick.error
    async def forcenick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need to have admin perms")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user or nickname provided.")
        else:
            await ctx.send("An error occurred while executing the cmd")

    @stopforcenick.error
    async def stopforcenick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need to have admin perms to use this cmd")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user provided.")
        else:
            await ctx.send("An error occurred while executing the cmd")

def setup(bot):
    bot.add_cog(Admin(bot))
