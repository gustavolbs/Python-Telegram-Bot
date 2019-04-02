# coding: utf-8
import sys, pickle
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


def save():
    afile = open(r'all_user_data.pkl', 'wb')
    pickle.dump(all_user_data, afile)
    afile.close()

# All lists
try:
    # reload object from file
    file2 = open(r'all_user_data.pkl', 'rb')
    all_user_data = pickle.load(file2)
    file2.close()

except:
    all_user_data = dict()
    save()


# check for new messages --> polling
token = '818262027:AAHwNrZal6dNo4fgYugGNZewtU2knok61-g'
updater = Updater(token=token)

# allows to register handler --> command, text, video, audio, etc.
dispatcher = updater.dispatcher


# define a command callback function
def start(bot, update):
    user_id = update.message.from_user.id

    # Create user dict if it doesn't exist
    if user_id not in all_user_data:
        all_user_data[user_id] = []

    bot.send_message(chat_id=update.message.chat_id,
                     text='Olá, eu sou o ListasBot!\nVamos começar?\n\nUtilize "/help" para exibir os comandos disponíveis.'
                     )
    save()


def help(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Esses são os comandos disponíveis no momento no ListasBot:'
             '\n\n/start para iniciar uma conversa com o Bot'
             '\n/help para listar os comandos'
             '\n/listar para exibir as listas'
             '\n/exibir_lista NomeDaLista para exibir uma lista específica'
             '\n/criar_lista NomeDaLista para criar novas listas'
             '\n/criar_evento NomeDaLista NomeDoEvento para criar novos eventos'
             '\n/deletar_evento NomeDaLista NomeDoEvento para deletar um evento'
             '\n/deletar_lista NomeDaLista para deletar um evento'
             '\n/limpar_lista NomeDaLista para deletar todos os eventos de uma lista',
        parse_mode=ParseMode.MARKDOWN
    )


def listar(bot, update):
    user_id = update.message.from_user.id

    if len(all_user_data[user_id]) == 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Você não possui *nenhuma* lista.\nQue tal criar uma? Utilize o comando "/criar_lista" passando um nome para criar uma nova lista.\nExemplo: "/criar_lista A Fazeres"',
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        mensagem = ""
        for i in range(len(all_user_data[user_id])):
            mensagem += "* {}:*".format(all_user_data[user_id][i]["nome"])
            for j in all_user_data[user_id][i]["itens"]:
                mensagem += "\n   • {}".format(j)
            mensagem += "\n\n"

        bot.send_message(
            chat_id=update.message.chat_id,
            text=mensagem,
            parse_mode=ParseMode.MARKDOWN
        )


def exibirlistaunica(bot, update, args):
    user_id = update.message.from_user.id
    nome_lista = ' '.join(args).strip()

    if len(all_user_data[user_id]) == 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Você não possui *nenhuma* lista.\nQue tal criar uma? Utilize o comando "/criar_lista" passando um nome para criar uma nova lista.\nExemplo: "/criar_lista A Fazeres"',
            parse_mode=ParseMode.MARKDOWN
        )

    else:
        mensagem = ""
        for i in range(len(all_user_data[user_id])):
            if nome_lista == all_user_data[user_id][i]["nome"]:
                mensagem += "* {}:*".format(nome_lista)
                if len(all_user_data[user_id][i]["itens"]) > 0:
                    for j in all_user_data[user_id][i]["itens"]:
                        mensagem += "\n   • {}".format(j)
                    mensagem += "\n\n"
                else:
                    mensagem = "Você não possui itens na lista."
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=mensagem,
                    parse_mode=ParseMode.MARKDOWN
                )
                break


def criarlista(bot, update, args):
    user_id = update.message.from_user.id
    nome_lista = ' '.join(args).strip()

    if nome_lista != "":
        for i in range(len(all_user_data[user_id])):
            if nome_lista in all_user_data[user_id][i]["nome"]:
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
        all_user_data[user_id].append(lista)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Lista criada com sucesso!"
        )

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nome Inválido.\nTente novamente utilizando outro nome.'
        )
    save()


