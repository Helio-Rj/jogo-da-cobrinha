import pygame
import random
import sys
import os

pygame.init()

LARGURA = 600
ALTURA = 600
TAMANHO = 20

ecra = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobrinha: Degradê e Recordes")
relogio = pygame.time.Clock()

# Cores
PRETO = (0, 0, 0)
VERMELHO = (220, 0, 0)
BRANCO = (255, 255, 255)
MARROM = (139, 69, 19)
VERDE_FOLHA = (50, 205, 50)
CINZA = (128, 128, 128)
AMARELO = (255, 215, 0)

ARQUIVO_RECORDE = "recorde.txt"


# --- FUNÇÕES DO RECORDE ---
def ler_recorde():
    if os.path.exists(ARQUIVO_RECORDE):
        with open(ARQUIVO_RECORDE, "r") as f:
            return int(f.read())
    return 0


def salvar_recorde(novo_recorde):
    with open(ARQUIVO_RECORDE, "w") as f:
        f.write(str(novo_recorde))


def tela_game_over(pontos):
    recorde_atual = ler_recorde()
    novo_recorde_batido = False

    if pontos > recorde_atual:
        recorde_atual = pontos
        salvar_recorde(recorde_atual)
        novo_recorde_batido = True

    esperando = True
    fonte_titulo = pygame.font.SysFont(None, 70)
    fonte_texto = pygame.font.SysFont(None, 40)

    ecra.fill(PRETO)

    texto_fim = fonte_titulo.render("FIM DE JOGO", True, VERMELHO)
    texto_pontos = fonte_texto.render(f"Sua Pontuação: {pontos}", True, BRANCO)
    texto_recorde = fonte_texto.render(f"Recorde Histórico: {recorde_atual}", True, AMARELO)
    texto_aviso = fonte_texto.render("Pressione ESPAÇO para tentar de novo", True, CINZA)

    ecra.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, 120))
    ecra.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, 250))
    ecra.blit(texto_recorde, (LARGURA // 2 - texto_recorde.get_width() // 2, 300))

    if novo_recorde_batido:
        texto_parabens = fonte_texto.render("NOVO RECORDE!", True, VERDE_FOLHA)
        ecra.blit(texto_parabens, (LARGURA // 2 - texto_parabens.get_width() // 2, 350))

    ecra.blit(texto_aviso, (LARGURA // 2 - texto_aviso.get_width() // 2, 500))
    pygame.display.flip()

    while esperando:
        relogio.tick(15)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False


# --- FUNÇÕES DE DESENHO ---
def desenhar_fundo_degrade():
    # Desenha 600 linhas horizontais misturando as cores
    for y in range(ALTURA):
        p = y / ALTURA
        # Do Azul Céu (135, 206, 235) para o Verde Grama (34, 139, 34)
        r = int(135 + (34 - 135) * p)
        g = int(206 + (139 - 206) * p)
        b = int(235 + (34 - 235) * p)
        pygame.draw.line(ecra, (r, g, b), (0, y), (LARGURA, y))


def desenhar_maca_realista(x, y):
    cx = x + TAMANHO // 2
    pygame.draw.ellipse(ecra, VERMELHO, (x, y + 2, TAMANHO, TAMANHO - 3))
    pygame.draw.line(ecra, MARROM, (cx, y + 2), (cx, y - 5), 3)
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
    # A comida agora sorteia respeitando o limite da borda cinza
    comida_x = random.randrange(TAMANHO, LARGURA - TAMANHO, TAMANHO)
    comida_y = random.randrange(TAMANHO, ALTURA - TAMANHO, TAMANHO)


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
        nx = cobra[0][0] + dx
        ny = cobra[0][1] + dy

        # Teletransporte ajustado por causa da borda cinza
        if nx < TAMANHO:
            nx = LARGURA - TAMANHO * 2
        elif nx >= LARGURA - TAMANHO:
            nx = TAMANHO

        if ny < TAMANHO:
            ny = ALTURA - TAMANHO * 2
        elif ny >= ALTURA - TAMANHO:
            ny = TAMANHO

        nova_cabeca = (nx, ny)

        # O Fim de Jogo acontece EXCLUSIVAMENTE se a cobra morder ela mesma
        if nova_cabeca in cobra:
            tela_game_over(comidas_comidas)
            reiniciar_jogo()
            continue

        cobra.insert(0, nova_cabeca)

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
    desenhar_fundo_degrade()

    # Desenhar a Borda Cinza por cima do fundo (Espessura = TAMANHO)
    pygame.draw.rect(ecra, CINZA, (0, 0, LARGURA, ALTURA), TAMANHO)

    # Desenhar Comida e Corpo
    if comidas_comidas % 2 == 0:
        desenhar_maca_realista(comida_x, comida_y)
    else:
        pygame.draw.rect(ecra, PRETO, (comida_x, comida_y, TAMANHO, TAMANHO))

    for i in range(len(cobra) - 1, 0, -1):
        x, y = cobra[i]
        cor_atual = cores_corpo[i - 1]
        if i == len(cobra) - 1 and len(cobra) > 1:
            desenhar_rabo(x, y, cobra[i - 1][0], cobra[i - 1][1], cor_atual)
        else:
            pygame.draw.rect(ecra, cor_atual, (x, y, TAMANHO, TAMANHO))

    desenhar_cabeca(cobra[0][0], cobra[0][1], direcao_atual)

    pygame.display.flip()

pygame.quit()
sys.exit()
