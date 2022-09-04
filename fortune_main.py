from multiprocessing import parent_process
from typing import ParamSpecArgs
import discord
from subprocess import getoutput
from random import randrange
from PIL import Image, ImageDraw, ImageFont
from math import ceil
from discord.ext.commands import Bot
import random
import os
from dotenv import load_dotenv
load_dotenv("token.env")
client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print('Fortune Bot has logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # v cowsay fortunes
    if (message.content.startswith('!fortune')):
        # Choose a random cow type from the list of all cowsay characters
        # Remove the non-animal characters
        cowTypes = getoutput('cowsay -l')[37:]
        cowTypes = cowTypes.split()  # split into cowsay animals
        typechoice = cowTypes[randrange(0, len(cowTypes), 1)]
        # Use our choice to generate a cowsay
        msg = getoutput('fortune | cowsay -f {}'.format(typechoice))

        # Image generation: calculate length and width of image and instantiate
        msgFont = ImageFont.truetype("UbuntuMono-R.ttf", 12)
        msgDim = msgFont.getsize_multiline(msg)

        msgImg = Image.new('RGB', (ceil(
            msgDim[0] + 0.1*msgDim[0]), ceil(msgDim[1] + 0.1*msgDim[1])), (54, 57, 62, 0))
        msgDraw = ImageDraw.Draw(msgImg)
        msgDraw.text((16, 0), msg, fill=(255, 255, 255, 255), font=msgFont)
        msgImg.save('/tmp/fortune.png')
        embed=discord.Embed(title='The Oracle Says:', color=discord.Color.random())
        file = discord.File('/tmp/fortune.png', filename='fortune.png')
        embed.set_image(url="attachment://fortune.png")
        await message.channel.send(embed=embed, file=file)
    # v coin flipper
    if (message.content.startswith('!flip')):
        flip_range = randrange(0,2)
        if flip_range == 0:
            flip_result = "Heads"
        elif flip_range == 1:
            flip_result = "Tails"
        embed=discord.Embed(title='Coinflip!', description=f'You flipped: {flip_result}', color=discord.Color.random())
        await message.channel.send(embed=embed)
    # v magic 8 ball
    if (message.content.startswith('!8ball')):
        responses = ('It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely',
 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good',
 'Signs point to yes', 'Yes', 'Reply hazy, try again', 'Ask again later',
 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
 "Don't bet on it", 'My reply is no', 'My sources say no', 'Outlook not so good',
 'Very doubtful')
        magic_answer = random.choice(responses)
        embed=discord.Embed(title='The Oracle Says: ', description=magic_answer, color=discord.Color.random())
        await message.channel.send(embed=embed)
    # v help command
    if (message.content.startswith('!help')):
        embed=discord.Embed (title='Help!', description='''I can only do a few things at the moment:

!fortune:  Will run the cowsay fortunes command!
!flip:  Will flip a coin heads or tails Style!
!8ball:  Will give a magic 8ball response!
!rps: <!rps @anyone> in the server and reply to the dm with Rock Paper or Scissors''', color=discord.Color.random())
        await message.channel.send(embed=embed)
    if (message.content.startswith("!vibe")):
        await message.channel.send("wack")

    def check_player1(message):
        return message.author == player1 and isinstance(message.channel, discord.DMChannel)
    def check_player2(message):
        return message.author == player2 and isinstance(message.channel, discord.DMChannel)
    if (message.content.startswith("!rps")):
        #above create embed response saying game between two people has started
        channelid = message.channel.id
        channel = client.get_channel(channelid)
        player1 = message.author
        player1_id = message.author.id
        player2 = message.mentions[0]
        player2_id = message.mentions[0].id
        await player1.send(f"Rock Paper Scissors against {player2}")
        await player2.send(f"Rock Paper Scissors against {player1}")
        player1_choice = await client.wait_for('message', check=check_player1)
        player2_choice = await client.wait_for('message', check=check_player2)
        player1_compare = player1_choice.content.lower()
        player2_compare = player2_choice.content.lower()
    #two concurrent rps logic || comparing two inputs 0w0
        if player1_compare == 'rock' and player2_compare == 'scissors':
            await channel.send(f'<@{player1_id}> wins!')
        elif player1_compare == 'rock' and player2_compare  == 'paper':
            await channel.send(f'<@{player2_id}> wins!')
        elif player1_compare == 'scissors' and player2_compare  == 'paper':
            await channel.send(f'<@{player1_id}> wins!')
        elif player1_compare == 'scissors' and player2_compare  == 'rock':
            await channel.send(f'<@{player2_id}> wins!')
        elif player1_compare == 'paper' and player2_compare  == 'rock':
            await channel.send(f'<@{player1_id}> wins!')
        elif player1_compare == 'paper' and player2_compare  == 'scissors':
            await channel.send(f'<@{player2_id}> wins!')
        elif player1_compare == player2_compare:
            await channel.send('no one wins!')
        else:
            print('error')
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)

# Below is projects in progress
