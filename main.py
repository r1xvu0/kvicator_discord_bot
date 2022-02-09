import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from random import randint


load_dotenv()

# intents = discord.Intents().all()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')

@bot.command(name="kvic-help", help="Help menu")
async def print_help(ctx):
    await ctx.send(f"""
    !join: Joins your Voice Channel
    !leave: Leaves current Voice Channel
    !play: Play random Ludas sound
    !stop: Stops playing
    !pause: Pauses current sound
    !resume: Resumes and plays from where left off.
    """)

@bot.command(name='join', help="joins the audio channel")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel.".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name="leave", help="leave voice channel")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Bot is not connected to any channel.")

@bot.command(name="play", help="Play Ludas")
async def play(ctx):
    id = randint(1, 93)
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            voice_channel.play(discord.FFmpegPCMAudio(source='./ludas/' + str(id) + '.m4a'))
            # voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source='./ludas/' + str(id) + '.m4a'))
        await ctx.send('ID: {}'.format(id))
    except:
        await ctx.send("Bot is not connected to a voice channel.")

@bot.command(name="pause", help='Pauses the Bot')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("Bot is not playing anything atm.")

@bot.command(name="resume", help="Resumes the Bot")
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("Bot is not playing anything atm. Use !play")

@bot.command(name="stop", help="Stops the Bot")
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not running atm.")

bot.run(BOT_TOKEN)
