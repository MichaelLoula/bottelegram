import os.path

import telebot
import requests
import io
from datetime import datetime
from pytz import timezone
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from functools import partial
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#chave api do CONSISTE _Bot
CHAVE_API = "6994012488:AAEP_1lS1hIyhOk7peViJK61a_Sbpij6HiA"

bot = telebot.TeleBot(CHAVE_API)
#, retry_interval=10
#Mensagem de continuidade do bot
message_continius = "Você está no controle! Se quiser experimentar outras opções ou precisar de mais informações, estou à disposição:"

messages_sent = set()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1saG-dfVZEUmu_dLoOjm85XEc0xyMIQMLUWslXTVjrQc'
SAMPLE_RANGE_NAME = 'DadosTelegram!A1:D10'

def main():
    global user_data
    user_data = {}
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Erro de coxexão: {e}")

#autentifica e salva dados no google sheets
def save_to_google_sheets(user_data):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        
        result = service.spreadsheets().values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="DadosTelegram!A:A"  
        ).execute()
        values = result.get('values', [])
        next_empty_row = len(values) + 1


        range_name = f"DadosTelegram!A{next_empty_row}" 
        date_now = datetime.now()
        time_zone = timezone('America/Sao_Paulo')
        date_timenow = date_now.astimezone(time_zone)
        user_data.append(date_timenow.strftime('%d/%m/%Y - %H:%M:%S'))
        values_update = [
            user_data,
        ]

        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            body={'values': values_update}
        ).execute()

    except HttpError as err:
        print(err)

#Mensagem de Boas-Vindas
@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    user_data[message.chat.id] = []

    if os.path.exists("logoConsisteXTR.png"):
        with open("logoConsisteXTR.png", "rb") as img:
            bot.send_photo(message.chat.id, img)
    
    bot.send_message(message.chat.id, """Boas-vindas à CONSISTE / XTR, onde <b> "O seu sucesso, é o nosso compromisso!"</b>""", parse_mode="HTML")
    send_keyboard(message, "Escolha uma opção para continuar:")

