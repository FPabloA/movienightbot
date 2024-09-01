import os
import discord
import spinner
import time
from dotenv import load_dotenv
from imdb import Cinemagoer





if __name__ == "__main__":
    load_dotenv()
    cg = Cinemagoer()

    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    client = discord.Client(intents=discord.Intents.all())

    #actions on successful connection
    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    #actions on message received
    @client.event
    async def on_message(message):
        #message is from this bot
        if message.author == client.user:
            return
        
        #message is a command
        if message.content.startswith('!'):
            #generate wheel and send
            if message.content[0:6] == "!wheel":
                valueList = message.content[6:]
                spinner.main(valueList)
                winner, numframes = spinner.getWinner()
                file = discord.File("output.gif")
                e = discord.Embed()
                e.set_image(url="attachment://output.gif")
                await message.channel.send(file=file, embed=e)
                #when gif finishes playing send winner msg (TODO timing changes based on processes currently running on host)
                time.sleep(numframes//24 + 2)
                await message.channel.send("The winner is: " + winner + "  !")
                movie = cg.search_movie(winner)[0]
                movie = cg.get_movie(movie.movieID, info=['plot'])
                
                await message.channel.send("https://www.imdb.com/title/tt" + movie.movieID)
                await message.channel.send(movie.get('plot')[0])
                
            elif message.content[0:5] == "!help":
                await message.channel.send("Currently Supported Commands are: !wheel [list]")
                
            else:
                await message.channel.send("Command not recognized, Proper usage: !wheel [list of values separated w/ commas]")

    client.run(TOKEN)
