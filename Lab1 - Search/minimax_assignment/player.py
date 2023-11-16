#!/usr/bin/env python3
import random, math, time
from collections import defaultdict

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

        # #############################
        # HYPERPARAMETERS        
        self.depth = 4
        # #############################

        self.start = time.time()

        children = initial_tree_node.compute_and_get_children()
        best_move = 0
        best_score = float('-inf')

        self.visited = defaultdict(self.default_value)

        try:
            childrenSorted = sorted(children, key=lambda child: self.heuristic(child), reverse=True)
        except:
            childrenSorted = children

        loop = True
        while loop:
            try:
                for child in childrenSorted:
                    score = self.alphabeta(child, float('-inf'), float('inf'))        
                    if score > best_score:
                        best_score = score
                        best_move = childrenSorted.index(child)
                # self.depth += 1
                break
                print(self.depth)
            except TimeoutError as e:
                print("hej", e)
                loop = False
            except Exception as e:
                print("hej2", e)
                loop = False


        return childrenSorted[best_move]

        
    def alphabeta(self, node, alpha, beta):

        current = time.time()
        diff = current - self.start
        if diff > 0.055:
            raise TimeoutError

        """
        if self.visited[self.hashState(node.state)] != None:
            return self.visited[self.hashState(node.state)]
        """

        heuristic = self.heuristic(node)
        # self.visited[self.hashState(node.state)] = heuristic

        children = node.compute_and_get_children()
        
        if children == [] or node.depth == self.depth:
            return heuristic

        if node.state.get_player() == 0:
            children = sorted(children, key=lambda child: self.heuristic(child), reverse=True)
        else:
            children = sorted(children, key=lambda child: self.heuristic(child))
        

        if node.state.get_player() == 0:
            v = float('-inf')
            for child in children:
                ab = self.alphabeta(child, alpha, beta)
                v = max(v, ab)
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
                 
        else:
            v = float('inf')
            for child in children:
                ab = self.alphabeta(child, alpha, beta)
                v = min(v, ab)
                beta = min(beta, v)
                if alpha >= beta:
                    break

        return v
    
    def hashState(self, state):
        hash = ""
        hash += str(state.hook_positions[0][0])
        hash += str(state.hook_positions[0][1])
        hash += str(state.hook_positions[1][0])
        hash += str(state.hook_positions[1][1])
        hash += str(state.player_scores[0])
        hash += str(state.player_scores[1])
        for fish in state.fish_positions:
            hash += str(state.fish_positions[fish][0])
            hash += str(state.fish_positions[fish][1])
            hash += str(state.fish_scores[fish])
        return hash

    def heuristic(self, node):
        score = (node.state.player_scores[0] - node.state.player_scores[1]) * 2

        fish_pos = node.state.fish_positions
        hook_pos = node.state.hook_positions[0]
        fish_scores = node.state.fish_scores

        heuristic_score = 0
        for i in fish_pos:
            # Manhattan distance
            delta_x = abs(fish_pos[i][0] - hook_pos[0])
            delta_x = min(delta_x, 20 - delta_x)
            delta_y = abs(fish_pos[i][1] - hook_pos[1])
            dist = delta_x + delta_y

            if dist == 0 and fish_scores[i] > 0:
                return float('inf') # If we can catch a fish, we should do it
            elif dist == 0 and fish_scores[i] <= 0:
                return float('-inf')
            heuristic_score = max(heuristic_score, fish_scores[i] / dist) 

        return score + heuristic_score

    def default_value(self):
        return None