#botão que direciona para o XTR!
def button_xtr(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Conhecer o XTR", url="xtrbrasil.com") #https://l.instagram.com/?u=http%3A%2F%2Fxtrbrasil.com%2F&e=AT33UamwqeaIvupphMZ7tLCBcXVaf5BMrJZD5rZO3_rvHNxl-O5dKJk8eQGEx2hh2fB2T6oJ0Zj4zblAVpaDTQND6xRhj1jeaiMO3f2FPYiZ-jdk2wcKrg

    keyboard.row(button1)

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

def button_contacts(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("WhatsApp", url="https://wa.me/557181255686?text=Ol%C3%A1%2C+quero+saber+mais+sobre+o+XTR") 
                                                   #https://xtr.consiste .com.br/cq/zap?phone=+5571981255686&text=Quero%20saber%20mais%20sobre%20o%20XTR
    button2 = InlineKeyboardButton("Laddingpage", url="https://www.consiste.com.br/portal.nsf/faleconosco.xsp")
    keyboard.row(button1)
    keyboard.row(button2)
    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#botão link do site CONSISTE 
def button_webConsi(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Site", url="www.consiste.com.br/portal.nsf/index.xsp")
    
    keyboard.row(button1)

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

#Botões para exibir formas de contato
def button_social(message, message_text):
    keyboard = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton("Youtube", url="https://www.youtube.com/@CONSISTECONSULTORIA")
    button2 = InlineKeyboardButton("Instagram", url="https://www.instagram.com/plataformaxtr/")
    button3 = InlineKeyboardButton("Facebook", url="https://www.facebook.com/CONSISTE")
    button4 = InlineKeyboardButton("X (antigo Twitter)", url="https://twitter.com/CONSISTE")

    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)

def button_terms(message, message_text):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Li e concordo", callback_data="concordo")
    keyboard.row(button1)
    bot.send_message(message.chat.id, message_text,reply_markup=keyboard)
    print()

#bottões padrões do chat
def send_keyboard(message, message_text):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Quero Saber Mais Sobre a CONSISTE / XTR", callback_data="opcao1")
    button2 = InlineKeyboardButton("Quero Entrar em Contato com a CONSISTE / XTR", callback_data="opcao2")
    button3 = InlineKeyboardButton("Quero Conhecer as redes sociais da CONSISTE / XTR", callback_data="opcao3")
    button4 = InlineKeyboardButton("Quero que a CONSISTE / XTR entre em contato comigo", callback_data="opcao4")
    button5 = InlineKeyboardButton("Finalizar Atendimento", callback_data="finalizar")
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    
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
        #print("Mensagem já foi apagada:", e)

    if call.message.message_id in messages_sent:
        # Se a mensagem já foi enviada, não faça nada
        return
    else:
        # Adicione o ID da mensagem ao conjunto de mensagens enviadas
        messages_sent.add(call.message.message_id)

    if call.data == "opcao1":
        #bot.send_photo(call.message.chat.id,"https://lh3.googleusercontent.com/pw/AP1GczNPDnuneEaYoLC6HmZh8Q8BqVZtLNL5pWAKqqQRbG624igV79QJlopPLRfHmZSRX04rjIU5DIjzFan1xUJxasuRjtZfUnLpdkznUAor0n26nf-9Pz6KwQ7H1KxpduzFxUE9fd7lzJ9GvZu1T08SfmEqvI5EXQMaqmacNEXfdOLQdO_2hn4MAK4bMhufhvDhEIj56f9IupNKHbCj6GADZrYwRjTlmYGfB8Hbv_C3Z0-oRRHP6WqpPQZrHc6o0fn4J1S5kP04QrICSbvtmFlDy9hhKJX-X64p6ObAwneA58f-LFYfzOs9Vj_mJIsa8nZx076ZYf3m0kwTnfe7OlzdcNXTvGFORelXkAJRmYSuDXgof47Xc53bV2OVT0h2ybD96ToNROFIKGbsrv4cQDuaGrvSI9eKCbxV8tlr4PYv7P7Bc4PlGTylYPXIG96EmP1zGmkY61u7JVSh3pj__k6rGt-BADZgTb6OPjUbVVZPabJ0y9Mt10-LOs84C7t5RvitJw969Avpy9lpjOjaCOoJ0g2vpvFhxqHdCjjGboGVcMOCm1b-27mUZMg6llYnALQltJi0Dej80EIvkNH6I7bKd9fRho-Hl4loyOw-QcHyiQSgwY6RfNifkTx-dLHri2cww0lAEYTKPEmXX3bZ48v0Zz7p5Ie-DZxw0YKf2RdF5bUpMmRSMszp2SZ6BxChCR8CSiHmlxbTHXEQEwqV8F-qkKVnj1pwz8OE_ciB7o7c6gLjaX33Wq4pWvD8igihPDfo3aLaONnblDMnnfl4qRG6vA7QhYXhB6o-M8dUf4B_-YrrTdDFwYINVsqIC9M0TS6tnzi17QDp_yv3ESJSTH66FHwklif37BV7y3-YkmV1RftQfrWiXTR2aw4qHUVkefMGa5X5D9O9JgxiHft8CK_7Wsf4roQspy8il6Q7ZOrzp5V-IJ13MPm3gez5CtqJSP92WJinD9kQsTOL0SsWgpwg-xFmOs0a=w200-h200-s-no-gm?authuser=2")
        
        if os.path.exists("mosqueteiros.png"):
            with open("mosqueteiros.png", "rb") as img:
                bot.send_photo(call.message.chat.id, img)
        
        bot.send_message(call.message.chat.id, """
    |   Moisés Bastos       |   Marcos Vinicius    |      Jorge Ramalho   |
             CTO                               CEO                                QC
                         """)
        bot.send_message(call.message.chat.id,"""CONSISTE / XTR:
    
    Missão: impulsionar o sucesso dos nossos clientes. Combinamos paixão por tecnologia e comprometimento com resultados para oferecer soluções inovadoras.
    
    nossa equipe, composta por profissionais íntegros e criativos, trabalha em um ambiente de confiança e colaboração, onde o cliente é prioridade absoluta.
    
    O XTR, nossa solução, é flexível e adaptável a diversas áreas. Desde a coleta de dados até o relacionamento com clientes, promove uma gestão eficiente e focada em resultados tangíveis.
    
    Venha conhecer a CONSISTE / XTR  e descubra como podemos ajudar a impulsionar o seu sucesso empresarial, servir é nossa paixão e seu sucesso, nossa prioridade!""")
        button_webConsi(call.message,"Para saber mais sobre a CONSISTE / XTR você também pode entrar em nosso site:")
        button_xtr(call.message,"Conheça a Ferramenta Que Vai Impulsionar os Seus Objetivos!")
        
        send_keyboard(call.message, message_continius)
    #Usario quer entrar em contato com a Consiste

    elif call.data == "opcao2":
        button_contacts(call.message, """Você pode entrar em contato com a CONSISTE / XTR  das seguintes formas:           
    Fone: (71) 2102-6969
    E-mail: contato@consiste.com.br
                         """)

        send_keyboard(call.message, message_continius)

    
    #exibindo as redes sociais da CONSISTE
    elif call.data == "opcao3":
        button_social(call.message,"Conheça a CONSISTE / XTR Nas Redes Sociais:")
        send_keyboard(call.message, message_continius)


    #Pedindo Nome e inicializando a coleta de dados
    elif call.data == "opcao4":  
        privacy_link = "www.consiste.com.br/portal.nsf/artigo.xsp?area=politica+de+privacidade"
        privacy_message = "Antes leia nossas [políticas de privacidade](" + privacy_link + ")."
        bot.send_message(call.message.chat.id, privacy_message, parse_mode="Markdown")
        button_terms(call.message, "Agora nós diga se você leu e concorda com as nossas politicas de privacidade!")

    
    #verificando se o usuario clickou em aceitar
    elif call.data == "concordo":
        bot.send_message(call.message.chat.id, "Por favor, digite seu Nome:")
        bot.register_next_step_handler(call.message, partial(get_email, user_id=call.message.chat.id))
    #verificando se o usuario clickou em negar

    elif call.data == "finalizar":
        bot.send_message(call.message.chat.id, "Atendimento finalizado, a CONSISTE / XTR agradeçe!")
        bot.clear_step_handler(call.message)
    else:
        bot.send_message(call.message.chat.id, "Opção inválida. Por favor, tente novamente.")

#função pedindo email ao usuario
def get_email(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, "Por favor, digite seu E-mail:")
    bot.register_next_step_handler(message, partial(get_telefone, user_id=user_id))

#função pedindo telefone ao usuario
def get_telefone(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, "Por favor, digite seu Telefone: Ex: (##) ####-#####")
    bot.register_next_step_handler(message, partial(get_motivo, user_id=user_id))
    

#Função pedindo motivo do contato
def get_motivo(message, user_id):
    user_data[user_id].append(message.text)
    bot.send_message(message.chat.id, "Informe o motivo do contato:")
    bot.register_next_step_handler(message, partial(save_data, user_id=user_id))

#salvando dados
def save_data(message, user_id):
    phone = message.text
    if user_data[user_id][-1]!= phone:
        user_data[user_id].append(phone)    
        bot.send_message(message.chat.id, "Obrigado pela colaboração, entraremos em contato em breve!")
        save_to_google_sheets(user_data[user_id])
        bot.send_message(message.chat.id, "Atendimento finalizado, a CONSISTE / XTR agradeçe!")
        bot.clear_step_handler(message)
    else:
        bot.send_message(message.chat.id, "Você já forneceu essas informações. Por favor, forneça um número de telefone diferente.")

if __name__ == "__main__":
    main()