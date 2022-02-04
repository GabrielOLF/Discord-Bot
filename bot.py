import discord
from discord.ext.commands.bot import Bot
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord_components import *
from asyncio import TimeoutError
from keep_alive import keep_alive
from discord.utils import get
import io
import aiohttp
from abraco import cod
import requests
from bs4 import BeautifulSoup as bs
import re
import random
import time
import sqlite3


bot = ComponentsBot(command_prefix='!', intents=discord.Intents.all())

sad_words = ['Eu não consigo, bot', 'Estou triste', 'que tristeza', 'meu deus']
nilismo = ["A filosofia é o exílio voluntário entre montanhas geladas.", "Nós, homens do conhecimento, não nos conhecemos; de nós mesmo somos desconhecidos.", "Não me roube a solidão sem antes me oferecer verdadeira companhia.", "O amor é o estado no qual os homens têm mais probabilidades de ver as coisas tal como elas não são.", "Como são múltiplas as ocasiões para o mal-entendido e para a ruptura hostil!", "Deus está morto. Viva Perigosamente. Qual o melhor remédio? - Vitória!", "A diferença fundamental entre as duas religiões da decadência: o budismo não promete, mas assegura. O cristianismo promete tudo, mas não cumpre nada.", "Quando se coloca o centro de gravidade da vida não na vida mas no além - no nada -, tira-se da vida o seu centro de gravidade.", "Para ler o Novo Testamento é conveniente calçar luvas. Diante de tanta sujeira, tal atitude é necessária."]

@bot.event
async def on_ready():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    """cur.execute('DROP TABLE IF EXISTS grades')"""
    cur.execute('''CREATE TABLE IF NOT EXISTS grades(
                            id TEXT,
                            segunda TEXT,
                            terca TEXT,
                            quarta TEXT,
                            quinta TEXT,
                            sexta TEXT
                            )''')
    conn.commit()
    cur.close()
    DiscordComponents(bot)
    print(f'{bot.user} ta vivo caraio.')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='música erudita'))
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      if ctx.author.bot:return
      else:
        await ctx.send('Este comando não existe. Digite !comandos para conhecer os meus comandos.')
    return


  
