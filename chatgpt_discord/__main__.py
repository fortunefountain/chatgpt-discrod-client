import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv
load_dotenv(".env")
TOKEN = os.environ.get("TOKEN")
GPT_API_KEY = os.environ.get("GPT_API_KEY")

openai.api_key = GPT_API_KEY

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

async def query_chatgpt(prompt):
    data = {
        'model':'gpt-3.5-turbo',
        'messages': [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": f"{prompt}"}],
        'max_tokens': 100,
        'temperature': 0.5,
    }
    response = openai.ChatCompletion.create(**data)
    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='chatgpt')
async def chatgpt_command(ctx, *, message: str):
    response = await query_chatgpt(message)
    await ctx.send(response)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(TOKEN)
