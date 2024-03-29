import discord
from discord.ext import commands


class Information(commands.Cog, name="Information.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info', usage='info <mention>',
    description='Retrieve information about a user.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.top_role == member.guild.default_role:
            embed = discord.Embed(color=0xFFFFFF)
        else:
            embed = discord.Embed(color=member.color)

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name + "#" + member.discriminator, icon_url=member.avatar_url)
        embed.add_field(name="Account Creation Date", value=member.created_at.strftime('%d-%B %Y @ %I:%M %p'),
                        inline=False)
        embed.add_field(name="Server Join Date", value=member.joined_at.strftime('%d-%B %Y @ %I:%M %p'), inline=False)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=False)
        if not member.top_role == member.guild.default_role:
            embed.add_field(name=f"Top Role", value=member.top_role, inline=False)
        if member.bot:
            embed.set_footer(text="This user is a bot.")

        await ctx.message.reply(embed=embed, mention_author = False)

    @commands.command(name='avatar', aliases=["pfp"],
    usage='avatar <mention>',
    description='Gets the specified users avatar.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if member.top_role == member.guild.default_role:
            embed = discord.Embed(title="Avatar URL", url=str(member.avatar_url), color=0xc0d4ff)
        else:
            embed = discord.Embed(title="Avatar URL", url=str(member.avatar_url), color=member.color)

        embed.set_image(url=member.avatar_url_as(size=256))
        embed.set_author(name=member.display_name + "#" + member.discriminator, icon_url=member.avatar_url)
        
        if member.bot:
            embed.set_footer(text="This user is a bot.")

        await ctx.message.reply(embed=embed, mention_author = False)

    @avatar.error
    async def avatar_error(self, ctx, error):
        errormsg = await ctx.message.reply("Invalid user, usage: <avatar <username>", mention_author = False)
        await discord.Message.delete(errormsg, delay=5)

    @commands.command(name='members', usage='members',
    description='Displays an embed showing all members, humans, bots, and offline/offline users in the server.')
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def members(self, ctx):
        bots = 0
        online = 0
        offline = 0
        
        for member in ctx.author.guild.members:
            if member.bot:
                bots += 1
            if str(member.status) == "online" or str(member.status) == "idle" or str(member.status) == "dnd":
                online += 1
            if str(member.status) == "offline":
                offline += 1

        embed = discord.Embed(title=f"{ctx.author.guild}", description=None, color=0xc0d4ff)
        embed.add_field(name="All Members", value=ctx.author.guild.member_count, inline=True)
        embed.add_field(name="Humans", value=str(bots), inline=True)
        embed.add_field(name="Bots", value=ctx.author.guild.member_count - bots, inline=True)
        embed.add_field(name="Online", value=str(online), inline=True)
        embed.add_field(name="Offline", value=str(offline), inline=True)

        await ctx.message.reply(embed=embed, mention_author = False)

def setup(bot):
    bot.add_cog(Information(bot))
