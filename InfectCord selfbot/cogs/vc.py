import discord
from discord.ext import commands
from decouple import config
from discord.ext.commands import has_permissions, CheckFailure
from main import infected

class Vc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = {}
        self.channel_id = None
    
    async def check_permissions(self, ctx, member: discord.Member):
        if not ctx.author.guild_permissions.move_members:
            await ctx.send(f"I dont have perms")
            return False
        return True

    @commands.command(name='vc247', aliases=['247'], brief="24/7 a vc", usage=".vc247 <vc.channel.id>")
    @infected()
    async def vc247(self, ctx, channel_id: int = None):
        await ctx.message.delete()
        if channel_id is not None:
            self.channel_id = channel_id
            channel = self.bot.get_channel(channel_id)
            if isinstance(channel, discord.VoiceChannel):
                self.vc[ctx.guild.id] = await channel.connect()
            else:
                await ctx.send("This is not a valid voice channel ID.")
        elif self.vc.get(ctx.guild.id):
            await self.vc[ctx.guild.id].disconnect()
            del self.vc[ctx.guild.id]
            self.channel_id = None

    @commands.command(name='vckick', aliases=['vkick'], brief="Kicks vc user", usage=".vckick <mention.user>")
    @infected()
    async def vckick(self, ctx, user: discord.Member):
        await ctx.message.delete()
        if await self.check_permissions(ctx, user):
            if user.voice and user.voice.channel:
                await user.move_to(None)

    @commands.command(name='vcmoveall', aliases=['moveall'], brief="Moves all users to another vc", usage=".vcmoveall <from.channel.id> <to.channel.id>")
    @infected()
    async def vcmoveall(self, ctx, channel1_id: int, channel2_id: int):
        await ctx.message.delete()
        channel1 = self.bot.get_channel(channel1_id)
        channel2 = self.bot.get_channel(channel2_id)
        if isinstance(channel1, discord.VoiceChannel) and isinstance(channel2, discord.VoiceChannel):
            members = channel1.members
            for member in members:
                if await self.check_permissions(ctx, member):
                    await member.move_to(channel2)

    @commands.command(name='vcmute', aliases=['stfu'], brief="Mutes a vc user", usage=".vcmute <mention.user>")
    @infected()
    async def vcmute(self, ctx, user: discord.Member):
        await ctx.message.delete()
        if await self.check_permissions(ctx, user):
            if user.voice and user.voice.channel:
                await user.edit(mute=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.vc.get(member.guild.id) is not None:
            if member.id == config['userid']  and before.channel is not None and after.channel is None:
                channel = self.bot.get_channel(self.channel_id)
                if channel is not None:
                    self.vc[member.guild.id] = await channel.connect()

def setup(bot):
    bot.add_cog(Vc(bot))