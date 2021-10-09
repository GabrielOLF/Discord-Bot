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

bot = ComponentsBot(command_prefix='!', intents=discord.Intents.all())
sad_words = ['Eu não consigo, bot', 'Estou triste', 'que tristeza']
nilismo = ["A filosofia é o exílio voluntário entre montanhas geladas.", "Nós, homens do conhecimento, não nos conhecemos; de nós mesmo somos desconhecidos.", "Não me roube a solidão sem antes me oferecer verdadeira companhia.", "O amor é o estado no qual os homens têm mais probabilidades de ver as coisas tal como elas não são.", "Como são múltiplas as ocasiões para o mal-entendido e para a ruptura hostil!", "Deus está morto. Viva Perigosamente. Qual o melhor remédio? - Vitória!", "A diferença fundamental entre as duas religiões da decadência: o budismo não promete, mas assegura. O cristianismo promete tudo, mas não cumpre nada.", "Quando se coloca o centro de gravidade da vida não na vida mas no além - no nada -, tira-se da vida o seu centro de gravidade.", "Para ler o Novo Testamento é conveniente calçar luvas. Diante de tanta sujeira, tal atitude é necessária.",
           "O cristianismo foi, até o momento, a maior desgraça da humanidade, por ter desprezado o Corpo.", "E aqueles que foram vistos dançando foram julgados insanos por aqueles que não podiam escutar a música.", "A moralidade é o instinto do rebanho no indivíduo.", "O idealista é incorrigível: se é expulso do seu céu, faz um ideal do seu inferno.", "Em qualquer lugar onde encontro uma criatura viva, encontro desejo de poder.", "Um político divide os seres humanos em duas classes: instrumentos e inimigos.", "Quanto mais me elevo, menor eu pareço aos olhos de quem não sabe voar. ", "Torna-te quem tu és!", "Aquele que luta com monstros deve acautelar-se para não tornar-se também um monstro. Quando se olha muito tempo para um abismo, o abismo olha para você.", "A alma nobre tem reverência por si mesma.", "Não existem fenômenos morais, mas apenas uma interpretação moral dos fenômenos."]
@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f'Loguei como {bot.user}!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='eu não aguento mais'))
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      if ctx.author.bot:return
      else:
        await ctx.send('Este comando não existe. Digite !comandos para conhecer os meus comandos.')
    return


# PEDRA PAPEL TESOURA
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
        title="Você não escolheu a tempo.", color=0x00ff00)
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
# DADOS

