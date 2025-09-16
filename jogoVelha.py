import pygame
import sys
import random

# --- Inicialização do Pygame ---
pygame.init()

# --- Constantes de Design e Layout ---
LARGURA, ALTURA = 400, 550  # Aumentei a altura para a pergunta de matemática
TAMANHO_CELULA = LARGURA // 3
ESPESSURA_LINHA_GRADE = 10
ESPESSURA_SIMBOLO = 15
RAIO_CIRCULO = TAMANHO_CELULA // 3
OFFSET_X = TAMANHO_CELULA // 4

# --- Paleta de Cores ---
COR_FUNDO = (28, 170, 156)
COR_GRADE = (13, 161, 146)
COR_INFO = (23, 145, 135)
COR_X = (84, 84, 84)
COR_O = (242, 235, 211)
COR_VITORIA = (255, 87, 34)
COR_TEXTO = (255, 255, 255)
COR_PERGUNTA = (255, 224, 130) # Amarelo claro para a pergunta

# --- Configuração da Tela e Fontes ---
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha Matemático')
fonte_status = pygame.font.SysFont('Arial', 30, bold=True)
fonte_pergunta = pygame.font.SysFont('Arial', 32, bold=True)
fonte_input = pygame.font.SysFont('Arial', 28)

# --- Estados do Jogo ---
# 'JOGANDO': Escolhendo uma casa no tabuleiro
# 'RESPONDENDO': Respondendo à pergunta de matemática
# 'GAME_OVER': O jogo terminou
estado_jogo = 'JOGANDO'

# --- Variáveis de Estado do Jogo ---
tabuleiro = [[None] * 3 for _ in range(3)]
jogador_atual = "X"
vencedor = None
linha_vitoria = None

# --- Variáveis para o Desafio Matemático ---
pergunta_matematica = ""
resposta_correta = 0
input_usuario = ""
jogada_pendente = None # Armazena a (linha, coluna) que o jogador escolheu

# --- Funções de Desenho (a maioria permanece a mesma) ---
def desenhar_fundo_e_grade():
    tela.fill(COR_FUNDO)
    pygame.draw.rect(tela, COR_INFO, (0, LARGURA, LARGURA, ALTURA - LARGURA))
    for i in range(1, 3):
        pygame.draw.line(tela, COR_GRADE, (0, i * TAMANHO_CELULA), (LARGURA, i * TAMANHO_CELULA), ESPESSURA_LINHA_GRADE)
        pygame.draw.line(tela, COR_GRADE, (i * TAMANHO_CELULA, 0), (i * TAMANHO_CELULA, LARGURA), ESPESSURA_LINHA_GRADE)

def desenhar_simbolos():
    for linha in range(3):
        for coluna in range(3):
            centro_x = coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
            centro_y = linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
            if tabuleiro[linha][coluna] == "X":
                p1 = (centro_x - OFFSET_X, centro_y - OFFSET_X)
                p2 = (centro_x + OFFSET_X, centro_y + OFFSET_X)
                p3 = (centro_x + OFFSET_X, centro_y - OFFSET_X)
                p4 = (centro_x - OFFSET_X, centro_y + OFFSET_X)
                pygame.draw.line(tela, COR_X, p1, p2, ESPESSURA_SIMBOLO)
                pygame.draw.line(tela, COR_X, p3, p4, ESPESSURA_SIMBOLO)
            elif tabuleiro[linha][coluna] == "O":
                pygame.draw.circle(tela, COR_O, (centro_x, centro_y), RAIO_CIRCULO, ESPESSURA_SIMBOLO)

def desenhar_linha_vitoria():
    if linha_vitoria:
        tipo, indice = linha_vitoria
        if tipo == 'linha': y = indice * TAMANHO_CELULA + TAMANHO_CELULA // 2; pygame.draw.line(tela, COR_VITORIA, (15, y), (LARGURA - 15, y), 15)
        elif tipo == 'coluna': x = indice * TAMANHO_CELULA + TAMANHO_CELULA // 2; pygame.draw.line(tela, COR_VITORIA, (x, 15), (x, LARGURA - 15), 15)
        elif tipo == 'diag1': pygame.draw.line(tela, COR_VITORIA, (25, 25), (LARGURA - 25, LARGURA - 25), 20)
        elif tipo == 'diag2': pygame.draw.line(tela, COR_VITORIA, (LARGURA - 25, 25), (25, LARGURA - 25), 20)

