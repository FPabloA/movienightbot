import os
import discord
from discord import app_commands
import spinner
import time
from dotenv import load_dotenv
from imdb import Cinemagoer





if __name__ == "__main__":
    load_dotenv()
    cg = Cinemagoer()

    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    GUILDID = os.getenv('DISCORD_GUILD_ID')

    client = discord.Client(intents=discord.Intents.all())
    tree = app_commands.CommandTree(client)

    # Add the guild ids in which the slash command will appear.
    # If it should be in all, remove the argument, but note that
    # it will take some time (up to an hour) to register the
    # command if it's for all guilds.
    @tree.command(
        name="wheel",
        description="Spin the wheel using the provided list",
        guild=discord.Object(id=GUILDID)
    )
    @app_commands.describe(text="The text to send!", channel="The channel to send the message in!")
    async def wheel(interaction: discord.Interaction, text: str, channel: discord.TextChannel=None):
        channel = channel or interaction.channel
        spinner.main(text)
        winner, numframes = spinner.getWinner()
        file = discord.File("output.gif")
        e = discord.Embed()
        e.set_image(url="attachment://output.gif")
        await interaction.channel.send(file=file, embed=e)
        #when gif finishes playing send winner msg (TODO timing changes based on processes currently running on host)
        time.sleep(numframes//24 + 2)
        await interaction.channel.send("The winner is: " + winner + "  !")
        movie = cg.search_movie(winner)[0]
        movie = cg.get_movie(movie.movieID, info=['plot'])
        
        await interaction.channel.send("https://www.imdb.com/title/tt" + movie.movieID)
        await interaction.channel.send(movie.get('plot')[0])

    #actions on successful connection
    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        await tree.sync(guild=discord.Object(id=GUILDID))
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    client.run(TOKEN)
