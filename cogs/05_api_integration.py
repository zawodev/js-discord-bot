from discord.ext import commands
import requests

class ExternalAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, city: str):
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY')
        data = response.json()
        if data['cod'] == 200:
            weather = data['weather'][0]['description']
            await ctx.send(f'The weather in {city} is currently {weather}.')
        else:
            await ctx.send(f'Could not retrieve weather for {city}.')

async def setup(bot):
    await bot.add_cog(ExternalAPI(bot))
