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
        self.depth = 7
        # #############################

        self.start = time.time()

        children = initial_tree_node.compute_and_get_children()
        best_move = 0
        best_score = float('-inf')

        try:
            childrenSorted = sorted(children, key=lambda child: self.heuristic(child), reverse=True)
        except:
            childrenSorted = children

        loop = True
        depth = 7
        visited = defaultdict(lambda: None)
        
        while loop:
            visited.clear()
            best_score = float('-inf')
            try:
                for child in childrenSorted:        
                    score = self.alphabeta(child, float('-inf'), float('inf'), depth, visited)
                    if score > best_score:
                        best_score = score
                        best_move = child.move
                depth += 1
            except TimeoutError as e:
                loop = False
                return ACTION_TO_STR[best_move]

        return ACTION_TO_STR[best_move]

        
    def alphabeta(self, node, alpha, beta, depth, visited):

        if time.time() - self.start > 0.06:
            raise TimeoutError("Time limit exceeded")
        
        if visited[self.hashNode(node)] != None:
            return visited[self.hashNode(node)]        

        children = node.children

        if children == []:
            children = node.compute_and_get_children()
        

        if children == [] or node.depth == depth:
            return self.heuristic(node)

        if node.state.get_player() == 0:
            children = sorted(children, key=lambda child: self.heuristic(child), reverse=True)
        else:
            children = sorted(children, key=lambda child: self.heuristic(child))
        

        if node.state.get_player() == 0:
            v = float('-inf')
            for child in children:
                ab = self.alphabeta(child, alpha, beta, depth, visited)
                v = max(v, ab)
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
                 
        else:
            v = float('inf')
            for child in children:
                ab = self.alphabeta(child, alpha, beta, depth, visited)
                v = min(v, ab)
                beta = min(beta, v)
                if alpha >= beta:
                    break

        visited[self.hashNode(node)] = v
        return v

    def hashNode(self, node):
        hash = ""
        for i in node.state.fish_positions:
            hash += str(node.state.fish_positions[i])
        for i in node.state.hook_positions:
            hash += str(node.state.hook_positions[i])
        for i in node.state.player_scores:
            hash += str(node.state.player_scores[i])
        
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
