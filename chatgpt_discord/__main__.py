import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os
load_dotenv(".env")


TOKEN = os.environ.get('TOKEN', "")
GPT_API_KEY = os.environ.get('GPT_API_KEY', "")
openai.api_key = GPT_API_KEY

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

async def query_chatgpt(prompt, message_history, bot_member):
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{"role": "system", "content": "You are a helpful assistant."}]
    }

    for message in message_history:
        data['messages'].append({"role": "user" if message.author != bot_member else "assistant", "content": message.content})

    data['messages'].append({"role": "user", "content": prompt})
    data['max_tokens'] = 100
    data['temperature'] = 0.5

    response = openai.ChatCompletion.create(**data)
    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='chatgpt')
async def chatgpt_command(ctx, *, message: str):
    message_history = []
    async for prev_message in ctx.channel.history(limit=10, before=ctx.message):
        if prev_message.author.bot:
            continue
        message_history.append(prev_message)

    message_history.reverse()
    response = await query_chatgpt(message, message_history, ctx.guild.me)
    await ctx.send(response)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(TOKEN)
