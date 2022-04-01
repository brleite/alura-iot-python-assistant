import speech_recognition as sr
from subprocess import call     # MAC / LINUX
#from playsound import playsound # WINDOWS


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
                    print('Comando: ', trigger)
                    responde('feedback')
                    ### executar os comandos
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    call(['afplay', 'audios/' + arquivo + '.mp3'])





def main():
    monitora_audio()

main()



