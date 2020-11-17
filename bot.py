# bot.py
import os
import re
import shitposter

import discord
from dotenv import load_dotenv
from discord.ext import commands

#load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID = os.getenv('DISCORD_USER_ID')
bot = commands.Bot(command_prefix='!')

NSFW_BOARDS = [
'h', 'd', 'gif', 'r9k'
]




@bot.event
async def on_ready():
    if not os.path.isdir( './data' ):
        os.mkdir( './data' )

    servers = bot.fetch_guilds()
    async for server in servers:
        print(f'connected to {server.name}\n')
 
@bot.command(name='shitpost', help='Generates shitposts from a 4chan board: "!shitpost /b/"')
async def shitpost(ctx, board):

    cleansed_board = board.replace( '/', '' )

    if ctx.channel.is_nsfw() is False:
        if cleansed_board in NSFW_BOARDS:
            await ctx.send('Shitposts from nsfw boards can only be posted in nsfw channels, sorry!')
            return


    
    if shitposter.board_loaded(cleansed_board) is False:
        message = f'No data loaded for {board}, please use !load {board}'
    else:
        print(f'generating shitpost from {board}')
        mc, images = shitposter.load_or_train_board(cleansed_board)
        image = shitposter.grab_image(images, cleansed_board)
        shitpost = mc.generateString()
        message = f'{shitpost}\n{image}'

    await ctx.send(message)


@bot.command(name='load', help='Loads a board, only Zoyd can use this command.')
async def load(ctx, board):

    cleansed_board = board.replace( '/', '' )
    
    if ctx.author.id == int(USER_ID):
        await ctx.send(f'Loading posts for {board}, bare with a few minutes...')
        mc, images = shitposter.load_or_train_board(cleansed_board)
        await ctx.send(f'/{cleansed_board}/ loaded')
    else:
        await ctx.send(f'Only Zoyd can load boards, ask him if you want a particular board :~)')


@bot.command(name='refresh', help='Refreshes data for a board, only Zoyd can use this command.')
async def refresh(ctx, board):

    cleansed_board = board.replace( '/', '' )
    
    if ctx.author.id == int(USER_ID):
        await ctx.send(f'Refreshing posts for {board}, bare with a few minutes...')
        _, _ = shitposter.refresh_board(cleansed_board)
        await ctx.send(f'/{cleansed_board}/ data refreshed')
    else:
        await ctx.send(f'Only Zoyd can load boards, ask him if you want a particular board :~)')


@bot.command(name='everything', help='Refreshes data for all boards, used very rarely.')
async def refresh_all_boards(ctx):
    
    if ctx.author.id == int(USER_ID):
        await ctx.send(f'Refreshing all loaded boards, this will take a while.')

        loaded_boards = shitposter.reload_all_boards(ctx)
        boards = '/, /'.join(loaded_boards)

        await ctx.send(f'Data refreshed for boards: /{boards}/')
    else:
        await ctx.send(f'Yeah there\'s no way you\'re allowed to use this command pal')
    

@bot.command(name='image', help='Posts a random image from a 4chan board: "!image /c/"')
async def image(ctx, board):
    cleansed_board = board.replace( '/', '' )

    if ctx.channel.is_nsfw() is False:
        if cleansed_board in NSFW_BOARDS:
            await ctx.send('No lewds in this channel!!!')
            return

    if shitposter.board_loaded(cleansed_board) is False:
        message = f'No data loaded for /{cleansed_board}/, please use !load /{board}/'
    else:
        print(f'generating shitpost from {board}')
        mc, images = shitposter.load_or_train_board(cleansed_board)
        image = shitposter.grab_image(images, cleansed_board)
        message = f'{image}'

    await ctx.send(message)


@bot.command(name='boards', help='Lists the loaded boards!')
async def boards(ctx):
    loaded_boards = shitposter.loaded_boards()

    boards = '/, /'.join(loaded_boards)

    await ctx.send(f'I have the following boards loaded!: /{boards}/')


bot.run(TOKEN)
