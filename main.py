# coding: utf-8
import sys

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

# All lists
all_lists = []

# check for new messages --> polling
updater = Updater(token="818262027:AAHwNrZal6dNo4fgYugGNZewtU2knok61-g")

# allows to register handler --> command, text, video, audio, etc.
dispatcher = updater.dispatcher


# define a command callback function
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Olá, eu sou o ListasBot!\nVamos começar?\n\nUtilize '
                                                          '"/help" para exibir os comandos disponíveis.')


def help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Esses são os comandos disponíveis no momento no ListasBot:'
             '\n\n"/start" para iniciar uma conversa com o Bot'
             '\n"/help" para listar os comandos'
             '\n"/listar" para exibir as listas'
             '\n"/criarLista" para criar novas listas',
        parse_mode=ParseMode.MARKDOWN
    )


def listar(bot, update):
    if len(all_lists) == 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Você não possui *nenhuma* lista.\nQue tal criar uma? Utilize o comando "/criarLista" para criar uma nova lista.',
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        mensagem = ""
        for i in range(len(all_lists)):
            mensagem += "* %s :*\n" % all_lists[i]["nome"]
        bot.send_message(
            chat_id=update.message.chat_id,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )


def criarlista(bot, update, args):
    user_says = " ".join(args)
    update.message.reply_text("You said: " + user_says)
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Vamos criar uma nova lista. Qual o nome de sua nova lista?'
    )
    print "Nome da lista %s" % user_says
    lista = {"nome": user_says}
    print "Lista criada"
    all_lists.append(lista)
    print "Lista adicionada"
    print all_lists
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Lista criada com sucesso!"
    )


# create a command handler
start_handler = CommandHandler("start", start)
listar_handler = CommandHandler("listar", listar)
criarLista_handler = CommandHandler("criarLista", criarlista, pass_args=True)
help_handler = CommandHandler("help", help)

handlers = [start_handler, listar_handler, criarLista_handler, help_handler]

# add command handler to dispatcher
for i in handlers:
    dispatcher.add_handler(i)


# start polling
def main_loop():
    updater.start_polling()


if __name__ == '__main__':
    try:
        main_loop()
    except Exception as e:
        print e
        sys.exit(0)