def criarevento(bot, update, args):
    user_id = update.message.from_user.id
    param = ' '.join(args).strip()
    nome_lista = param.split(' ', 1)[0]
    nome_evento = param.split(' ', 1)[1]

    if nome_lista != "" and nome_evento != "":
        listas = ""
        for i in range(len(all_user_data[user_id])):
            listas += "\n" + all_user_data[user_id][i]["nome"]
            if nome_lista == all_user_data[user_id][i]["nome"]:
                if nome_evento not in all_user_data[user_id][i]["itens"]:
                    all_user_data[user_id][i]["itens"].append(nome_evento)
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

            if nome_lista != all_user_data[user_id][i]["nome"] and i == len(all_user_data[user_id])-1:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
                )
                return None
        save()

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nome da lista ou nome do evento inválido.'
        )


def deletarevento(bot, update, args):
    user_id = update.message.from_user.id
    param = ' '.join(args).strip()
    nome_lista = param.split(' ', 1)[0]
    nome_evento = param.split(' ', 1)[1]

    if nome_lista != "" and nome_evento != "":
        listas = ""
        for i in range(len(all_user_data[user_id])):
            listas += "\n" + all_user_data[user_id][i]["nome"]
            if nome_lista == all_user_data[user_id][i]["nome"]:
                if nome_evento in all_user_data[user_id][i]["itens"]:
                    index = all_user_data[user_id][i]["itens"].index(nome_evento)
                    all_user_data[user_id][i]["itens"].pop(index)
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

            if nome_lista != all_user_data[user_id][i]["nome"] and i == len(all_user_data[user_id])-1:
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
    save()


def deletarlista(bot, update, args):
    user_id = update.message.from_user.id
    nome_lista = ' '.join(args).strip()

    listas = ""
    for i in range(len(all_user_data[user_id])):
        listas += "\n" + all_user_data[user_id][i]["nome"]
        if nome_lista == all_user_data[user_id][i]["nome"]:
            all_user_data[user_id].pop(i)
            bot.send_message(
                chat_id=update.message.chat_id,
                text='A lista foi deletada com sucesso.'
            )
            break
        if nome_lista != all_user_data[user_id][i]["nome"] and i == len(all_user_data[user_id])-1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Lista não existe ou já foi deletada. Essas são as listas disponíveis:\n{}'.format(listas)
            )
            return None
    save()


def limparlista(bot, update, args):
    user_id = update.message.from_user.id
    nome_lista = ' '.join(args).strip()

    listas = ""
    for i in range(len(all_user_data[user_id])):
        listas += "\n" + all_user_data[user_id][i]["nome"]
        if nome_lista == all_user_data[user_id][i]["nome"]:
            while len(all_user_data[user_id][i]["itens"]) != 0:
                all_user_data[user_id][i]["itens"].pop()
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Todos os eventos da lista foram deletados.'
            )
            break

        if nome_lista != all_user_data[user_id][i]["nome"] and i == len(all_user_data[user_id])-1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Lista não existe. Essas são as listas disponíveis:\n{}'.format(listas)
            )
            return None
    save()


def mostrarbotoes(bot, update):
    user_id = update.message.from_user.id

    button = []

    for i in range(len(all_user_data[user_id])):
        lista = "{}".format(all_user_data[user_id][i]["nome"])
        l = [InlineKeyboardButton("{}".format(lista), callback_data=lista)]
        button.append(l)

    reply_markup = InlineKeyboardMarkup(button)
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Escolha uma lista',
        reply_markup=reply_markup,
    )


def button(bot, update):
    query = update.callback_query

    bot.send_message(
        chat_id=query.message.chat_id,
        text='{}'.format(query.data),
    )
    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=[]
    )
    global selected
    selected = query.data


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
exibirlistaunica_handler = CommandHandler("exibir_lista", exibirlistaunica, pass_args=True)

criarLista_handler = CommandHandler("criar_lista", criarlista, pass_args=True)
criarEvento_handler = CommandHandler("criar_evento", criarevento, pass_args=True)

deletarevento_handler = CommandHandler("deletar_evento", deletarevento, pass_args=True)
deletarlista_handler = CommandHandler("deletar_lista", deletarlista, pass_args=True)
limparlista_handler = CommandHandler("limpar_lista", limparlista, pass_args=True)

mostrarbotoes_handler = CommandHandler("botoes", mostrarbotoes)
botoes_handler = CallbackQueryHandler(button)

handlers = [botoes_handler, mostrarbotoes_handler, exibirlistaunica_handler, deletarlista_handler, limparlista_handler, start_handler, listar_handler, deletarevento_handler, criarLista_handler, criarEvento_handler, help_handler, unknown_handler]

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
