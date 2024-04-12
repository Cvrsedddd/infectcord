import discord
import json
from discord.ext import commands
from main import infected

class ARs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_responses = {}
        self.load_auto_responses()
        self.is_listing_responses = False

    def cog_unload(self):
        self.save_auto_responses()

    def load_auto_responses(self):
        try:
            with open("auto_responses.json", "r") as file:
                self.auto_responses = json.load(file)
        except FileNotFoundError:
            self.auto_responses = {}

    def save_auto_responses(self):
        with open("auto_responses.json", "w") as file:
            json.dump(self.auto_responses, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            return

        trigger = message.content.lower()

        if trigger in self.auto_responses:
            response = self.auto_responses[trigger]
            await message.channel.send(response)

    @commands.command(name='addar', aliases=['aa'], brief="Add auto response", usage=".addar <trigger> <response>")
    @infected()
    async def addar(self, ctx, trigger: str, *, response: str):
        trigger = trigger.lower()

        if trigger in self.auto_responses:
            await ctx.send("Auto response for this trigger already exists.")
            return

        self.auto_responses[trigger] = response
        self.save_auto_responses()

        await ctx.send("AR Added", delete_after=5)

    @commands.command(name='deletar', aliases=['ra', 'removear', 'delar'], brief="Remove auto response", usage=".removear <trigger>")
    @infected()
    async def removear(self, ctx, trigger: str):
        trigger = trigger.lower()

        if trigger not in self.auto_responses:
            await ctx.send("No AR Found", delete_after=5)
            return

        self.auto_responses.pop(trigger)
        self.save_auto_responses()

        await ctx.send("AR Deleted", delete_after=5)

    @commands.command(name='listar', aliases=['la'], brief="List all auto responses", usage=".listar")
    @infected()
    async def listauto(self, ctx):
        self.is_listing_responses = True
        response = "Auto Responses:\n\n"

        for trigger, response_text in self.auto_responses.items():
            response += f"**Trigger**: {trigger}\n"
            response += f"**Response**: `{response_text}`\n\n"

        await ctx.send(response, delete_after=5)
        self.is_listing_responses = False

def setup(bot):
    bot.add_cog(ARs(bot))