"""----------Consertar essa porra depois
@bot.command()
async def anime(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.reply('De qual anime/manga você deseja saber a nota?')
  resp = await bot.wait_for('message', check=check)
  tag = resp.content
  if ' ' in tag:
    tag = tag.replace(' ', '%20')
    tag_search = tag.replace('%20', ' ')
  else:
    tag = tag
    tag_search = tag
  url = f'https://myanimelist.net/search/all?q={tag}&cat=all'
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  try:
    div = doc.find(class_='wrapper')
    try:
      name_search = div.find(class_='information di-tc va-t pl8')
      name = str(name_search).split('>')[2].split('<')[0]
    except:
      name = tag_search
    real_div = div.find(class_='list di-t w100')
    image_search = real_div.find(class_='lazyload')
    image_link = str(image_search).split('src=')[1].split('"')[1]
    try:
      score_search = real_div.find(class_='pt4 fs10 lh14 fn-grey4')
      score = str(score_search).split('/>')[1].split('<')[0].replace('\n', '').split('Scored')[1].replace(' ', '')
    except:
      try:
        score_search = real_div.find(class_='pt8 fs10 lh14 fn-grey4')
        score = str(score_search).split('/>')[1].split('<')[0].replace('\n', '').split('Scored')[1].replace(' ', '')
      except:
        await ctx.send(f'Não consegui encontrar ``{tag_search}``.')
  except:
    await ctx.send(f'Não consegui encontrar ``{tag_search}``.')
  embedA = discord.Embed(
            title=f"Nota de {name}", description=f'MAL: **{score}**', color=0x00ffce)
  embedA.set_thumbnail(url=f"{image_link}")
  await ctx.send(embed=embedA)
"""
@bot.command()
async def criar_grade(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.send('Digite a disciplina em cada horário. Caso não tenha disciplina em tal horário, digite "-".')
  run = True
  await ctx.send('**SEGUNDA-FEIRA**')
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  num = 0
  segunda_lista = []
  while run:
    await ctx.send(f'Aula às {horarios[num]}:')
    resp = await bot.wait_for('message', check=check)
    resposta = str(resp.content)
    cur.execute(f'INSERT INTO grades (id, segunda) VALUES (?, ?)', (user_id, resposta))
    conn.commit()
    segunda_lista.append(resposta)
    num += 1
    if len(segunda_lista) == 8:
      run = False
    else:
      continue

  await ctx.send('**TERÇA-FEIRA**')
  nums = 0
  segunda_lista_1 = []
  runs = True
  while runs:
    await ctx.send(f'Aula às {horarios[nums]}:')
    respo = await bot.wait_for('message', check=check)
    respostas = str(respo.content)
    cur.execute(f'INSERT INTO grades (id, terca) VALUES (?, ?)', (user_id, respostas))
    conn.commit()
    segunda_lista_1.append(respostas)
    nums += 1
    if len(segunda_lista_1) == 8:
      runs = False
    else:
      continue

  await ctx.send('**QUARTA-FEIRA**')
  num = 0
  segunda_lista = []
  run = True
  while run:
    await ctx.send(f'Aula às {horarios[num]}:')
    resp = await bot.wait_for('message', check=check)
    resposta = str(resp.content)
    cur.execute(f'INSERT INTO grades (id, quarta) VALUES (?, ?)', (user_id, resposta))
    conn.commit()
    segunda_lista.append(resposta)
    num += 1
    if len(segunda_lista) == 8:
      run = False
    else:
      continue

  await ctx.send('**QUINTA-FEIRA**')
  
  num = 0
  segunda_lista = []
  run = True
  while run:
    await ctx.send(f'Aula às {horarios[num]}:')
    resp = await bot.wait_for('message', check=check)
    resposta = str(resp.content)
    cur.execute(f'INSERT INTO grades (id, quinta) VALUES (?, ?)', (user_id, resposta))
    conn.commit()
    segunda_lista.append(resposta)
    num += 1
    if len(segunda_lista) == 8:
      run = False
    else:
      continue
  run = True
  await ctx.send('**SEXTA-FEIRA**')
  
  num = 0
  segunda_lista = []
  while run:
    await ctx.send(f'Aula às {horarios[num]}:')
    resp = await bot.wait_for('message', check=check)
    resposta = str(resp.content)
    cur.execute(f'INSERT INTO grades (id, sexta) VALUES (?, ?)', (user_id, resposta))
    conn.commit()
    segunda_lista.append(resposta)
    num += 1
    if len(segunda_lista) == 8:
      run = False
    else:
      continue
  
  await ctx.send("Sua grade foi salvada no banco com sucesso. Caso queira checar individualmente cada dia, digite '!{dia da semana}'")
  
@bot.command()
async def grade_geral(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, segunda FROM grades WHERE segunda IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas_segunda = ''
  materias_segunda = ''
  number_segunda = 0
  for row in cur:
      materias_segunda =  f'**{horarios[number_segunda]}**' + ': ' + row[1] + '\n'
      aulas_segunda += materias_segunda
      number_segunda += 1
  try:
    cur.execute(f'SELECT id, terca FROM grades WHERE terca IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas_terca = ''
  materias_terca = ''
  number_terca = 0
  for row in cur:
      materias_terca =  f'**{horarios[number_terca]}**' + ': ' + row[1] + '\n'
      aulas_terca += materias_terca
      number_terca += 1
  try:
    cur.execute(f'SELECT id, quarta FROM grades WHERE quarta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas_quarta = ''
  materias_quarta = ''
  number_quarta = 0
  for row in cur:
      materias_quarta =  f'**{horarios[number_quarta]}**' + ': ' + row[1] + '\n'
      aulas_quarta += materias_quarta
      number_quarta += 1
  try:
    cur.execute(f'SELECT id, quinta FROM grades WHERE quinta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas_quinta = ''
  materias_quinta = ''
  number_quinta = 0
  for row in cur:
      materias_quinta =  f'**{horarios[number_quinta]}**' + ': ' + row[1] + '\n'
      aulas_quinta += materias_quinta
      number_quinta += 1
  try:
    cur.execute(f'SELECT id, sexta FROM grades WHERE sexta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas_sexta = ''
  materias_sexta = ''
  number_sexta = 0
  for row in cur:
      materias_sexta =  f'**{horarios[number_sexta]}**' + ': ' + row[1] + '\n'
      aulas_sexta += materias_sexta
      number_sexta += 1
  embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Segunda-Feira",color=0x06adc4)
  embedVar.add_field(name='Segunda-Feira', value=f"{aulas_segunda}")
  embedVar.add_field(name='Terça-Feira', value=f"{aulas_terca}")
  embedVar.add_field(name='Quarta-Feira', value=f"{aulas_quarta}")
  embedVar.add_field(name='Quinta-Feira', value=f"{aulas_quinta}")
  embedVar.add_field(name='Sexta-Feira', value=f"{aulas_sexta}")
  await ctx.send(embed=embedVar)
@bot.command()
async def deletar_grade(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  user_id = str(ctx.author).split('#')[0]
  await ctx.send('Você tem certeza que deseja deletar a sua grade?')
  resp = await bot.wait_for('message', check=check)
  response = str(resp.content)
  if response == 'Sim' or response == 'sim':
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    try:
      cur.execute(f'DELETE FROM grades WHERE id= ?', (user_id, ))
      conn.commit()
      await ctx.send('Pronto.')
    except:
      await ctx.send('Não consegui deletar a sua grade.')
  else:
    await ctx.send('Entendível, até um outro dia.')

@bot.command()
async def segunda(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, segunda FROM grades WHERE segunda IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas = ''
  materias = ''
  number = 0
  for row in cur:
      materias =  f'**{horarios[number]}**' + ': ' + row[1] + '\n'
      aulas += materias
      number += 1
  if len(aulas) == 0:
    await ctx.send('Você ainda não fez sua grade de horários.')
  else:
    embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Segunda-Feira", description=(f'{aulas}'),color=0x06adc4)
    await ctx.send(embed=embedVar)
@bot.command()
async def terca(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, terca FROM grades WHERE terca IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas = ''
  materias = ''
  number = 0
  try:
    for row in cur:
      materias =  f'**{horarios[number]}**' + ': ' + row[1] + '\n'
      aulas += materias
      number += 1
  
  except:
    await ctx.send('erro aqui')
  
  if len(aulas) == 0:
    await ctx.send('Você ainda não fez sua grade de horários.')
  else:
    embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Terça-Feira", description=(f'{aulas}'),color=0x06adc4)
    await ctx.send(embed=embedVar)
@bot.command()
async def quarta(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, quarta FROM grades WHERE quarta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas = ''
  materias = ''
  number = 0
  for row in cur:
    materias =  f'**{horarios[number]}**' + ': ' + row[1] + '\n'
    aulas += materias
    number += 1
  if len(aulas) == 0:
    await ctx.send('Você ainda não fez sua grade de horários.')
  else:
    embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Quarta-Feira", description=(f'{aulas}'),color=0x06adc4)
    await ctx.send(embed=embedVar)
@bot.command()
async def quinta(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, quinta FROM grades WHERE quinta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas = ''
  materias = ''
  number = 0
  for row in cur:
    materias =  f'**{horarios[number]}**' + ': ' + row[1] + '\n'
    aulas += materias
    number += 1
  if len(aulas) == 0:
    await ctx.send('Você ainda não fez sua grade de horários.')
  else:
    embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Quinta-Feira", description=(f'{aulas}'),color=0x06adc4)
    await ctx.send(embed=embedVar)
@bot.command()
async def sexta(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  horarios = ['08:00-8:50', '8:50-9:40', '10:00-10:50', '10:50-11:40', '14:00-14:50', '14:50-15:40', '18:50-19:35', '19:35-20:20']
  try:
    cur.execute(f'SELECT id, sexta FROM grades WHERE sexta IS NOT NULL and id= "{user_id}"')
  except:
    await ctx.send('erro erro erro erro')
  aulas = ''
  materias = ''
  number = 0
  for row in cur:
    materias =  f'**{horarios[number]}**' + ': ' + row[1] + '\n'
    aulas += materias
    number += 1
  if len(aulas) == 0:
    await ctx.send('Você ainda não fez sua grade de horários.')
  else:
    embedVar = discord.Embed(
                              title=f"Sua grade de aulas na Sexta-Feira", description=(f'{aulas}'),color=0x06adc4)
    await ctx.send(embed=embedVar)
  
  
  
@bot.command()
async def palavras(ctx):
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  cur.execute('SELECT palavras FROM words')
  words = ''
  for row in cur:
    words = words + row[0] + ', '
  words = words[:-1]
  words = words[:-1]
  embedG = discord.Embed(
        title="Palavras do jogo **!forca**", description=f'**{words}**', color=0x00ff00)
  await ctx.send(embed=embedG)
@bot.command()
async def adicionar(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  await ctx.send('Que palavra deseja adicionar a ``!forca``?')
  resp = await bot.wait_for('message', check=check)
  palavra = str(resp.content)
  palavra = palavra.lower()
  cur.execute('SELECT palavras from words')
  words = ''
  for row in cur:
    words = words + row[0] + ','
  if palavra in words.lower():
    await ctx.send(f'A palavra {palavra} já está inserida no banco de dados, tente outra.')
  else:
    try:
      cur.execute('INSERT INTO words (palavras) VALUES (?)',(palavra, ))
      conn.commit()
      await ctx.send(f'A palavra {palavra} foi adicionada ao banco de dados com sucesso!')
    except:
      await ctx.send(f'Não consegui adicionar {palavra} ao banco de dados.')

  cur.execute('SELECT palavras FROM words')
  words = ''
  for row in cur:
    words = words + row[0] + ', '
  words = words[:-1]
  words = words[:-1]
  embedG = discord.Embed(
        title="Palavras do jogo ``!forca``", description=f'``{words}``', color=0x00ff00)
  await ctx.send(embed=embedG)
@bot.command()
async def remover(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  cur.execute('SELECT palavras FROM words')
  words = ''
  for row in cur:
    words = words + row[0] + ', '
  words = words[:-1]
  words = words[:-1]
  embedG = discord.Embed(
        title="Palavras do jogo ``!forca``", description=f'``{words}``', color=0x00ff00)
  await ctx.send(embed=embedG)
  await ctx.send('Que palavra você deseja remover?')
  resp = await bot.wait_for('message', check=check)
  palavra = resp.content
  palavra = palavra.lower()
  words = words.lower()
  if palavra in words:
    try:
      cur.execute('DELETE FROM words WHERE palavras = ?', (palavra, ))
      conn.commit()
      await ctx.send(f'{palavra} foi removida do banco com sucesso!')
    except:
      await ctx.send(f'Não consegui remover {palavra} do banco.')
  else:
    await ctx.send(f'Não foi possível retirar a palavra {palavra} pois ela não está inserida no banco.')
@bot.command()
async def ricos(ctx):
  # Conecta ao banco de dados
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  # Seleciona as linhas id e money da tabela userid ordenada pelo dinheiro
  cur.execute('SELECT id, money FROM userid ORDER BY money DESC LIMIT 5')
  usuarios = ''
  num = 1
  # Retorna cada linha do banco selecionadas anteriormente
  for row in cur:
    if num == 1:
      usuarios = usuarios + f":first_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    if num == 2:
      usuarios = usuarios + f":second_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    if num == 3:
      usuarios = usuarios + f":third_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    elif num != 1 and num != 2 and num != 3:
      usuarios = usuarios + f":small_blue_diamond: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    num += 1
  embedG = discord.Embed(
        title="Ricos do servidor", description=f'{usuarios}', color=0x00ff00)
  await ctx.send(embed=embedG)
# GATINHO
@bot.command()
async def gatinho(ctx):
  url = 'http://random.cat/view'
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  find_photo = str(doc).split('src=')[1].split('"')[1]
  await ctx.send(find_photo)
# RANK PONTOS
@bot.command()
async def rank(ctx):
  # Se conecta ao banco de dados
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  # Seleciona os ids e pontos da tabela userid ordenada pelos pontos
  cur.execute('SELECT id, points FROM userid ORDER BY points DESC LIMIT 5')
  usuarios = ''
  num = 1
  # Retorna cada linha selecionada anteriormente 
  for row in cur:
    if num == 1:
      usuarios = usuarios + f":first_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    if num == 2:
      usuarios = usuarios + f":second_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    if num == 3:
      usuarios = usuarios + f":third_place: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    elif num != 1 and num != 2 and num != 3:
      usuarios = usuarios + f":small_blue_diamond: **{row[0]}**" + ": " + f"``{row[1]}``" + "\n"
    num += 1

  embedG = discord.Embed(
        title="Ranking de pontos", description=f'{usuarios}', color=0x00ff00)
  await ctx.send(embed=embedG)

@bot.command()
async def apostar(ctx):
  user_id = str(ctx.author).split('#')[0]
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  cur.execute(f'SELECT id, money FROM userid WHERE id="{user_id}"')
  for row in cur:
    money = int(row[1])
  if money > 0:
    await ctx.reply('Quanto você quer apostar? ')
  else:
    await ctx.reply('Você não tem nada pra apostar.')
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  response = await bot.wait_for('message', check=check)
  apostado = int(response.content)
  aposta = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
  sorte = random.choice(aposta)
  user_id = str(ctx.author).split('#')[0]
 
  money_won =  int(2 * apostado)
  money_won2 = int(apostado + 250)
  for row in cur:
    money = int(row[1])
  if money < apostado:
    await ctx.reply('Você não tem tudo isso.')
  elif apostado == 0:
    await ctx.reply('Sério?')
  else:
    if sorte == 'a':
        cur.execute(f'UPDATE userid SET money = money + {money_won} WHERE id= "{user_id}"')
        conn.commit()
        cur.execute(f'SELECT id, money FROM userid WHERE id="{user_id}"')
        for row in cur:
          money = int(row[1])
        await ctx.reply(f'Você ganhou o ``dobro`` :money_mouth:. Agora você tem ``{money}``!')
    elif sorte == 'b' or sorte == 'c':
        cur.execute(f'UPDATE userid SET money = money + {money_won2} WHERE id= "{user_id}"')
        conn.commit()
        cur.execute(f'SELECT id, money FROM userid WHERE id="{user_id}"')
        for row in cur:
          money = int(row[1])
        await ctx.reply(f'Você ganhou, ``{user_id}``! Agora você tem ``{money}``.')
    else:
        cur.execute(f'UPDATE userid SET money = money - {apostado} WHERE id= "{user_id}"')
        conn.commit()
        cur.execute(f'SELECT id, money FROM userid WHERE id="{user_id}"')
        for row in cur:
          money = int(row[1])
        await ctx.reply(f'Você perdeu, ``{user_id}``! Agora você tem ``{money}``.')
# DIRSON
@bot.command()
async def dirso(ctx):
  await ctx.send('https://cdn.discordapp.com/attachments/840110683785658369/905443717626884116/20211103_100824.jpg')
# BANCO DE IDS
@bot.command()
async def database(ctx):
  conn = sqlite3.connect('users.db')
  cur = conn.cursor()
  cur.execute(f'SELECT id FROM userid ORDER BY id DESC')
  usuarios = ''
  for row in cur:
    usuarios = usuarios + f'**{row[0]}**' + '\n'
  await ctx.send(f'Usuarios que estão inseridos no banco de dados:\n{usuarios}')
"""----------Arrumar essa merda depois
# SIGNIFICADO SCRAPING
@bot.command()
async def significado(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.reply('De qual palavra você deseja saber o significado?')
  response = await bot.wait_for('message', check=check)
  tag = response.content
  if ' ' in tag:
    tag = tag.replace(' ', '+')
    tag_search = tag.replace('+', ' ')
  else:
    tag = tag
    tag_search = tag
  try:
      url = f'https://www.significados.com.br/?s={tag}'
      result = requests.get(url).text
      doc = bs(result, 'html.parser')
      div = doc.find(class_='row')
      real_div = div.find(class_='col-lg-8 mt20')
      description_search = real_div.find(class_='description')
      description_found = str(description_search).replace('<br/', '').replace('>','').replace('</','').replace('<p class="description" ','').split('"')[2]
      if '<em' in description_found:
        description_found = description_found.replace('<em', '')
      if 'em.p' in description_found:
        description_found = description_found.replace('em.p', '')
      embedSig = discord.Embed(title=f"Significado de {tag_search}", description=f"{description_found}",color=0x121274)
      await ctx.send(embed=embedSig)
  except:
      await ctx.reply(f'Não consegui encontrar {tag_search}.')
"""

# RANDOM DOG
@bot.command()
async def doguinho(ctx):
  run = True
  url = 'https://random.dog/'
  while run:
    result = requests.get(url).text
    doc = bs(result, 'html.parser')
    div = doc.find(id="dog-img")
    try:
      img = str(div).split('"')[3]
      format = str(img).split('.')[1]
      async with aiohttp.ClientSession() as session:
              async with session.get(f'https://random.dog/{img}') as resp:
                  if resp.status != 200:
                      return await ctx.send('eu não... eu não consegui baixar a foto do doguinho :pensive:')
                  data = io.BytesIO(await resp.read())
      await ctx.send(file=discord.File(data, f'doguinho.{format}'))
    except:
      async with aiohttp.ClientSession() as session:
              async with session.get('https://cdn.discordapp.com/attachments/879834445169963018/896813049778946058/doguinho.jpg') as resp:
                  if resp.status != 200:
                      return await ctx.send('eu não... eu não consegui baixar a foto do doguinho :pensive:')
                  data = io.BytesIO(await resp.read())
      await ctx.send(file=discord.File(data, 'doguinho.jpg'))
      run = False
    run = False

  
# CINEMA SCRAPING
@bot.command()
async def cinema(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.send('Qual filme você deseja saber a nota?')
  response = await bot.wait_for('message', check=check)
  movie = response.content
  if ' ' in movie:
      movie_search = movie.replace(' ', '+')
  else:
      movie_search = movie
  try:
    url = f'https://www.adorocinema.com/pesquisar/?q={movie_search}'
    result = requests.get(url).text
    doc = bs(result, 'html.parser')
    div = doc.find(class_='content-layout')
    section = div.find(class_='section movies-results')
    movie_div = section.find(class_='card entity-card entity-card-list cf')
    try:
      image_search = movie_div.find(class_='thumbnail')
      image_found = str(image_search).split('src=')[1].split('"')[1]
    except:
      image_found = 'https://cdn.pixabay.com/photo/2017/04/09/12/45/error-2215702_960_720.png'
    name_search = movie_div.find(class_='meta')
    name_found = name_search.find(class_='meta-title')
    try:
      rating_div = movie_div.find(class_='rating-holder rating-holder-1')
      rating_stars = rating_div.find_all(class_='stareval-note')
    except:
      try:
        rating_div = movie_div.find(class_='rating-holder rating-holder-2')
        rating_stars = rating_div.find_all(class_='stareval-note')
      except:
        try:
          rating_div = movie_div.find(class_='rating-holder rating-holder-3')
          rating_stars = rating_div.find_all(class_='stareval-note')
        except:
          try:
            rating_div = movie_div.find(class_='rating-holder rating-holder-4')
            rating_stars = rating_div.find_all(class_='stareval-note')
          except:
            await ctx.send(f'Não consegui encontrar {movie}. Tente escrever o nome de outra forma.')
    name = str(name_found).split('>')[2].split('<')[0]
    nome_nota = rating_div.find_all(class_='rating-item-content')
    nome_nota1 = str(nome_nota).split('>')[2].split('<')[0].replace(' ', '')
    nome_nota2= str(nome_nota).split('>')[22].split('<')[0].replace(' ', '')
    nome_nota3 = str(nome_nota).split('>')[42].split('<')[0].replace(' ', '')
    try:
      rating_imprensa = str(rating_stars).split('>')[1].split('<')[0]
      rating_cinema = str(rating_stars).split('<')[5].split('>')[1]
    except:
      rating_imprensa = 'Nota não encontrada'
      rating_cinema = 'Nota não encontrada'
    if len(rating_div.find_all(class_='rating-item')) == 2:
      rating_users = str(rating_stars).split('>')[1].split('<')[0]
    else:
      rating_users = str(rating_stars).split('<')[3].split('>')[1]
    embedVar = discord.Embed(
                              title=f"{name}", color=0x06adc4)
    embedVar.add_field(name=nome_nota1, value=f"**{rating_imprensa}**")
    embedVar.add_field(name=nome_nota2, value=f"**{rating_users}**")
    if str(nome_nota3) != 'Meusamigos':
      embedVar.add_field(name=nome_nota3, value=f"**{rating_cinema}**")
    embedVar.set_thumbnail(url=f"{image_found}")
    await ctx.send(embed=embedVar)
  except:
    await ctx.send(f'Não consegui encontrar {movie}. Me chame novamente e tente escrever o nome do filme de outra forma.')
  
# PEDRA PAPEL TESOURA
@bot.command()
async def pdt(ctx):
    user_id = str(ctx.author).split('#')[0]
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    choices = ['pedra', 'papel', 'tesoura']
    comp = random.choice(choices)
    ainda = discord.Embed(title="Pedra, papel ou tesoura.", color=0x00ff00)
    empate = discord.Embed(title="Empate!", color=0x00ff00)
    vitoria = discord.Embed(title=f'{ctx.author.display_name} você ganhou!',
                            description=f'O bot escolheu {comp}.', color=0x00ff00)
    derrota = discord.Embed(title=f'{ctx.author.display_name} você perdeu!',
                            description=f'O bot escolheu {comp}.', color=0xc50b0b)
    fora = discord.Embed(
        title="Você não clicou a tempo, você está fora.", color=0xc50b0b)
    m = await ctx.send(
        embed=ainda,
        components=[[Button(style=1, label="pedra"), Button(style=1, label="papel"), Button(style=1, label="tesoura")]]
    )
    try:
        res = await bot.wait_for('button_click', check=check, timeout=10.0)
        player = res.component.label
        if player == comp:
            await m.edit(embed=empate, components=[])
        if player == "pedra" and comp == "papel":
            await m.edit(embed=derrota, components=[])
        if player == "pedra" and comp == "tesoura":
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await m.edit(embed=vitoria, components=[])
        if player == "papel" and comp == "tesoura":
            await m.edit(embed=derrota, components=[])
        if player == 'papel' and comp == 'pedra':
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await m.edit(embed=vitoria, components=[])
        if player == "tesoura" and comp == "pedra":
            await m.edit(embed=derrota, components=[])
        if player == "tesoura" and comp == "papel":
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await m.edit(embed=vitoria, components=[])
            
    except TimeoutError:
        await m.edit(embed=fora, components=[])
# MM

@bot.command()
async def mm(ctx):
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel
    user_id = str(ctx.author).split('#')[0]
    num = random.choice(range(10, 20))
    num_v = random.choice(range(1, 20))
    al = discord.Embed(title="Maior ou Menor",
                       description=f'O número aleatório é igual ou está perto de {num}', color=0x00ff00)
    fora = discord.Embed(
        title="Você não escolheu a tempo.", color=0xc50b0b)
    vitoria = discord.Embed(title=f'{ctx.author.display_name} você ganhou!',
                            description=f'O bot escolheu {num_v}', color=0x00ff00)
    derrota = discord.Embed(title=f'{ctx.author.display_name} você perdeu!',
                            description=f'O bot escolheu {num_v}', color=0xc50b0b)
    m = await ctx.send(
        embed=al,
        components=[[Button(style=1, label='Maior', custom_id="button1"), Button(
            style=1, label='Igual', custom_id='button2'), Button(style=1, label='Menor', custom_id='button3')]]
    )
    try:
        res = await bot.wait_for('button_click', check=check, timeout=10.0)
        player = res.component.label
        if player == 'Maior':
            if num_v > num:
                pontos = 1
                conn = sqlite3.connect('users.db')
                cur = conn.cursor()
                cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
                conn.commit()
                await m.edit(embed=vitoria, components=[])
                await ctx.send('+1 ponto')
            elif num_v < num:
                await m.edit(embed=derrota, components=[])
            elif num_v == num:
                await m.edit(embed=derrota, components=[])
        if player == 'Igual':
            if num_v > num:
                await m.edit(embed=derrota, components=[])
            elif num_v < num:
                await m.edit(embed=derrota, components=[])
            elif num_v == num:
                pontos = 1
                conn = sqlite3.connect('users.db')
                cur = conn.cursor()
                cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
                conn.commit()
                await m.edit(embed=vitoria, components=[])
                await ctx.send('+1 ponto')
        if player == 'Menor':
            if num_v > num:
                await m.edit(embed=derrota, components=[])
            elif num_v < num:
                pontos = 1
                conn = sqlite3.connect('users.db')
                cur = conn.cursor()
                cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
                conn.commit()
                await m.edit(embed=vitoria, components=[])
                await ctx.send('+1 ponto')
            elif num_v == num:
                await m.edit(embed=derrota, components=[])
    except TimeoutError:
        await m.edit(embed=fora, components=[])   
# LOTERIA

@bot.command()
async def loteria(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    await ctx.reply('Escolha 6 números de 1 a 100')
    resp = await bot.wait_for('message',check=check)
    answer = resp.content.split()
    answer1 = list(map(int, answer))
    sort = random.sample(range(1, 100), 6)
    acertadas = 0
    if len(answer1) > 6:
        await ctx.channel.send('Apenas 6 números. Tente novamente.')
    elif len(answer1) < 6:
        await ctx.channel.send('São 6 números, burro.')
    elif len(answer1) == 6:
        for apostada in answer1:
            for sorteada in sort:
                if apostada == sorteada:
                    acertadas += 1
                    break
        num_resposta = str(answer1).replace('[', '').replace(']','')
        num_sorteadas = str(sort).replace('[', '').replace(']','')
        num_acertos = str(acertadas).replace('[', '').replace(']', '')

        embedVar = discord.Embed(title="Resultado", color=0xff6500)
        embedVar.add_field(name="Apostadas", value=(num_resposta), inline=False)
        embedVar.add_field(name="Sorteadas", value=(num_sorteadas), inline=False)
        embedVar.add_field(name='Número de acertos', value=(num_acertos))
        await ctx.reply(embed=embedVar)
# DADOS

@bot.command()
async def dados(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    gold = 2000
    while gold >= 0:
        dado_1 = random.choice(range(1, 7))
        dado_2 = random.choice(range(1, 7))
        await ctx.channel.send(ctx.author.mention + ' quantos bonoros você quer apostar?')
        gold_bet1 = await bot.wait_for('message',check=check)
        gold_bet3 = str(gold_bet1.content)
        if gold_bet3 == 'break':
            await ctx.reply('flws :wave:', mention_author=False)
            break
        gold_bet2 = int(gold_bet1.content)
        if dado_1 == 1:
            if dado_2 == 1:
                gold = int(gold) + int(gold_bet2 * 10)
                embedVar = discord.Embed(
                    title="Dado 1", description=f'{dado_1}', color=0x00ff00)
                embedVar.add_field(name='Dado 2', value=f'{dado_2}')
                await ctx.channel.send(embed=embedVar)
                await ctx.channel.send(f'Taporra! Você conseguiu o olho do tigre! Agora você tem ``{gold}`` bonoros!')
                await ctx.channel.send
                (ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S':
                    continue
                else:
                    await ctx.reply('vlw flw!', mention_author=False)
                    break

            else:
                gold = int(gold) + int(gold_bet2 * 2)
                embedVar = discord.Embed(
                    title="Dado 1", description=f'{dado_1}', color=0x00ff00)
                embedVar.add_field(name='Dado 2', value=f'{dado_2}')
                await ctx.channel.send(embed=embedVar)
                await ctx.channel.send(f'Parabéns! Você conseguiu a metade de um olho de tigre! Agora você tem ``{gold}`` bonoros!')
                await ctx.channel.send(f'{ctx.author.mention} quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S':
                    continue
                else:
                    await ctx.reply('vlw flw!', mention_author=False)
                    break
        if dado_1 != 1:
            if dado_2 != 1:
                gold = int(gold) - int(gold_bet2)
                embedVar = discord.Embed(
                    title="Dado 1", description=f'{dado_1}', color=0x00ff00)
                embedVar.add_field(name='Dado 2', value=f'{dado_2}')
                await ctx.channel.send(embed=embedVar)
                if gold_bet2 > 2000:
                    if gold == 0:
                        await ctx.reply('VOCÊ PERDEU TUDO.\nAdeus! :wave:')
                        break
                    else:
                        await ctx.channel.send(f'Perdeu. Agora você só tem ``{gold}`` bonoros, kkkkkkkkkkkkkkkkkkk')

                else:
                    await ctx.channel.send(f'Você perdeu ``{gold_bet2}`` bonoros.')

                await ctx.channel.send(ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S' and gold > 0:
                    continue
                elif guess == 'S' and gold <= 0:
                    await ctx.reply('TU NÃO TEM NADA MALUCO', mention_author=False)
                    break
                else:
                    await ctx.reply('vlw flw')
                    break
            else:
                gold = int(gold) + int(gold_bet2 * 2)
                embedVar = discord.Embed(
                    title="Dado 1", description=f'{dado_1}', color=0x00ff00)
                embedVar.add_field(name='Dado 2', value=f'{dado_2}')
                await ctx.channel.send(embed=embedVar)
                await ctx.channel.send(f'Parabéns, você conseguiu a metade de um olho de tigre! Agora você tem ``{gold}``de ouro!')
                await ctx.channel.send(ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S':
                    continue
                else:
                    await ctx.reply('vlw flw!', mention_author=False)
                    break

# OP

@bot.command()
async def op(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    y = ['multiplicação', 'subtração', 'adição']
    op = random.choice(y)
    time.sleep(1)
    if op == 'multiplicação':
        num_al1 = random.choice(range(1, 12))
        num_al2 = random.choice(range(1, 12))
        embedVar = discord.Embed(
            title="Multiplicação!", description=f'{num_al1} x {num_al2}', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        resposta_certa = num_al1 * num_al2
        tentativa2 = await bot.wait_for('message',check=check)
        tentativa = int(tentativa2.content)
        if tentativa == resposta_certa:
            await ctx.reply('Você acertou! :partying_face:', mention_author=False)
        else:
            await ctx.reply('Você errou! ||imagina não saber multiplicaçãok||', mention_author=False)
    elif op == 'subtração':
        num_al1 = random.choice(range(1, 100))
        num_al2 = random.choice(range(1, 100))
        embedVar = discord.Embed(
            title="Subtração!", description=f'{num_al1} - {num_al2}', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        resposta_certa = num_al1 - num_al2
        tentativa2 = await bot.wait_for('message',check=check)
        tentativa = int(tentativa2.content)
        if tentativa == resposta_certa:
            await ctx.reply('Você acertou! :partying_face:', mention_author=False)
        else:
            await ctx.reply('Você errou! ||imagina não saber subtraçãok||', mention_author=False)
    elif op == 'adição':
        num_al1 = random.choice(range(1, 100))
        num_al2 = random.choice(range(1, 100))
        embedVar = discord.Embed(
            title="Adição!", description=f'{num_al1} + {num_al2}', color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        resposta_certa = num_al1 + num_al2
        tentativa2 = await bot.wait_for('message',check=check)
        tentativa = int(tentativa2.content)
        if tentativa == resposta_certa:
            await ctx.reply('Você acertou! :partying_face:', mention_author=False)
        else:
            await ctx.reply('Você errou! ||imagina não saber adiçãok||', mention_author=False)


# JOGO DA FORCA

@bot.command()
async def forca(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT palavras FROM words')
    palavra_lista = ''
    palavra_lista1 = []
    for row in cur:
      palavra_lista = palavra_lista + row[0] + ' '
    palavra_lista = palavra_lista.split(' ')
    for palavra in palavra_lista:
      palavra_lista1.append(palavra)
    word = random.choice(palavra_lista1)
    if word == '':
      while word == '':
        word = random.choice(palavra_lista1)
        if word != '':
          break
    word = word.lower()
    digitadas = []
    chances = 6
    user_id = str(ctx.author).split('#')[0]
    embedG = discord.Embed(
        title="Jogo da forca! ", description=f'A palavra tem {len(word)} letras!', color=0x00ff00)
    await ctx.send(embed=embedG)
    while True:
        resp = await bot.wait_for('message', check=check)
        tentativa = str(resp.content)
        letra = tentativa.lower()
        if len(letra) > 1:
            if letra == 'dica':
              await ctx.send(f'A palavra começa com ``{word[0]}`` e termina com ``{word[-1]}``')
              continue
            else:
              await ctx.send('Apenas uma letra.')
              continue
        digitadas.append(letra)
        tempo_secret = ''
        for letra_secreta in word:
            if letra_secreta in digitadas:
                tempo_secret += letra_secreta
            else:
                tempo_secret += ' x '
        if letra not in word:
            chances -= 1
        if tempo_secret == word:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply(f'Você ganhou! A palavra era ``{word}``')
            break
        else:
            if chances <= 0:
                await ctx.reply(f'Você perdeu! A palavra era ``{word}``')
                break
            else:
                embedF = discord.Embed(
            title="Palavra secreta: ", description=f'{tempo_secret}', color=0x00ff00)
                embedF.add_field(
        name="Situação", value=f"Você tem {chances} chances restantes.", inline=False)
                await ctx.send(embed=embedF)
                continue
# JOGO DAS CORES
@bot.command()
async def cores(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT palavras FROM words')
    """palavras = ['``abacate``', '``feijoada``',
                '``viniboyola``', '``celular``', '``liquidificador``']"""
    palavra_lista = ''
    palavra_lista1 = []
    for row in cur:
      palavra_lista = palavra_lista + row[0] + ' '
    palavra_lista = palavra_lista.split(' ')
    for palavra in palavra_lista:
      palavra_lista1.append(palavra)
    palavras = palavra_lista1
    cor = [':orange_circle:', ':red_circle:',
           ':blue_circle:', ':yellow_circle:', ':green_circle:']
    sorteados = random.sample(cor, len(cor))
    sorteados1 = random.sample(palavras, len(palavras))
    cor1 = sorteados[1]
    cor2 = sorteados[2]
    cor3 = sorteados[3]
    palavra1 = sorteados1[1]
    palavra2 = sorteados1[2]
    palavra3 = sorteados1[3]
    if palavra1 == '' or palavra2 == '' or palavra3 == '':
      if palavra1 == '':
        palavra1 = sorteados1[4]
      elif palavra2 == '':
        palavra2 = sorteados1[4]
      elif palavra3 == '':
        palavra3 = sorteados1[4]
      
    lista = [palavra1, palavra2, palavra3]
    palavra = random.choice(lista)
    embedG = discord.Embed(
          title="Atenção:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
    msg = await ctx.send(embed=embedG)
    embedE = discord.Embed(
        description=f'Qual era a cor da palavra {palavra}?', color=0x00b2ff)
    time.sleep(2)
    await msg.edit(embed=embedE)
    res = await bot.wait_for('message',check=check)
    tentativa = str(res.content)
    user_id = str(ctx.author).split('#')[0]
    if tentativa == 'Amarelo' or tentativa == 'amarelo':
        if cor1 == ':yellow_circle:' and palavra == palavra1 or cor2 == ':yellow_circle:' and palavra == palavra2 or cor3 == ':yellow_circle:' and palavra == palavra3:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00b2ff)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
            await msg.edit(embed=embedF)
    elif tentativa == 'Azul' or tentativa == 'azul':
        if cor1 == ':blue_circle:' and palavra == palavra1 \
        or cor2 == ':blue_circle:' and palavra == palavra2 \
        or cor3 == ':blue_circle:' and palavra == palavra3:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00b2ff)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
            await msg.edit(embed=embedF)
    elif tentativa == 'Vermelho' or tentativa == 'vermelho':
        if cor1 == ':red_circle:' and palavra == palavra1 \
        or cor2 == ':red_circle:' and palavra == palavra2 \
        or cor3 == ':red_circle:' and palavra == palavra3:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00b2ff)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
            await msg.edit(embed=embedF)
    elif tentativa == 'Verde' or tentativa == 'verde':
        if cor1 == ':green_circle:' and palavra == palavra1 \
        or cor2 == ':green_circle:' and palavra == palavra2 \
        or cor3 == ':green_circle:' and palavra == palavra3:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00b2ff)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
            await msg.edit(embed=embedF)
    elif tentativa == 'Laranja' or tentativa == 'laranja':
        if cor1 == ':orange_circle:' and palavra == palavra1 \
        or cor2 == ':orange_circle:' and palavra == palavra2 \
        or cor3 == ':orange_circle:' and palavra == palavra3:
            pontos = 1
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f'UPDATE userid SET points = points + {pontos} WHERE id="{user_id}"')
            conn.commit()
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00b2ff)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
            await msg.edit(embed=embedF)

    else:
      embedF = discord.Embed(title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0xc50b0b)
      await ctx.reply('Você errou! :rofl:')
      await msg.edit(embed=embedF)
      
@bot.command()
async def niilismo(ctx):
        await ctx.reply(random.choice(nilismo) + str(' - Friedrich Nietzsche'), mention_author=False)
        async with aiohttp.ClientSession() as session:
          async with session.get('https://c.tenor.com/6oSEDVpeB-YAAAAd/dies-of-cringe-cringe.gif') as resp:
              if resp.status != 200:
                  return await ctx.send('O bot não conseguiu baixar a imagem...')
              data = io.BytesIO(await resp.read())
              await ctx.send(file=discord.File(data, 'danilao.gif'))
@bot.command()
async def previsao(ctx):
        await ctx.send('**!previsao** agora é **!tempo**')
# MATRIZES PARA ESTATISTICA
@bot.command()
async def matriz(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Matrizes para Estatística: ' +
                 'https://meet.google.com/ptx-urqy-bhc')
        await ctx.channel.send(quote, delete_after=200.0)
# DEMOGRAFIA
@bot.command()
async def demografia(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Demografia: ' +
                 'https://meet.google.com/gvv-cpby-vie')
        await ctx.channel.send(quote, delete_after=200.0)

# PROB 2
@bot.command()
async def prob2(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Probabilidade 2: ' +
                 'http://meet.google.com/mpn-oarf-bhz')
        await ctx.channel.send(quote, delete_after=200.0)

# METODOS NAO PARAMETRICOS
@bot.command()
async def metodos(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Métodos não paramétricos: ' +
                 'https://meet.google.com/nop-wfbe-rwd')
        await ctx.channel.send(quote, delete_after=200.0)

# INFERENCIA
@bot.command()
async def inferencia(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Inferência I: ' +
                 'https://meet.google.com/uvg-mnfj-fjq')
        await ctx.channel.send(quote, delete_after=200.0)

# CALCULO NUMERICO
@bot.command()
async def calcnum(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Calculo Numerico: ' +
                 'https://meet.google.com/noy-vwwh-oha')
        await ctx.channel.send(quote, delete_after=200.0)

# TOPICOS DE ESTATISTICA
@bot.command()
async def topicos(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Topicos em Estatistica: ' +
                 'https://meet.google.com/mwm-rxcf-uma')
        await ctx.channel.send(quote, delete_after=200.0)

# CONTROLE ESTATISTICO DE QUALIDADE
@bot.command()
async def controle(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Controle Estatístico de Qualidade: ' +
                 'https://meet.google.com/hzy-gkir-wbq')
        await ctx.channel.send(quote, delete_after=200.0)
        

# CALC INTEGRAL
@bot.command()
async def calc(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Calculo Integral: ' +
                 'https://meet.google.com/non-jaue-nya')
        await ctx.channel.send(quote, delete_after=200.0)

@bot.command()
async def aulas(ctx):
  embedA = discord.Embed(
        title="Links das aulas", description='**!controle** - Controle Estatístico de Qualidade\n**!topicos** - Tópicos em Estatística\n**!calcnum** - Cálculo Numérico\n**!calc** - Cálculo Integral\n**!inferencia** - Inferência I\n**!metodo** - Métodos não Paramétricos\n**!prob2** - Probabilidade II\n**!matriz** - Matrizes para Estatística\n**!demografia** - Demografia', color=0x00b2ff)
  imagem_url = 'https://cfoc.org/wp-content/uploads/2014/11/click-or-not-suspicious-link-1140x500@2x.jpg'
  embedA.set_thumbnail(url=imagem_url)
  await ctx.send(embed=embedA)

# RPG
@bot.command()
async def rpg(ctx):
    monster = ['Rato gordo', 'Ogro primo do shrek', 'Dragão voador que gospe fogo e tudo mais', 'Gosma verde']
    monstro = random.choice(monster)

    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    espada = 25
    bonk = 35
    arco = 30
    espada_preco = 100
    bonk_preco = 100
    arco_preco = 100
    bonoros = 100
    embedA = discord.Embed(
        title=f"Role play - Você começa com {bonoros} bonoros. Escolha uma arma: ", description=f'``Espada``: ``{espada_preco}``\n``Bonk``: ``{bonk_preco}``\n``Arco``: ``{arco_preco}`` ', color=0x00ff00)
    await ctx.send(embed=embedA)
    while bonoros != 0:
        resp = await bot.wait_for('message', check=check)
        resposta = str(resp.content)
        if resposta == 'Espada' or resposta == 'espada':
            arma = espada
            bonoros -= espada_preco 
        elif resposta == 'bonk' or resposta == 'Bonk':
            arma = bonk
            bonoros -= bonk_preco
        elif resposta == 'Arco' or resposta == 'arco':
            arma = arco
            bonoros -= arco_preco
        if bonoros == 0:
            break
        else:
            continue
    vida_monstro = 100
    vida_player = 100
    ataque_monstro = 20
    await ctx.send(f'Um ``{monstro}`` apareceu! Quer atáca-lo?')
    res = await bot.wait_for('message', check=check)
    resposta = str(res.content)
    if resposta == 'sim' or res == 'Sim':
            while vida_player > 0 and vida_monstro > 0:
                vida_monstro -= arma
                if vida_player <= 0:
                    await ctx.reply('Você morreu!')
                    break
                if vida_monstro <= 0:
                    await ctx.reply(f'Você conseguiu matar o ``{monstro}``!')
                    break
                if arma == bonk:
                    async with aiohttp.ClientSession() as session:
                        async with session.get('https://i.imgur.com/LmEFXsV.jpg') as resp:
                            if resp.status != 200:
                                return await ctx.send('O bot não conseguiu baixar o arquivo de imagem...')
                            data = io.BytesIO(await resp.read())
                            await ctx.send(file=discord.File(data, 'eaquilo.jpg'))
                await ctx.send(f'Você tirou ``{arma}`` de vida dele! Agora ele tem ``{vida_monstro}`` de vida! É a vez dele agora!')
                time.sleep(2)
                vida_player -= ataque_monstro
                await ctx.send(f'Ele te atacou e tirou ``{ataque_monstro}`` sua! Agora você tem ``{vida_player}`` de vida!')
                await ctx.send(f'Você deseja continuar atacando ou correr que nem um ||marica||? Responda com atacar ou correr.')
                res = await bot.wait_for('message', check=check)
                resposta = str(res.content)
                if resposta == 'atacar':
                    continue
                else:
                    await ctx.send('kkkkkkk correu')
                    break
                
    else:
        await ctx.send('blz flw')
# ROLETA RUSSA

@bot.command()
async def roleta(ctx):
    if ctx.author == bot.user:
        return
    nomes = ['Joaquim','Betânia','Amarildo','Cleyton','Cleitin da Kombi','Weeb da Silva','Maria','Naruto','Sasque','Takeshi']
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    def no_douplicates(x):
        return list(dict.fromkeys(x))
    players = []
    embedA = discord.Embed(
        title=f"Roleta Russa. ", description=f'Diga bot para jogar contra o bot ou jogadores para jogar contra outros jogadores', color=0x00ff00)
    await ctx.send(embed=embedA)
    jogador_sozinho = await bot.wait_for('message', check=check)
    jogar_sozinho = jogador_sozinho.content
    if jogar_sozinho == 'bot' or jogar_sozinho == 'Bot':
        players.append(str(jogador_sozinho.author.name))
        while len(players) != 6:
            players.append(random.choice(nomes))
            players = no_douplicates(players)
            if len(players) == 6:
                break
    elif jogar_sozinho == 'Jogadores' or jogar_sozinho == 'jogadores':
        while len(players) != 6:
            await ctx.send('Digite eu para participar. Se não tiver jogadores suficientes, digite bot para o bot completar a lista.')
            resp = await bot.wait_for('message')
            response = resp.content
            if response == 'eu' or response == 'Eu':
                players.append(str(resp.author.name))
                await ctx.send(f'Jogadores atuais: {players}')
                continue
            if response == 'bot' or response == 'Bot':
                while len(players) != 6:
                    players.append(random.choice(nomes))
                    players = no_douplicates(players)
                    if len(players) == 6:
                        break
    else:
      await ctx.send('tente novamente.')            
        
    bullet = ['a', 'b', 'c', 'd', 'e', 'f']
    chances = 0
    await ctx.send(f'Jogadores atuai: {players}')
    while len(players) != 1:
        jogadores = random.sample(players, len(players))
        bala = random.choice(bullet)
        jogador = random.choice(jogadores)
        if chances == 0:
            await ctx.send(f'o primeiro a tentar a sorte vai ser: {jogador}')
        else:
            await ctx.send(f'O próximo a tentar a sorte vai ser: {jogador}')
        time.sleep(2)
        if bala == 'd' or bala == 'a' or bala == 'c':
            chances += 1
            await ctx.reply(f'O jogador {str(jogador)} morreu!')
            players.remove(jogador)
            if len(players) == 1:
                await ctx.send(f'O {str(players[0])} venceu! :partying_face:')
                break
            if len(players) == 0:
                await ctx.reply('Nenhum jogador restou.')
                break
            else:
                continue
        else:
            chances += 1
            if len(players) > 0:
                await ctx.send(f'O {jogador} continua vivo! Diga **girar** para continuar!')
                girar = await bot.wait_for('message', check=check)
                girar_tambor = girar.content
                if girar_tambor == 'girar' or girar_tambor == 'Girar':
                    continue
                else:
                    await ctx.send('blz')
                    break
        if len(players) == 0:
                chances += 1
                await ctx.reply('Nenhum jogador restou.')
                break
       
# IMAGEM ALEATÓRIA
@bot.command()
async def imagem(ctx):
  url = f'https://www.generatormix.com/random-image-generator'
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  get_image = doc.find(class_='col-12 tile-block group')
  src_image = get_image.find(class_='thumbnail-col-1')
  get_src = str(src_image).split('src=')[1].replace('"','')
  await ctx.send(get_src)
  
# PREVISÃO DO TEMPO
@bot.command()
async def tempo(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.send('Você deseja saber o tempo de agora ou a previsão da semana? Responda com **semana** ou **agora**.')
  i = True
  while i:
    resp = await bot.wait_for('message', check=check)
    response = resp.content
    if response == 'agora' or response == 'Agora':
      agora = True
      i = False
    elif response == 'semana' or response == 'Semana':
      agora = False
      i = False
    else:
      await ctx.send('Não entendi. Digite novamente.')
      continue

  # Lê o html da página 
  url = f'https://www.tempo.com/goiania.htm'
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  try:
      div = doc.find(class_='dos-semanas nuevo-1')
      datas = div.find(class_='datos-dos-semanas')
  except:
      try:
        div = doc.find(class_='dos-semanas nuevo-2')
        datas = div.find(class_='datos-dos-semanas')
      except:
        try:
          div = doc.find(class_='dos-semanas nuevo-3')
          datas = div.find(class_='datos-dos-semanas')
        except:
          try:
            div = doc.find(class_='dos-semanas nuevo-4')
            datas = div.find(class_='datos-dos-semanas')
          except:
            try:
              div = doc.find(class_='dos-semanas nuevo-5')
              datas = div.find(class_='datos-dos-semanas')
            except:
              try:
                div = doc.find(class_='dos-semanas nuevo-6')
                datas = div.find(class_='datos-dos-semanas')
              except:
                try:
                  div = doc.find(class_='dos-semanas nuevo-7')
                  datas = div.find(class_='datos-dos-semanas')
                except:
                  try:
                    div = doc.find(class_='dos-semanas noche-nuevo')
                    datas = div.find(class_='datos-dos-semanas')
                  except:
                    await ctx.send('erro no bot alguém me desconfiguro')

  if agora == True:
    # Pegar as informações do dia atual
    div_temp = doc.find(class_='datos-estado-actual')
    real_div = div_temp.find(class_='principal')
    dia = datas.find(class_=f'dia d1 activo')
    item_temp = dia.find(class_='temperatura')
    temp_max_found = item_temp.find(class_='maxima changeUnitT')
    temp_min_found = item_temp.find(class_='minima changeUnitT')
    temp_max = str(temp_max_found).split('>')[1].split('<')[0]
    temp_min = str(temp_min_found).split('>')[1].split('<')[0]
    sensacao_search = real_div.find(class_='sensacion changeUnitT')
    sensacao_found = str(sensacao_search).split('>')[2].split('<')[0]
    # Procura pela temperatura atual
    temp_search = real_div.find(class_='temperatura')
    temp_found = temp_search.find(class_='dato-temperatura changeUnitT')
    temperatura_atual = str(temp_found).split('>')[1].split('<')[0]
    dia = datas.find(class_=f'dia d1 activo') 
    # Procura pela probabilidade de chuva, caso tenha
    try:
        chuva = dia.find(class_='prediccion')
        chuva_get = chuva.find(class_='probabilidad-lluvia')
        chuva_porc = str(chuva_get).split('>')[1].split('<')[0].replace(' ', '')
    except:
        chuva_porc = '0%'
    chuva_porc_imagem = chuva_porc.replace('%', '')
    chuva_porc_imagem_num = int(chuva_porc_imagem)
    embedT = discord.Embed(title='Tempo agora - Goiânia',
                  description=f'Agora está fazendo **{temperatura_atual}** com a sensação térmica de **{sensacao_found}**.\nA temperatura máxima de hoje é de **{temp_max}** e a mínima de **{temp_min}**.\nA chance de chover hoje é de **{chuva_porc}**.', color=0x00b2ff)
    if chuva_porc_imagem_num < 50 and chuva_porc_imagem_num >= 30:
      imagem_url = 'https://images.emojiterra.com/google/android-11/512px/1f327.png'
      embedT.set_thumbnail(url=imagem_url)
    elif chuva_porc_imagem_num > 50:
      imagem_url = 'https://www.nicepng.com/png/full/9-91464_thunder-lightning-clip-art-thunder-and-lightning-clipart.png'
      embedT.set_thumbnail(url=imagem_url)
    elif chuva_porc_imagem_num < 30:
      imagem_url = 'https://images.emojiterra.com/openmoji/v12.2/512px/26c5.png'
      embedT.set_thumbnail(url=imagem_url)
    await ctx.reply(embed=embedT)

  else:
    num = 1
    items_found = {}
    for num in range(1,7):
        if num == 1:
            dia = datas.find(class_=f'dia d{num} activo')  
        else:
            dia = datas.find(class_=f'dia d{num}')
        try:
          chuva = dia.find(class_='prediccion')
          chuva_get = chuva.find(class_='probabilidad-lluvia')
          chuva_porc = str(chuva_get).split('>')[1].split('<')[0].replace(' ', '')
        except:
          chuva_porc = '0%'
        div_temp = doc.find(class_='datos-estado-actual')
        chuva_porc_imagem = chuva_porc.replace('%', '')
        chuva_porc_imagem_num = int(chuva_porc_imagem)
        item_temp = dia.find(class_='temperatura')
        temp_max_found = item_temp.find(class_='maxima changeUnitT')
        temp_min_found = item_temp.find(class_='minima changeUnitT')
        temp_max = str(temp_max_found).split('>')[1].split('<')[0]
        temp_min = str(temp_min_found).split('>')[1].split('<')[0]
        data_found = dia.find(class_='cuando')
        data = str(data_found).split('>')[1].split('<')[0]
        items_found[num] = {'Data': data, 'Temp Max': temp_max,'Temp Min': temp_min, 'Chuva': chuva_porc, 'Chuva Imagem': chuva_porc_imagem_num}
        num += 1
    sorted_items = items_found.items()
    for item in sorted_items:
      embedVar = discord.Embed(
                  title=f'{item[1]["Data"]}', description='', color=0x00ff00)
      embedVar.add_field(name='Temperatura Max', value=f"**{item[1]['Temp Max']}**")
      embedVar.add_field(name='Temperatura Min', value=f"**{item[1]['Temp Min']}**")
      embedVar.add_field(name='Chance de chover', value=f"**{item[1]['Chuva']}**")
      if int(item[1]['Chuva Imagem']) == 50:
        imagem_url = 'https://images.emojiterra.com/google/android-11/512px/1f327.png'
        embedVar.set_thumbnail(url=imagem_url)
      elif int(item[1]['Chuva Imagem']) > 50:
        imagem_url = 'https://www.nicepng.com/png/full/9-91464_thunder-lightning-clip-art-thunder-and-lightning-clipart.png'
        embedVar.set_thumbnail(url=imagem_url)
      elif int(item[1]['Chuva Imagem']) < 50:
        imagem_url = 'https://images.emojiterra.com/openmoji/v12.2/512px/26c5.png'
        embedVar.set_thumbnail(url=imagem_url)
      await ctx.send(embed=embedVar)
    
# COMANDO AJUDA
@bot.command()
async def comandos(ctx):
  embedVar = discord.Embed(
                          title="!comandos", description=f'``!rank``\n=> Ranking de pontos.\n\n``!mercadolivre``\n=> O bot realiza um webscraping em tempo real no site __Mercado Livre__. Nisto, você poderá pesquisar qualquer produto que esteja disponível e filtrar os resultados pelo preço.\n\n``!previsao``\n=> O bot realiza um web scraping em um site de previsão do tempo. Retorna a temperatura máxima, mínima e seus determinados dias.\n\n``!imagem``\n=> O bot manda uma imagem aleatória buscada por web scraping.\n\n``!cinema``\n=> Dê um nome de algum filme para o bot e ele retornará as notas que o filme recebeu de acordo com o site ``Adoro Cinema``.\n\n``!anime``\n=> Web Scraping no site MyAnimeList, o bot retorna a nota que o anime/manga recebeu.\n\n``!doguinho``\n=> doguinho fofo lindo\n\n``!significado``\n=> Quer saber o que significa Dacriocistossiringotomia? O bot vai te falar!\n\n``!ping``\n=> Teste para saber se o bot ainda está ativo no servidor do replit.\n\n``!rpg``\n=>role play\n\n``!loteria``\n=> O bot fará uma seleção de 6 números aleatórios. Cabe ao jogador apostar 6 números distintos para tentar a sorte ||de ganhar nada||.\n\n``!roleta``\n=> Roleta russa. Um tambor de 6 entradas e 1 bala girará. O bot irá rodar os jogadores aleatoriamente e disparará o gatilho. Ganha quem ficar vivo até o final. O jogador poderá escolher jogar contra outros 5 jogadores ou contra o bot.\n\n``!mm``\n=> Jogo do mais, igual ou menos. O bot escolherá um número aleatório e dará uma dica. Tal dica será um número supostamente perto do __número secreto__. Cabe ao jogador escolher as seguintes opções: o número secreto ser maior que a dica, o número secreto ser menor que a dica ou o número secreto ser igual a dica.\n\n``!pdt``\n=> Pedra, papel e tesoura.\n\n``!dados``\n=> Jogue dois dados e torça para pelo menos um deles cair com o número 1.\n\n``!cores``\n=> O bot colocará uma palavra aleatória na frente de uma cor aleatória. Após determinado tempo, o bot ocultará as palavras e as cores e, então, perguntar ao jogador qual cor se designava determinada palavra.\n\n``!bd, !al, !prob, !calc2``\n=> O bot mandará o link do meet para a aula determinada pelo usuário.\n\n``!dirso``\n=> Simplesmente dirso.\n\n``!op``\n=> O bot escolherá uma operação matemática aleatória entre números aleatórios. Acerte e não seja zoado pelo bot.\n\n``!forca``\n=> Jogo da forca.\n\n``!niilismo``\n=> cringe.', color=0xc50b0b)
  await ctx.send(embed=embedVar)
  
# MERCADO LIVRE SCRAPING

@bot.command()
async def mercadolivre(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  # Parâmetros para a pesquisa
  await ctx.reply('Qual produto você quer pesquisar?')
  tag_resp = await bot.wait_for('message', check=check)
  tag = tag_resp.content
  await ctx.send('Deseja filtar os produtos pelo preço? Responda com sim ou não.\nObs: o bot recomenda que filtre os produtos pelo preço para não floodar o canal em que foi chamado.')
  filtro_res = await bot.wait_for('message',check=check)
  if filtro_res.content == 'sim' or filtro_res.content == 'Sim' or filtro_res.content == 'S' or filtro_res.content == 's':
    filtro = True
  else:
    filtro = False
  if ' ' in tag:
    tag_search = tag.replace(' ', '-')
  else:
    tag_search = tag
  url = f'https://lista.mercadolivre.com.br/{tag_search}'

  if filtro == True:
    await ctx.send('Qual o valor máximo que deseja filtrar? Digite um número inteiro.')
    max_pr = await bot.wait_for('message', check=check)
    max_price = max_pr.content
    await max_pr.add_reaction('👍')
    await ctx.send('Qual o valor mínimo que deseja filtrar? Digite um número inteiro.')
    min_pr = await bot.wait_for('message', check=check)
    min_price = min_pr.content
    await min_pr.add_reaction('👍')
  # Ler o HTML da página
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  items_found = {}
  # Procurar pela classe que contém apenas os resultados da pesquisa
  div = doc.find(class_='ui-search-results')
  item_search = tag.split(' ')
  if len(item_search) >= 2:
    item_search = item_search[0]
  else:
    item_search = tag_search
  # Procura somente os items que contém o texto que o usuário determinou
  try:
    items = div.find_all(text=re.compile(item_search, re.IGNORECASE))
  except:
    items = False
  if items != False:
      for item in items:
        # Procura pela árvore que contém o item 
        try:
            next_parent = item.find_parent(class_='ui-search-layout__item')
        except:
            await ctx.send('.')
        try:
          frete_search = next_parent.find(class_='ui-search-item__group ui-search-item__group--shipping')
          frete_found = str(frete_search).split('>')[3].split('<')[0]
          if frete_found != 'Frete grátis':
            frete = 'Pago'
          else:
            frete = frete_found
        except:
          frete = 'Pago'
        # Procura o link que está dentro da árvore - Este será o link do item
        try:
            links = next_parent.find(class_='ui-search-result__image')
            link_get = str(links).split('<a')[1].split('title')[-2].split('href')[1].split('=')[1]
            link_new = link_get.split('//')[1]
            if link_new[0] == 'p' or link_new[1] == 'w' or link_new[0] == 'm' or link_new[0] == 'c':
              if 'click1' not in link_new:
                link = link_get
              else:
                link = 'o bot não conseguiu encontrar o link'
            else:
              link = 'o bot não conseguiu encontrar o link'
        except:
            link = 'o bot não conseguiu encontrar o link'
        # Procura pela fonte da imagem que está dentro da árvore
        try:
            image_src = links.find(class_='carousel-container arrow-visible')
            link_image = str(image_src).split('src=')[1].split('height')[0].replace('"','')
        except:
            link_image = 'https://cdn.pixabay.com/photo/2017/04/09/12/45/error-2215702_960_720.png'
        # Procura pelo preço do item dentro da árvore
        try:
            prices = next_parent.find(class_="price-tag-fraction")
            price = str(prices).split('>')[-2].split('<')[0]
            items_found[item] = {'price': price.replace(",", ""),'link': link.replace('"',''), 'image': link_image, 'frete': frete}
        except:
            price = 'preço não encontrado'

      sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
      num_items = 0
      for item in sorted_items:
        if filtro == True:
          try:
              if int(item[1]['price'].replace('.', '')) <= int(max_price) and int(item[1]['price'].replace('.', '')) >= int(min_price):
                num_items += 1
                embedVar = discord.Embed(
                            title=f"{item[0]}", color=0x121274)
                embedVar.add_field(name='Valor do item', value=f"**R${item[1]['price']}**")
                embedVar.add_field(name='Link do item', value=f" {item[1]['link']}")
                embedVar.add_field(name='Frete', value=f" **{item[1]['frete']}**")
                embedVar.set_thumbnail(url=f"{item[1]['image']}")
                await ctx.channel.send(embed=embedVar)
          except:
            await ctx.send('quebrei')
        else:
          embedVar = discord.Embed(
                      title=f"{item[0]}", color=0x121274)
          embedVar.add_field(name='Valor do item', value=f"**R${item[1]['price']}**")
          embedVar.add_field(name='Link do item', value=f" {item[1]['link']}")
          embedVar.add_field(name='Frete', value=f" **{item[1]['frete']}**")
          embedVar.set_thumbnail(url=f"{item[1]['image']}")
          await ctx.channel.send(embed=embedVar)
          
      if filtro == True:
        if num_items >= 1:
              await ctx.send(f'Estes foram os ``{num_items}`` resultados da minha busca filtrada!')
        else:
              await ctx.send(f'Não consegui encontrar ``{tag}`` filtrado em ``R${max_price}``. Aumente o valor do filtro ou escreva o nome do produto de outra forma.')
      else:
        if len(items_found) >= 1:
              await ctx.send(f'Estes foram os ``{len(items_found)}`` resultados da minha busca!')
        elif len(items_found) == 0:
              await ctx.send(f'Infelizmente não consegui encontrar ``{tag}``. Por favor, me chame novamente e tente escrever o nome do produto de outra forma.')
  else:
    await ctx.send(f'Infelizmente não consegui encontrar ``{tag}``. Por favor, me chame novamente e tente escrever o nome do produto de outra forma.')


# PING

@bot.command()
async def ping(ctx):
  await ctx.send('https://gifimage.net/wp-content/uploads/2018/11/small-might-gif.gif')

# MEMBRO NOVO

@bot.event
async def on_member_join(member):
    channel = get(member.guild.channels, name="🗣-discussões-gerais")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/Crw2Gvs.png') as resp:
            if resp.status != 200:
                return await channel.send('O bot não conseguiu baixar a imagem...')
            data = io.BytesIO(await resp.read())
    await channel.send(member.mention, file=discord.File(data, 'danilao.png'))

@bot.event
async def on_message(message):
    def check(res):
        return message.author == res.author and res.channel == message.channel
    await bot.process_commands(message)
    msg = message.content
    if message.author == bot.user:
        return
    # Nome ou id do usuário 
    user_id = str(message.author).split('#')[0]
    # Conectando ao banco de addos
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    # Selecionando o id da tabela userid
    cur.execute(f'SELECT id FROM userid WHERE id="{user_id}"')
    # Checa se tal id já existe no banco de dados, se não existir ele cria um novo
    result = cur.fetchone()
    if result is None:
      # Ignora se o usuário é um bot ou o próprio Bot do Link
      if message.author == bot.user:
        return
      elif message.author.bot:
        return
      else:
        # Insere o id do novo usuário dentro do banco de dados
        cur.execute('INSERT INTO userid (id) VALUES (?)', (user_id, ))
        print(f'{user_id} foi adicionado ao banco')
        # Atualiza o banco de dados
        conn.commit()
    
    if any(word in msg for word in sad_words):
        async with aiohttp.ClientSession() as session:
          async with session.get('https://c.tenor.com/iq2DpeeqfugAAAAC/ganbatte-butterfly-estate.gif') as resp:
              if resp.status != 200:
                  return await message.send('O bot não conseguiu baixar a imagem...')
              data = io.BytesIO(await resp.read())
        await message.reply(file=discord.File(data, 'gambate.gif'))
    if message.content.startswith('me da o meu id ai bot'):
        await message.channel.send(message.author.id)
    if message.content.startswith('salve bot'):
        await message.reply('salve cachorro')
    if message.content.startswith('quem é o mais lindo'):
      pessoas = ['danilo', 'gabs',' vinihomem', 'dori', 'eu']
      extra = ['é claro uai', 'é o mais lindo com certeza', 'com certeza']
      people = random.choice(pessoas)
      extra2 = random.choice(extra)
      if people == 'eu':
        extra2 = 'sou o mais lindo'
        await message.channel.send(f'{people} {extra2}')
      else:
        await message.channel.send(f'{people} {extra2}')
    if message.content.startswith('bot burro'):
        palavras = ['teu pai', 'quem?','q-que eu fiz de errado?', 'd-desculpa :pensive:','quem?','quem?','quem?','quem?']
        palavra = random.choice(palavras)
        await message.reply(f'{palavra}')
        if palavra == 'quem?':
            res = await bot.wait_for('message',check=check)
            response = res.content
            if response == 'você' or response == 'Você':
                await message.channel.send('te perguntoukkkkkkkkkkkkkkkkkkk')
            else:
                return
    if message.content.startswith('bot lindo'):
        await message.reply('<:sapo_amor:846410960666361890>')
    if message.content.startswith('tchau bot'):
        await message.channel.send('flws :wave:')
    quotes_musical = 'TAKE ME HOMEEEEEEEEEEEE, ITS THE ONLY PLACE I CAN REST IN PIECEEEEEE'
    trigger_musical = ['take']
    for word in trigger_musical:
        if word in message.content:
            resposta = quotes_musical
            await message.reply(resposta, mention_author=False)
            await message.channel.send(file=discord.File("D:\Área de Trabalho\pyhonn\pepe_singing.jpg"))
    quotes = 'cringe'
    trigger = ['niilismo', 'Nilismo', 'Niilismo']
    for word in trigger:
        if message.content == '!niilismo':
            break
        else:
            if word in message.content:
                resposta = quotes
                await message.reply(resposta, mention_author=False)
                break
keep_alive()
bot.run(cod)


