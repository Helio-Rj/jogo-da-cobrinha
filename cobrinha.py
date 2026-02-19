import pygame
import random
import sys

# Ligar o motor do Pygame
pygame.init()

# Dimensões do ecrã e tamanho dos blocos
LARGURA = 600
ALTURA = 600
TAMANHO = 20

ecra = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha: Paredes Infinitas & Maçã Real")
relogio = pygame.time.Clock()

# Cores (R, G, B)
VERDE_GRAMA = (34, 139, 34)
PRETO = (0, 0, 0)
VERMELHO = (220, 0, 0)
BRANCO = (255, 255, 255)
MARROM = (139, 69, 19)  # Para o cabo da maçã
VERDE_FOLHA = (50, 205, 50)  # Para a folha da maçã


# --- FUNÇÕES DE DESENHO ---

def desenhar_maca_realista(x, y):
    # O centro do quadrado da comida
    cx = x + TAMANHO // 2

    # 1. O corpo da maçã (um círculo ligeiramente achatado)
    # Usamos ellipse para não ser uma bola perfeita
    pygame.draw.ellipse(ecra, VERMELHO, (x, y + 2, TAMANHO, TAMANHO - 3))

    # 2. O cabinho marrom no topo
    pygame.draw.line(ecra, MARROM, (cx, y + 2), (cx, y - 5), 3)

    # 3. Uma pequena folha verde ao lado do cabo
    pygame.draw.ellipse(ecra, VERDE_FOLHA, (cx, y - 6, 8, 5))


