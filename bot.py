from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging

PROXY={'proxy_url':'socks5://t1.learn.python.ru:1080','urllib3_proxy_kwargs':{'username':'learn','password':'python'}}

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

def main():
    mybot= Updater('686048294:AAGgofWDL1WGR1CZuP97zJH8iJ1zvn7do-8',request_kwargs=PROXY)
    
    logging.info('Bot started')

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()

main()