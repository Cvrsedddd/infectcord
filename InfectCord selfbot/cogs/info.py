import discord
import os
import platform
import datetime
import psutil
import time
import asyncio
import requests
from main import infected
from discord.ext import commands
from decouple import config

languages = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
}

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = 'a91c8e0d5897462581c0c923ada079e5'
        self.infectoken = config("token")


    @commands.command(name='avatar', aliases=['av','ava'], brief="Shows user avatar", usage=".avatar <mention.user>")
    @infected()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.author
        await ctx.send(member.avatar_url, delete_after=30)

    @commands.command(name="userinfo", usage="<@member>", description="Show user info")
    @infected()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        infected.xd = {
            1133410789429084190: "Dev Of InfectCord"
        }

        special = infected.xd.get(user.id, "")

        date_format = "%a, %d %b %Y %I:%M %p"
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at or ctx.guild.created_at)
        role_string = ', '.join([r.name for r in user.roles][1:])
        perm_string = ', '.join(
            [str(p[0]).replace("_", " ").title()
             for p in user.guild_permissions if p[1]]
        )

        infected.whois = (
            f"- User » {user.mention}\n"
            f"- User info\n\n"
            f"- Joined » {user.joined_at.strftime(date_format)}\n"
            f"- Join position » {members.index(user) + 1}\n"
            f"- Registered » {user.created_at.strftime(date_format)}\n\n"
            f"- User server Info\n\n"
            f"- Roles Count » {len(user.roles) - 1}\n"
            f"- Roles\n\n{role_string}\n\n"
            f"- Perms\n\n{perm_string}{special}"
        )

        await ctx.send(infected.whois, delete_after=30)
        
        
    @commands.command(name="whois", usage="[user_id]", description="User information")
    @infected()
    async def whois(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        
        r = requests.get(
            f'https://discord.com/api/v9/users/{user.id}',
            headers={
                'authorization': self.infectoken,
                'user-agent': 'Mozilla/5.0'
            }
        ).json()
        
        req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req.get("banner")
        if banner_id:
            banner_url = f"https://cdn.discord.com/banners/{user.id}/{banner_id}?size=1024"
            if not banner_url.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                banner_url += ".png"
        else:
            banner_url = None
      
        response = (
            "- **InfectCord Userinfo**\n\n"
            f"- {'User':12} ~ {user.name}#{user.discriminator}\n"
            f"- {'ID':12} ~ {user.id}\n"
            f"- {'Status':12} ~ {user.status}\n"
            f"- {'Bot':12} ~ {user.bot}\n"
            f"- {'Public Flags':12} ~ {r['public_flags']}\n"
            f"- {'Banner Color':12} ~ {r['banner_color']}\n"
            f"- {'Accent Color':12} ~ {r['accent_color']}\n\n"
            f"- Created at:\n - {user.created_at}\n\n"
            "- Profile Img Info\n\n"
            f"- Avatar URL:\n - {user.avatar_url}\n\n"
            f"- Banner URL:\n - {banner_url}"
        )
        
        await ctx.send(response, delete_after=30)       


    @commands.command(name='stats', aliases=['info'], brief="I N F E C T E D", usage=".stats")
    @infected()
    async def stats(self, ctx):
        await ctx.message.delete()
        process = psutil.Process(os.getpid())
        ram_usage = process.memory_info().rss / 1024**2
        cpu_usage = psutil.cpu_percent()
        total_commands = len(self.bot.commands)
        infectedinfo = "**__Infect Cord x1__**\n\n"
        infectedinfo += "**• Infect Cord: x1\n"
        infectedinfo += f"• Total Cmds: {total_commands}\n"
        infectedinfo += f"• OS: {platform.system()}\n"
        infectedinfo += f"• RAM Usage: {ram_usage:.2f} MB\n"
        infectedinfo += f"• CPU Usage: {cpu_usage}%\n"
        infectedinfo += f"• Python: {platform.python_version()}\n\n"
        infectedinfo += "• Follow On Git: <https://github.com/zaddyinfected> **\n"
        await ctx.send(infectedinfo, delete_after=30)
      
        

    @commands.command(name='ping', aliases=['pong'], brief="Shows Selfbot Latency", usage=".ping")
    @infected()
    async def ping(self, ctx):
        await ctx.message.delete()
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'**~ {latency}ms**', delete_after=30)

    @commands.command(name='tokeninfo', aliases=['tdox'], brief="Shows token info", usage=".tokeninfo <user.token>")
    @infected()
    async def tokeninfo(self, ctx, _token):
        await ctx.message.delete()
        headers = {
            'Authorization': _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = f"<t:{int(((int(user_id) >> 22) + 1420070400000) / 1000)}:R>"
        except KeyError:
            headers = {
                'Authorization': "Bot " + _token,
                'Content-Type': 'application/json'
            }
            try:
                res = requests.get('https://canary.discordapp.com/api/v9/users/@me', headers=headers)
                res = res.json()
                user_id = res['id']
                locale = res['locale']
                avatar_id = res['avatar']
                language = languages.get(locale)
                creation_date = f"<t:{int(((int(user_id) >> 22) + 1420070400000) / 1000)}:R>"
                message = (
                    f"**~ Name: {res['username']}#{res['discriminator']}  **BOT**\n"
                    f"~ ID: {res['id']}\n"
                    f"~ Email: {res['email']}\n"
                    f"~ Created on: {creation_date}`"
                )
                fields = [
                    {'name': '~ Flags', 'value': res['flags']},
                    {'name': '~ Lang', 'value': res['locale']},
                    {'name': '~ Verified', 'value': res['verified']},
                ]
                for field in fields:
                    if field['value']:
                        message += f"\n{field['name']}: {field['value']}"
                message += f"\n~ Avatar URL: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id} **"
                return await ctx.send(message)
            except KeyError:
                return await ctx.send("Invalid token", delete_after=30)

        message = (
            f"**~ Name: {res['username']}#{res['discriminator']}\n"
            f"~ ID: {res['id']}\n"
            f"~ Created On: {creation_date}"
        )
        nitro_type = "None"
        if "premium_type" in res:
            if res['premium_type'] == 2:
                nitro_type = "Nitro Boost"
            elif res['premium_type'] == 3:
                nitro_type = "Nitro Basic"
        fields = [
            {'name': '~ Phone', 'value': res['phone']},
            {'name': '~ Flags', 'value': res['flags']},
            {'name': '~ Lang', 'value': res['locale']},
            {'name': '~ 2FA', 'value': res['mfa_enabled']},
            {'name': '~ Verified', 'value': res['verified']},
            {'name': '~ Nitro', 'value': nitro_type},
        ]
        for field in fields:
            if field['value']:
                message += f"\n{field['name']}: {field['value']}"
        message += f"\n~ Avatar URL: https://cdn.discordapp.com/avatars/{user_id}/{avatar_id} **"
        await ctx.send(message, delete_after=30)

    @commands.command(name='iplook', aliases=['geolocate', 'iptogeo', 'iptolocation', 'ip2geo', 'ip'], brief="Looks for IP", usage=".iplook <ip.address>")
    @infected()
    async def iplook(self, ctx, ip):
        api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={ip}'
        
        response = requests.get(api_url)
        data = response.json()
        
        if 'country_name' in data:
            country = data['country_name']
            city = data['city']
            isp = data['isp']
            current_time_unix = data['time_zone']['current_time_unix']
    
            current_time_formatted = f"<t:{int(current_time_unix)}:f>"
            
            message = f"IP Lookup Results for {ip}:\n"
            message += f"Country: {country}\n"
            message += f"City: {city}\n"
            message += f"ISP: {isp}\n"
            message += f"Current Time: {current_time_formatted}\n"
            
            await ctx.send(message, delete_after=30)
        else:
            await ctx.send("Invalid IP address", delete_after=30)


    @commands.command(name='id', aliases=['snowflake'], brief="Shows dev id of target", usage=".id <target>")
    @infected()
    async def id(self, ctx, *targets):
        if not targets:
            await ctx.send(f"Your ID is: {ctx.author.id}")
        else:
            for target in targets:
                if target.lower() == "server":
                        await ctx.send("**~ ID of the server is**", delete_after=30)
                        await ctx.send(ctx.guild.id, delete_after=30)
                elif len(ctx.message.mentions) > 0:
                    for member in ctx.message.mentions:
                        await ctx.send(f"**~ ID of {member.name} is**", delete_after=30)
                        await ctx.send(member.id, delete_after=30)
                elif len(ctx.message.channel_mentions) > 0:
                    for channel in ctx.message.channel_mentions:
                        await ctx.send(f"**~ ID of {channel.name} is**", delete_after=30)
                        await ctx.send(channel.id, delete_after=30)
                elif len(ctx.message.role_mentions) > 0:
                    for role in ctx.message.role_mentions:
                        await ctx.send(f"**~ ID of {role.name} role is**", delete_after=30)
                        await ctx.send(role.id, delete_after=30)
                else:
                    await ctx.send(f"~ Cant look for this mention: {target}", delete_after=30)
      
def setup(bot):
    bot.add_cog(Info(bot))
