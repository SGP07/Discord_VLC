from typing import AsyncContextManager
import discord
from discord import channel
from discord import message
from discord.ext import commands
import vlc
import time
import re


print("Chargement...")
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

#enter your path here
source = "Paprika.mp4"

# creating vlc media player object
media_player = vlc.MediaPlayer()

# setting mrl to the media player
media_player.set_mrl(source)
  
# start playing video
media_player.play()
time.sleep(2)


#getting resolution
resolution = media_player.video_get_size()

# getting the duration of the video
duration = int(media_player.get_length())

# checking if it is playing
state = media_player.get_state()
paused = vlc.State.Paused
playing = vlc.State.Playing

#current movie time
current_time = media_player.get_time()
print(f"current time{current_time}")

#converting milliseconds to hours 
def convert(millis):
    millis = int(millis)
    millis_seconds=int((millis/1000)%60)
    millis_minutes=int((millis/(1000*60))%60)
    millis_hours=int((millis/(1000*60*60))%24)
    converted = "%d:%d:%d" % (millis_hours, millis_minutes, millis_seconds)
    return converted

#converting the duration of the media
converted_duration = convert(duration)

#getting the name of the media form the path
name = re.findall('(.+)\.[a-z0-9]+', source)
name = str(name)


#initiation of the bot
@bot.event
async def on_ready():
    print('Ready!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Anime'))
     
    channel = bot.get_channel(843133363334152192)
    emoji = '⏯'
    #message embed
    embedVar = discord.Embed(
        title="Informations sur le media :", description="", color=0x0193e9)
    embedVar.add_field(
        name="Titre : ", value=name, inline=False)
    embedVar.add_field(
        name="Durée ", value=str(converted_duration), inline=False)
    embedVar.add_field(
        name="Resolution : ", value=str(resolution), inline=False)
    
    message = await channel.send(embed=embedVar)
    await message.add_reaction(emoji)


@bot.event
async def on_raw_reaction_add(payload):
    #getting the emoji name and the channel 
    react_emoji = payload.emoji.name
    id_channel = payload.channel_id

    if react_emoji == '⏯' and id_channel == 843133363334152192 :
              
        if state == playing :
            media_player.pause()
            print('pause')
            
        elif state == paused : 
            media_player.play()
            print('play')
            
        else:
             print("error")

    else:
        print("Not the right react or channel")


@bot.event
async def on_raw_reaction_remove(payload):
    #getting the removed emoji name and the channel
    react_emoji = payload.emoji.name
    id_channel = payload.channel_id
    if react_emoji == '⏯' and id_channel == 843133363334152192 :

        if state == playing :
            media_player.pause()
            print('pause')
            
        elif state == paused : 
            media_player.play()
            print('play')
            
        else:
             print("error")

    else:
        print("Not the right react or the right channel")

#converting current time
converted_current_time = convert(current_time)

#converting time left
time_left = duration - current_time

converted_time_left = convert(time_left)



#command to get informations about the time
@bot.command()
async def uptime(ctx):
    embedVar = discord.Embed(
        title="", description="", color=0x0193e9)
    embedVar.add_field(
        name="Temps actuel : ", value=str(converted_current_time), inline=False)
    embedVar.add_field(
        name="Temps restant ", value=str(converted_time_left), inline=False)
    await ctx.send(embed=embedVar)
        


    
token = ""

#running the bot
bot.run(token)
