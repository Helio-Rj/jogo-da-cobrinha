import turtle
import time
import random

delay = 0.1

# 1. Configuração da Tela do Jogo
tela = turtle.Screen()
tela.title("Jogo da Cobrinha")
tela.bgcolor("green")  # Cor do fundo (gramado)
tela.setup(width=600, height=600)
tela.tracer(0)  # Desliga a atualização automática da tela para o jogo rodar suave

# 2. Cabeça da Cobra
cabeca = turtle.Turtle()
cabeca.speed(0)
cabeca.shape("square")
cabeca.color("black")
cabeca.penup()
cabeca.goto(0, 0)
cabeca.direction = "stop"

# 3. Comida da Cobra
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

corpo = []  # Lista que vai guardar os pedaços da cobra


# 4. Funções para controlar a direção
def ir_cima():
    if cabeca.direction != "down":
        cabeca.direction = "up"


def ir_baixo():
    if cabeca.direction != "up":
        cabeca.direction = "down"


def ir_esquerda():
    if cabeca.direction != "right":
        cabeca.direction = "left"


def ir_direita():
    if cabeca.direction != "left":
        cabeca.direction = "right"


def mover():
    if cabeca.direction == "up":
        y = cabeca.ycor()
        cabeca.sety(y + 20)
    if cabeca.direction == "down":
        y = cabeca.ycor()
        cabeca.sety(y - 20)
    if cabeca.direction == "left":
        x = cabeca.xcor()
        cabeca.setx(x - 20)
    if cabeca.direction == "right":
        x = cabeca.xcor()
        cabeca.setx(x + 20)


# 5. Configurando o Teclado (Usando as Setas)
tela.listen()
tela.onkeypress(ir_cima, "Up")
tela.onkeypress(ir_baixo, "Down")
tela.onkeypress(ir_esquerda, "Left")
tela.onkeypress(ir_direita, "Right")

# 6. O "Coração" do Jogo (Loop principal)
while True:
    tela.update()

    # Verifica se bateu nas paredes
    if cabeca.xcor() > 290 or cabeca.xcor() < -290 or cabeca.ycor() > 290 or cabeca.ycor() < -290:
        time.sleep(1)
        cabeca.goto(0, 0)
        cabeca.direction = "stop"

        # Esconde os pedaços antigos do corpo
        for pedaco in corpo:
            pedaco.goto(1000, 1000)
        corpo.clear()

    # Verifica se a cobra "comeu" a comida
    if cabeca.distance(comida) < 20:
        # Move a comida para um lugar aleatório
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)

        # Adiciona um novo pedaço ao corpo (alternando as cores do Flamengo)
        novo_pedaco = turtle.Turtle()
        novo_pedaco.speed(0)
        novo_pedaco.shape("square")
        if len(corpo) % 2 == 0:
            novo_pedaco.color("red")
        else:
            novo_pedaco.color("black")
        novo_pedaco.penup()
        corpo.append(novo_pedaco)

    # Faz o corpo seguir a cabeça
    for index in range(len(corpo) - 1, 0, -1):
        x = corpo[index - 1].xcor()
        y = corpo[index - 1].ycor()
        corpo[index].goto(x, y)

    if len(corpo) > 0:
        x = cabeca.xcor()
        y = cabeca.ycor()
        corpo[0].goto(x, y)

    mover()

    # Verifica se a cobra bateu no próprio corpo
    for pedaco in corpo:
        if pedaco.distance(cabeca) < 20:
            time.sleep(1)
            cabeca.goto(0, 0)
            cabeca.direction = "stop"
            for pedaco in corpo:
                pedaco.goto(1000, 1000)
            corpo.clear()

    time.sleep(delay)

tela.mainloop()
