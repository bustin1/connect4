import pygame
import numpy as np
from game import Game
from player import Player

SCREEN_W = 700
SCREEN_H = 700
CELL_W = SCREEN_W // 7
CELL_H = SCREEN_W // 7
r = 40




def main():

    surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("CONNECT FOUR")

    game = Game()

#    maxie = Player(game, 5, 1)#depth of 3, player 1
    minnie = Player(game, 5, 2)#depth of 3, player 2

    #random color
    color = np.random.randint(2)
    myColor = 0x000000 if color == 0 else 0xFF0000
    cpuColor = 0xFF0000 if color == 0 else 0x000000

    over = False

    while True:

        surface.fill(0xFFFF00)
        pygame.draw.rect(surface, 0xFFFFFF, (0, 0, SCREEN_W, CELL_H))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP and game.isMyTurn() and not over:
                col = (x // CELL_W)
                game.move(col)

# if ur playing with maxie, uncomment below:

#        if game.isMyTurn():
#            bestMove = maxie.next_move()
#            print("Maxie moves: " + str(bestMove))
#            game.move(bestMove)


        #draw already placed pieces
        for i in range(game.board.w):
            for j in range(game.board.h):
                c = ((i * CELL_W) + 50, ((j+1) * CELL_H) + 50)
                if game.board.amIAt(j, i):
                    pygame.draw.circle(surface, myColor, c, r)
                elif game.board.isCpuAt(j, i):
                    pygame.draw.circle(surface, cpuColor, c, r)
                else:
                    pygame.draw.circle(surface, 0xFFFFFF, c, r)

        #draw current piece
        (x, y) = pygame.mouse.get_pos()
        if game.isMyTurn():
            pygame.draw.circle(surface, myColor, (x,y), r)
#        if game.isCpuTurn():
#            pygame.draw.circle(surface, cpuColor, (x,y), r)

        if game.isOver():
            over = True
            print("-------------------> someone won")

        pygame.display.update()

        if game.isCpuTurn() and not over:
            bestMove = minnie.next_move()
            print("Minnie moves: " + str(bestMove))
            game.move(bestMove)


        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main()





