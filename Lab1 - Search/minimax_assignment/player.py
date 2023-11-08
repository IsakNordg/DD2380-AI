#!/usr/bin/env python3
import random, math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    # Inhertis from PlayerController, SettingLoader, and Communicator classes
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        # HYPERPARAMETER
        depth = 7
        #########

        children = initial_tree_node.compute_and_get_children()
        best_move = None
        best_score = float('-inf')

        for child in children:
            score = self.alphabeta(child, depth, float('-inf'), float('inf'))
            if score > best_score:
                print("updated best score to: ", score)
                best_score = score
                best_move = child.move
            #print(child.move, score)
        print(best_move)
        return ACTION_TO_STR[best_move]

    
    def minmax(self, node):
        children = node.compute_and_get_children()
        
        if children == [] or node.depth == 4: 
            scores = node.state.get_player_scores()
            return self.heuristic(node)
            # Theory: This value could be (1, 0 or -1), since this is a zero-sum game

        if node.state.get_player() == 0:
            bestPossible = float('-inf')
            for child in children:
                v = self.minmax(child)

                if v > bestPossible:
                    bestPossible = v
            return bestPossible
        else:
            bestPossible = float('inf')
            for child in children:
                v = self.minmax(child)

                if v < bestPossible:
                    bestPossible = v
            return bestPossible
        
    def alphabeta(self, node, depth, alpha, beta):
        children = node.compute_and_get_children()
        
        if children == [] or node.depth == depth: #or node.depth==0 in pseudo code
            return self.heuristic(node)
            # Theory: This value could be (1, 0 or -1), since this is a zero-sum game

        if node.state.get_player() == 0:
            v = float('-inf')
            for child in children:
                ab = self.alphabeta(child, depth, alpha, beta)
                v = max( v, ab)
                alpha = max(alpha, v)
                if alpha >= beta:
                    break #β prune - tror kanske denna behöver fixas, minns inte hur break funkar i python
                 
        else:
            v = float('inf')
            for child in children:
                ab = self.alphabeta(child, depth, alpha, beta)
                v = min(v, ab)
                beta = min(beta, v)
                if alpha >= beta:
                    break #α prune - tror kanske denna behöver fixas, minns inte hur break funkar i python

        return v

    def heuristic(self, node):
        """
        Computes a heuristic for a particular node.
        :param node: Given node
        :type node: game_tree.Node
        :return: Heuristic score
        :rtype: float
        """

        total_score = node.state.player_scores[0] - node.state.player_scores[1]

        h = 0
        for i in node.state.fish_positions:
            distance = self.l1_distance(node.state.fish_positions[i], node.state.hook_positions[0])
            if distance == 0 and node.state.fish_scores[i] > 0:
                return float('inf')
            h = max(h, node.state.fish_scores[i] * math.exp(-distance))

        return 2 * total_score + h
        #Ideas to test
        """
        remove 2* ?
        add more fishes than just one?"""

    def l1_distance(self, fish_positions, hook_positions): #Byt denna mot euclidian distance? Fast manhattan borde ju stämma bäst efetrsom vi inte kan gå raka vägen
        """
        Computes the Manhattan distance between the player hook and a given fish
        :param hook_positions: Position of the player's hook
        :type hook_positions: array
        :param fish_positions: Position of a given fish
        :type fish_positions: array
        :return: Manhattan distance
        :rtype: int
        """

        y = abs(fish_positions[1] - hook_positions[1])

        delta_x = abs(fish_positions[0] - hook_positions[0])
        x = min(delta_x, 20 - delta_x)

        return x + y
    


# TODO imorgon:
"""
    Egen heuristic
    Alpha-beta pruning
"""