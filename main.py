import os
import telebot
import requests
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from functools import partial

CHAVE_API = os.getenv('')#key sistema

bot = telebot.TeleBot(CHAVE_API)
message_continius = "Você está no controle! Se quiser experimentar outras opções ou precisar de mais informações, estou à disposição:"
user_data = {}

def main():
    global user_data
    
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Erro de coxexão: {e}")

def send_to(user_data):
    url = ""#url para conexão de api
    
    data = {
        "mkt": {
            "ref_instalacao": "",#chave sistema
            "nome": user_data[0],
            "email": user_data[1],
            "telefone": user_data[2],
            "motivoContato": user_data[3]
        },
        "email": {
            "email": "",#email
            "assunto": f"Contato de {user_data[0]} pelo Telegram"
        },
        "nomeLp": "Telegram BOT"
    }

    if len(user_data) > 4:
        data["mkt"]["sobrenome"] = user_data[4]

    response = requests.post(url, json=data)

#Mensagem de Boas-Vindas
@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    user_data[message.chat.id] = []

    if os.path.exists("xxx.png"):
        with open("xxx.png", "rb") as img:
            bot.send_photo(message.chat.id, img)
    
    bot.send_message(message.chat.id, """Boas-vindas à , onde <b> "O seu sucesso, é o nosso compromisso!"</b>""", parse_mode="HTML")
    send_keyboard(message, "Escolha uma opção para continuar:")

#botão que direciona para!
def button_func(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Conhecer", url="")
    keyboard.row(button1)

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#botão whatsapp e ladding page
def button_contacts(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("WhatsApp", url="") 
                                                   
    button2 = InlineKeyboardButton("Landing Page", url="")
    keyboard.row(button1)
    keyboard.row(button2)
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#Botões para exibir formas de contato
def button_social(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Youtube", url="")
    button2 = InlineKeyboardButton("Instagram", url="")
    button3 = InlineKeyboardButton("Facebook", url="")
    button4 = InlineKeyboardButton("X (antigo Twitter)", url="")

    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#botão de aceite de termos de privacidade
def button_terms(message, message_text):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Li e concordo", callback_data="concordo")
    keyboard.row(button1)
    bot.send_message(message.chat.id, message_text,reply_markup=keyboard)
    

#botão que chama o teclado de botões
def button_more(message,message_text):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Quero Assinar o", url="")
    button2 = InlineKeyboardButton("Quero ver mais opções", callback_data="keyboard")
    keyboard.row(button1)
    keyboard.row(button2)

    
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#bottões padrões do chat
def send_keyboard(message, message_text):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Quero Assinar o", url="")
    button2 = InlineKeyboardButton("Quero Saber Mais Sobre a ", callback_data="opcao2")
    button3 = InlineKeyboardButton("Quero Entrar em Contato com a ", callback_data="opcao3")
    button4 = InlineKeyboardButton("Quero Conhecer as redes sociais da ", callback_data="opcao4")
    button5 = InlineKeyboardButton("Quero que a entre em contato comigo", callback_data="opcao5")
    button6 = InlineKeyboardButton("Finalizar Atendimento", callback_data="finalizar")
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    keyboard.row(button6)
    
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#Função de mensagens
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    #deletando botões do teclado
    try:
        # Deletando botões do teclado
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass

    if call.data == "opcao2":

        #Foto dos chefes
        if os.path.exists("yyyy.png"):
            with open("yyyy.png", "rb") as img:
                bot.send_photo(call.message.chat.id, img)

        bot.send_message(call.message.chat.id, """
                         """)
        bot.send_message(call.message.chat.id,"""""")
        button_func(call.message,"Para saber mais sobre, convidamos você a descobrir a ferramenta que impulsionará seus objetivos!")
        button_more(call.message, message_continius)

    #chamada do teclado (opções)
    elif call.data == "keyboard":
        send_keyboard(call.message, message_continius)

    #Usario quer entrar em contato
    elif call.data == "opcao3":
        button_contacts(call.message, """
                         """)

        button_more(call.message, message_continius)

    #exibindo as redes sociais
    elif call.data == "opcao4":
        button_social(call.message,"Conheça nas redes sociais:")
        button_more(call.message, message_continius)

    #Pedindo Nome e inicializando a coleta de dados
    elif call.data == "opcao5":
        privacy_link = ""
        privacy_message = "Antes leia nossas [políticas de privacidade](" + privacy_link + ")."
        bot.send_message(call.message.chat.id, privacy_message, parse_mode="Markdown")
        button_terms(call.message, "Agora nos diga se você leu e concorda com nossas políticas de privacidade!")

    
    #verificando se o usuario clickou em aceitar
    elif call.data == "concordo":
        bot.send_message(call.message.chat.id, "Digite seu nome:")
        bot.register_next_step_handler(call.message, partial(get_email, user_id=call.message.chat.id))
    #verificando se o usuario clickou em negar

    elif call.data == "finalizar":
        bot.send_message(call.message.chat.id, "Atendimento finalizado, agradeçe!")
        if call.message.chat.id in user_data:
            del user_data[call.message.chat.id]
    else:
        bot.send_message(call.message.chat.id, "Opção inválida. Por favor, tente novamente.")

#função pedindo email ao usuario
def get_email(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, "Digite seu e-mail:")
    bot.register_next_step_handler(message, partial(get_telefone, user_id=user_id))

#função pedindo telefone ao usuario
def get_telefone(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, """Digite seu telefone:
Ex: (##) ####-#####""")
    bot.register_next_step_handler(message, partial(get_motivo, user_id=user_id))

#Função pedindo motivo do contato
def get_motivo(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, "Informe o motivo do contato:")
    bot.register_next_step_handler(message, partial(save_data, user_id=user_id))


    

#salvando dados
def save_data(message, user_id):
    phone = message.text
    user_data[user_id].append(phone)

    name = user_data[user_id][0].strip()
    if " " in name:
        split_name = name.split(" ", 1)
        user_data[user_id][0] = split_name[0].strip()
        user_data[user_id].append(split_name[1].strip())
    
    bot.send_message(message.chat.id, "Obrigado pela colaboração, em breve, entraremos em contato!")
    send_to(user_data[user_id])
    bot.send_message(message.chat.id, "Atendimento finalizado, agradece!")
    bot.clear_step_handler(message)

if __name__ == "__main__":
    main()