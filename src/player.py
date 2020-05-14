import copy
import logging

#logging.basicConfig(level=logging.DEBUG)

'''
REQUIRES: game object, settings object, and player int type
ENSURES: a minnie player who plays with alpha beta pruning
'''
class Player:
    def __init__(self, game, depth, player):
        self.game = game
        self.depth = depth
        self.player = player

    def next_move(self):
        moves = []
        game = copy.deepcopy(self.game)
        val = self.search(game, self.depth, moves, -100000, 100000)
        moves = sorted(moves, key=lambda x:x[1])        #possible chance
        logging.debug(moves)
        logging.debug("best move: " + str(moves[-1]))
        logging.debug("best value: " + str(val))
        return moves[0][0]

    #minimax with alpha beta pruning
    def search(self, game, depth, moveTierList, alpha, beta):

        if depth == 0:
            return game.estimate()

        if game.isOver():
            if game.isMyTurn():
#                logging.debug("the best for maxie is: " + str(m) + " with value 100000 at depth: " + str(depth))
                return -100000
#            logging.debug("the best for minnie is: " + str(m) + " with value -100000 at depth: " + str(depth))
            return 100000

        moves = game.moves()
        bMove = 0
        bVal = alpha if game.isMyTurn() else beta

#        logging.debug("player is: " + str(player))
#        logging.debug(str(len(moves)) + " many moves at depth: " + str(depth))

        for m in moves:

            if depth == self.depth:
                logging.debug("---> move that minnie might take is " + str(m))

            game.move(m)
            val = self.search(game, depth - 1, moveTierList, alpha, beta)
            game.undo(m)

            if game.isMyTurn():
                if val > bVal:
                    alpha, bVal = val, val
                    bMove = m
            else:
                if val < bVal:
                    beta, bVal = val, val
                    bMove = m

            if beta <= alpha:
                break

        if depth == self.depth:
            moveTierList.append((bMove, bVal))

        strs = ""
        if game.isCpuTurn():
            strs = "minnie"
        else:
            strs = "maxie"
        logging.debug("the best for " + strs + " is: " + str(bMove) + " with value " + str(bVal) + " at depth: " + str(depth))

        return bVal












