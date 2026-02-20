import pygame
import random

TAMANHO = 20
MARROM = (139, 69, 19)

def desenhar_pedra(ecra, x, y):
    pygame.draw.ellipse(ecra, (105, 105, 105), (x, y, TAMANHO, TAMANHO))
    pygame.draw.ellipse(ecra, (169, 169, 169), (x+4, y+3, TAMANHO-8, TAMANHO-8))

def desenhar_tronco(ecra, x, y):
    pygame.draw.rect(ecra, MARROM, (x, y, TAMANHO, TAMANHO))
    pygame.draw.line(ecra, (160, 82, 45), (x, y+5), (x+TAMANHO, y+5), 2)
    pygame.draw.line(ecra, (160, 82, 45), (x, y+10), (x+TAMANHO, y+10), 2)

def adicionar_obstaculo(cobra, comida_x, comida_y, largura, altura):
    while True:
        ox = random.randrange(TAMANHO, largura - TAMANHO, TAMANHO)
        oy = random.randrange(TAMANHO, altura - TAMANHO, TAMANHO)
        if (ox, oy) not in cobra and (ox, oy) != (comida_x, comida_y):
            tipo = random.choice(["pedra", "tronco"])
            return (ox, oy, tipo)

def desenhar_obstaculos(ecra, obstaculos):
    for ox, oy, tipo in obstaculos:
        if tipo == "pedra":
            desenhar_pedra(ecra, ox, oy)
        else:
            desenhar_tronco(ecra, ox, oy)