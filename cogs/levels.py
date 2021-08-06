import discord
from discord.ext import commands
from pymongo import MongoClient
import datetime
from discord.ext.commands.cooldowns import BucketType

general = [663234840530780173]

bot_channel = [663234840530780173]

level = ["Level 1", "Level 2", "Level 3"]
levelnum = [5, 10, 15]

cluster = MongoClient(
   "mongodb://127.0.0.1:27017/praetoria")


db = cluster.experience
accountXP = db.accountExperience
guildXP = db.guildExperience


class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        # Retry_After Prevents spamming to earn score.
        if retry_after:
            return
        else:
            if message.channel.id in general:
                stats = accountXP.find_one({"_id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"_id": message.author.id, "xp": 100}
                    accountXP.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    accountXP.update_one({"_id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                            break
                        lvl += 1
                    xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
                    if xp == 0:
                        await message.channel.send(
                            f"well done {message.author.mention}! You leveled up to **level: {lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(
                                    description=f"{message.author.mention} you have gotten role **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(2.0, 60.0, commands.BucketType.user)
    async def rank(self, ctx):
        print('0')
        stats = accountXP.find_one({"id": ctx.author.id})
        if stats is None:
            print('2')
            embed = discord.Embed(description="You haven't sent any messages, no rank!!!")
            await ctx.channel.send(embed=embed)
        else:
            print('3')
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                    break
                lvl += 1
                xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
                rankings = accountXP.find().sort("xp", -1)
                print('4')
            for x in rankings:
                rank += 1
                print('5')
                if stats["id"] == x["id"]:
                    print('6a')
                    break
                    print('6b')
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                print('6c')
                embed.set_thumbnail(url=ctx.author.avatar_url)
                print('6d')
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        if (ctx.channel.id == bot_channel):
            rankings = accountXP.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Rankings:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(LevelSys(client))