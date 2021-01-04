import discord
import json
import datetime
import asyncio

dClient = discord.Client()

# Load config
config = {}
with open("config.json", "r") as f:
    config = json.loads(f.read())

async def statusTask():
    while True:
        for status in config["statuses"]:
            if status["type"] == "game":
                await dClient.change_presence(activity=discord.Game(name=status["name"], start=datetime.datetime.now()-datetime.timedelta(status["duration"]), end=datetime.datetime.now()))
            if status["type"] == "stream":
                await dClient.change_presence(activity=discord.Streaming(name=status["name"], platform="YouTube", url=status["url"]))
            if status["type"] == "competing":
                await dClient.change_presence(activity=discord.Activity(name=status["name"], type=5, details=status["description"]))
            if status["type"] == "watching":
                await dClient.change_presence(activity=discord.Activity(name=status["name"], type=3, details=status["description"]))
            await asyncio.sleep(status["delay"])

@dClient.event
async def on_message(message : discord.message):
    if message.author == dClient.user:
        if message.content.startswith(config["config"]["prefix"]):
            command = message.content[1:].split(" ")[0].lower()
            args = message.content[len(message.content.split(" ")[0])+1:]
            
            if command == "showchannels":
                guild = dClient.get_guild(int(args))
                embed=discord.Embed(title=" ", color=int(config["embeds"]["success color"], 0))
                embed.set_author(name=f"Channels in {guild.name}", icon_url=guild.icon_url)
                embed.set_footer(text=config["embeds"]["footer"])
                for channel in guild.text_channels:
                    try:
                        await channel.history(limit=1).next()
                        embed.add_field(name=channel.name, value=":keyboard:", inline=False)
                    except discord.NoMoreItems:
                        embed.add_field(name=channel.name, value=":keyboard:", inline=False)
                    except:
                        embed.add_field(name=channel.name, value=":keyboard: :no_entry_sign:", inline=False)
                for channel in guild.voice_channels:
                    embed.add_field(name=channel.name, value=":speaker:", inline=False)
                await message.channel.send("", embed=embed)
            
            await message.delete()


@dClient.event
async def on_ready():
    print(f"logged in as {dClient.user} and changing status!")
    dClient.loop.create_task(statusTask())

dClient.run(config["config"]["token"], bot=False)