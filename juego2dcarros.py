import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego
ventana = pygame.display.set_mode((800, 600))

# Configurar el reloj del juego
reloj = pygame.time.Clock()

# Configurar el carro
carro = pygame.image.load('carro.png')  # Asegúrate de tener una imagen llamada 'carro.png' en tu directorio
carro_rect = carro.get_rect()

# Configurar las franjas
franjas = [pygame.Rect(i * 100, 300, 50, 10) for i in range(8)]
velocidad_franjas = 5

# Lista para almacenar objetos cuadrados
objetos_cuadrados = []

# Bucle principal del juego
while True:
    # Eventos del juego
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del carro con las teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        carro_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        carro_rect.x += 5
    if keys[pygame.K_UP]:
        carro_rect.y -= 5
    if keys[pygame.K_DOWN]:
        carro_rect.y += 5

    # Movimiento de las franjas
    for franja in franjas:
        franja.x -= velocidad_franjas
        if franja.right < 0:
            franja.left = 800

    # Crear objetos cuadrados aleatorios
    if random.random() < 0.02:  # Probabilidad de aparición del objeto
        tamaño = random.randint(20, ventana.get_height() // 5)  # Tamaño aleatorio
        y = random.randint(0, ventana.get_height() - tamaño)  # Posición aleatoria (vertical)
        objeto_rect = pygame.Rect(ventana.get_width(), y, tamaño, tamaño)
        objetos_cuadrados.append(objeto_rect)

    # Mover los objetos cuadrados
    for objeto_rect in objetos_cuadrados:
        objeto_rect.x -= 5  # Velocidad de movimiento de los objetos

    # Eliminar objetos cuadrados que salen de la pantalla
    objetos_cuadrados = [objeto_rect for objeto_rect in objetos_cuadrados if objeto_rect.right > 0]

    # Dibujar el fondo, el carro, las franjas y los objetos cuadrados
    ventana.fill((0, 0, 0))
    ventana.blit(carro, carro_rect)
    for franja in franjas:
        pygame.draw.rect(ventana, (255, 255, 255), franja)
    for objeto_rect in objetos_cuadrados:
        pygame.draw.rect(ventana, (255, 0, 0), objeto_rect)  # Dibujar objetos cuadrados en rojo

    # Actualizar la pantalla y establecer el reloj a 60 FPS
    pygame.display.flip()
    reloj.tick(60)

