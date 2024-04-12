import discord
from discord.ext import commands
from main import infected
import asyncio
import random
import string
import requests
import os
from decouple import config

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.infectoken = config("token")

    @commands.command(name='spam', aliases=['say'], brief="Start Spamming", usage=".spam <times> <message.content>")
    async def spam(self, ctx, times: int, *, content:str):
        if times < 1:
            await ctx.send('Error')
        else:
            for i in range(times):
                try:
                    await ctx.send(content)
                    await asyncio.sleep(0.450)
                except discord.errors.HTTPException as e:
                    if 'You are being rate limited' in str(e):
                        delay = e.retry_after + 5
                        await asyncio.sleep(delay)
                        await ctx.send(content)
                    else:
                        raise e

    @commands.command(name='massreact', aliases=['mreact'], brief="Mass react on last message", usage=".massreact")
    @infected()
    async def massreact(self, ctx):
        try:

            
            message = await ctx.channel.history(limit=2).flatten()
            message = message[1]  

            
            emojis = ["❤️", "🤍", "🖤", "💜", "🔥", "💧", "💨", "🍎", "🍇", "🍓", "🍒", "🌸", "🌺", "🌹", "🌷", "🌈", "⭐", "🌟", "🌙", "☀️"]
            
            random.shuffle(emojis) 

            
            for emoji in emojis[:20]:  
                try:
                    await message.add_reaction(emoji)
                    await asyncio.sleep(1)  
                except discord.errors.HTTPException as e:
                    if 'You are being rate limited.' in str(e):
                        delay = e.retry_after
                        await asyncio.sleep(delay)
                        await message.add_reaction(emoji)
                    else:
                        raise e
        except Exception as e:
            error_message = f"An error occurred: {type(e).__name__} - {str(e)}"
            await ctx.send(error_message)
            await ctx.message.delete() 

    @massreact.error
    async def massreact_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            error_message = "Sorry, Error Occured"
            await ctx.send(error_message)

    @commands.command()
    @infected()
    async def clear(self, ctx, amount: int = 0, links: bool = False):
        if not amount:
            await ctx.send(
                '- `.clear 10 1`~ Delete 10 messages with links\n'
                '- `.clear -1`~ Delete all messages (may take time)',
                delete_after=15
            )
            return

        count = 0
        async for message in self.get_messages(ctx, amount, links):
            await message.delete()
            count += 1
            print(f'Deleted {count}/{amount if amount > 0 else "all"} messages.')
            await asyncio.sleep(1)

        print(f'---- Infected Task done, deleted {count} {"message" if count == 1 else "messages"} ----')
        await ctx.send(f'- Deleted `{count}` messages', delete_after=5)

    async def get_messages(self, ctx, amount, links):
        count = 0
        async for message in ctx.channel.history(limit=None):
            if count == amount:
                return
            if message.author != ctx.author:
                continue
            if links:
                if 'http://' in message.content or 'https://' in message.content:
                    count += 1
                    yield message
                continue
            count += 1
            yield message

    @commands.command()
    @infected()
    async def massmention(self, ctx, *, message=None):
        await ctx.message.delete()
        if len(list(ctx.guild.members)) >= 50:
            userList = list(ctx.guild.members)
            random.shuffle(userList)
            sampling = random.choices(userList, k=50)
            if message is None:
                post_message = ""
                for user in sampling:
                    post_message += user.mention
                await ctx.send(post_message)
            else:
                post_message = message + "\n\n"
                for user in sampling:
                    post_message += user.mention
                await ctx.send(post_message)
        else:
            if message is None:
                post_message = ""
                for user in list(ctx.guild.members):
                    post_message += user.mention
                await ctx.send(post_message)
            else:
                post_message = message + "\n\n"
                for user in list(ctx.guild.members):
                    post_message += user.mention
                await ctx.send(post_message)

    @commands.command(name='cum', aliases=['muth'], brief="Wanna cum?", usage=".cum")
    @infected()
    async def cum(self, ctx):
        await ctx.message.delete()
        message = await ctx.send('''
                :ok_hand:            :smile:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8=:punch:=D 
                 :trumpet:      :eggplant:''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                          :ok_hand:            :smiley:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8==:punch:D 
                 :trumpet:      :eggplant:  
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                          :ok_hand:            :grimacing:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8=:punch:=D 
                 :trumpet:      :eggplant:  
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                          :ok_hand:            :persevere:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8==:punch:D 
                 :trumpet:      :eggplant:   
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                          :ok_hand:            :confounded:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8=:punch:=D 
                 :trumpet:      :eggplant: 
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                           :ok_hand:            :tired_face:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8==:punch:D 
                 :trumpet:      :eggplant:    
             ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                           :ok_hand:            :weary:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8=:punch:= D:sweat_drops:
                 :trumpet:      :eggplant:        
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                           :ok_hand:            :dizzy_face:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8==:punch:D :sweat_drops:
                 :trumpet:      :eggplant:                 :sweat_drops:
         ''')
        await asyncio.sleep(0.5)
        await message.edit(content='''
                           :ok_hand:            :drooling_face:
       :eggplant: :zzz: :necktie: :eggplant: 
                       :oil:     :nose:
                     :zap: 8==:punch:D :sweat_drops:
                 :trumpet:      :eggplant:                 :sweat_drops:''', delete_after=60)


    @commands.command(name='fakenitro', aliases=['nitro'], brief="Give nitros", usage=".fakenitro")
    @infected()
    async def fakenitro(self, ctx):
        nitro_code = self.generate_nitro_code()
        fake_link = f"discord.gift/{nitro_code}"
        await ctx.send(fake_link, delete_after=30)

    def generate_nitro_code(self):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        nitro_code = self.generate_random_string(16, characters)
        return nitro_code

    def generate_random_string(self, length, characters):
        return ''.join(random.choices(characters, k=length))
        
    @commands.command(name="infect", usage="[@member] <infection>", description="Animated infected message")
    @infected()
    async def infect(self, ctx, user: discord.Member = None, *, infection: str = "trojan"):
        user = user or ctx.author
        start = await ctx.send(f"{ctx.author.mention} has started to spread {infection}")
        animation_list = (
            f"``[▓▓▓                    ] / {infection}-infection.exe Packing files.``",
            f"``[▓▓▓▓▓▓▓                ] - {infection}-infection.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓           ] {infection}-infection.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {infection}-infection.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {infection}-infection.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {infection}-infection.exe Packing files..``",
            f"``[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] {infection}-infection.exe Packing files..``",
            f"``Successfully downloaded {infection}-infection.exe``",
            "``Injecting infection.   |``",
            "``Injecting infection..  /``",
            "``Injecting infection... -``",
            f"``Successfully Injected {infection}-infection.exe into {user.name}``",
        )
        for i in animation_list:
            await asyncio.sleep(1.5)
            await start.edit(content=i)  
            
    @commands.command(name="spamgp", usage="<delay> <amount> <@member>", aliases=['spg', 'spamghostping', 'sghostping'], description="Ghostpings")
    @infected()
    async def spamgp(self, ctx, delay: int = None, amount: int = None, user: discord.Member = None):
        try:
            if delay is None or amount is None or user is None:
                await ctx.send(f"Usage: {self.bot.prefix}spamghostping <delay> <amount> <@member>")
            else:
                for _ in range(amount):
                    await asyncio.sleep(delay)
                    await ctx.send(user.mention, delete_after=0)
        except Exception as e:
            await ctx.send(f"Error: {e}")    
            
    @commands.command(name="spamdm", usage="<delay> <amount> <@user> <message>", description="DMs")
    @infected()
    async def spamdm(self, ctx, delay: int, amount: int, user: discord.User, *, message: str):
        try:
            for _ in range(amount):
                await asyncio.sleep(delay)
                await user.send(f"{message}")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            
    @commands.command(name="spamrep", usage="<message_id> <amount>", aliases=['spamreport'], description="Reports")
    async def spamrep(self, ctx, message_id: str, amount: int):
        try:
            print("Spam report started...")
            for _ in range(amount):
                await asyncio.sleep(2)
                reason = "Illegal Content"
                payload = {
                    'message_id': message_id,
                    'reason': reason
                }
                requests.post(
                    'https://discord.com/api/v9/report',
                    json=payload,
                    headers={
                        'authorization': self.infectoken,
                        'user-agent': 'Mozilla/5.0'
                    }
                )
            print("Spam report finished")
            await ctx.send(f"- Msg **{message_id}** has been reported __{amount}__ times", delete_after=10)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            

def setup(bot):
    bot.add_cog(Fun(bot))