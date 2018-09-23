from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging
import settings
import datetime
import ephem

calcdict={'один':'1','два':'2','три':'3','четыре':'4','пять':'5','шесть':'6','девять':'9',
'ноль':'0','умножить':'*','делить':'/','плюс':'+','минус':'-','сколько будет':'','на':'','и':'.'}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
def greet_user(bot, update):
    logging.info('Users start')
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):

    user_text=update.message.text.lower()
    for i in calcdict:
        user_text=user_text.replace(i,calcdict[i])
    
    user_text=user_text.replace('восемь','8')
    user_text=user_text.replace('семь','7')
    user_text=user_text.replace(' ','')
     
    
    plus_cord=user_text.find('+')
    minus_cord=user_text.find('-')
    divide_cord=user_text.find('/')
    multiply_cord=user_text.find('*')
    
    
    if plus_cord==-1 and minus_cord==-1 and divide_cord==-1 and multiply_cord==-1:
        update.message.reply_text('Формат выражения: Сколько будет один плюс два или сколько будет три и два умножить на шесть и восемь')
    elif (user_text.count('+')+user_text.count('-')+user_text.count('*')+user_text.count('/'))>1:
        update.message.reply_text('Можно использовать только одну арифметическую операцию')
    elif plus_cord !=-1:
        try:
            number1=float(user_text[:plus_cord])
            number2=float(user_text[plus_cord+1::])
            update.message.reply_text(number1+number2)
        except ValueError:
            update.message.reply_text('Формат выражения: Сколько будет один плюс два или сколько будет три и два умножить на шесть и восемь')
    elif minus_cord !=-1:
        try:
            number1=float(user_text[:minus_cord])
            number2=float(user_text[minus_cord+1::])
            update.message.reply_text(number1-number2)
        except ValueError:
            update.message.reply_text('Формат выражения: Сколько будет один плюс два или сколько будет три и два умножить на шесть и восемь')
    elif divide_cord !=-1:
        try:
            number1=float(user_text[:divide_cord])
            number2=float(user_text[divide_cord+1::])
            if number2==0:
                update.message.reply_text('Серьёзно ? хочешь поделить на ноль ?')
            else:
                update.message.reply_text(number1/number2)
        except ValueError:
            update.message.reply_text('Формат выражения: Сколько будет один плюс два или сколько будет три и два умножить на шесть и восемь')
    elif multiply_cord !=-1:
        try:
            number1=float(user_text[:multiply_cord])
            number2=float(user_text[multiply_cord+1::])
            update.message.reply_text(number1*number2)
        except ValueError:
            update.message.reply_text('Формат выражения: Сколько будет один плюс два или сколько будет три и два умножить на шесть и восемь')


def wordcount (bot,update):
    user_text_wo=update.message.text[10::].lstrip()
    if update.message.text=='/wordcount':
        update.message.reply_text('Pls enter the phrase after "/wordcount"')
    elif user_text_wo.startswith('"') and user_text_wo.endswith('"'):
        words_count=len(user_text_wo.split(' '))
        update.message.reply_text('Words count:{}'.format(words_count)) 
        
    else:
        update.message.reply_text('Pls enter the phrase starts with " and end with " after "/wordcount"')

def planets(bot,update):
    if update.message.text=='/planet':
        update.message.reply_text('Pls enter the planet name after "/planet" like Mars, Jupiter, Venus e.t.c')
    else:
        a,planet_name=update.message.text.split(' ')
        date=datetime.datetime.now()
        datestr=date.strftime('%Y.%m.%d')
        
        try:
            planet_position=getattr(ephem,planet_name)(datestr)
            print (planet_position)
            ans=ephem.constellation(planet_position)[1]
            update.message.reply_text(ans)
        except(AttributeError):
            update.message.reply_text('Pls enter the planet name after "/planet" like Mars, Jupiter, Venus e.t.c')    
    

def main():
    mybot= Updater(settings.API_key,request_kwargs=settings.PROXY)
    
    logging.info('Bot started')

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler('planet',planets))
    dp.add_handler(CommandHandler('wordcount',wordcount))

    mybot.start_polling()
    mybot.idle()

main()