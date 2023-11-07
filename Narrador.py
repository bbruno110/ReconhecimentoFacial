from gtts import gTTS
import pygame
    
def narrar(permissao, nome):

    texto = ""
    
    if(permissao == False):
        texto = "Acesso negado"
        
    else:
        
        texto = "Acesso autorizado Bem vindo" + nome
        
        
    tts2 = gTTS(text=texto, lang='pt-br')
    tts2.save('permissao.mp3')    
    
    
    pygame.init()
    pygame.mixer.music.load('./permissao.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(5000)  # Espera por 3 segundos (3000 milissegundos)
    



    
    
    
    
    