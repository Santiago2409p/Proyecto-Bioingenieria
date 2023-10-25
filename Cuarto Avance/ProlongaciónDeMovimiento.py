import pygame
import sys
import speech_recognition as sr
import threading
from collections import deque
import random

carro_rect = None
juego_en_ejecucion = True

buffer_comandos = deque()

# Estados de los comandos
comando_arriba_activo = False
comando_abajo_activo = False
comando_izquierda_activo = False
comando_derecha_activo = False
comando_detener_activo = False

velocidad_carro = 1

def inicializar_pygame():
    global carro_rect, juego_en_ejecucion, buffer_comandos, comando_arriba_activo, comando_abajo_activo, comando_izquierda_activo, comando_derecha_activo, comando_detener_activo
    pygame.init()

    ventana = pygame.display.set_mode((800, 600))
    reloj = pygame.time.Clock()

    fondo = pygame.image.load('fondo.jpg')

    carro = pygame.image.load('carro.png')
    carro = pygame.transform.scale(carro, (carro.get_width() // 3, carro.get_height() // 3))
    carro_rect = carro.get_rect()
    carro_rect.y = 300

    franjas = [pygame.Rect(i * 100, 300, 50, 10) for i in range(8)]
    velocidad_franjas = 5

    obstaculos = []
    for _ in range(5):
        obstaculo = pygame.image.load('obstaculo.png')
        obstaculo = pygame.transform.scale(obstaculo, (obstaculo.get_width() // 4, obstaculo.get_height() // 4))
        obstaculo_rect = obstaculo.get_rect()
        obstaculo_rect.x = random.randint(800, 1600)
        obstaculo_rect.y = random.randint(0, 600)
        velocidad_obstaculo = random.randint(1, 2)
        obstaculos.append((obstaculo, obstaculo_rect, velocidad_obstaculo))

    while juego_en_ejecucion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for franja in franjas:
            franja.x -= velocidad_franjas
            if franja.right < 0:
                franja.left = 800

        ventana.blit(fondo, (0, 0))

        for franja in franjas:
            pygame.draw.rect(ventana, (255, 255, 255), franja)

        ventana.blit(carro, carro_rect)

        for obstaculo, obstaculo_rect, velocidad_obstaculo in obstaculos:
            obstaculo_rect.x -= velocidad_obstaculo
            if obstaculo_rect.right < 0:
                obstaculo_rect.left = random.randint(800, 1600)
                obstaculo_rect.y = random.randint(0, 600)
                velocidad_obstaculo = random.randint(1, 2)
            ventana.blit(obstaculo, obstaculo_rect)

        if comando_arriba_activo:
            carro_rect.y -= velocidad_carro
        elif comando_abajo_activo:
            carro_rect.y += velocidad_carro
        elif comando_izquierda_activo:
            carro_rect.x -= velocidad_carro
        elif comando_derecha_activo:
            carro_rect.x += velocidad_carro

        pygame.display.flip()
        reloj.tick(60)

def manejar_comandos_voz():
    global juego_en_ejecucion, buffer_comandos, comando_arriba_activo, comando_abajo_activo, comando_izquierda_activo, comando_derecha_activo, comando_detener_activo

    r = sr.Recognizer()
    comandos = ["arriba", "izquierda", "derecha", "detener", "abajo", "salir"]

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Esperando a que inicies los comandos de voz...")

    while juego_en_ejecucion:
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=3)
                texto = r.recognize_google(audio, language='es-ES')
                
                if texto.lower() in comandos:
                    print(f"Comando reconocido: {texto}")
                    # Activar el estado del comando correspondiente y desactivar otros comandos
                    if texto.lower() == "arriba":
                        comando_arriba_activo = True
                        comando_abajo_activo = False
                    elif texto.lower() == "abajo":
                        comando_abajo_activo = True
                        comando_arriba_activo = False
                    elif texto.lower() == "izquierda":
                        comando_izquierda_activo = True
                        comando_derecha_activo = False
                    elif texto.lower() == "derecha":
                        comando_derecha_activo = True
                        comando_izquierda_activo = False
                    elif texto.lower() == "detener":
                        comando_detener_activo = True
                        comando_arriba_activo = False
                        comando_abajo_activo = False
                        comando_izquierda_activo = False
                        comando_derecha_activo = False
                    elif texto.lower() == "salir":
                        print("Saliendo del juego...")
                        juego_en_ejecucion = False
                    
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado. Intenta de nuevo.")
            except sr.UnknownValueError:
                print("No se pudo entender el audio. Intenta de nuevo.")
            except sr.RequestError as e:
                print(f"Error al solicitar resultados; {e}. Intenta de nuevo.")

if __name__ == '__main__':

    pygame_thread = threading.Thread(target=inicializar_pygame)
    pygame_thread.start()

    voz_thread = threading.Thread(target=manejar_comandos_voz)
    voz_thread.start()

    pygame_thread.join()
    voz_thread.join()
