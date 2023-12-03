#!/usr/bin/env python3

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random


def generate_rand(size = 1):
    prel = [1/size + random.rand/100 for i in range(size)]
    normalized = []
    for i in range(size):
        normalized.append(prel[i]/sum(prel))
    return normalized

class Model():
    def _init_(self, emissions): #Kan vara heeelt fel
        self.A = generate_rand()
        self.B = generate_rand(emissions)
        self.pi = generate_rand

    def update(self):
        """to be written"""
        pass


class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        """
        In this function you should initialize the parameters you will need,
        such as the initialization of models, or fishes, among others.
        """
        self.fish_models = []
        for i in range(N_SPECIES):
            self.fish_models.append(Model(N_EMISSIONS))

        self.fish_list = []
        for i in range(N_FISH):
            self.fish_list.append([])


    def guess(self, step, observations):
        """
        This method gets called on every iteration, providing observations.
        Here the player should process and store this information,
        and optionally make a guess by returning a tuple containing the fish index and the guess.
        :param step: iteration number
        :param observations: a list of N_FISH observations, encoded as integers
        :return: None or a tuple (fish_id, fish_type)
        """
        for i in range(N_FISH):
            self.fish_list.append(observations[i])

        if self.step < 110:
            #self.updateModel()
            return None #As we only want to train the model once we have as many observations as possible
        else:
            self.makeGuess()

        # This code would make a random guess on each step:
        return (step % N_FISH, random.randint(0, N_SPECIES - 1))

    def updateModel(self):
        """
        This method updates the model with the new observations.
        """
        pass

    def makeGuess(self):
        """
        This method makes a guess.
        """
        pass


    def reveal(self, correct, fish_id, true_type):
        """
        This methods gets called whenever a guess was made.
        It informs the player about the guess result
        and reveals the correct type of that fish.
        :param correct: tells if the guess was correct
        :param fish_id: fish's index
        :param true_type: the correct type of the fish
        :return:
        """
        pass
