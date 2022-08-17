import discord
from os import system, path
from subprocess import getoutput
from random import randrange
from PIL import Image, ImageDraw, ImageFont
from math import ceil
from discord.ext.commands import Bot
import secrets

client = discord.Client()

@client.event
async def on_ready():
    print('Fortune Bot has logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # v cowsay fortunes
    if (message.content.find('!fortune') != -1):
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
        # TODO: Don't save to hard drive just to load again
        msgImg.save('/tmp/fortune.png')
        embed=discord.Embed(title='The Oracle Says:', color=discord.Color.blue())
        file = discord.File('/tmp/fortune.png', filename='fortune.png')
        embed.set_image(url="attachment://fortune.png")
        await message.channel.send(embed=embed, file=file)
    # v coin flipper
    if (message.content.find('!flip') != -1):
        flip_range = randrange(0,2)
        if flip_range == 0:
            flip_result = "Heads"
        elif flip_range == 1:
            flip_result = "Tails"
        embed=discord.Embed(title='Coinflip!', description=f'You flipped: {flip_result}', color=discord.Color.blue())
        await message.channel.send(embed=embed)
    # v magic 8 ball
    if (message.content.find('!8ball') != -1):
        secretsGenerator = secrets.SystemRandom()
        number_list = [0,1,2,3,4,5]
        magic_ball_result = secretsGenerator.choice(number_list)
        if magic_ball_result == 0:
            magic_ball_answer=('Without a doubt.')
        elif magic_ball_result == 1:
            magic_ball_answer=('Outlook good.')
        elif magic_ball_result == 2:
            magic_ball_answer=('Better not tell you now.')
        elif magic_ball_result == 3:
            magic_ball_answer=('Outlook not so good')
        elif magic_ball_result == 4:
            magic_ball_answer=('My reply is no.')
        elif magic_ball_result == 5:
            magic_ball_answer=('Cannot predict now.')
        else:
            print("Error!!")
        embed=discord.Embed(title='The Oracle Says: ', description=magic_ball_answer, color=discord.Color.blue())
        await message.channel.send(embed=embed)
    # v help command
    if (message.content.find('!help') != -1):
        embed=discord.Embed (title='Help!', description='''I can only do a few things at the moment:

!fortune:  Will run the cowsay fortunes command!
!flip:  Will flip a coin heads or tails Style!
!8ball:  Will give a magic 8ball response!''', color=discord.Color.blue())
        await message.channel.send(embed=embed)

DISCORD_TOKEN = "no"
client.run(DISCORD_TOKEN)