@bot.command()
async def dados(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    gold = 2000
    embedVar = discord.Embed(title="Jogo dos Dados", description="Dois dados serão rodados. Se um dos dados der 1, você ganha 2x o valor que apostou. Se ambos os dados derem 1, você ganha 10x o valor que apostou. Se nenhum dos dados derem 1, você perde tudo que apostou.')", color=0x00ff00)
    embedVar.add_field(
        name="Situação", value=f"Você tem ``{gold}`` bonoros", inline=False)
    ##embedVar.add_field(name="Field2", value="hi2", inline=False)
    await ctx.channel.send(embed=embedVar)
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
# JOGO DA FORCA

@bot.command()
async def forca(ctx):
    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
    words_animal = ['RINOCERONTE','ELEFANTE','GIRAFA','CROCODILO','PANDA','RATO','MACACO']
    words_amigos = ['VINIBOYOLA','DORI','THIELLY','DANILO','PANDA']
    word_choiced = [words_animal, words_amigos]
    word_ch = random.choice(word_choiced)
    word = random.choice(word_ch)
    word = word.lower()
    digitadas = []
    chances = 6
    if word_ch == words_amigos:
        x = 'membro da família Estatisticamente Inviável'
    else:
        x = 'animal'
    embedG = discord.Embed(
        title="Jogo da forca! ", description=f'A palavra tem {len(word)} letras! Dica: é um {x}.', color=0x00ff00)
    await ctx.send(embed=embedG)
    while True:
        resp = await bot.wait_for('message', check=check)
        tentativa = str(resp.content)
        letra = tentativa.lower()
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
            await ctx.send(f'A palavra era ``{word}``')
            break
        else:
            if chances <= 0:
                await ctx.reply('Você perdeu!')
                await ctx.send(f'A palavra era ``{word}``')
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
    palavras = ['``abacate``', '``feijoada``',
                '``viniboyola``', '``celular``', '``liquidificador``']
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
@bot.command()
async def niilismo(ctx):
        await ctx.reply(random.choice(nilismo) + str(' - Friedrich Nietzsche'), mention_author=False)
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
                await ctx.send(f'O {jogador} ||infelizmente|| não morreu! Diga ||girar|| para girar o tambor novamente!')
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
async def previsao(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.send('Você deseja saber a previsão do tempo da semana ou apenas de agora? Responda com ``semana`` ou ``agora``.')
  resp = await bot.wait_for('message', check=check)
  response = resp.content
  if response == 'agora' or response == 'Agora':
    agora = True
  else:
    agora = False
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
    div_temp = doc.find(class_='datos-estado-actual')
    real_div = div_temp.find(class_='principal')
    temp_search = real_div.find(class_='temperatura')
    temp_found = temp_search.find(class_='dato-temperatura changeUnitT')
    temperatura_atual = str(temp_found).split('>')[1].split('<')[0]
    dia = datas.find(class_=f'dia d1 activo') 
    try:
        chuva = dia.find(class_='prediccion')
        chuva_get = chuva.find(class_='probabilidad-lluvia')
        chuva_porc = str(chuva_get).split('>')[1].split('<')[0].replace(' ', '')
    except:
        chuva_porc = '0%'
    await ctx.reply(f'Agora está fazendo ``{temperatura_atual}``.\nChance de chover é ``{chuva_porc}``')

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
        item_temp = dia.find(class_='temperatura')
        temp_max_found = item_temp.find(class_='maxima changeUnitT')
        temp_min_found = item_temp.find(class_='minima changeUnitT')
        temp_max = str(temp_max_found).split('>')[1].split('<')[0]
        temp_min = str(temp_min_found).split('>')[1].split('<')[0]
        data_found = dia.find(class_='cuando')
        data = str(data_found).split('>')[1].split('<')[0]
        items_found[num] = {'Data': data, 'Temp Max': temp_max,'Temp Min': temp_min, 'Chuva': chuva_porc}
        num += 1
    sorted_items = items_found.items()
    for item in sorted_items:
      embedVar = discord.Embed(
                  title=f'{item[1]["Data"]}', description='', color=0x00ff00)
      embedVar.add_field(name='Temperatura Max', value=f"``{item[1]['Temp Max']}``")
      embedVar.add_field(name='Temperatura Min', value=f"`` {item[1]['Temp Min']}``")
      embedVar.add_field(name='Chance de chover', value=f"``{item[1]['Chuva']}``")
      await ctx.channel.send(embed=embedVar)
# COMANDO AJUDA
@bot.command()
async def comandos(ctx):
  embedVar = discord.Embed(
                          title="!comandos", description=f'``!mercadolivre``\n=> O bot realiza um webscraping em tempo real no site __Mercado Livre__. Nisto, você poderá pesquisar qualquer produto que esteja disponível e filtrar os resultados pelo preço.\n\n``!previsao``\n=> O bot realiza um web scraping em um site de previsão do tempo. Retorna a temperatura máxima, mínima e seus determinados dias.\n\n``!imagem``\n=>O bot manda uma imagem aleatória buscada por web scraping.\n\n ``!ping``\n=> Teste para saber se o bot ainda está ativo no servidor do replit.\n\n``!loteria``\n=> O bot fará uma seleção de 6 números aleatórios. Cabe ao jogador apostar 6 números distintos para tentar a sorte ||de ganhar nada||.\n\n``!roleta``\n=> Roleta russa. Um tambor de 6 entradas e 1 bala girará. O bot irá rodar os jogadores aleatoriamente e disparará o gatilho. Ganha quem ficar vivo até o final. O jogador poderá escolher jogar contra outros 5 jogadores ou contra o bot.\n\n``!mm``\n=> Jogo do mais, igual ou menos. O bot escolherá um número aleatório e dará uma dica. Tal dica será um número supostamente perto do __número secreto__. Cabe ao jogador escolher as seguintes opções: o número secreto ser maior que a dica, o número secreto ser menor que a dica ou o número secreto ser igual a dica.\n\n``!pdt``\n=> Pedra, papel e tesoura.\n\n``!dados``\n=> Jogue dois dados e torça para pelo menos um deles cair com o número 1.\n\n``!cores``\n=> O bot colocará uma palavra aleatória na frente de uma cor aleatória. Após determinado tempo, o bot ocultará as palavras e as cores e, então, perguntar ao jogador qual cor se designava determinada palavra.\n\n``!bd, !al, !prob, !calc2``\n=> O bot mandará o link do meet para a aula determinada pelo usuário.\n\n``!dirso``\n=> Simplesmente dirso.\n\n``!op``\n=> O bot escolherá uma operação matemática aleatória entre números aleatórios. Acerte e não seja zoado pelo bot.\n\n``!forca``\n=>Jogo da forca.\n\n``!niilismo``\n=> cringe.', color=0x00ff00)
  await ctx.send(embed=embedVar)
  
# WEB SCRAPING
@bot.command()
async def mercadolivre(ctx):
  def check(res):
        return ctx.author == res.author and res.channel == ctx.channel
  await ctx.reply('Qual produto você quer pesquisar?')
  tag_resp = await bot.wait_for('message', check=check)
  tag = tag_resp.content
  await ctx.send('Deseja filtar os produtos pelo preço? Responda com sim ou não.\nObs: o bot recomenda que filtre os produtos pelo preço para não floodar o canal em que foi chamado.')
  filtro_res = await bot.wait_for('message',check=check)
  if filtro_res.content == 'sim' or filtro_res.content == 'Sim' or filtro_res.content == 'S' or filtro_res.content == 's':
    filtro = True
  else:
    filtro = False
  if filtro == True:
    if ' ' in tag:
      tag_search = tag.replace(' ', '-')
    else:
      tag_search = tag
    url = f'https://lista.mercadolivre.com.br/{tag_search}'
    await ctx.send('Qual o valor máximo que deseja filtrar? Digite um número inteiro.')
    max_pr = await bot.wait_for('message', check=check)
    max_price = max_pr.content
  else:
    url = f'https://lista.mercadolivre.com.br/{tag}'

  
  result = requests.get(url).text
  doc = bs(result, 'html.parser')
  items_found = {}
  #div = doc.find(class_='ui-search-results ui-search-results--without-disclaimer')
  div = doc.find(class_='ui-search-results')
  item_search = tag.split(' ')
  if len(item_search) >= 2:
    item_search = item_search[0]
  else:
    item_search = tag_search
  try:
    items = div.find_all(text=re.compile(item_search, re.IGNORECASE))
  except:
    items = False
  if items != False:
      for item in items:
        try:
          next_parent = item.find_parent(class_='ui-search-layout__item')
          links = next_parent.find(class_='ui-search-result__image')
        except:
          await ctx.send('.')
        try:
            link_get = str(links).split('<a')[1].split('title')[-2].split('href')[1].split('=')[1]
            link_new = link_get.split('//')[1]
            if link_new[0] == 'p' or link_new[1] == 'w' or link_new[0] == 'm':
              link = link_get
            else:
              link = 'o bot não conseguiu encontrar o link'
        except:
            link = 'o bot não conseguiu encontrar o link'
        image_src = links.find(class_='carousel-container arrow-visible')
        link_image = str(image_src).split('src=')[1].split('height')[0].replace('"','')
      
        try:
          prices = next_parent.find(class_="price-tag-fraction")
          price = str(prices).split('>')[-2].split('<')[0]
          items_found[item] = {'price': price.replace(",", ""),'link': link.replace('"',''), 'image': link_image}
        except:
          price = 'preço not found'

      sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
      num_items = 0
      for item in sorted_items:
        if filtro == True:
          try:
              if int(item[1]['price'].replace('.', '')) <= int(max_price):
                num_items += 1
                embedVar = discord.Embed(
                            title="Nome do item", description=f'{item[0]}', color=0x00ff00)
                embedVar.add_field(name='Valor do item', value=f"``R${item[1]['price']}``")
                embedVar.add_field(name='Link do item', value=f" {item[1]['link']}")
                embedVar.set_thumbnail(url=f"{item[1]['image']}")
                await ctx.channel.send(embed=embedVar)
                #await ctx.send(item[0])
                #await ctx.send(f"R${item[1]['price']}")
                #await ctx.send(f"Link: {item[1]['link']}"
          except:
            await ctx.send('erro')
        else:
          embedVar = discord.Embed(
                      title="Nome do item", description=f'{item[0]}', color=0x00ff00)
          embedVar.add_field(name='Valor do item', value=f"``R${item[1]['price']}``")
          embedVar.add_field(name='Link do item', value=f" {item[1]['link']}")
          await ctx.channel.send(embed=embedVar)
          
      if filtro == True:
        if num_items >= 1:
              await ctx.send(f'Estes foram os ``{num_items}`` resultados da minha busca filtrada!\nObs: por motivos de lentidão do replit ou do próprio mercado livre, a quantidade de resultados pode variar a cada varredura.')
        else:
            await ctx.send(f'Não consegui encontrar ``{tag}`` filtrado em ``R${max_price}``. Aumente o valor do filtro ou escreva o nome do produto de outra forma.')
      else:
        if len(items_found) >= 1:
            await ctx.send(f'Estes foram os ``{len(items_found)}`` resultados da minha busca!\nObs: por motivos de lentidão do replit ou do próprio mercado livre, a quantidade de resultados podem variar a cada varredura.')
        elif len(items_found) == 0:
            await ctx.send(f'Infelizmente não consegui encontrar ``{tag}``. Por favor, me chame novamente e tente escrever o nome do produto de outra forma.')
  else:
    await ctx.send(f'Infelizmente não consegui encontrar ``{tag}``. Por favor, me chame novamente e tente escrever o nome do produto de outra forma.')


# PING

@bot.command()
async def ping(ctx):
  await ctx.send('to aqui')
# MEMBRO NOVO

@bot.event
async def on_member_join(member):
    channel = get(member.guild.channels, name="🗣-discussões-gerais")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://i.imgur.com/Crw2Gvs.png') as resp:
            if resp.status != 200:
                return await channel.send('O bot não conseguiu baixar a imagem...')
            data = io.BytesIO(await resp.read())
    await channel.send(file=discord.File(data, 'danilao.png'))

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
keep_alive()
bot.run(cod)

