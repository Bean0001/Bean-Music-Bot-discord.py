import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import youtube_dl
import os

bot = commands.Bot(command_prefix='-')
status = cycle(['Currently being worked on!', 'Being programmed by Bean!', 'Not done yet!'])


@bot.event
async def on_ready():
    change_status.start()
    print('Bot is ready.')

# Music Code ---------------------------------------------------------------------------------


@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")
    
    @bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Paused")
        voice.pause()
        await ctx.send("Music Paused")
    else:
        print("Music not playing!")
        await ctx.send("Music not playing, failed to pause")

@bot.command(pass_context=True, aliases=['resm', 'r'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Music resumed playing")
        voice.resume()
        await ctx.send("Music resumed playing")
    else:
        print("Music is already playing!")
        await ctx.send("Music is already playing **:(**")

@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("Music not playing!")
        await ctx.send("Music not playing, failed to stop")

# Code After Music ----------------------------------------------------------------------------

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run('NzY5NjYxNzU5MDA2NzAzNjI1.X5SRXg.YfUqdKEz-B2_wQh99XTXgesBSEU')
