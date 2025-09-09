import pygame
import sys

pygame.init()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)

largura = 300
altura = 300
linha_espessura = 15

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Velha')

tabuleiro = [[None]*3 for _ in range(3)]
jogador_atual = "X"
fonte = pygame.font.SysFont(None, 100)
game_over = False

def desenhar_linhas():
    pygame.draw.line(tela, PRETO, (100, 0), (100, 300), linha_espessura)
    pygame.draw.line(tela, PRETO, (200, 0), (200, 300), linha_espessura)
    pygame.draw.line(tela, PRETO, (0, 100), (300, 100), linha_espessura)
    pygame.draw.line(tela, PRETO, (0, 200), (300, 200), linha_espessura)

def desenhar_simbolos():
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] is not None:
                textp = fonte.render(tabuleiro[linha][coluna], True, AZUL)
                tela.blit(textp, (coluna * 100 + 25, linha * 100 + 10))
                
def checar_vencedor():
    for linha in tabuleiro:
        if linha.count(linha[0]) == 3 and linha[0] is not None :
            return linha[0]
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] and tabuleiro[0][col] is not None:
            return tabuleiro[0][col]
        if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] and tabuleiro[0][0] is not None:
            return tabuleiro[0][0]
        if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] and tabuleiro[0][2] is not None:
            return tabuleiro[0][2]
    return None

while True:
    tela.fill(BRANCO)
    desenhar_linhas()
    desenhar_simbolos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            linha = y // 100
            coluna = x // 100
            
            if tabuleiro[linha][coluna] is None:
                tabuleiro[linha][coluna] = jogador_atual
                vencedor = checar_vencedor()
                if vencedor:
                    print(f'Jogador {vencedor} venceu!')
                    game_over = True
                    
                elif all(all(cell is not None for cell in row) for row in tabuleiro):
                    print('Empate!')
                    game_over = True
                jogador_atual = "O" if jogador_atual == "X" else "X"
                
            pygame.display.update()