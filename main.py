# coding: utf-8
import sys, os
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# All lists
all_lists = []

# check for new messages --> polling
# token = os.environ['BOT_API_TOKEN']
token = '818262027:AAHwNrZal6dNo4fgYugGNZewtU2knok61-g'
updater = Updater(token=token)

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
             '\n"/exibirLista NomeDaLista" para exibir uma lista específica'
             '\n"/criarLista NomeDaLista" para criar novas listas'
             '\n"/criarEvento NomeDaLista NomeDoEvento" para criar novos eventos'
             '\n"/deletarEvento NomeDaLista NomeDoEvento" para deletar um evento'
             '\n"/deletarLista NomeDaLista" para deletar um evento'
             '\n"/limparLista NomeDaLista" para deletar todos os eventos de uma lista',
        parse_mode=ParseMode.MARKDOWN
    )


def listar(bot, update):
    if len(all_lists) == 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Você não possui *nenhuma* lista.\nQue tal criar uma? Utilize o comando "/criarLista" passando um nome para criar uma nova lista.\nExemplo: "/criarLista A Fazeres"',
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        mensagem = ""
        for i in range(len(all_lists)):
            mensagem += "* {}:*".format(all_lists[i]["nome"])
            for j in all_lists[i]["itens"]:
                mensagem += "\n   • {}".format(j)
            mensagem += "\n\n"

        bot.send_message(
            chat_id=update.message.chat_id,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )


def exibirlistaunica(bot, update, args):
    nome_lista = ' '.join(args).strip()

    if len(all_lists) == 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Você não possui *nenhuma* lista.\nQue tal criar uma? Utilize o comando "/criarLista" passando um nome para criar uma nova lista.\nExemplo: "/criarLista A Fazeres"',
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        mensagem = ""
        listas = ""
        for i in range(len(all_lists)):
            if nome_lista == all_lists[i]["nome"]:
                listas += "\n" + all_lists[i]["nome"]
                mensagem += "* {}:*".format(all_lists[i]["nome"])
                for j in all_lists[i]["itens"]:
                    mensagem += "\n   • {}".format(j)
            mensagem += "\n\n"

            if nome_lista != all_lists[i]["nome"] and i == len(all_lists) - 1:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
                )
                return None
        bot.send_message(
            chat_id=update.message.chat_id,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )


def criarlista(bot, update, args):
    nome_lista = ' '.join(args).strip()

    if nome_lista != "":
        for i in range(len(all_lists)):
            if nome_lista in all_lists[i]["nome"]:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Uma lista com esse nome já foi criada.\nTente novamente utilizando outro nome.'
                )
                return None
        bot.send_message(
            chat_id=update.message.chat_id,
            text='A lista {} será criada.'.format(nome_lista)
        )
        lista = {
            "nome": nome_lista,
            "itens": []
        }
        all_lists.append(lista)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Lista criada com sucesso!"
        )


    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nome Inválido.\nTente novamente utilizando outro nome.'
        )


def criarevento(bot, update, args):
    param = ' '.join(args).strip()
    nome_lista = param.split(' ', 1)[0]
    nome_evento = param.split(' ', 1)[1]

    if nome_lista != "" and nome_evento != "":
        listas = ""
        for i in range(len(all_lists)):
            listas += "\n" + all_lists[i]["nome"]
            if nome_lista == all_lists[i]["nome"]:
                if nome_evento not in all_lists[i]["itens"]:
                    all_lists[i]["itens"].append(nome_evento)
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Evento foi criado com sucesso.'
                    )
                    break
                else:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Evento já existe.'
                    )

            if nome_lista != all_lists[i]["nome"] and i == len(all_lists)-1:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
                )
                return None

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nome da lista ou nome do evento inválido.'
        )


def deletarevento(bot, update, args):
    param = ' '.join(args).strip()
    nome_lista = param.split(' ', 1)[0]
    nome_evento = param.split(' ', 1)[1]

    if nome_lista != "" and nome_evento != "":
        listas = ""
        for i in range(len(all_lists)):
            listas += "\n" + all_lists[i]["nome"]
            if nome_lista == all_lists[i]["nome"]:
                if nome_evento in all_lists[i]["itens"]:
                    index = all_lists[i]["itens"].index(nome_evento)
                    all_lists[i]["itens"].pop(index)
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Evento foi deletado com sucesso.'
                    )
                    break
                else:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Evento não existe ou já foi deletado.'
                    )

            if nome_lista != all_lists[i]["nome"] and i == len(all_lists)-1:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
                )
                return None

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nome da lista ou nome do evento inválido.'
        )


def deletarlista(bot, update, args):
    nome_lista = ' '.join(args).strip()

    listas = ""
    for i in range(len(all_lists)):
        listas += "\n" + all_lists[i]["nome"]
        if nome_lista == all_lists[i]["nome"]:
            all_lists.pop(i)
            bot.send_message(
                chat_id=update.message.chat_id,
                text='A lista foi deletada com sucesso.'
            )
            break
        if nome_lista != all_lists[i]["nome"] and i == len(all_lists)-1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Lista não existe ou já foi deletada. Essas são as listas disponíveis:\n{}'.format(listas)
            )
            return None


def limparlista(bot, update, args):
    nome_lista = ' '.join(args).strip()

    listas = ""
    for i in range(len(all_lists)):
        listas += "\n" + all_lists[i]["nome"]
        if nome_lista == all_lists[i]["nome"]:
            while len(all_lists[i]["itens"]) != 0:
                all_lists[i]["itens"].pop()
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Todos os eventos da lista foram deletados.'
            )
            break

        if nome_lista != all_lists[i]["nome"] and i == len(all_lists)-1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
            )
            return None


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Comando não encontrado.\nDigite "/help" para listar todos os comandos.'
    )


# create a command handler
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
unknown_handler = MessageHandler([Filters.command], unknown)

listar_handler = CommandHandler("listar", listar)
exibirlistaunica_handler = CommandHandler("exibirLista", exibirlistaunica, pass_args=True)

criarLista_handler = CommandHandler("criarLista", criarlista, pass_args=True)
criarEvento_handler = CommandHandler("criarEvento", criarevento, pass_args=True)

deletarevento_handler = CommandHandler("deletarEvento", deletarevento, pass_args=True)
deletarlista_handler = CommandHandler("deletarLista", deletarlista, pass_args=True)
limparlista_handler = CommandHandler("limparLista", limparlista, pass_args=True)

handlers = [exibirlistaunica_handler, deletarlista_handler, limparlista_handler, start_handler, listar_handler, deletarevento_handler, criarLista_handler, criarEvento_handler, help_handler, unknown_handler]

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
        print (e)
        sys.exit(0)
