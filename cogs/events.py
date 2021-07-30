import random
import datetime
import time

import discord 
from discord import Embed
from discord.ext import commands


# In cogs we make our own class
# for d.py which subclasses commands.Cog


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # On member joins we find a channel called general and if it exists,
        # send an embed welcoming them to our guild
        # Repeated to handle various discord account ages, applies visual differences in the join log embed.
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        if time.time() - member.created_at.timestamp() < 2592000:
            if channel:
                embed = discord.Embed(
                    description=f"{member.mention} ( {member.name} )\nNewAccUserID: {member.id}\nCreated: {member.created_at}",
                    color=random.choice(self.bot.color_list),
                )
                embed.set_thumbnail(url=member.avatar_url)
                embed.title=f"{member.display_name} Age:🛑",
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
                embed.timestamp = datetime.datetime.utcnow()

                await channel.send(embed=embed) 
        else:
            if channel:
                embed = discord.Embed(
                description=f"{member.mention} ( {member.name} )\nAccountUserID: {member.id}\nCreated: {member.created_at}",
                color=random.choice(self.bot.color_list),
            )
            embed.title=f"{member.display_name} Age:✅",
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()          
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # On member remove we find a channel called general and if it exists,
        # send an embed saying goodbye from our guild-
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        if channel:
            embed = discord.Embed(
                description="Goodbye from all of us..",
                color=random.choice(self.bot.color_list),
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title=":page_facing_up: Username Change",
                          colour=9807270,
                          timestamp=datetime.datetime.utcnow())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            self.log_channel = self.bot.get_channel(798324364301959169)
            await self.log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(description=f":page_facing_up: {after.mention} **ID ( {after.id} )**",
                          colour=612934,
                          timestamp=datetime.datetime.utcnow())

            embed.set_author(
                name=f"Nickname Updated", icon_url=f"{after.avatar_url}")

            namemessage = before.display_name + " :arrow_right:  " + after.name

            fields = [
                ("New Name ", namemessage, False)]
            # , ("Joined", after.JoinedAt, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        elif before.roles != after.roles:

            before_set = set(before.roles)
            after_set = set(after.roles)

            difference = set(before.roles)-set(after.roles)

            isEmpty = (len(difference) == {})
            print(difference)

            if not isEmpty:
                embed = discord.Embed(title="Role Update",
                              description=f"{after.mention} ~ {after.name}",
                              colour=9807270,
                              timestamp=datetime.datetime.utcnow())

                fields = [("Removed", ", ".join(
                    [r.mention for r in difference]), False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                    embed.set_footer(text=f"ID: {after.id}")

            else:

                embed = discord.Embed(title="Role Updates",
                              colour=9807270,
                              timestamp=datetime.datetime.utcnow())

                fields = [("Added", ", ".join(
                    [r.mention for r in difference]), False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

            self.log_channel = self.bot.get_channel(798324364301959169)
            await self.log_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content and not before.author.bot:
            acontent_clamp = after.content
            bcontent_clamp = before.content
            embed = discord.Embed(description=f":page_facing_up: {after.author.mention} **ID (**{after.author.id}**)**",
                          colour=0xFFE4AF,
                          timestamp=datetime.datetime.utcnow())

            fields = [("Before", bcontent_clamp[:750], False),
                      ("After", acontent_clamp[:750], False)]

            embed.set_author(
                name=f"Edited By {after.author.name}", icon_url=f"{after.author.avatar_url}")
           # embed.set_footer(text=f"Message ID {before.author.message.id}")

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            self.log_channel = self.bot.get_channel(798324364301959169)
            await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            msg_clamp = message.content
            embed = discord.Embed(description=f":warning: {message.author.mention} **ID (*{message.author.id}*)**",
                          colour=15158332,
                          footer=f"UserID {message.author.id}.",
                          timestamp=datetime.datetime.utcnow())
            embed.set_author(
                name=f"Deletion By {message.author.name}", icon_url=f"{message.author.avatar_url}")
            embed.set_footer(text=f"Deleted Message ID = {message.id}")
            fields = [("Message Content", msg_clamp[:950], False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            
        self.log_channel = self.bot.get_channel(798324364301959169)
        await self.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f" You must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f" You must wait {int(m)} minutes and {int(s)} seconds to use this command!"
                )
            else:
                await ctx.send(
                    f" You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!"
                )
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        # Implement further custom checks for errors here...
        raise error


def setup(bot):
    bot.add_cog(Events(bot))
