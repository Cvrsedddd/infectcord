from discord.ext import commands, tasks
import requests
import json
import asyncio
from main import infected
from collections import defaultdict

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.supported_currencies = {
            'btc': 'bitcoin', 
            'eth': 'ethereum', 
            'ltc': 'litecoin', 
            'xrp': 'ripple', 
            'usdt': 'tether', 
            'usdc': 'usd-coin',
            'doge': 'dogecoin',
        }
      
    async def delete_message(self, message, delay=None):
        try:
            await message.delete(delay=delay)
        except discord.Forbidden:
            pass

    @commands.command(name='getbal', aliases=['bal', 'ltcbal'], brief="Shows User LTC Bal", usage=".getbal <ltc.addy>")
    @infected()
    async def getbal(self, ctx, ltcaddress: str = None):
        if ltcaddress is None:
            await ctx.send("- Please provide a LTC Address", delete_after=5)
            return

        if len(ltcaddress) not in [34, 43]:
            await ctx.reply("- The provided LTC address isnt valid", delete_after=5)
            return            

        response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                await ctx.send("Invalid LTC address.")
            else:
                await ctx.send(f"Failed to retrieve balance. Error {response.status_code}. Please try again later", delete_after=5)
            return

        data = response.json()
        balance = data['balance'] / 10 ** 8
        total_balance = data['total_received'] / 10 ** 8
        unconfirmed_balance = data['unconfirmed_balance'] / 10 ** 8

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

        if cg_response.status_code != 200:
            await ctx.send(
                f"Failed to retrieve the current price of LTC. Error {cg_response.status_code}. Please try again later", delete_after=5)
            return

        usd_price = cg_response.json()['litecoin']['usd']
        usd_balance = balance * usd_price
        usd_total_balance = total_balance * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        message = f"LTC Address: `{ltcaddress}`\n"
        message += f"__Current LTC__ ~ **${usd_balance:.2f} USD**\n"
        message += f"__Total LTC Received__ ~ **${usd_total_balance:.2f} USD**\n"
        message += f"__Unconfirmed LTC__ ~ **${usd_unconfirmed_balance:.2f} USD**"

        await ctx.send(message, delete_after=30)
        await self.delete_message(ctx.message)

    @commands.command(name='price', aliases=['current'], brief="Shows current crypto prices", usage=".price <crypto.name>")
    @infected()
    async def price(self, ctx, crypto='ltc'):
        if crypto not in self.supported_currencies:
            error_message = await ctx.send(f'~ Invalid crypto \n~ Supported currencies are \n~ ***{", ".join(self.supported_currencies.keys())}***', delete_after=20)
            await ctx.message.delete()
            return
            
        crypto_full = self.supported_currencies[crypto]
     
        coingecko_url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_full}&vs_currencies=usd'
        
        try:
            response = requests.get(coingecko_url).json()

            price = response[crypto_full]['usd']
            infected = await ctx.send(f'- The current price of **{crypto}** is **__${price}__**', delete_after=30)
            await ctx.message.delete()
            await asyncio.sleep(15)
            await infected.delete()
            
        except Exception as e:
            
            await ctx.send('Error occurred while fetching crypto')
            print(e)
  
    @commands.command(name='getbtcbal', aliases=['btcbal'], brief="Shows User BTC Bal", usage=".getbtcbal <btc.addy>")
    @infected()
    async def getbtcbal(self, ctx, btcaddress: str = None):
        if btcaddress is None:
            await ctx.reply("- Please provide a BTC Addy", delete_after=5)
            return

        if len(btcaddress) not in [34, 43, 42]:
            await ctx.reply("- The provided BTC address isnt valid", delete_after=5)
            return
            
        response = requests.get(f'https://api.blockcypher.com/v1/btc/main/addrs/{btcaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                await ctx.reply("Invalid BTC Addy")
            else:
                await ctx.reply(f"Failed to retrieve balance. Error {response.status_code}. Please try again later", delete_after=5)
            return

        data = response.json()
        balance = data['balance'] / 10 ** 8
        total_received = data['total_received'] / 10 ** 8
        unconfirmed_balance = data['unconfirmed_balance'] / 10 ** 8

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')

        if cg_response.status_code != 200:
            await ctx.reply(
                f"Failed to retrieve the current price of BTC. Error {cg_response.status_code}. Please try again later", delete_after=5)
            return

        usd_price = cg_response.json()['bitcoin']['usd']
        usd_balance = balance * usd_price
        usd_total_received = total_received * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        message = f"BTC Address: `{btcaddress}`\n"
        message += f"__Current BTC__ ~ **${usd_balance:.2f} USD**\n"
        message += f"__Total BTC Received__ ~ **${usd_total_received:.2f} USD**\n"
        message += f"__Unconfirmed BTC__ ~ **${usd_unconfirmed_balance:.2f} USD**"

        await ctx.reply(message, delete_after=30)
        
    @commands.command(name='getethbal', aliases=['ethbal'], brief="Shows User ETH Bal", usage=".getethbal <eth.addy>")
    @infected()
    async def getethbal(self, ctx, ethaddress: str = None):
        if ethaddress is None:
            await ctx.reply("Please provide an ETH address", delete_after=5)
            return

        if len(ethaddress) != 42:
            await ctx.reply("The provided ETH addy isnt valid", delete_after=5)
            return

        response = requests.get(f'https://api.blockcypher.com/v1/eth/main/addrs/{ethaddress}/balance')

        if response.status_code != 200:
            if response.status_code == 400:
                await ctx.reply("Invalid ETH Addy")
            else:
                await ctx.reply(f"Failed to retrieve balance. Error {response.status_code}. Please try again later", delete_after=5)
            return

        data = response.json()
        balance = int(data['balance']) / 10 ** 18
        total_received = int(data['total_received']) / 10 ** 18
        unconfirmed_balance = int(data['unconfirmed_balance']) / 10 ** 18

        cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')

        if cg_response.status_code != 200:
            await ctx.reply(
                f"Failed to retrieve the current price of ETH. Error {cg_response.status_code}. Please try again later", delete_after=5)
            return

        usd_price = cg_response.json()['ethereum']['usd']
        usd_balance = balance * usd_price
        usd_total_received = total_received * usd_price
        usd_unconfirmed_balance = unconfirmed_balance * usd_price

        message = f"ETH Address: `{ethaddress}`\n"
        message += f"__Current ETH__ ~ **${usd_balance:.2f} USD**\n"
        message += f"__Total ETH Received__ ~ **${usd_total_received:.2f} USD**\n"
        message += f"__Unconfirmed ETH__ ~ **${usd_unconfirmed_balance:.2f} USD**"

        await ctx.reply(message, delete_after=30)
        
    @commands.command(name='convert', aliases=['con'], brief="Convert cryptos", usage=".convert <amt> <from> <to>")
    @infected()
    async def convert(self, ctx, amount: float, _from: str, _to: str):
        if _from not in self.supported_currencies or _to not in self.supported_currencies:
            infection = await ctx.reply(f'~ Invalid crypto \n~ Supported currencies are \n~ ***{", ".join(self.supported_currencies.keys())}***')
            await asyncio.sleep(5)
            await infection.delete()  
            return

        _from_full = self.supported_currencies[_from]
        _to_full = self.supported_currencies[_to]

        coingecko_url = f'https://api.coingecko.com/api/v3/simple/price?ids={_from_full},{_to_full}&vs_currencies=usd'

        try:
            response = requests.get(coingecko_url).json()

            conversion_rate = response[_from_full]['usd'] / response[_to_full]['usd']
            converted_amount = amount * conversion_rate

            conversion_msg = await ctx.reply(f'{amount} {_from} = **__{converted_amount:.6f}__** {_to}', delete_after=5)
            
            await asyncio.sleep(30)  
            await conversion_msg.delete()  
            
        except Exception as e:
            
            await ctx.reply('Error occurred while converting', delete_after=5)
            await asyncio.sleep(5)  
            await ctx.message.delete()  
            print(e)
      
def setup(bot):
    bot.add_cog(Crypto(bot))