def desenhar_cabeca(x, y, direcao):
    cx = x + TAMANHO // 2
    cy = y + TAMANHO // 2

    pygame.draw.circle(ecra, PRETO, (cx, cy), TAMANHO // 2)

    if direcao == "PARADA": direcao = "DIREITA"

    if direcao == 'DIREITA':
        olho1, olho2 = (cx + 2, cy - 4), (cx + 2, cy + 4)
        l_inicio, l_meio = (cx + TAMANHO // 2, cy), (cx + TAMANHO // 2 + 8, cy)
        l_ponta1, l_ponta2 = (cx + TAMANHO // 2 + 12, cy - 4), (cx + TAMANHO // 2 + 12, cy + 4)
    elif direcao == 'ESQUERDA':
        olho1, olho2 = (cx - 2, cy - 4), (cx - 2, cy + 4)
        l_inicio, l_meio = (cx - TAMANHO // 2, cy), (cx - TAMANHO // 2 - 8, cy)
        l_ponta1, l_ponta2 = (cx - TAMANHO // 2 - 12, cy - 4), (cx - TAMANHO // 2 - 12, cy + 4)
    elif direcao == 'CIMA':
        olho1, olho2 = (cx - 4, cy - 2), (cx + 4, cy - 2)
        l_inicio, l_meio = (cx, cy - TAMANHO // 2), (cx, cy - TAMANHO // 2 - 8)
        l_ponta1, l_ponta2 = (cx - 4, cy - TAMANHO // 2 - 12), (cx + 4, cy - TAMANHO // 2 - 12)
    elif direcao == 'BAIXO':
        olho1, olho2 = (cx - 4, cy + 2), (cx + 4, cy + 2)
        l_inicio, l_meio = (cx, cy + TAMANHO // 2), (cx, cy + TAMANHO // 2 + 8)
        l_ponta1, l_ponta2 = (cx - 4, cy + TAMANHO // 2 + 12), (cx + 4, cy + TAMANHO // 2 + 12)

    pygame.draw.circle(ecra, BRANCO, olho1, 3)
    pygame.draw.circle(ecra, BRANCO, olho2, 3)
    pygame.draw.circle(ecra, PRETO, olho1, 1)
    pygame.draw.circle(ecra, PRETO, olho2, 1)
    pygame.draw.line(ecra, VERMELHO, l_inicio, l_meio, 2)
    pygame.draw.line(ecra, VERMELHO, l_meio, l_ponta1, 2)
    pygame.draw.line(ecra, VERMELHO, l_meio, l_ponta2, 2)


def desenhar_rabo(x, y, x_ant, y_ant, cor):
    cx = x + TAMANHO // 2
    cy = y + TAMANHO // 2
    if x_ant > x:
        pontos = [(x + TAMANHO, y), (x + TAMANHO, y + TAMANHO), (x, cy)]
    elif x_ant < x:
        pontos = [(x, y), (x, y + TAMANHO), (x + TAMANHO, cy)]
    elif y_ant > y:
        pontos = [(x, y + TAMANHO), (x + TAMANHO, y + TAMANHO), (cx, y)]
    else:
        pontos = [(x, y), (x + TAMANHO, y), (cx, y + TAMANHO)]
    pygame.draw.polygon(ecra, cor, pontos)


# --- LÓGICA DO JOGO ---

def reiniciar_jogo():
    global cobra, cores_corpo, direcao_atual, dx, dy, comidas_comidas, comida_x, comida_y
    cobra = [(300, 300)]
    cores_corpo = []
    direcao_atual = "PARADA"
    dx, dy = 0, 0
    comidas_comidas = 0
    sortear_comida()


def sortear_comida():
    global comida_x, comida_y
    comida_x = random.randrange(0, LARGURA, TAMANHO)
    comida_y = random.randrange(0, ALTURA, TAMANHO)


reiniciar_jogo()

rodando = True
while rodando:
    relogio.tick(10)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and direcao_atual != "BAIXO":
                direcao_atual = "CIMA"
                dx, dy = 0, -TAMANHO
            elif evento.key == pygame.K_DOWN and direcao_atual != "CIMA":
                direcao_atual = "BAIXO"
                dx, dy = 0, TAMANHO
            elif evento.key == pygame.K_LEFT and direcao_atual != "DIREITA":
                direcao_atual = "ESQUERDA"
                dx, dy = -TAMANHO, 0
            elif evento.key == pygame.K_RIGHT and direcao_atual != "ESQUERDA":
                direcao_atual = "DIREITA"
                dx, dy = TAMANHO, 0

    if direcao_atual != "PARADA":
        # Calcula onde será a nova cabeça
        nx = cobra[0][0] + dx
        ny = cobra[0][1] + dy

        # --- LÓGICA DAS PAREDES INFINITAS (TELETRANSPORTE) ---
        if nx < 0:
            nx = LARGURA - TAMANHO  # Saiu pela esquerda, aparece na direita
        elif nx >= LARGURA:
            nx = 0  # Saiu pela direita, aparece na esquerda

        if ny < 0:
            ny = ALTURA - TAMANHO  # Saiu por cima, aparece em baixo
        elif ny >= ALTURA:
            ny = 0  # Saiu por baixo, aparece em cima

        nova_cabeca = (nx, ny)
        # -----------------------------------------------------

        # Bater no próprio corpo (ainda morre se bater nela mesma)
        if nova_cabeca in cobra:
            pygame.time.wait(1000)
            reiniciar_jogo()
            continue

        cobra.insert(0, nova_cabeca)

        # Verificar se comeu
        if nova_cabeca[0] == comida_x and nova_cabeca[1] == comida_y:
            if comidas_comidas % 2 == 0:
                cores_corpo.append(VERMELHO)
            else:
                cores_corpo.append(PRETO)
            comidas_comidas += 1
            sortear_comida()
        else:
            cobra.pop()

    # --- DESENHAR O ECRÃ ---
    ecra.fill(VERDE_GRAMA)

    # Desenhar a Comida atual
    if comidas_comidas % 2 == 0:
        # Agora chama a função da maçã realista!
        desenhar_maca_realista(comida_x, comida_y)
    else:
        # Chocolate continua quadrado preto
        pygame.draw.rect(ecra, PRETO, (comida_x, comida_y, TAMANHO, TAMANHO))

    # Desenhar o Corpo
    for i in range(len(cobra) - 1, 0, -1):
        x, y = cobra[i]
        cor_atual = cores_corpo[i - 1]
        if i == len(cobra) - 1 and len(cobra) > 1:
            desenhar_rabo(x, y, cobra[i - 1][0], cobra[i - 1][1], cor_atual)
        else:
            pygame.draw.rect(ecra, cor_atual, (x, y, TAMANHO, TAMANHO))

    # Desenhar a Cabeça
    desenhar_cabeca(cobra[0][0], cobra[0][1], direcao_atual)

    pygame.display.flip()

pygame.quit()
sys.exit()