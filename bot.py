import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os
import scrapy
from bs4 import BeautifulSoup

load_dotenv(".env")

TOKEN = os.getenv("TOKEN")

prefix = "!"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=prefix, intents=intents)

#Mensaje login por terminal
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Funcion de saludar al usuario que ejecuta el comano
@bot.command(name='hola', help='Saluda al usuario')

async def saludar(ctx):
    await ctx.send(f'Hola {ctx.author.mention}!')

#Funcion de busqueda en google que devuelve el primer enlace
@bot.command(name='buscar', help='Busca en google y te devuelve la primera búsqueda')
async def buscar(ctx, *, query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.1 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('div', class_='tF2Cxc')
        
        if first_result:
            title = first_result.find('h3').text
            link = first_result.find('a')['href']
            
            await ctx.send(f"Título del primer resultado: {title}\nEnlace del primer resultado: {link}")
        else:
            await ctx.send("No se encontraron resultados.")
    else:
        await ctx.send("Error al realizar la búsqueda.")

#Funcion para devolver el rango en 2s de rocket league
@bot.command(name='rangoRL', help='introduciendo id epic devuelve el rango en 2s')

async def rangoRL(ctx, *, query):
    url = f"https://rocketleague.tracker.network/rocket-league/profile/epic/{query}/overview"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.1 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('main').text
        
        if result:
            
            await ctx.send(f"El rango del jugador {query} es : {result}\nEnlace del tracker: {url}")
        else:
            await ctx.send(f"No se encontraron resultados.\nEnlace del tracker: {url}")
    else:
        await ctx.send("Error al realizar la búsqueda.")



bot.run(TOKEN)