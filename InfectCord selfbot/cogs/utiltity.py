import discord
import os
import asyncio
import ast
import requests
import art
import aiohttp
from decouple import config
import datetime
from dateutil import parser
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.errors import Forbidden, HTTPException
from asyncio import sleep
import aiofiles
import math
from html import escape
from main import infected


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nicknames = {}
        self.contexts = {}
        self.indexes = {}
        self.change_nicknames.start()
        self.infectoken = config("token")

    def cog_unload(self):
        self.change_nicknames.cancel()

    async def delete_message(self, message, delay=None):
        try:
            await message.delete(delay=delay)
        except discord.Forbidden:
            pass

    @commands.command()
    @infected()
    async def calc(self, ctx, *, expression):
        infected_allw = "0123456789+-*/(). "
        if all(char in infected_allw for char in expression):
            try:
                result = eval(expression)
                await ctx.send(f'**{result}**', delete_after=30)
            except Exception as e:
                await ctx.send(f'Error: {e}')
        else:
            await ctx.send("Not Allowed", delete_after=5)
        await ctx.message.delete()    

    @commands.command(name='nickscan', aliases=['scan'], brief="Scans for servers where I have nicknames", usage=".nickscan")
    @infected()
    async def nickscan(self, ctx):
        response = "**Here are the servers where I have nicknames set:**\n"
        for guild in self.bot.guilds:
            if guild.me.nick:
                response += f"Server ID: {guild.id}, Server Name: {guild.name}, Nickname: {guild.me.nick}\n"
        if response == "**Here are the servers where I have nicknames set:**\n":
            response = "I don't have nicknames set in any server."
        await ctx.send(response, delete_after=30)
        await self.delete_message(ctx.message)

    @commands.command(name='adminscan', brief="Scans for servers where I have admins", usage=".adminscan")
    @infected()
    async def adminscan(self, ctx):
        guilds_with_admin = [f"Server ID: {guild.id}, Server Name: {guild.name}" for guild in self.bot.guilds if guild.me.guild_permissions.administrator]

        response = "__Servers where I have admins:__\n\n" + "\n".join(guilds_with_admin)
        await ctx.send(response, delete_after=30)
        await self.delete_message(ctx.message)

    @commands.command(name='scrape', brief="Scrapes msges in a channel", usage=".scrape <no.>")
    @infected()
    async def scrape(self, ctx, num_messages: int):
        messages = []
        async for message in ctx.channel.history(limit=num_messages):
            content = escape(message.content)
            timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            messages.append(f'{message.author.name} ({timestamp}): {content}\n')

        file_name = f"scrape_{ctx.message.id}.txt"

        text_content = ''.join(reversed(messages))

        async with aiofiles.open(file_name, mode='w') as f:
            await f.write(text_content)

        await ctx.send(file=discord.File(file_name), delete_after=30)
        await self.delete_message(ctx.message)
        os.remove(file_name)

    @commands.command(name='asci', aliases=['ascii'], brief="Generate ASCII art", usage=".asci <text>")
    @infected()
    async def ascii(self, ctx, *, text: str):
        try:
            ascii_art = art.text2art(text)
            await ctx.send(f"```{ascii_art}```", delete_after=30)

        except Exception as e:
            await ctx.send(f"⚠️ Error generating ASCII art:\n `{str(e)}`", delete_after=30)
        await self.delete_message(ctx.message)

    @commands.command(name='massleave', aliases=['leaveserver'], brief="Leaves all servers", usage=".massleave")
    @infected()
    async def massleave(self, ctx):
        confirmation_message = "**~ Type infected to continue**"
        await ctx.send(confirmation_message)
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower() in ["infected", "no"]
            
        try:
            message = await self.bot.wait_for('message', check=check, timeout=60)
        except TimeoutError:
            await ctx.send('Time out... Please try the cmd again.')
            return

        if message.content.lower() == "infected":
            guild_counter = len(self.bot.guilds)
            index = 0
            for guild in self.bot.guilds:
                index +=1
                if guild.owner_id == self.bot.user.id:
                    await ctx.send(f"Im the owner of {guild.name}, Seems like cant leave")
                    continue
                try:
                    await guild.leave()
                    await ctx.send(f"[{index}/{guild_counter}] Left {guild.name}")
                    await asyncio.sleep(2)
                except Exception as e:
                    await ctx.send(f"[{index}/{guild_counter}] Couldn't leave {guild.name} - {e}")
        elif message.content.lower() == "no":
            await ctx.send("Phew...")

    @commands.command(name='serverlist', aliases=['slist', 'listserver'], brief="Shows user server lists", usage=".serverlist <no.>")
    @infected()
    async def serverlist(self, ctx, page_number: int):
        await ctx.message.delete()

        if page_number < 1:
            await ctx.send("Page number must be at least 1.", delete_after=30)
            return

        servers = self.bot.guilds
        servers_per_page = 10
        pages = math.ceil(len(servers) / servers_per_page)

        if page_number > pages:
            await ctx.send(f"Page no. is out of range. Please enter a no. between 1 and {pages}.", delete_after=30)
            return

        start = (page_number - 1) * servers_per_page
        end = start + servers_per_page

        server_list = '\n'.join([f'{server.name} ({server.id})' for server in 
        servers[start:end]])

        await ctx.send(f'**~ List {page_number}**\n```\n{server_list}\n```', delete_after=30)

    @commands.command(name='firstmsg', aliases=['firstm'], brief="Shows first message of channel/dm", usage=".firstmsg")
    @infected()
    async def firstmsg(self, ctx):
        
        message = await ctx.channel.history(limit=1, oldest_first=True).next()

        
        
        bot_response = await ctx.send(message.jump_url)

        
        await ctx.message.delete()

        
        await asyncio.sleep(30)
        await bot_response.delete()

    @commands.command(name='nickloop', aliases=['nnloop'], brief="Loop through different nicknames", usage=".nickloop nick1 nick2 nick3")
    @infected()
    async def nickloop(self, ctx, *args):
        self.nicknames[ctx.guild.id] = args
        self.contexts[ctx.guild.id] = ctx
        self.indexes[ctx.guild.id] = 0
        await ctx.send("Started the nickname loop", delete_after=5)

    @commands.command(name='stopnickname', aliases=['snnloop'], brief="Stop looping nicknames", usage=".stopnickname")
    @infected()
    async def stopnickloop(self, ctx):
        if ctx.guild.id in self.nicknames:
            del self.nicknames[ctx.guild.id]
            del self.contexts[ctx.guild.id]
            del self.indexes[ctx.guild.id]
            await ctx.send("Stopped the nickname loop.")
        else:
            await ctx.send("No nickname loop is currently running", delete_after=5)

    @tasks.loop(seconds=10)
    async def change_nicknames(self):
        for guild_id in list(self.nicknames.keys()):
            try:
                await self.contexts[guild_id].guild.me.edit(nick=self.nicknames[guild_id][self.indexes[guild_id]])
                self.indexes[guild_id] = (self.indexes[guild_id] + 1) % len(self.nicknames[guild_id])
            except discord.Forbidden:
                await self.contexts[guild_id].send("I do not have permission to change my nickname")

    @nickloop.error
    async def nickloop_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Try again")


    @commands.command(name='servercopy', aliases=['clone'], brief="Clones any server", usage=".servercopy")
    @infected()
    async def servercopy(self, ctx, destination_guild_id: int):
        try:
            
            source_guild = ctx.guild

            
            destination_guild = self.bot.get_guild(destination_guild_id)
            if destination_guild is None:
                await ctx.send("Server not found", delete_after=5)
                return

            
            for channel in destination_guild.channels:
                try:
                    await channel.delete()
                    await sleep(1)  
                except HTTPException as e:
                    await ctx.send(f"Error deleting channel {channel.name}: {e}")
                except Forbidden:
                    await ctx.send(f"Not enough permissions to delete channel {channel.name}")

            
            for role in destination_guild.roles:
                if not role.managed and role.name != "@everyone":
                    try:
                        await role.delete()
                        await sleep(1)  
                    except HTTPException as e:
                        await ctx.send(f"Error deleting role {role.name}: {e}")
                    except Forbidden:
                        await ctx.send(f"Not enough permissions to delete role {role.name}")

            
            for role in reversed(source_guild.roles):
                if not role.managed and role.name != "@everyone":
                    try:
                        await destination_guild.create_role(name=role.name, permissions=role.permissions, 
                                                            colour=role.color, hoist=role.hoist, 
                                                            mentionable=role.mentionable)
                        await sleep(1)  
                    except HTTPException as e:
                        await ctx.send(f"Error creating role {role.name}: {e}")
                    except Forbidden:
                        await ctx.send(f"Not enough permissions to create role {role.name}")

            
            channels = sorted(source_guild.channels, key=lambda x: x.position)

            
            category_mapping = {}
            for channel in channels:
                overwrites = {target: perm for target, perm in channel.overwrites.items() if not isinstance(target, discord.Role) or not target.managed}
                try:
                    if isinstance(channel, discord.CategoryChannel):
                        new_category = await destination_guild.create_category(name=channel.name, overwrites=overwrites)
                        category_mapping[channel.id] = new_category

                    elif isinstance(channel, discord.TextChannel):
                        category = category_mapping.get(channel.category_id, None)
                        await destination_guild.create_text_channel(name=channel.name, overwrites=overwrites, category=category)

                    elif isinstance(channel, discord.VoiceChannel):
                        category = category_mapping.get(channel.category_id, None)
                        await destination_guild.create_voice_channel(name=channel.name, overwrites=overwrites, category=category)

                    await sleep(1)  

                except HTTPException as e:
                    await ctx.send(f"Error creating channel {channel.name}: {e}")
                except Forbidden:
                    await ctx.send(f"Not enough permissions to create channel {channel.name}")

            
            await destination_guild.edit(name=source_guild.name, icon=source_guild.icon)

        except Forbidden:
            await ctx.send("I dont have enough permissions to do that!", delete_after=3)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name='status', aliases=['mode'], brief="Change your activity", usage=".status <mode> <message>")
    @infected()
    async def status(self, ctx, activity_type: str, *, activity_message: str):
        if activity_type.lower() == "playing":
            await self.bot.change_presence(activity=discord.Game(name=activity_message))
        elif activity_type.lower() == "streaming":
            await self.bot.change_presence(activity=discord.Streaming(name=activity_message, url="http://twitch.tv/infectedx7"))
        elif activity_type.lower() == "listening":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_message))
        else:
            await ctx.send('Invalid Use either "playing", "streaming", or "listening" \n- status <mode> <message>')
        await ctx.message.delete()

    @commands.command(name='checkpromo', aliases=['promo'], brief="Check promos", usage=".checkpromo <check.promo>")
    @infected()
    async def checkpromo(self, ctx, *, promo_links: str):
        await ctx.message.delete()
        if not isinstance(promo_links, str):
            await ctx.send("Enter promos", delete_after=5)
            return

        links = promo_links.split('\n')

        async with aiohttp.ClientSession() as session:
            for link in links:
                try:
                    promo_code = self.extract_promo_code(link)
                    if promo_code:
                        result = await self.check_promo(session, promo_code)
                        await ctx.send(result)
                    else:
                        await ctx.send(f'Invalid promo link: {link}')
                except Exception as e:
                    await ctx.send(f'An error occurred while processing the link: {link}. Error: {str(e)}')

    async def check_promo(self, session, promo_code):
        url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

        try:
            async with session.get(url) as response:
                if response.status in [200, 204, 201]:
                    data = await response.json()
                    if "uses" in data and "max_uses" in data and data["uses"] == data["max_uses"]:
                        return f'**~ Already Claimed: {promo_code}**'
                    elif "expires_at" in data and "promotion" in data and "inbound_header_text" in data["promotion"]:
                        exp_at = data["expires_at"].split(".")[0]
                        parsed = parser.parse(exp_at)
                        unix_timestamp = int(parsed.timestamp())
                        title = data["promotion"]["inbound_header_text"]
                        return f'**~ Valid: {promo_code}  \n~ Expires At: <t:{unix_timestamp}:R>  \n~ Offer: {title}**'
                elif response.status == 429:
                    retry_after = response.headers.get("retry-after", "Unknown")
                    return f'Rate Limited for {retry_after} seconds'
                else:
                    return f'Invalid Code -> {promo_code}'
        except Exception as e:
            return f'An error occurred while checking the promo code: {promo_code}. Error: {str(e)}'

    def extract_promo_code(self, promo_link):
        try:
            promo_code = promo_link.split('/')[-1]
            return promo_code
        except Exception as e:
            return None
            

    @commands.command(name="hypesquad", usage="<bravery/brilliance/balance>", description="Change Hypesquad house")
    @infected()
    async def hypesquad(self, ctx, house: str):
        ttoken = self.infectoken
        headers = {
            'Authorization': ttoken,
            'Content-Type': 'application/json'
        }

        if house.lower() in ["bravery", "brilliance", "balance"]:
            payload = {'house_id': {"bravery": 1, "brilliance": 2, "balance": 3}[house.lower()]}

            try:
                response = requests.post(
                    f'https://discord.com/api/v9/hypesquad/online',
                    headers=headers, json=payload
                )
                response.raise_for_status()
                await ctx.send(f"Infected your Hypesquad house to {house.capitalize()}..", delete_after=30)

            except requests.RequestException:
                await ctx.send("Failed to infect", delete_after=5)
        else:
            await ctx.send("Invalid Hypesquad. Choose from bravery, brilliance, or balance", delete_after=10)

    @commands.command(name='screenshot', aliases=['ss'])
    @infected()
    async def screenshot(self, ctx, url):
        infectedsskey = 'da1f63'
        endpoint = 'https://api.screenshotmachine.com'

        params = {
            'key': infectedsskey,
            'url': url,
            'dimension': '1024xfull',
            'format': 'png',
            'cacheLimit': '0',
            'timeout': '200'
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()

            with open('infected.png', 'wb') as f:
                f.write(response.content)
                
            await ctx.message.delete()    

            await ctx.send(file=discord.File('infected.png'), delete_after=30)
        except requests.exceptions.RequestException as e:
            await ctx.send('- Failed to take SS {}'.format(str(e)), delete_after=3)
        except Exception as e:
            await ctx.send('An error occurred: {}'.format(str(e)))
        finally:
            os.remove('infected.png')    

    @commands.command(aliases=['findphoto', 'showphoto'])
    async def getpic(self, ctx, *, query):
        
        google_api_key = 'AIzaSyDVaNy89jV_K6KP-ks5pdqJR839g3iLbdo'
        search_engine_id = '47f928af66b3d4185'
        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'key': google_api_key,
            'cx': search_engine_id,
            'q': query,
            'searchType': 'image',
            'num': 1
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                image_url = data['items'][0]['link']
                await ctx.send(image_url, delete_after=30)
            else:
                await ctx.send("Couldnt Find", delete_after=3)
        else:
            await ctx.send("Error Occured/ Ratelimited", delete_after=3)          


def setup(bot):
    bot.add_cog(Utility(bot))