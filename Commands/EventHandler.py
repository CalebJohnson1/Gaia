import asyncio
import math
import random
import re
import time

import discord
from discord.ext import commands

class EventHandler(commands.Cog, name="EventHandler.py"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='startevent', aliases=["event"],
    usage='startevent',
    description='Interactively set up a timed event of your choice within a server.')
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def startevent(self, ctx):
        msgchannel = ctx.message.channel
        typeoptions = ["custom", "invite", "message"]
        invitedescription = "Invite users and gain rewards!\n\nInvites you must reach to gain rewards:\n:diamond_shape_with_a_dot_inside:1 Invite\n:diamond_shape_with_a_dot_inside:2 Invites\n:diamond_shape_with_a_dot_inside:3 Invites\n:diamond_shape_with_a_dot_inside:4 Invites\n:diamond_shape_with_a_dot_inside:5 Invites"

        def check(m):
            return m.author == ctx.author and m.channel == msgchannel

        description = "No Description"
    
        try:
            await ctx.message.reply("What type of event would you like?\n**Options: custom, message, invite**\nType **cancel** anytime to cancel event creation process.", mention_author = False)
            event = await self.bot.wait_for('message', check=check, timeout=120)

            if event.content.lower() == "cancel":
                await ctx.message.reply("Event creation cancelled", mention_author = False)
                return

            # Custom event
            if event.content.lower() in typeoptions[0]:
                await ctx.message.reply(f"Alright, what would you like the event to be?", mention_author = False)
                event = await self.bot.wait_for('message', check=check, timeout=120)

                if event.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                await ctx.message.reply(f"An {event.content.lower()} event, neat!\nWhat channel do you want the event in?\n**Type in the name of a channel in this server.**", mention_author = False)
                channelname = await self.bot.wait_for('message', check=check, timeout=120)

                if channelname.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                for channels in ctx.author.guild.channels:
                    if channelname.content in channels.name:
                        channel = channels

                await ctx.message.reply(f"Great! The {event.content} event will be in {channel.mention}!\nPlease enter what you'd like the description to be (this will be the information about the event)", mention_author = False)

                descmsg = await self.bot.wait_for('message', check=check, timeout=120)

                if descmsg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                description = f"**{descmsg.content}**"
                embed = discord.Embed(title=f"Event: {event.content}", description = description, color=0xc0d4ff)

                await ctx.message.reply("Now, how long would you like this event to last? You can input durations such as ***60s***, ***60m***, ***1h***, and ***1d***!\nYou can choose your own time, and only input one increment of time or it will not work.", mention_author = False)
                timemsg = await self.bot.wait_for('message', check=check, timeout=120)

                if timemsg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                timeamount = int(re.search(r'\d+', timemsg.content).group())
                
                if "h" in timemsg.content.lower():
                    timeamount = timeamount*3600
                elif "m" in timemsg.content.lower():
                    timeamount = timeamount*60
                elif "s" in timemsg.content.lower():
                    timeamount = timeamount
                elif "d" in timemsg.content.lower():
                    timeamount = timeamount*86400

                days = math.floor(timeamount/86400)

                if days >= 2:
                    footer = f"Event ends in: {time.strftime(f'{days} days', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** days', time.gmtime(timeamount))}"
                elif days == 1:
                    footer = f"Event ends in: {time.strftime(f'{days} day', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** day', time.gmtime(timeamount))}"
                elif timeamount >= 7200 and timeamount < 86400:
                    footer = f"Event ends in: {time.strftime('%#H hours, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hours and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3660 and timeamount < 7200:
                    footer = f"Event ends in: {time.strftime('%#H hour, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3600 and timeamount < 3660:
                    footer = f"Event ends in: {time.strftime('%#H hour', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour', time.gmtime(timeamount))}"
                elif timeamount >= 120 and timeamount < 3600:
                    footer = f"Event ends in: {time.strftime('%#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 60 and timeamount < 120:
                    footer = f"Event ends in: {time.strftime('%#M minute', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minute', time.gmtime(timeamount))}"
                else:
                    footer = f"Event ends in: {time.strftime('%#S seconds', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#S** seconds', time.gmtime(timeamount))}"

                await ctx.message.reply(sendmsg, mention_author = False)
                embed.set_footer(text=footer)

                await ctx.message.reply("Now, how many winners will there be?", mention_author = False)
                winners = await self.bot.wait_for('message', check=check, timeout=120)
                if winners.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                winners = int(re.search(r'\d+', winners.content).group())

                embed.add_field(name="Winners", value=f"**{winners}**")

                if winners == 1:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winner! Now, what would you like the reward(s) to be?", mention_author = False)
                else:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winners! Now, what would you like the reward(s) to be?", mention_author = False)
                
                reward = await self.bot.wait_for('message', check=check, timeout=120)

                if reward.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                embed.add_field(name=":gift: Rewards", value=f"**{reward.content}**", inline=False)

                await ctx.message.reply("And finally, would you like to ping a role? (y/n)", mention_author = False)
                ping = await self.bot.wait_for('message', check=check, timeout=120)

                if ping.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                if ping.content.lower() == "y" or ping.content.lower() == "yes":
                    await ctx.message.reply("Sounds good, what role would you like to ping? (case sensitive)", mention_author = False)
                    rolename = await self.bot.wait_for('message', check=check, timeout=120)

                    if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                    role = discord.utils.get(ctx.guild.roles, name=rolename.content)
                    while not role in ctx.author.guild.roles:
                        await ctx.message.reply("This role doesn't exist! (remember it's case sensitive)\nPlease choose a different role.", mention_author = False)
                        rolename = await self.bot.wait_for('message', check=check, timeout=120)

                        if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                        role = discord.utils.get(ctx.guild.roles, name=rolename.content)

                    embed.add_field(name="Ping", value=role.mention, inline=True)

                elif ping.content.lower() == "n" or ping.content.lower() == "no":
                    await ctx.message.reply("Alright, no role will be pinged!", mention_author = False)

            # Invite event
            elif event.content.lower() in typeoptions[1]:
                await ctx.message.reply(f"An {event.content.lower()} event, neat!\nFirst, what channel do you want the event in?\n**Type in the name of a channel in this server.**", mention_author = False)
                channelname = await self.bot.wait_for('message', check=check, timeout=120)

                if channelname.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                for channels in ctx.author.guild.channels:
                    if channelname.content in channels.name:
                        channel = channels

                await ctx.message.reply(f"Great! The {event.content} event will be in {channel.mention}!\nWould you like an auto-generated description? (y/n)\nThis will generate a random invite event description.", mention_author = False)
                msg = await self.bot.wait_for('message', check=check, timeout=120)

                if msg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                if msg.content.lower() == "y" or msg.content.lower() ==  "yes":
                    description = f"**{invitedescription}**"

                if msg.content.lower() == "n" or msg.content.lower() == "no":
                    await ctx.message.reply("Ok, what would you like the description to be? (this will be the information about the event)", mention_author = False)
                    msg = await self.bot.wait_for('message', check=check, timeout=120)

                    if msg.content.lower() == "cancel":
                        await ctx.message.reply("Event creation cancelled", mention_author = False)
                        return

                    description = f"**{msg.content}**"

                embed = discord.Embed(title=f"Invite Event", description = description, color=0xc0d4ff)

                await ctx.message.reply("Now, how long would you like this event to last? You can input durations such as ***60s***, ***60m***, ***1h***, and ***1d***!\nYou can choose your own time, and only input one increment of time or it will not work.", mention_author = False)
                timemsg = await self.bot.wait_for('message', check=check, timeout=120)

                if timemsg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                timeamount = int(re.search(r'\d+', timemsg.content).group())

                if "h" in timemsg.content.lower():
                    timeamount = timeamount*3600
                elif "m" in timemsg.content.lower():
                    timeamount = timeamount*60
                elif "s" in timemsg.content.lower():
                    timeamount = timeamount
                elif "d" in timemsg.content.lower():
                    timeamount = timeamount*86400

                days = math.floor(timeamount/86400)

                if days >= 2:
                    footer = f"Event ends in: {time.strftime(f'{days} days', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** days', time.gmtime(timeamount))}"
                elif days == 1:
                    footer = f"Event ends in: {time.strftime(f'{days} day', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** day', time.gmtime(timeamount))}"
                elif timeamount >= 7200 and timeamount < 86400:
                    footer = f"Event ends in: {time.strftime('%#H hours, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hours and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3660 and timeamount < 7200:
                    footer = f"Event ends in: {time.strftime('%#H hour, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3600 and timeamount < 3660:
                    footer = f"Event ends in: {time.strftime('%#H hour', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour', time.gmtime(timeamount))}"
                elif timeamount >= 120 and timeamount < 3600:
                    footer = f"Event ends in: {time.strftime('%#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 60 and timeamount < 120:
                    footer = f"Event ends in: {time.strftime('%#M minute', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minute', time.gmtime(timeamount))}"
                else:
                    footer = f"Event ends in: {time.strftime('%#S seconds', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#S** seconds', time.gmtime(timeamount))}"

                await ctx.message.reply(sendmsg, mention_author = False)
                embed.set_footer(text=footer)

                await ctx.message.reply("Now, how many winners will there be?", mention_author = False)
                winners = await self.bot.wait_for('message', check=check, timeout=120)
                if winners.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                winners = int(re.search(r'\d+', winners.content).group())

                embed.add_field(name="Winners", value=f"**{winners}**")

                if winners == 1:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winner! Now, what would you like the reward(s) to be?", mention_author = False)
                else:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winners! Now, what would you like the reward(s) to be?", mention_author = False)

                reward = await self.bot.wait_for('message', check=check, timeout=120)

                if reward.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return
                    
                embed.add_field(name=":gift: Rewards", value=f"**{reward.content}**", inline=False)

                await ctx.message.reply("And finally, would you like to ping a role? (y/n)", mention_author = False)
                ping = await self.bot.wait_for('message', check=check, timeout=120)

                if ping.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                if ping.content.lower() == "y" or ping.content.lower() == "yes":
                    await ctx.message.reply("Sounds good, what role would you like to ping? (case sensitive)", mention_author = False)
                    rolename = await self.bot.wait_for('message', check=check, timeout=120)

                    if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                    role = discord.utils.get(ctx.guild.roles, name=rolename.content)
                    while not role in ctx.author.guild.roles:
                        await ctx.message.reply("This role doesn't exist! (remember it's case sensitive)\nPlease choose a different role.", mention_author = False)
                        rolename = await self.bot.wait_for('message', check=check, timeout=120)

                        if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                        role = discord.utils.get(ctx.guild.roles, name=rolename.content)

                    embed.add_field(name="Ping", value=role.mention, inline=True)

                elif ping.content.lower() == "n" or ping.content.lower() == "no":
                    await ctx.message.reply("Alright, no role will be pinged!", mention_author = False)

            # Message event
            elif event.content.lower() in typeoptions[2]:
                await ctx.message.reply(f"A {event.content.lower()} event, neat!\nWhat channel do you want the event in?\n**Type in the name of a channel in this server.**", mention_author = False)
                channelname = await self.bot.wait_for('message', check=check, timeout=120)

                if channelname.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                for channels in ctx.author.guild.channels:
                    if channelname.content in channels.name:
                        channel = channels

                await ctx.message.reply(f"Great! The {event.content} event will be in {channel.mention}!\nWould you like an auto-generated description? (y/n)\nThis will generate a random message event description.", mention_author = False)
                msg = await self.bot.wait_for('message', check=check, timeout=120)

                if msg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                if msg.content.lower() == "y" or msg.content.lower() ==  "yes":
                    description = f"**Send a message 10 minutes before another one is sent. Last one to send a message wins!**"

                if msg.content.lower() == "n" or msg.content.lower() == "no":
                    await ctx.message.reply("Ok, what would you like the description to be? (this will be the information about the event)", mention_author = False)
                    msg = await self.bot.wait_for('message', check=check, timeout=120)

                    if msg.content.lower() == "cancel":
                        await ctx.message.reply("Event creation cancelled", mention_author = False)
                        return

                    description = f"**{msg.content}**"

                embed = discord.Embed(title=f"Message Event", description = description, color=0xc0d4ff)

                await ctx.message.reply("Now, how long would you like this event to last? You can input durations such as ***60s***, ***60m***, ***1h***, and ***1d***!\nYou can choose your own time, and only input one increment of time or it will not work.", mention_author = False)
                timemsg = await self.bot.wait_for('message', check=check, timeout=120)

                if timemsg.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                timeamount = int(re.search(r'\d+', timemsg.content).group())

                if "h" in timemsg.content.lower():
                    timeamount = timeamount*3600
                elif "m" in timemsg.content.lower():
                    timeamount = timeamount*60
                elif "s" in timemsg.content.lower():
                    timeamount = timeamount
                elif "d" in timemsg.content.lower():
                    timeamount = timeamount*86400

                days = math.floor(timeamount/86400)

                if days >= 2:
                    footer = f"Event ends in: {time.strftime(f'{days} days', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** days', time.gmtime(timeamount))}"
                elif days == 1:
                    footer = f"Event ends in: {time.strftime(f'{days} day', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime(f'**{days}** day', time.gmtime(timeamount))}"
                elif timeamount >= 7200 and timeamount < 86400:
                    footer = f"Event ends in: {time.strftime('%#H hours, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hours and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3660 and timeamount < 7200:
                    footer = f"Event ends in: {time.strftime('%#H hour, %#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour and **%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3600 and timeamount < 3660:
                    footer = f"Event ends in: {time.strftime('%#H hour', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#H** hour', time.gmtime(timeamount))}"
                elif timeamount >= 120 and timeamount < 3600:
                    footer = f"Event ends in: {time.strftime('%#M minutes', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minutes', time.gmtime(timeamount))}"
                elif timeamount >= 60 and timeamount < 120:
                    footer = f"Event ends in: {time.strftime('%#M minute', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#M** minute', time.gmtime(timeamount))}"
                else:
                    footer = f"Event ends in: {time.strftime('%#S seconds', time.gmtime(timeamount))}"
                    sendmsg = f"Alright! The event will last for {time.strftime('**%#S** seconds', time.gmtime(timeamount))}"

                await ctx.message.reply(sendmsg, mention_author = False)
                embed.set_footer(text=footer)

                await ctx.message.reply("Now, how many winners will there be?", mention_author = False)
                winners = await self.bot.wait_for('message', check=check, timeout=120)
                if winners.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                winners = int(re.search(r'\d+', winners.content).group())

                embed.add_field(name="Winners", value=f"**{winners}**")

                if winners == 1:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winner! Now, what would you like the reward(s) to be?", mention_author = False)
                else:
                    await ctx.message.reply(f"Alright, there will be **{winners}** winners! Now, what would you like the reward(s) to be?", mention_author = False)

                reward = await self.bot.wait_for('message', check=check, timeout=120)

                if reward.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                embed.add_field(name=":gift: Rewards", value=f"**{reward.content}**", inline=False)

                await ctx.message.reply("And finally, would you like to ping a role? (y/n)", mention_author = False)
                ping = await self.bot.wait_for('message', check=check, timeout=120)

                if ping.content.lower() == "cancel":
                    await ctx.message.reply("Event creation cancelled", mention_author = False)
                    return

                if ping.content.lower() == "y" or ping.content.lower() == "yes":
                    await ctx.message.reply("Sounds good, what role would you like to ping? (case sensitive)", mention_author = False)
                    rolename = await self.bot.wait_for('message', check=check, timeout=120)
                    
                    if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                    role = discord.utils.get(ctx.guild.roles, name=rolename.content)
                    while not role in ctx.author.guild.roles:
                        await ctx.message.reply("This role doesn't exist! (remember it's case sensitive)\nPlease choose a different role.", mention_author = False)
                        rolename = await self.bot.wait_for('message', check=check, timeout=120)

                        if rolename.content.lower() == "cancel":
                            await ctx.message.reply("Event creation cancelled", mention_author = False)
                            return

                        role = discord.utils.get(ctx.guild.roles, name=rolename.content)

                    embed.add_field(name="Ping", value=role.mention, inline=True)

                elif ping.content.lower() == "n" or ping.content.lower() == "no":
                    await ctx.message.reply("Alright, no role will be pinged!", mention_author = False)

            else:
                await ctx.message.reply("Error: Not a valid choice.", mention_author = False)

            msg = await channel.send(embed=embed)

            while timeamount > 30:
                await asyncio.sleep(30)
                timeamount -= 30
                days = math.floor(timeamount/86400)

                if days >= 2:
                    footer = f"Event ends in: {time.strftime(f'{days} days', time.gmtime(timeamount))}"
                elif days == 1:
                    footer = f"Event ends in: {time.strftime(f'{days} day', time.gmtime(timeamount))}"
                elif timeamount >= 7200 and timeamount < 86400:
                    footer = f"Event ends in: {time.strftime('%#H hours, %#M minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3660 and timeamount < 7200:
                    footer = f"Event ends in: {time.strftime('%#H hour, %#M minutes', time.gmtime(timeamount))}"
                elif timeamount >= 3600 and timeamount < 3660:
                    footer = f"Event ends in: {time.strftime('%#H hour', time.gmtime(timeamount))}"
                elif timeamount >= 120 and timeamount < 3600:
                    footer = f"Event ends in: {time.strftime('%#M minutes', time.gmtime(timeamount))}"
                elif timeamount >= 60 and timeamount < 120:
                    footer = f"Event ends in: {time.strftime('%#M minute', time.gmtime(timeamount))}"
                else:
                    footer = f"Event ends in: {time.strftime('%#S seconds', time.gmtime(timeamount))}"

                embed.set_footer(text=footer)
                await discord.Message.edit(msg, embed=embed)

            await asyncio.sleep(timeamount)
            embed.set_footer(text="Event Ended")
            await discord.Message.edit(msg, embed=embed)
            await channel.send(f"The **{event.content}** event has ended.")

        except asyncio.TimeoutError:
            await ctx.message.reply("You took too long to respond **(2 minutes)**. Event creation cancelled.", mention_author = False)
        except ValueError:
            await ctx.message.reply("Seems like you've gave me a wrong value!", mention_author = False)
        except discord.NotFound:
            await ctx.message.reply(f"Uh oh! It looks like the event message was deleted, the **{event.content}** event has been cancelled.", mention_author = False)
        except ConnectionResetError:
            await ctx.message.reply(f"Connection has been lost, {event.content} event has been removed", mention_author = False)
            await discord.Message.delete(msg, delay=0)

    @startevent.error
    async def startevent_error(self, ctx, error):
        await ctx.send(error)
        
def setup(bot):
    bot.add_cog(EventHandler(bot))
