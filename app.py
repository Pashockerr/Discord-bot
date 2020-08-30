from bs4 import BeautifulSoup
import requests
import random
import config
import discord
from discord.ext import commands
from fuzzywuzzy import fuzz

#Imports

sended = False

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
async def get_image(ctx,word):
    link = randImage(word)
    await ctx.send(str(link))

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
async def talk(ctx,*phrase1):
    from talk_patterns import phrases
    global sended
    phrase = ''
    for i in phrase1:
        phrase += i
    for pattern in phrases:
        if fuzz.partial_ratio(pattern[0],phrase) >= 70:
            await ctx.send(pattern[random.randint(1,len(pattern)-1)])
            sended = True
            break
    if sended == False:
        await ctx.send('Сори, я не знаю что тебе ответить.')
    sended = False

#Command for add user talk patterns
@bot.command(description="Научи бота говорить")
async def add_talk_pattern(ctx,pattern,*reaction):
    from talk_patterns import phrases
    to_append = [pattern]
    for reaction1 in reaction:
        to_append.append(reaction1)
    phrases.append(to_append)
    file = open('talk_patterns.py','w',encoding="utf8")
    file.write('phrases = '+str(phrases))
    file.close()
    await ctx.send("Паттерн успешно добавлен.")
bot.run(config.params['TOKEN'])