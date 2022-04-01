from gtts import gTTS
import speech_recognition as sr
from subprocess import call     # MAC / LINUX
#from playsound import playsound # WINDOWS
from requests import get
from bs4 import BeautifulSoup



##### CONFIGURAÇÕES #####
hotword = 'rose'

with open('rosie-python-assistente-fe02a8d39c53.json') as credenciais_google:
    credenciais_google = credenciais_google.read()


##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    call(['afplay', 'audios/' + arquivo + '.mp3'])

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    print('ROSIE: ', mensagem)
    call(['afplay', 'audios/mensagem.mp3']) # OSX


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()



    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        cria_audio(mensagem)





def main():
    while True:
        monitora_audio()

main()




