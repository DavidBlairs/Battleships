#import the necessary modules
import pygame, ctypes


#Function to create layer relative to screen size
def LayerSurface(Dimensions):
    Size = int(Dimensions[0]*ctypes.windll.user32.GetSystemMetrics(0)),\
           int(Dimensions[1]*ctypes.windll.user32.GetSystemMetrics(1)) #Decimal percentage of screen size
    return pygame.Surface(Size) #---> surface with relative sizes

#get the percentage coordinates of a destination
def GetPercentageCoordinates(Destination):
    return (int(Destination[0]*ctypes.windll.user32.GetSystemMetrics(0)),
            int(Destination[1]*ctypes.windll.user32.GetSystemMetrics(1)))

#draw the border with width 2 on surface
def DrawBorder(Surface):
    return pygame.draw.rect(Surface, BorderColour,
                            [0, 0, Surface.get_width(), Surface.get_height()], 3)

#get rect for a layer on a surface
def GetRect(Location, Surface):
    return pygame.Rect(GetPercentageCoordinates(Location), (Surface.get_width(), Surface.get_height()))

#function to change background colour and place background
def ChangeBackgroundColour(Layer, Colour):
    Layer.fill(Colour)
    DrawBorder(Layer)

BoardLayer = LayerSurface((0.4, 0.4))           #--> House the grid
LogLayer = LayerSurface((0.28, 0.4))            #--> Output the commands run and other events
Button1Layer = LayerSurface((0.12, 0.175))      #--> The top right button
Button2Layer = LayerSurface((0.12, 0.175))      #--> The button just underneath button1
CommandLineLayer = LayerSurface((0.73, 0.1))    #--> Input commands for the game such as those to do with AI
Button3Layer = LayerSurface((0.12, 0.1))        #--> General name but will be the enter button for the commandline
BattleshipLayer = LayerSurface((0.4, 0.3))      #--> Store the data of the currently active ships
AILayer = LayerSurface((0.45, 0.3))             #--> Where the conditions are changed for the AI

#The colour for all the borders --> Blue: 000,000,255
BorderColour = (0, 0, 255)

#Draw blue border around all declared layers
DrawBorder(BoardLayer)
DrawBorder(LogLayer)
DrawBorder(Button1Layer)
DrawBorder(Button2Layer)
DrawBorder(CommandLineLayer)
DrawBorder(Button3Layer)
DrawBorder(BattleshipLayer)
DrawBorder(AILayer)

#Place all the Layers onto one layer
InputOutputFeatureLayer = LayerSurface((1, 1))

#Used in other classes for detection of button hovering and press
BoardLayerCoordinates = (0.05, 0.05)
LogLayerCoordinates = (0.5, 0.05)
Button1LayerCoordinates = (0.83, 0.05)
Button2LayerCoordinates = (0.83, 0.275)
CommandLineLayerCoordinates = (0.05, 0.5)
Button3LayerCoordinates = (0.83, 0.5)
BattleshipLayerCoordinates = (0.05, 0.65)
AILayerCoordinates = (0.5, 0.65)

#place all the aspects on one layer
def UpdateIOFeatures():
    InputOutputFeatureLayer.fill((0, 0, 0))
    InputOutputFeatureLayer.blit(BoardLayer, GetPercentageCoordinates(BoardLayerCoordinates))                   #--> House the grid
    InputOutputFeatureLayer.blit(LogLayer, GetPercentageCoordinates(LogLayerCoordinates))                       #--> Output the commands run and other events
    InputOutputFeatureLayer.blit(Button1Layer, GetPercentageCoordinates(Button1LayerCoordinates))               #--> The top right button
    InputOutputFeatureLayer.blit(Button2Layer, GetPercentageCoordinates(Button2LayerCoordinates))               #--> The button just underneath button1
    InputOutputFeatureLayer.blit(CommandLineLayer, GetPercentageCoordinates(CommandLineLayerCoordinates))       #--> Input commands for the game such as those to do with AI
    InputOutputFeatureLayer.blit(Button3Layer, GetPercentageCoordinates(Button3LayerCoordinates))               #--> General name but will be the enter button for the commandline
    InputOutputFeatureLayer.blit(BattleshipLayer, GetPercentageCoordinates(BattleshipLayerCoordinates))         #--> Store the data of the currently active ships
    InputOutputFeatureLayer.blit(AILayer, GetPercentageCoordinates(AILayerCoordinates))                         #--> Where the conditions are changed for the AI

#Used as a function for later update.
UpdateIOFeatures()

#establish rectangles for the layers
BoardLayerRect = GetRect(BoardLayerCoordinates, BoardLayer)
LogLayerRect = GetRect(LogLayerCoordinates, LogLayer)
Button1LayerRect = GetRect(Button1LayerCoordinates, Button1Layer)
Button2LayerRect = GetRect(Button2LayerCoordinates, Button2Layer)
CommandLineLayerRect = GetRect(CommandLineLayerCoordinates, CommandLineLayer)
Button3LayerRect = GetRect(Button3LayerCoordinates, Button3Layer)
BattleshipLayerRect = GetRect(BattleshipLayerCoordinates, BattleshipLayer)
AILayerRect = GetRect(AILayerCoordinates, AILayer)
