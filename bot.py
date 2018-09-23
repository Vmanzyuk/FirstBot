from telegram.ext import Updater,CommandHandler,MessageHandler,Filters, RegexHandler
import logging
import settings
import datetime
import ephem

cities=['москва','анадырь','ростов на дону','урал','липецк','калининград','дмитров','волгоград','дзержинск','кострома',
'архангельск','кишинев','волжский','иркутск','клязьма','астрахань','новгород','домодедово','омск']
cities_new=['москва','анадырь','ростов на дону','урал','липецк','калининград','дмитров','волгоград','дзержинск','кострома',
'архангельск','кишинев','волжский','иркутск','клязьма','астрахань','новгород','домодедово','омск']



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

    user_text = update.message.text
    user_text_wo= update.message.text[:len(update.message.text)-1]
    plus_cord=user_text_wo.find('+')
    minus_cord=user_text_wo.find('-')
    divide_cord=user_text_wo.find('/')
    multiply_cord=user_text_wo.find('*')
    
    if not user_text.endswith('='):
        update.message.reply_text('Expression must end with =')
    elif plus_cord==-1 and minus_cord==-1 and divide_cord==-1 and multiply_cord==-1:
        update.message.reply_text('Expression must be include + or - or / or *')
    elif (user_text.count('+')+user_text.count('-')+user_text.count('*')+user_text.count('/'))>1:
        update.message.reply_text('Pls enter one arithmetic sign')
    elif plus_cord !=-1:
        try:
            number1=float(user_text_wo[:plus_cord])
            number2=float(user_text_wo[plus_cord+1::])
            update.message.reply_text(number1+number2)
        except ValueError:
            update.message.reply_text('Pls enter the numbers on format number1+number2 or number1-number or number1/number2 or number1/number2')
    elif minus_cord !=-1:
        try:
            number1=float(user_text_wo[:minus_cord])
            number2=float(user_text_wo[minus_cord+1::])
            update.message.reply_text(number1-number2)
        except ValueError:
            update.message.reply_text('Pls enter the numbers on format number1+number2 or number1-number or number1/number2 or number1/number2')
    elif divide_cord !=-1:
        try:
            number1=float(user_text_wo[:divide_cord])
            number2=float(user_text_wo[divide_cord+1::])
            if number2==0:
                update.message.reply_text('divide by zero')
            else:
                update.message.reply_text(number1/number2)
        except ValueError:
            update.message.reply_text('Pls enter the numbers on format number1+number2 or number1-number or number1/number2 or number1/number2')
    elif multiply_cord !=-1:
        try:
            number1=float(user_text_wo[:multiply_cord])
            number2=float(user_text_wo[multiply_cord+1::])
            update.message.reply_text(number1*number2)
        except ValueError:
            update.message.reply_text('Pls enter the numbers on format number1+number2 or number1-number or number1/number2 or number1/number2')


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

def next_full_moon(bot,update):
    update.message.reply_text(ephem.next_full_moon(update.message.text[33::]))
    
def goroda(bot,update):
    
    city_name=update.message.text[8::]
    city_name=city_name.lower()

    if city_name in cities:
        if city_name in cities_new:
            
            if city_name[len(city_name)-1]=='й' or city_name[len(city_name)-1]=='ь' or city_name[len(city_name)-1]=='ъ' or city_name[len(city_name)-1]=='ы':
                for i in cities:
                    if i[0]==city_name[len(city_name)-2]:
                        answ=i
                        break
                    else:
                        pass
            else:
                for i in cities:
                    if i[0]==city_name[len(city_name)-1]:
                        answ=i
                        break
                    else:
                        pass

            if answ in cities_new:
                cities_new.remove(answ)
                cities_new.remove(city_name)
                update.message.reply_text(answ)
                
            else:
                update.message.reply_text('Моя больше не знать ответов, ты победил')
                

        else:
            update.message.reply_text('Какой хитренький, уже было')
    else:
        update.message.reply_text('Чёт не знаю такого города пока')





def main():
    mybot= Updater(settings.API_key,request_kwargs=settings.PROXY)
    
    logging.info('Bot started')

    dp=mybot.dispatcher
    dp.add_handler(RegexHandler('^(Когда ближайшее полнолуние после)',next_full_moon))
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet',planets))
    dp.add_handler(CommandHandler('wordcount',wordcount))
    dp.add_handler(CommandHandler('goroda',goroda))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()