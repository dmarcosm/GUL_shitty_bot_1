from telegram.ext import *
import logging
import subprocess

updater = Updater(token='BOT TOKEN HERE')
dispatcher = updater.dispatcher

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

message_usage = "Usage:\ntype '/bash' and a valid (or not) bash command.\nThe output will be sent back"

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=message_usage)

def bash_command(bot, update, args):
    print(args)

    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        print("File not found error thrown, catching and sending...")
        message_send = "bash: " + str(e) 
    except Exception as e:
        print("Some other error thrown, abort mission!")
        print(e)
        return 1
    else:
        print("Command found, sending output...")
        output_bash, error_bash = process.communicate()
        try:
            message_send = "bash: " + output_bash.decode("utf-8") + error_bash.decode("utf-8")
            print(output_bash)
            print(error_bash)
        except Exception as e:
            print(str(e))
            #you thought i had all this figured out, right?
            return 2
        else:
            print(message_send)
            #i had to put something in here

    bot.send_message(chat_id=update.message.chat_id, text=message_send)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
bash_command_handler = CommandHandler('bash', bash_command, pass_args=True)
dispatcher.add_handler(bash_command_handler)


updater.start_polling()
