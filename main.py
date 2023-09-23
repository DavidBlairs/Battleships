import pygame
from Battleships.instance import BattleshipInstance

x = BattleshipInstance((25, 25))
x.RandomPlacement([4, 5, 6, 7,8,9,10,4,5,6,7,8])
x.AIUpdate()
while True:
    x.CheckMouseButtonOverlay()
    x.UpdateDisplayShipsBoard()
    x.CommandLineInputUpdate()
    pygame.event.get()
    x.UpdateShipDisplay()
    x.RefreshDisplay()
    x.UpdateDisplay()
    x.AIUpdate()
    x.Log(x.Command(x.CommandLineSavedText))

    pygame.display.flip()
    x.Clock.tick(60)

