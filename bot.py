import asyncio
from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY
import contextlib
from typing import *
import discord
from discord.ext.commands.bot import Bot
from discord.ext import commands
from discord_components import *
import requests
import json
import random
import time
import asyncpg
import musical
from asyncio import TimeoutError
from keep_alive import keep_alive


bot = ComponentsBot(command_prefix='!', intents=discord.Intents.all())
cogs = [musical]
for i in range(len(cogs)):
  cogs[i].setup(bot)
sad_words = ['Eu não consigo, bot', 'Estou triste', 'que tristeza']
nilismo = ["A filosofia é o exílio voluntário entre montanhas geladas.", "Nós, homens do conhecimento, não nos conhecemos; de nós mesmo somos desconhecidos.", "Não me roube a solidão sem antes me oferecer verdadeira companhia.", "O amor é o estado no qual os homens têm mais probabilidades de ver as coisas tal como elas não são.", "Como são múltiplas as ocasiões para o mal-entendido e para a ruptura hostil!", "Deus está morto. Viva Perigosamente. Qual o melhor remédio? - Vitória!", "A diferença fundamental entre as duas religiões da decadência: o budismo não promete, mas assegura. O cristianismo promete tudo, mas não cumpre nada.", "Quando se coloca o centro de gravidade da vida não na vida mas no além - no nada -, tira-se da vida o seu centro de gravidade.", "Para ler o Novo Testamento é conveniente calçar luvas. Diante de tanta sujeira, tal atitude é necessária.",
           "O cristianismo foi, até o momento, a maior desgraça da humanidade, por ter desprezado o Corpo.", "E aqueles que foram vistos dançando foram julgados insanos por aqueles que não podiam escutar a música.", "A moralidade é o instinto do rebanho no indivíduo.", "O idealista é incorrigível: se é expulso do seu céu, faz um ideal do seu inferno.", "Em qualquer lugar onde encontro uma criatura viva, encontro desejo de poder.", "Um político divide os seres humanos em duas classes: instrumentos e inimigos.", "Quanto mais me elevo, menor eu pareço aos olhos de quem não sabe voar. ", "Torna-te quem tu és!", "Aquele que luta com monstros deve acautelar-se para não tornar-se também um monstro. Quando se olha muito tempo para um abismo, o abismo olha para você.", "A alma nobre tem reverência por si mesma.", "Não existem fenômenos morais, mas apenas uma interpretação moral dos fenômenos."]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f'Loguei como {bot.user}!')

    
# ROLETA RUSSA

@bot.command()
async def roleta(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    players = []
    embedA = discord.Embed(
        title=f"Roleta Russa. ", description=f'O tambor de uma arma irá girar, os jogadores que quiserem participar devem mandar eu', color=0x00ff00)
    await ctx.send(embed=embedA)
    while len(players) != 2:
        res = await bot.wait_for('message')
        response = res.content
        if response == 'eu' or response == 'a':
            players.append(str(res.author.name))
            await ctx.send(f'Jogadores atuais: {players}')
            continue
        if len(players) == 2:
            break
    bullet = ['a', 'b', 'c', 'd', 'e', 'f']
    chances = 0
    while len(players) != 1:
        jogadores = random.sample(players, len(players))
        bala = random.choice(bullet)
        jogador = random.choice(jogadores)
        if chances == 0:
            await ctx.send(f'a bala vai comer - o primeiro a tentar a sorte vai ser: {jogador}')
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
                await ctx.send(f'O {jogador} ||infelizmente|| não morreu! Diga ||girar|| para girar o tambor novamente!')
                kao = await bot.wait_for('message')
                kaoo = kao.content
                if kaoo == 'girar' or kaoo == 'Girar':
                    continue
                else:
                    await ctx.send('blz')
                    break
        if len(players) == 0:
                chances += 1
                await ctx.reply('Nenhum jogador restou.')
                break
            

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
        title=f"Role play - Você começa com {bonoros} bonoros. Escolha uma arma: ", description=f'Espada: {espada_preco}\nBonk: {bonk_preco}\nArco: {arco_preco} ', color=0x00ff00)
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
    await ctx.send(f'Um {monstro} apareceu! Quer atáca-lo?')
    res = await bot.wait_for('message', check=check)
    resposta = str(res.content)
    if resposta == 'sim' or res == 'Sim':
            while vida_player > 0 and vida_monstro > 0:
                vida_monstro -= arma
                if vida_player <= 0:
                    await ctx.reply('Você morreu!')
                    break
                if vida_monstro <= 0:
                    await ctx.reply(f'Você conseguiu matar o {monstro}!')
                    break
                if arma == bonk:
                    await ctx.send(file=discord.File('D:\Área de Trabalho\pyhonn\zonk.jpg'))
                await ctx.send(f'Você tirou {arma} de vida dele! Agora ele tem {vida_monstro} de vida! É a vez dele agora!')
                time.sleep(2)
                vida_player -= ataque_monstro
                await ctx.send(f'Ele te atacou e tirou {ataque_monstro} sua! Agora você tem {vida_player} de vida!')
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

