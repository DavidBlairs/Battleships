import ctypes
import numpy
import pygame

while True:
    rand_5 = 5 * numpy.random.random_sample((10, 10, 10, 10)) - 1
    print(rand_5)
from Display import *

class BattleshipStore:
    def __init__(self, ShipIndex, ShipList):
        self.Layer = pygame.Surface((BattleshipLayer.get_width()/len(ShipList), BattleshipLayer.get_height()))

class UserInterfaceTemplate:
    def __init__(self):
        self.InputOutputFeatureLayer = InputOutputFeatureLayer
        self.ButtonLayerRect = [Button1LayerRect, Button2LayerRect, Button3LayerRect]
        self.ButtonLayers = [Button1Layer, Button2Layer,  Button3Layer]
        self.ButtonFunctions = [self.Button1Pressed, self.Button2Pressed, self.Button3Pressed]

        pygame.init()
        self.ScreenDimensions = (ctypes.windll.user32.GetSystemMetrics(0),
                                ctypes.windll.user32.GetSystemMetrics(1))
        self.Screen = pygame.display.set_mode(self.ScreenDimensions, pygame.FULLSCREEN)

        self.Clock = pygame.time.Clock()

    def Update(self):
        for Event in pygame.event.get():
            self.KeyboardEvent(Event)

        for Button in self.ButtonLayerRect:
            if Button.collidepoint(pygame.mouse.get_pos()):
                self.ButtonFunctions[self.ButtonLayerRect.index(Button)](
                    {1: True, 0: False}[pygame.mouse.get_pressed()[0]])
            else: self.ButtonFunctions[self.ButtonLayerRect.index(Button)](False)
        UpdateIOFeatures()
        self.Screen.blit(self.InputOutputFeatureLayer, (0, 0))

        pygame.display.flip()

        self.Clock.tick(60)


    def KeyboardEvent(self, Event):
        pass

    def Button1Pressed(self, Pressed):
        pass

    def Button2Pressed(self, Pressed):
        pass

    def Button3Pressed(self, Pressed):
        pass
