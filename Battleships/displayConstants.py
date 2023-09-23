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
                            [0, 0, Surface.get_width(), Surface.get_height()], 2)

#get rect for a layer on a surface
def GetRect(Location, Surface):
    return pygame.Rect(GetPercentageCoordinates(Location), (Surface.get_width(), Surface.get_height()))

#function to change background colour and place background
def ChangeBackgroundColour(Layer, Colour):
    Layer.fill(Colour)
    DrawBorder(Layer)

BoardLayer = LayerSurface((0.68, 0.72))           #--> House the grid
LogLayer = LayerSurface((0.2, 0.3))            #--> Output the commands run and other events
Button1Layer = LayerSurface((0.095, 0.16))      #--> The top right button
Button2Layer = LayerSurface((0.095, 0.16))      #--> The button just underneath button1
CommandLineLayer = LayerSurface((0.68, 0.095))    #--> Input commands for the game such as those to do with AI
Button3Layer = LayerSurface((0.2, 0.095))        #--> General name but will be the enter button for the commandline
BattleshipLayer = LayerSurface((0.2, 0.20))      #--> Store the data of the currently active ships

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


#Place all the Layers onto one layer
InputOutputFeatureLayer = LayerSurface((1, 1))

#Used in other classes for detection of button hovering and press
BoardLayerCoordinates = (0.05, 0.05)
LogLayerCoordinates = (0.75, 0.05)
Button1LayerCoordinates = (0.75, 0.381)
Button2LayerCoordinates = (0.856, 0.381)
CommandLineLayerCoordinates = (0.05, 0.8)
Button3LayerCoordinates = (0.75, 0.8)
BattleshipLayerCoordinates = (0.75, 0.567)

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