# AL
@bot.command()
async def al(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Algebra Linear: ' +
                 'http://meet.google.com/uoy-bwyx-amo')
        await ctx.channel.send(quote, delete_after=30.0)

# CAL2
@bot.command()
async def calc2(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Cálculo 2: ' +
                 'http://meet.google.com/rts-sene-itn')
        await ctx.channel.send(quote, delete_after=30.0)
# BD
@bot.command()
async def bd(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Bando de Dados: ' +
                 'https://meet.google.com/xcw-eexd-pph')
        await ctx.channel.send(quote, delete_after=30.0)
# PROB
@bot.command()
async def prob(ctx):
        quote = (ctx.author.mention + ' tome aqui o link de Probabilidade: ' +
                 'https://meet.google.com/lookup/eslvyzohyi?authuser=1&hs=179')
        await ctx.channel.send(quote, delete_after=30.0)

# QUOTE
@bot.command()
async def frase(ctx):
        quote = get_quote()
        await ctx.channel.send(quote)
 
# NIILISMO

@bot.command()
async def niilismo(ctx):
        await ctx.reply(random.choice(nilismo) + str(' - Friedrich Nietzsche'), mention_author=False)

# JOGO DA FORCA

@bot.command()
async def forca(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    if ctx.author == bot.user:
        return
    words_animal = ['RINOCERONTE','ELEFANTE','GIRAFA','CROCODILO','PANDA','RATO','MACACO']
    words_amigos = ['VINIBOYOLA','DORI','THIELLY','DANILO','PANDA']
    word_choiced = [words_animal, words_amigos]
    word_ch = random.choice(word_choiced)
    word = random.choice(word_ch)
    digitadas = []
    chances = 6
    if word_ch == words_amigos:
        x = 'membro da família Estatisticamente Inviável'
    else:
        x = 'animal'
    embedG = discord.Embed(
        title="Jogo da forca! ", description=f'||a letra deve estar em caixa alta||\nA palavra tem {len(word)} letras! Dica: é um {x}.', color=0x00ff00)
    await ctx.send(embed=embedG)
    while True:
        resp = await bot.wait_for('message', check=check)
        tentativa = str(resp.content)
        letra = tentativa
        if len(letra) > 1:
            await ctx.reply('Apenas uma letra.')
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
            await ctx.reply('Você ganhou!')
            await ctx.send(f'A palavra era {word}')
            break
        else:
            if chances <= 0:
                await ctx.reply('Você perdeu!')
                await ctx.send(f'A palavra era {word}')
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
    palavras = ['abacate', 'feijoada',
                'viniboyola', 'celular', 'liquidificador']
    embedVar = discord.Embed(title="Joguinho das cores",
                             description='O bot colocará uma cor aleatória do lado de uma palavra aleatória. Responda escrevendo a sua cor e ganhe ||nada||', color=0x00ff00)
    await ctx.reply(embed=embedVar)
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
    lista = [palavra1, palavra2, palavra3]
    palavra = random.choice(lista)
    embedG = discord.Embed(
        title="Atenção:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
    msg = await ctx.send(embed=embedG)
    embedE = discord.Embed(
        description=f'Qual era a cor da palavra {palavra}?', color=0x00ff00)
    time.sleep(8)
    await msg.edit(embed=embedE)
    res = await bot.wait_for('message',check=check)
    tentativa = str(res.content)
    if tentativa == 'Amarelo' or tentativa == 'amarelo':
        if cor1 == ':yellow_circle:' and palavra == palavra1 or cor2 == ':yellow_circle:' and palavra == palavra2 or cor3 == ':yellow_circle:' and palavra == palavra3:
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
    elif tentativa == 'Azul' or tentativa == 'azul':
        if cor1 == ':blue_circle:' and palavra == palavra1 \
        or cor2 == ':blue_circle:' and palavra == palavra2 \
        or cor3 == ':blue_circle:' and palavra == palavra3:
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
    elif tentativa == 'Vermelho' or tentativa == 'vermelho':
        if cor1 == ':red_circle:' and palavra == palavra1 \
        or cor2 == ':red_circle:' and palavra == palavra2 \
        or cor3 == ':red_circle:' and palavra == palavra3:
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
    elif tentativa == 'Verde' or tentativa == 'verde':
        if cor1 == ':green_circle:' and palavra == palavra1 \
        or cor2 == ':green_circle:' and palavra == palavra2 \
        or cor3 == ':green_circle:' and palavra == palavra3:
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
    elif tentativa == 'Laranja' or tentativa == 'laranja':
        if cor1 == ':orange_circle:' and palavra == palavra1 \
        or cor2 == ':orange_circle:' and palavra == palavra2 \
        or cor3 == ':orange_circle:' and palavra == palavra3:
            await ctx.reply('Você acertou! :partying_face:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)
        else:
            await ctx.reply('Você errou! :rofl:')
            embedF = discord.Embed(
        title="As cores eram:", description=f'{cor1} {palavra1}\n{cor2} {palavra2}\n{cor3} {palavra3}', color=0x00ff00)
            await msg.edit(embed=embedF)

#DIRSON

@bot.command()
async def dirso(ctx):
    adam_sandler = ['adam_sandler1', 'adam_sandler2', 'adam_sandler3', 'adam_sandler4', 'adam_sandler5',
                    'adam_sandler6', 'jim_carrey1', 'jim_carrey2', 'jim_carrey3', 'jim_carrey4', 'jim_carrey5', 'jim_carrey6']
    dirson = random.choice(adam_sandler)
    await ctx.send('Isto é dirso.')
    await ctx.send(file=discord.File(f'D:\Área de Trabalho\pyhonn\{dirson}.jpg'))

#MATH

@bot.command()
async def math(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    y = ['multiplicação', 'subtração', 'adição']
    op = random.choice(y)
    embedVar = discord.Embed(title="Joguinho de operações matemáticas",
                             description='O bot escolherá uma operação aleatória entre números aleatórios. Responda corretamente e ganhe ||nada||', color=0x00ff00)
    await ctx.channel.send(embed=embedVar)
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
# DADOS


@bot.command()
async def dados(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    gold = 2000
    embedVar = discord.Embed(title="Jogo dos Dados", description="Dois dados serão rodados. Se um dos dados der 1, você ganha 2x o valor que apostou. Se ambos os dados derem 1, você ganha 10x o valor que apostou. Se nenhum dos dados derem 1, você perde tudo que apostou.')", color=0x00ff00)
    embedVar.add_field(
        name="Situação", value=f"Você tem {gold} bonoros", inline=False)
    ##embedVar.add_field(name="Field2", value="hi2", inline=False)
    await ctx.channel.send(embed=embedVar)
    time.sleep(1)
    while gold >= 0:
        dado_1 = random.choice(range(1, 7))
        dado_2 = random.choice(range(1, 7))
        time.sleep(2)
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
                await ctx.channel.send('Taporra! Você conseguiu o olho do tigre! Agora você tem ' + str(gold) + str(' bonoros!'))
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
                time.sleep(2)
                await ctx.channel.send("Parabéns! Você conseguiu a metade de um olho de tigre! Agora você tem " + str(gold) + str(' bonoros!'))
                time.sleep(1)
                await ctx.channel.send(ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
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
                        await ctx.reply('VOCÊ PERDEU TUDO. O bot agradece a sua má sorte. Até a próxima! :wave:')
                        break
                    else:
                        await ctx.channel.send("Perdeu. Agora você só tem " + str(gold) + str(' bonoros, kkkkkkkkkkkkkkkkkkk'))

                else:
                    await ctx.channel.send("Você perdeu " + str(gold_bet2) + str(' bonoros.'))

                time.sleep(1)
                await ctx.channel.send(ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S' and gold > 0:
                    continue
                elif guess == 'S' and gold <= 0:
                    await ctx.reply('TU NÃO TEM NADA, METE O PÉ', mention_author=False)
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
                time.sleep(2)
                await ctx.channel.send("Parabéns, você conseguiu a metade de um olho de tigre! Agora você tem " + str(gold) + str(' de ouro!'))
                time.sleep(1)
                await ctx.channel.send(ctx.author.mention + ' quer continuar jogando? Responda com S ou N')
                response = await bot.wait_for('message',check=check)
                guess = str(response.content)
                if guess == 'S':
                    continue
                else:
                    await ctx.reply('vlw flw!', mention_author=False)
                    break

# LOTERIA


@bot.command()
async def loteria(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    await ctx.channel.send(ctx.author.mention + ' escolha 6 números de 1 a 100:')
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
        embedVar = discord.Embed(title="Resultado", color=0x00ff00)
        embedVar.add_field(name="Apostadas", value=str(answer1), inline=False)
        embedVar.add_field(name="Sorteadas", value=str(sort), inline=False)
        embedVar.add_field(name='Número de acertos', value=str(acertadas))
        await ctx.reply(embed=embedVar)
# MM


@bot.command()
async def mm(ctx):
    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel
    num = random.choice(range(10, 100))
    num_v = random.choice(range(1, 100))
    al = discord.Embed(title="Maior ou Menor",
                       description=f'O número aleatório é igual ou está perto de {num}', color=0x00ff00)
    fora = discord.Embed(
        title="Você não clicou a tempo, você está fora.", color=0x00ff00)
    vitoria = discord.Embed(title=f'{ctx.author.display_name} você ganhou!',
                            description=f'O bot escolheu {num_v}', color=0x00ff00)
    derrota = discord.Embed(title=f'{ctx.author.display_name} você perdeu!',
                            description=f'O bot escolheu {num_v}', color=0x00ff00)
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
                await m.edit(embed=vitoria, components=[])
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
                await m.edit(embed=vitoria, components=[])
        if player == 'Menor':
            if num_v > num:
                await m.edit(embed=derrota, components=[])
            elif num_v < num:
                await m.edit(embed=vitoria, components=[])
            elif num_v == num:
                await m.edit(embed=derrota, components=[])
    except TimeoutError:
        await m.edit(embed=fora, components=[])

# PEDRA PAPEL OU TESOURA


@bot.command()
async def pdt(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    choices = ['pedra', 'papel', 'tesoura']
    comp = random.choice(choices)
    ainda = discord.Embed(title="Pedra, papel ou tesoura.", color=0x00ff00)
    empate = discord.Embed(title="Empate!", color=0x00ff00)
    vitoria = discord.Embed(title=f'{ctx.author.display_name} você ganhou!',
                            description=f'O bot escolheu {comp}.', color=0x00ff00)
    derrota = discord.Embed(title=f'{ctx.author.display_name} você perdeu!',
                            description=f'O bot escolheu {comp}.', color=0x00ff00)
    fora = discord.Embed(
        title="Você não clicou a tempo, você está fora.", color=0x00ff00)
    m = await ctx.send(
        embed=ainda,
        components=[[Button(style=1, label="Pedra", custom_id="button1"), Button(
            style=1, label="Papel", custom_id='button2'), Button(style=1, label="Tesoura", custom_id='button3')]]
    )
    try:
        res = await bot.wait_for('button_click', check=check, timeout=10.0)
        player = res.component.label
        if player == comp:
            await m.edit(embed=empate, components=[])
        if player == "Pedra" and comp == "papel":
            await m.edit(embed=derrota, components=[])
        if player == "Pedra" and comp == "tesoura":
            await m.edit(embed=vitoria, components=[])
        if player == "Papel" and comp == "tesoura":
            await m.edit(embed=derrota, components=[])
        if player == "Tesoura" and comp == "pedra":
            await m.edit(embed=derrota, components=[])
        if player == "Tesoura" and comp == "papel":
            await m.edit(embed=vitoria, components=[])
    except TimeoutError:
        await m.edit(embed=fora, components=[])


@bot.event
async def on_message(message):
    def check(res):
        return message.author == res.author and res.channel == message.channel
    await bot.process_commands(message)
    msg = message.content
    if message.author == bot.user:
        return
    if any(word in msg for word in sad_words):
        await message.channel.send('Gambatê!')
    if message.content.startswith('id'):
        await message.channel.send(message.author.id)
    if message.content.startswith('Olá, bot'):
        quote = ('Olá, ' + str(message.author.mention))
        await message.reply(quote, mention_author=False)
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
    if message.content.startswith('reação'):
        await message.add_reaction('<:sapo_amor:846410960666361890>')
    quotes_musical = 'TAKE ME HOMEEEEEEEEEEEE, ITS THE ONLY PLACE I CAN REST IN PIECEEEEEE'
    trigger_musical = ['take', 'home']
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
            
bot.run('ODc5NDI5Njc3NTI4MjUyNDQ2.YSPmtg.T-IMrn5ShbArZWy1WyDgt8wVbk4')