def desenhar_status_e_perguntas():
    """Exibe o status do jogo ou a pergunta de matemática."""
    if estado_jogo == 'RESPONDENDO':
        # Mostra a pergunta e a resposta do usuário
        pergunta_surf = fonte_pergunta.render(pergunta_matematica, True, COR_PERGUNTA)
        pergunta_rect = pergunta_surf.get_rect(center=(LARGURA / 2, LARGURA + 40))
        tela.blit(pergunta_surf, pergunta_rect)
        
        input_surf = fonte_input.render("Sua resposta: " + input_usuario, True, COR_TEXTO)
        input_rect = input_surf.get_rect(center=(LARGURA / 2, LARGURA + 90))
        tela.blit(input_surf, input_rect)
    else:
        # Mostra o status normal do jogo
        if vencedor:
            mensagem = f"Jogador '{vencedor}' venceu!" if vencedor != "Empate" else "Deu velha!"
        else:
            mensagem = f"Vez do jogador '{jogador_atual}'"
        
        status_surf = fonte_status.render(mensagem, True, COR_TEXTO)
        status_rect = status_surf.get_rect(center=(LARGURA / 2, LARGURA + 40))
        tela.blit(status_surf, status_rect)

        if estado_jogo == 'GAME_OVER':
            restart_surf = fonte_input.render("Pressione 'R' para reiniciar", True, COR_TEXTO)
            restart_rect = restart_surf.get_rect(center=(LARGURA / 2, LARGURA + 90))
            tela.blit(restart_surf, restart_rect)

# --- Lógica do Jogo e Matemática ---
def gerar_pergunta():
    """Gera uma nova pergunta de matemática."""
    global pergunta_matematica, resposta_correta
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operador = random.choice(['+', '-', '*'])
    
    if operador == '+':
        pergunta_matematica = f"{a} + {b} = ?"
        resposta_correta = a + b
    elif operador == '-':
        # Garante que a resposta não seja negativa
        if a < b: a, b = b, a
        pergunta_matematica = f"{a} - {b} = ?"
        resposta_correta = a - b
    elif operador == '*':
        pergunta_matematica = f"{a} * {b} = ?"
        resposta_correta = a * b

def proximo_jogador():
    """Passa a vez para o próximo jogador."""
    global jogador_atual
    jogador_atual = "O" if jogador_atual == "X" else "X"

def reiniciar_jogo():
    """Reseta o estado do jogo."""
    global tabuleiro, jogador_atual, estado_jogo, vencedor, linha_vitoria, input_usuario
    tabuleiro = [[None] * 3 for _ in range(3)]
    jogador_atual = "X"
    estado_jogo = 'JOGANDO'
    vencedor = None
    linha_vitoria = None
    input_usuario = ""

def checar_vencedor():
    global linha_vitoria
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] and tabuleiro[i][0] is not None: linha_vitoria = ('linha', i); return tabuleiro[i][0]
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] and tabuleiro[0][i] is not None: linha_vitoria = ('coluna', i); return tabuleiro[0][i]
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None: linha_vitoria = ('diag1', 0); return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None: linha_vitoria = ('diag2', 0); return tabuleiro[0][2]
    if all(all(cell is not None for cell in row) for row in tabuleiro): return "Empate"
    return None

# --- Loop Principal ---
def main():
    global estado_jogo, input_usuario, jogada_pendente, vencedor

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- Lógica para o estado 'JOGANDO' ---
            if estado_jogo == 'JOGANDO':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < LARGURA:
                        linha = y // TAMANHO_CELULA
                        coluna = x // TAMANHO_CELULA
                        if tabuleiro[linha][coluna] is None:
                            # Guarda a jogada e muda para o estado de resposta
                            jogada_pendente = (linha, coluna)
                            gerar_pergunta()
                            estado_jogo = 'RESPONDENDO'
                            input_usuario = ""

            # --- Lógica para o estado 'RESPONDENDO' ---
            elif estado_jogo == 'RESPONDENDO':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Pressionou Enter
                        try:
                            if int(input_usuario) == resposta_correta:
                                # Acertou! Realiza a jogada.
                                linha, coluna = jogada_pendente
                                tabuleiro[linha][coluna] = jogador_atual
                                vencedor = checar_vencedor()
                                if vencedor:
                                    estado_jogo = 'GAME_OVER'
                                else:
                                    proximo_jogador()
                                    estado_jogo = 'JOGANDO'
                            else:
                                # Errou! Perde a vez.
                                print("Resposta errada! Perdeu a vez.")
                                proximo_jogador()
                                estado_jogo = 'JOGANDO'
                        except ValueError:
                            # Input inválido (não é um número)
                            print("Entrada inválida. Perdeu a vez.")
                            proximo_jogador()
                            estado_jogo = 'JOGANDO'
                    elif event.key == pygame.K_BACKSPACE:
                        input_usuario = input_usuario[:-1]
                    elif event.unicode.isdigit():
                        input_usuario += event.unicode

            # --- Lógica para o estado 'GAME_OVER' ---
            elif estado_jogo == 'GAME_OVER':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reiniciar_jogo()

        # --- Renderização ---
        desenhar_fundo_e_grade()
        desenhar_simbolos()
        if estado_jogo == 'GAME_OVER' and vencedor != "Empate":
            desenhar_linha_vitoria()
        desenhar_status_e_perguntas()
        
        pygame.display.update()

if __name__ == "__main__":
    main()