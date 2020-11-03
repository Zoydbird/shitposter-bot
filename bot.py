# bot.py
import os
import shitposter

import discord
from dotenv import load_dotenv
from discord.ext import commands

#load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

NSFW_BOARDS = [
'h', 'd', 'gif'
]




@bot.event
async def on_ready():
    if not os.path.isdir( './data' ):
        os.mkdir( './data' )

    servers = bot.fetch_guilds()
    async for server in servers:
        print(f'connected to {server.name}\n')

 
@bot.command(name='shitpost', help='Generates shitposts from a 4chan board: Example use: "!shitpost /b/')
async def shitpost(ctx, board):

    cleansed_board = board.replace( '/', '' )

    if ctx.channel.is_nsfw() is False:
        if cleansed_board in NSFW_BOARDS:
            await ctx.send('No lewds in this channel!!!')
            return


    
    if shitposter.board_loaded(cleansed_board) is False:
        message = f'No data loaded for {board}, please use !load{board}'
    else:
        print(f'generating shitpost from {board}')
        mc, images = shitposter.load_or_train_board(cleansed_board)
        image = shitposter.grab_image(images, cleansed_board)
        shitpost = mc.generateString()
        message = f'{shitpost}\n{image}'

    await ctx.send(message)

    

# @bot.command(name='boards', help='Lists the loaded boards!')
# async def boards(ctx):


bot.run(TOKEN)
