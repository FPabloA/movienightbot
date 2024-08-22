import os
import discord
import spinner
import time
from dotenv import load_dotenv





if __name__ == "__main__":
    load_dotenv()

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
            if message.content == "!wheel":
                await message.channel.send("do wheel")
                spinner.main()
                winner = spinner.getWinner()
                file = discord.File("output.gif")
                e = discord.Embed()
                e.set_image(url="attachment://output.gif")
                await message.channel.send(file=file, embed=e)
                #TODO need more consistent way to wait unti gif finishes
                time.sleep(10)
                await message.channel.send(winner)
            else:
                await message.channel.send("Command not recognized, Proper usage:")

    client.run(TOKEN)
