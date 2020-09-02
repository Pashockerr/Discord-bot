from bs4 import BeautifulSoup
import requests
import random
import config
import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
import filter
import Levenshtein
import sqlite3
#Imports

#Connect sqlite3 database
connection = sqlite3.connect("patterns.db")
#Set cursor
cursor = connection.cursor()
#Create the table
#cursor.execute("CREATE TABLE patterns(phrase text, answ1 text, answ2 text, answ3 text)")

sended = False

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

bot = commands.Bot(command_prefix=config.params['PREF'])

#Function for search random images
def randImage(search):
    data = requests.get('https://www.google.ru/search?newwindow=1&hl=ru&authuser=0&tbm=isch&sxsrf=ALeKk00mYyct4OvLttM7gvJZdV23lx4tiA%3A1598685234357&source=hp&biw=1366&bih=693&ei=MgBKX7DcEoqsa528jPAB&q='+search+'&oq='+search+'&gs_lcp=CgNpbWcQAzIECCMQJzIGCAAQChABMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADIECAAQCjoFCAAQsQNQngxYyhBgzxloAHAAeACAAZYBiAHABJIBAzAuNJgBAKABAaoBC2d3cy13aXotaW1n&sclient=img&ved=0ahUKEwiwvf7L7r_rAhUK1hoKHR0eAx4Q4dUDCAY&uact=5')
    soup = BeautifulSoup(data.content,'lxml')
    res = soup.find_all("img")
    res = random.choice(res).attrs['src']
    if res != '/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif':
        return res
    else:
        randImage(search)

#Command for search the images
@bot.command(description="Команда для поиска изображений")
async def image(ctx,word):
    badword = False
    for word1 in filter.words:
        if fuzz.partial_ratio(word,word1) >= 50:
            badword = True
    if badword:
        await ctx.send("Обнаружено запрещенное слово, запрос отклонён.")
    else:
        link = randImage(word)
        await ctx.send(link)

#Command for help
@bot.command(description = 'Описание - введи эту команду для помощи')
async def help_for_bot(ctx):
    await ctx.send('Введите =image и через пробел слово по которому вы хотите найти изображение. Если слов больше одного, то заключите их в кавычки, вот так : =image "Ваше слово". Внимание! Контент который отправляет бот не модерируется, всю ответственность за свои запросы несёте вы.')

#Command who says author's name
@bot.command(description='Эта команда говорит кто тут крутой')
async def author(ctx):
    await ctx.send("Автор Pashockerr")

#Command for text
@bot.command(description='Не пиши это, если ты в чате анискорд стол')
async def spamirka(ctx,word,colichestvo):
    text = ''
    try:
        for i in range(1,int(colichestvo)):
            text += word
    except ValueError:
        await ctx.send("Цифры пиши, дебил")
    await ctx.send(text)

@bot.command(description='Поболтай с ботом')
async def talk(ctx,phrase1):
    patterns = cursor.execute("SELECT * FROM patterns")
    patterns = cursor.fetchall()
    answers = []
    answered = False
    for pattern in patterns:
        if fuzz.partial_ratio(pattern[0],phrase1) >= 70:
            for i in range(1,3):
                answers.append(pattern[i])
            await ctx.send(random.choice(answers))
            answered = True
            break
    if answered == False:
        await ctx.send("Сорян, я не знаю что тебе ответить.")

#Command for add user talk patterns
@bot.command(description="Научи бота говорить")
async def add_talk_pattern(ctx,pattern,answ1,answ2,answ3):
    cursor.execute("INSERT INTO patterns VALUES('"+pattern+"','"+answ1+"','"+answ2+"','"+answ3+"')")
    connection.commit()
    await ctx.send("Паттерн успешно добавлен.")

#Command for debug
@bot.command()
async def debug_talkPatterns_output_printTalkPatterns(ctx):
    cursor.execute("SELECT * FROM patterns")
    await ctx.send(cursor.fetchall())

@bot.command(pass_context=True)
async def music(ctx, url):
    channel = config.params['VoiceChannelId']
    await channel.connect()
    player = await VoiceChannel.create_ytdl_player(url)
    player.start()

@bot.command()
async def word(ctx,word,symbol):
    from pictures import letters
    for letter in word.lower():
        try:
            await ctx.send(letters[letter].format(symbol))
        except KeyError:
            await ctx.send("Символ не найден.")

bot.run(config.params['TOKEN'])
connection.close()