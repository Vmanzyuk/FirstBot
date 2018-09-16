from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging
import settings
import datetime
import ephem

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
    print(user_text)
    update.message.reply_text(user_text)

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

    mybot.start_polling()
    mybot.idle()

main()