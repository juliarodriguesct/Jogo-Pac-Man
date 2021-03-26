import pygame
from pygame.locals import *
import random
import time
import math

############### CORES ###############

# Pacman
PACMAN = (255, 255, 0)
RASTRO = (255, 255, 0)
PACMAN_PILULA_FORCA = (218, 165, 32)
RASTRO_PILULA_FORCA = (218, 165, 32) 

# Fantasmas
CLYDE = (255, 127, 000)
BLINK   = (255, 0, 0)
PINK = (255, 062, 150)
INKY  = (000, 191, 255)
FASTASMA_PILULA_FORCA = (0, 255, 0)

# Cenario
PILULA = (107, 142, 035)
PILULA_FORCA = (240,230,140)
PAREDE = (067, 170, 067)
TELA_AUX = (0, 0, 0)

class Mapa():
    def __init__ (self, X, Y):
        self.limite_horizontal = X
        self.limite_vertical = Y

    def criaObj(self, cenario):
        
        pacman = []
        fantasmas = []
        paredes = []
        pilulas = []
        pilulasDeForca = [] 
        k = 1
        
        for i in range(0, 12):

            for j in range(0, 12):
                if(cenario[j][i] == 0):
                    pilulas.append((64 * i, 32 * j))

                if(cenario[j][i] == 1):
                    paredes.append((64 * i, 32 * j))

                if(cenario[j][i] == 2):
                    pacman.append((64 * i, 32 * j, 0, 0))

                if(cenario[j][i] == 3 or cenario[j][i] == 4 or cenario[j][i] == 5 or cenario[j][i] == 6):
                    fantasmas.append((64 * i, 32 * j, k, 0))
                    k += 1

                if(cenario[j][i] == 10):
                    pilulasDeForca.append((64 * i, 32 * j))
        
        return (pacman, pilulas, pilulasDeForca, paredes, fantasmas)

    def renderizaObj(self, pacman, pilulas, pilulasDeForca, paredes, fantasmas, rastro, tela):
        
        for i in range(0, len(pilulas)):
            (xP, yP) = pilulas[i]
            pygame.draw.circle(tela, PILULA, (xP + 32, yP + 16), 5, 0)
        
        for i in range(0, len(pilulasDeForca)):
            (xP, yP) = pilulasDeForca[i]
            pygame.draw.circle(tela, PILULA_FORCA, (xP + 32, yP + 16), 10, 0)
                
        (xPM, yPM, est, _) = pacman[0]
       
        for i in range(0, len(rastro)):
            (xRs, yRs, _) = rastro[i]
            if(est == 0):
                pygame.draw.rect(tela, RASTRO, (xRs + 23, yRs + 11, 10, 10), 0)
            else:
                pygame.draw.rect(tela, RASTRO_PILULA_FORCA, (xRs + 23, yRs + 11, 10, 10), 0)
        if(est == 0):
            pygame.draw.circle(tela, PACMAN, (xPM + 32, yPM + 16), 10, 0)
        else:
            pygame.draw.circle(tela, PACMAN_PILULA_FORCA, (xPM + 32, yPM + 16), 10, 0)
        
        for i in range(0, len(fantasmas)):
            (xF, yF, nF, estF) = fantasmas[i]
            if(nF == 1 and est == 0):
                pygame.draw.circle(tela, CLYDE,(xF + 32, yF + 16), 10, 0)
            elif(nF == 2 and est == 0):
                pygame.draw.circle(tela, BLINK,(xF + 32, yF + 16), 10, 0)
            elif(nF == 3 and est == 0):
                pygame.draw.circle(tela, PINK,(xF + 32, yF + 16), 10, 0)
            elif(nF == 4 and est == 0):
                 pygame.draw.circle(tela, INKY,(xF + 32, yF + 16), 10, 0)
            else:
                pygame.draw.circle(tela, FASTASMA_PILULA_FORCA,(xF + 32, yF + 16), 10, 0)
        
        for i in range(0, len(paredes)):
            (xP, yP) = paredes[i]
            pygame.draw.rect(tela, PAREDE, (xP, yP, 64, 32), 0)
            
        pygame.draw.line(tela, PAREDE, (0, 384), (768, 384), 3)
        pygame.display.update()            

    def movimentaFantasmas(self, fantasma, pacman, rastro, mX, mY, paredes):
        i = 0
        movInv = 0
        (xP, yP, estP, _) = pacman[0]
        while(i < len(fantasma)):            
            (xF, yF, nF, est) = fantasma[i]
            dist = distanciaManhattan(xP, xF, yP, yF)

            if(dist >= 100): # mudanca aqui
               
                for j in range(0, len(rastro)):
                    (xR, yR, _) = rastro[j]
                    distR = distanciaManhattan(xR, xF, yR, yF)
                    if(distR < dist and not(xF == xR and yF == yF)):
                        dist = distR
                        xP = xR
                        yP = yR
                
            if(dist < 180 and estP == 0): 
                dist = 1000
                l = xF - mX
                r = xF + mX
                u = yF - mY
                d = yF + mY
                move = distanciaManhattan(xP, l, yP, yF)
                if(move < dist and self.movimentosPossiveis((l, yF), paredes) == 1):
                    dist = move
                    fX = l
                    fY = yF
                move = distanciaManhattan(xP, r, yP, yF) 
                if(move < dist and self.movimentosPossiveis((r, yF), paredes) == 1):
                    dist = move
                    fX = r
                    fY = yF
                move = distanciaManhattan(xP, xF, yP, d)
                if(move < dist and self.movimentosPossiveis((xF, d), paredes) == 1):
                    dist = move
                    fX = xF
                    fY = d
                move = distanciaManhattan(xP, xF, yP, u)
                if(move < dist and self.movimentosPossiveis((xF, u), paredes) == 1):
                    dist = move
                    fX = xF
                    fY = u
                fantasma[i] = (fX, fY, nF, est)
                i += 1
            elif(dist < 180 and estP == 1): 
                dist = 0
                l = xF - mX
                r = xF + mX
                u = yF - mY
                d = yF + mY
                move = distanciaManhattan(xP, l, yP, yF)
                if(move > dist and self.movimentosPossiveis((l, yF), paredes) == 1):
                    dist = move
                    fX = l
                    fY = yF
                move = distanciaManhattan(xP, r, yP, yF) 
                if(move > dist and self.movimentosPossiveis((r, yF), paredes) == 1):
                    dist = move
                    fX = r
                    fY = yF
                move = distanciaManhattan(xP, xF, yP, d)
                if(move > dist and self.movimentosPossiveis((xF, d), paredes) == 1):
                    dist = move
                    fX = xF
                    fY = d
                move = distanciaManhattan(xP, xF, yP, u)
                if(move > dist and self.movimentosPossiveis((xF, u), paredes) == 1):
                    dist = move
                    fX = xF
                    fY = u
                fantasma[i] = (fX, fY, nF, est)
                i += 1
            else:
                direction = random.randint(0,3)
                if(direction == 0):
                    xF -= mX
                elif(direction == 1):
                    xF += mX
                elif(direction == 2):
                    yF -= mY
                elif(direction == 3):
                    yF += mY
                if(self.movimentosPossiveis((xF, yF), paredes) == 1):
                    fantasma[i] = (xF, yF, nF, est)
                    i += 1
        
    def verificaColisao(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        if(x1 == x2 and y1 == y2):
            return 1 
        else:
            return 0 

    def movimentosPossiveis(self, mov, paredes):
        for i in range(0, len(paredes)):
            if(self.verificaColisao(mov,  paredes[i])):
               return 0
        (movX, movY) = mov
        if(movX < 0 or movX >= self.limite_horizontal or movY < 0 or movY >= self.limite_vertical):
            return 0
        return 1

    def contaPontoPilulas(self, pacman, pilulas, pilulasDeForca, score):
        (xP, yP, _, _) = pacman[0]
        for i in range(0, len(pilulas)):
            if(self.verificaColisao((xP, yP), pilulas[i])):
                score += 10
                (posX, posY) = pilulas[i]
                pilulas.remove((posX, posY))
                break
        for i in range(0, len(pilulasDeForca)):
            if(self.verificaColisao((xP, yP), pilulasDeForca[i])):
                score += 50
                (posX, posY) = pilulasDeForca[i]
                pilulasDeForca.remove((posX, posY))
                pacman[0] = (xP, yP, 1, 8)
                break
        return score

                    
    def comePacman(self, pacman, fantasmas, vidas):
        (xP, yP, est, _) = pacman[0]
        reset = 0
        for i in range(0, len(fantasmas)):
            (xF, yF, _, _) = fantasmas[i]
            if(self.verificaColisao((xP, yP), (xF, yF)) == 1 and est == 0):
                vidas -= 1
                reset = 1
                return (vidas, reset)
        return (vidas, reset)

    def comeFantasma(self, pacman, fantasmas, score, quantidade):
        (xP, yP, est, tempo) = pacman[0]
        if(quantidade > 4):
            quantidade = 1
        elif(tempo == 0):
            quantidade = 1
        reset = 0
        for i in range(0, len(fantasmas)):
            (xF, yF, nF, _) = fantasmas[i]
            if(self.verificaColisao((xP, yP), (xF, yF)) == 1 and est == 1):
                aux = 200 * quantidade
                score += aux
                quantidade += 1
                if(nF == 1):
                    fantasmas[0] = (320, 160, 1, 0)
                elif(nF == 2):
                    fantasmas[1] = (384, 160, 2, 0)
                elif(nF == 3):
                    fantasmas[2] = (320, 192, 3, 0)
                elif(nF == 4):
                    fantasmas[3] = (384, 192, 4, 0)
                return (score, quantidade, fantasmas)
        return (score, quantidade, fantasmas)                
    

    def fimDeJogo(self, vidas, pilulas, pilulasDeForca):
        
        if (len(pilulas) == 0 and len(pilulasDeForca) == 0):
            print("\nUHUL! O Pacman comeu todas as pilulas. Voce venceu! :D \n")
            fim = 1
        
        elif(vidas <= 0):
            print("\nPOXA! O Pacman foi derrotado pelos fantasmas. Voce perdeu! :( \n")
            fim = 1

        else:
            fim = 0
        
        return fim

    
def distanciaManhattan(x1, x2, y1, y2):
    resultado = math.fabs(x1 - x2) + math.fabs(y1 - y2)
    return resultado
    
def iniciaJogo():
    pygame.init() 
    pygame.mixer.init() 
    pygame.font.init()   
    telaTamX = 768 
    telaTamY = 450 
    tela = pygame.display.set_mode((telaTamX, telaTamY), 0, 32) 
    pygame.display.set_caption('PACMAN PERDIDO NO BOSQUE') 
    pygame.mixer.music.load('musica.ogg') #
    clock = pygame.time.Clock() 

    background_filename = 'fundo.png'
    background = pygame.image.load(background_filename).convert()
    
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.5)
   
    framerate = 5
    move_horizontal = 64
    move_vertical = 32
    quantidade = 1
    

    cenario = [[10,0,0,0,0,0,0,0,0,0,0,10], # 0 = pilulas
              [0,1,0,1,1,0,0,1,1,0,1,0], # 1 = parede
              [0,1,0,0,0,0,0,0,0,0,1,0], # 2 = pacman
              [0,1,1,1,0,1,1,0,1,1,1,0], # 3 a 6 = fantasmas
              [0,0,0,0,0,0,0,0,0,0,0,0], # 10 = pilula forca
              [0,1,0,1,0,3,4,0,1,0,1,0],
              [1,0,0,0,1,5,6,1,0,0,0,1],
              [0,1,1,0,1,1,1,1,0,1,1,0],
              [0,0,1,0,0,0,0,0,0,1,0,0],
              [0,0,0,1,0,0,0,0,1,0,0,0],
              [0,1,0,0,0,1,1,0,0,0,1,0],
              [10,0,0,0,0,2,0,0,0,0,0,10]]
    
    mapa = Mapa(telaTamX, 384)
    pontuacao = 0
    vida = 3
    reset = 0
    teclado = []

    (pacman, pilulas, pilulasDeForca, paredes, fantasmas) = mapa.criaObj(cenario)
    
    rastro = []
    comprimento_rastro = 3 
    
    while True: 

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.mixer.music.stop()
                exit()
   
        teclado = pygame.key.get_pressed()
        if teclado[K_RIGHT]:

            (xPM, yPM, est, tempo) = pacman[0]
            xPM += move_horizontal
            if(mapa.movimentosPossiveis((xPM, yPM), paredes)):
                pacman = []
                pacman.append((xPM, yPM, est, tempo))
                rastro.append((xPM, yPM, comprimento_rastro))

        elif teclado[K_LEFT]:

            (xPM, yPM, est, tempo) = pacman[0]
            xPM -= move_horizontal
            if(mapa.movimentosPossiveis((xPM, yPM), paredes)):
                pacman = []
                pacman.append((xPM, yPM, est, tempo))
                rastro.append((xPM, yPM, comprimento_rastro))

        elif teclado[K_UP]:
            
            (xPM, yPM, est, tempo) = pacman[0]
            yPM -= move_vertical
            if(mapa.movimentosPossiveis((xPM, yPM), paredes)):
                pacman = []
                pacman.append((xPM, yPM, est, tempo))
                rastro.append((xPM, yPM, comprimento_rastro))
        
        elif teclado[K_DOWN]:
            
            (xPM, yPM, est, tempo) = pacman[0]
            yPM += move_vertical
            if(mapa.movimentosPossiveis((xPM, yPM), paredes)):
                pacman = []
                pacman.append((xPM, yPM, est, tempo))
                rastro.append((xPM, yPM, comprimento_rastro))


        (xPM, yPM, est, tempo) = pacman[0]
        if(tempo > 0):
            tempo -= 1
        else:
            est = 0

        pacman = []
        pacman.append((xPM, yPM, est, tempo))

        (vida, reset) = mapa.comePacman(pacman, fantasmas, vida)
        (pontuacao, quantidade, fantasmas) = mapa.comeFantasma(pacman, fantasmas, pontuacao, quantidade)

        if(reset == 1):
            pacman[0] = (384, 352, 0, 0)
            fantasmas[0] = (320, 160, 1, 0)
            fantasmas[1] = (384, 160, 2, 0)
            fantasmas[2] = (320, 192, 3, 0)
            fantasmas[3] = (384, 192, 4, 0)
            reset = 0
            
        pontuacao = mapa.contaPontoPilulas(pacman, pilulas, pilulasDeForca, pontuacao) #calcula pontuacao

        (_, _, est, _) = pacman[0]
        
        if(est == 1):
            contador += 1
        else:
            contador = 0
            
        if((contador % 2) == 0):
            mapa.movimentaFantasmas(fantasmas, pacman, rastro, move_horizontal, move_vertical, paredes)

        
        (vida, reset) = mapa.comePacman(pacman, fantasmas, vida)
        (pontuacao, quantidade, fantasmas) = mapa.comeFantasma(pacman, fantasmas, pontuacao, quantidade)
        
        
        if(reset == 1):
            pacman[0] = (384, 352, 0, 0)
            fantasmas[0] = (320, 160, 1, 0)
            fantasmas[1] = (384, 160, 2, 0)
            fantasmas[2] = (320, 192, 3, 0)
            fantasmas[3] = (384, 192, 4, 0)
            reset = 0

        tela.blit(background, (0, 0))
        mapa.renderizaObj(pacman, pilulas, pilulasDeForca, paredes, fantasmas, rastro, tela)
        
 
        fontScore = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontScore.render("SCORE:", False, (255, 255, 0))
        tela.blit(textsurface,(5,385))
        pygame.draw.rect(tela, TELA_AUX, (90, 390, 80, 50), 0)
        fontScore = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontScore.render(str(pontuacao), False, (255, 0, 0))
        tela.blit(textsurface,(90,385))
       
        fontVidas = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontVidas.render("LIFE:", False, (255, 255, 0))
        tela.blit(textsurface,(5,415))
        pygame.draw.rect(tela, TELA_AUX, (65, 420, 80, 50), 0)
        fontVidas = pygame.font.SysFont("ARIAL BLACK", 20)
        textsurface = fontVidas.render(str(vida), False, (255, 0, 0))
        tela.blit(textsurface,(65,415))
        
        pygame.display.update() 
        fim = mapa.fimDeJogo(vida, pilulas, pilulasDeForca)
        
        novoRastro = []
        for i in range(0, len(rastro)):
            (xR, yR, T) = rastro[i]
            
            if T > 0:
                T -= 1
                novoRastro.append((xR, yR, T))
        
        rastro = novoRastro 

        if(fim == 1):
            print("A sua pontuacao foi: ")
            print(pontuacao)
            pygame.display.quit()
            pygame.mixer.music.stop()
            exit()
        
    
        time_passed = clock.tick(framerate) 


if __name__ == "__main__":
    iniciaJogo()
