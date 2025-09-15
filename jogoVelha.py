import pygame
import sys

# --- Constantes ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

LARGURA = 300
ALTURA = 300
LINHA_ESPESSURA = 15

# --- Inicialização do Pygame ---
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha Melhorado')
fonte_jogo = pygame.font.SysFont(None, 100)
fonte_mensagem = pygame.font.SysFont(None, 40)

# --- Variáveis de Estado do Jogo ---
tabuleiro = [[None]*3 for _ in range(3)]
jogador_atual = "X"
game_over = False
mensagem_final = ""

# --- Funções de Desenho ---
def desenhar_grade():
    """Desenha a grade do jogo da velha."""
    pygame.draw.line(tela, PRETO, (100, 0), (100, 300), LINHA_ESPESSURA)
    pygame.draw.line(tela, PRETO, (200, 0), (200, 300), LINHA_ESPESSURA)
    pygame.draw.line(tela, PRETO, (0, 100), (300, 100), LINHA_ESPESSURA)
    pygame.draw.line(tela, PRETO, (0, 200), (300, 200), LINHA_ESPESSURA)

def desenhar_simbolos():
    """Desenha os 'X' e 'O' no tabuleiro."""
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] is not None:
                texto_surf = fonte_jogo.render(tabuleiro[linha][coluna], True, AZUL)
                texto_rect = texto_surf.get_rect(center=(coluna * 100 + 50, linha * 100 + 50))
                tela.blit(texto_surf, texto_rect)

def desenhar_mensagem_final(mensagem):
    """Desenha a mensagem de vitória ou empate na tela."""
    texto_surf = fonte_mensagem.render(mensagem, True, VERMELHO)
    texto_rect = texto_surf.get_rect(center=(LARGURA / 2, ALTURA / 2))
    # Adiciona um fundo semi-transparente para destacar a mensagem
    fundo = pygame.Surface((LARGURA, 80), pygame.SRCALPHA)
    fundo.fill((255, 255, 255, 180))
    tela.blit(fundo, (0, ALTURA / 2 - 40))
    tela.blit(texto_surf, texto_rect)

# --- Lógica do Jogo ---
def checar_vencedor():
    """Verifica se há um vencedor ou se o jogo empatou."""
    # Checa linhas
    for linha in tabuleiro:
        if linha[0] == linha[1] == linha[2] and linha[0] is not None:
            return linha[0]
    # Checa colunas
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] and tabuleiro[0][col] is not None:
            return tabuleiro[0][col]
    # Checa diagonais
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None:
        return tabuleiro[0][0]
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None:
        return tabuleiro[0][2]
    # Checa empate
    if all(all(cell is not None for cell in row) for row in tabuleiro):
        return "Empate"
    return None

def reiniciar_jogo():
    """Reseta o estado do jogo para uma nova partida."""
    global tabuleiro, jogador_atual, game_over, mensagem_final
    tabuleiro = [[None]*3 for _ in range(3)]
    jogador_atual = "X"
    game_over = False
    mensagem_final = ""

# --- Loop Principal do Jogo ---
def main():
    global jogador_atual, game_over, mensagem_final

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                linha = y // 100
                coluna = x // 100

                if tabuleiro[linha][coluna] is None:
                    tabuleiro[linha][coluna] = jogador_atual
                    vencedor = checar_vencedor()
                    if vencedor:
                        game_over = True
                        if vencedor == "Empate":
                            mensagem_final = "Deu velha! Pressione R."
                        else:
                            mensagem_final = f"Jogador '{vencedor}' venceu! Pressione R."
                    else:
                        jogador_atual = "O" if jogador_atual == "X" else "X"

            # Evento de tecla pressionada para reiniciar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reiniciar_jogo()

        # --- Desenho na Tela ---
        tela.fill(BRANCO)
        desenhar_grade()
        desenhar_simbolos()

        if game_over:
            desenhar_mensagem_final(mensagem_final)

        pygame.display.update()

if __name__ == "__main__":
    main()