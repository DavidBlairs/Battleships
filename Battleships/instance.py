import random, pygame, socket
import Battleships, sys, time
from Battleships.displayConstants import *

#Class for saving and monitoring an instance of "battleships"
class BattleshipInstance:
    def __init__(self, GridDimensions):
        #The height and width of the grid
        self.GridDimensions = GridDimensions

        #Visual representation of the ships and the oceans
        self.ShipRepresentation = Battleships.AspectRepresentation[1]
        self.OceanRepresentation = Battleships.AspectRepresentation[0]
        self.ExplosionRepresentation = Battleships.AspectRepresentation[2]
        self.DestroyedRepresentation = Battleships.AspectRepresentation[3]

        #Establish a location the store the grid data
        self.GridData = [[self.OceanRepresentation for AspectX in range(self.GridDimensions[0])]
                         for AspectY in range(self.GridDimensions[1])]

        #List of the ships currently on the map
        self.ActiveShips = []

        #Store for the command line
        self.CommandLineCurrentText = ""
        self.CommandLineSavedText = ""

        #Estabish the IO Layer and button layers
        self.InputOutputFeatureLayer = InputOutputFeatureLayer
        self.ButtonLayerRect = [Button1LayerRect, Button2LayerRect, Button3LayerRect]
        self.ButtonLayers = [Button1Layer, Button2Layer,  Button3Layer]

        #mouse variables
        self.MouseMovementState = True

        #Initiate pygame for display
        pygame.init()

        #establish the screen with default dimensions
        self.ScreenDimensions = (ctypes.windll.user32.GetSystemMetrics(0),
                                ctypes.windll.user32.GetSystemMetrics(1))
        self.Screen = pygame.display.set_mode(self.ScreenDimensions, pygame.FULLSCREEN)

        #set the in game clock
        self.Clock = pygame.time.Clock()
        self.Font = pygame.font.Font(None, 36)

        #Board Variables
        self.BoardOffsetCoordinates = [0, 0]
        self.TemporaryCoordinates = None
        self.BoardSegmentSize = [20, 20]

        #Command Line Variables
        self.CommandLineState = False
        self.CommandLineSavedPerm = ""

        #Log Variables
        self.LogFont = pygame.font.Font(None, 12)

        self.UnrenderedText = ["==Log=="]
        self.RenderedText = []

        pygame.draw.rect(LogLayer, (102, 0, 204), [3, 3, LogLayer.get_width()-6, LogLayer.get_height()-6], 3)

        #AI variables
        self.AIState = False
        self.AIGrid = [[True for AspectX in range(self.GridDimensions[0])]
                         for AspectY in range(self.GridDimensions[1])]
        self.AIExplosionAvailable = True
        self.AIGrid[4][3] = False

        #Networking Variables
        self.NetworkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #Check for button overlay
    def CheckMouseButtonOverlay(self):
        #--> use this to check which button
        self.MouseOnePressed()
        self.MouseTwoPressed()
        self.MouseThreePressed(False)


    #Check whether mouse one has been pressed
    def MouseOnePressed(self):
        Text = self.Font.render("Exit", 1, (0, 100, 0))
        if Button1LayerRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]: #-->  change color when pressed
                ChangeBackgroundColour(Button1Layer, (0, 0, 0))
                sys.exit() #--> cancel the process
            else: pygame.draw.rect(Button1Layer ,(0, 200, 0), [3, 3, Button1Layer.get_width()-6, Button1Layer.get_height()-6], 3)
        else: pygame.draw.rect(Button1Layer, (0, 150, 0), [3, 3, Button1Layer.get_width()-6, Button1Layer.get_height()-6], 3)
        Button1Layer.blit(Text, ((Button1Layer.get_width()/2)-(Text.get_width()/2),
                                 (Button1Layer.get_height()/2)-(Text.get_height()/2)))

    #CHeck whether mouse two has been pressed
    def MouseTwoPressed(self):
        Text = self.Font.render("Scale", 1, (0, 100, 0))
        if Button2LayerRect.collidepoint(pygame.mouse.get_pos()):
            if not self.BoardSegmentSize[0] > 400: #--> placing upwards restrictions on scale
                if not self.BoardSegmentSize[0] < 25: #--> placing downwards restrictions on scale

                    if pygame.mouse.get_pressed()[0]: #-->  change color when pressed
                        ChangeBackgroundColour(Button2Layer, (0, 250, 0))
                        self.ScaleBoardSegments(0.1) #scaling positive
                    elif pygame.mouse.get_pressed()[2]:
                        ChangeBackgroundColour(Button2Layer, (0, 0, 0)) #change in colour for hover
                        self.ScaleBoardSegments(-0.1) #scale nagative

                    else: pygame.draw.rect(Button2Layer ,(0, 200, 0), [3, 3, Button2Layer.get_width()-6, Button2Layer.get_height()-6], 3)
                else: self.ScaleBoardSegments(0.1) #--> going to far down
            else: self.ScaleBoardSegments(-0.1) #--> going to far up
        else: pygame.draw.rect(Button2Layer ,(0, 150, 0), [3, 3, Button2Layer.get_width()-6, Button2Layer.get_height()-6], 3)

        #blit the final product to the screen with all modifications
        Button2Layer.blit(Text, ((Button2Layer.get_width()/2)-(Text.get_width()/2),
                                 (Button2Layer.get_height()/2)-(Text.get_height()/2)))


    #Scale the board segments
    def ScaleBoardSegments(self, scale):
        #self.BoardSegmentSize[0] += int((scale)*self.BoardSegmentSize[0]) #--> scale the board width
        #self.BoardSegmentSize[1] += int((scale)*self.BoardSegmentSize[1]) #--> scale the board height
        pass

    #place ship on the display
    def UpdateShipDisplay(self):
        ChangeBackgroundColour(BattleshipLayer, (0, 0, 0)) #--> restart the Battleship Layer

        for Ship in self.ActiveShips: #--> go over every active ship
            TemporaryLayer = pygame.Surface((BattleshipLayer.get_width()/len(self.ActiveShips), BattleshipLayer.get_height()))
            TemporaryLayer.fill((0, 0, 0)) #--> Create a surface to add details about the ship

            #Setup the secondary layer for adding aesthetics
            SecondaryTemporaryLayer = pygame.Surface((TemporaryLayer.get_width()*0.9,   #-->90% of the prior surface
                                                      TemporaryLayer.get_height()*0.9)) #-->90% of the prior surface

            #Fill the layer with a slight red and add border
            pygame.draw.rect(SecondaryTemporaryLayer, (150, 0, 0), [3,3, SecondaryTemporaryLayer.get_width()-6, SecondaryTemporaryLayer.get_height()-6], 3)
            DrawBorder(SecondaryTemporaryLayer)
            TemporaryLayer.blit(SecondaryTemporaryLayer, (TemporaryLayer.get_width()*0.05, #--> border of 5%
                                                          TemporaryLayer.get_height()*0.05))

            #Render text for the ships segment details
            RenderedText = self.Font.render(str(len(Ship.Segments)), 1, (100, 0, 0))
            TemporaryLayer.blit(RenderedText, ((TemporaryLayer.get_width()/2)-(RenderedText.get_width()/2),
                                               (TemporaryLayer.get_height()/2)-(RenderedText.get_height()/2)))

            #blit this text to the screen
            BattleshipLayer.blit(TemporaryLayer, ((self.ActiveShips.index(Ship)*BattleshipLayer.get_width())/len(self.ActiveShips), 0))
        DrawBorder(BattleshipLayer)


    #Get input from the command line
    def CommandLineInputUpdate(self):
        CommandLineLayer.fill((0, 0, 0))

        pygame.draw.rect(CommandLineLayer, (204, 102, 0), [3, 3, CommandLineLayer.get_width()-6, CommandLineLayer.get_height()-6], 3) #--> reset the commandline

        #handle the mouse in box and out functionality
        if pygame.mouse.get_pressed()[0]:
            if CommandLineLayerRect.collidepoint(pygame.mouse.get_pos()):
                if not self.CommandLineState:
                    self.CommandLineState = True #--> mouse in the box
            elif not CommandLineLayerRect.collidepoint(pygame.mouse.get_pos()):
                self.CommandLineState = False #--> mouse out of the box

        #Function for rendering text with Colour "Colour"
        def RenderText(Text, Colour):
            return self.Font.render(Text, 1, Colour) #Use self.Font

        #Event handling for the commandline
        if self.CommandLineState:
            for Event in pygame.event.get():
                if Event.type == pygame.KEYDOWN: #Check for keyboard event
                    if Event.key == pygame.K_BACKSPACE: #--> subtract a letter from the text
                        self.CommandLineCurrentText = self.CommandLineCurrentText[:-1] #:-1 --> backspace

                    elif Event.key == pygame.K_UP: #--reload past text
                        self.CommandLineCurrentText = self.CommandLineSavedPerm

                    elif not RenderText(self.CommandLineCurrentText + #Check new text is within boundary
                                      str(Event.unicode), (153, 76, 0)).get_width() > (CommandLineLayer.get_width() * 0.95):

                        #Set the new state of the text after conditions met
                        self.CommandLineCurrentText = self.CommandLineCurrentText + str(Event.unicode)

        #render the text depending on whether the user is in the box
        if self.CommandLineState: TextCommandLine = RenderText(self.CommandLineCurrentText + "_", (153, 76, 0))
        else: TextCommandLine = RenderText(self.CommandLineCurrentText, (153, 76, 0))

        #add to the CommandLineLayer and add the border
        CommandLineLayer.blit(TextCommandLine, ((CommandLineLayer.get_width()/2)-(TextCommandLine.get_width()/2),
                                                (CommandLineLayer.get_height()/2)-(TextCommandLine.get_height()/2)))
        DrawBorder(CommandLineLayer)#--> default blue border


    #Update grid with details about the currently active ships
    def UpdateDisplayShipsBoard(self):
        #Reset the board
        BoardLayer.fill((0, 0, 0))

        #Iterate over all coordinates available
        TempX = 0#--> compensate for poor iteration
        for XGrid in self.GridData: #--> go over every X
            TempY = 0
            for YGrid in XGrid: #--> go over every Y

                #Reset a temporary Surface for use
                TempGridSurface = pygame.Surface(self.BoardSegmentSize)
                pygame.draw.rect(TempGridSurface, { #Use representation for analysis
                    self.OceanRepresentation: (0, 0, 150),
                    self.ShipRepresentation: (150, 150, 150),
                    self.DestroyedRepresentation: (250, 0, 0),
                    self.ExplosionRepresentation: (150, 0, 0)
                }[YGrid], [2, 2, TempGridSurface.get_width() - 3, TempGridSurface.get_height() - 3], 2)

                #Draw the borders and blit the the game surface
                pygame.draw.rect(TempGridSurface, (0, 0, 0),
                                 [0, 0, TempGridSurface.get_width(), TempGridSurface.get_height()], 2)
                BoardLayer.blit(TempGridSurface, ((TempX*self.BoardSegmentSize[0])+self.BoardOffsetCoordinates[0],
                                                  (TempY*self.BoardSegmentSize[1])+self.BoardOffsetCoordinates[1]))
                TempY += 1
            TempX += 1
        #Draw final border for the game
        DrawBorder(BoardLayer)
        pygame.draw.rect(BoardLayer, (255, 255, 0), [3, 3, BoardLayer.get_width()-6, BoardLayer.get_height()-6], 3)

        #Small piece of logic to handle mouse movement
        if BoardLayerRect.collidepoint(pygame.mouse.get_pos()):

            #create temporary stores of data regarding the current and
            #only the current sate of the board.
            if pygame.mouse.get_pressed()[0]:
                if self.MouseMovementState:
                    self.TemporaryCoordinates = tuple(self.BoardOffsetCoordinates) #So it cant be edited
                    self.MovementOffset = pygame.mouse.get_pos()
                    self.MouseMovementState = False

                #Use this data to move the level with the mouse by looking at the level before and after movement
                self.BoardOffsetCoordinates[0] = self.TemporaryCoordinates[0] + (pygame.mouse.get_pos()[0] - self.MovementOffset[0])
                self.BoardOffsetCoordinates[1] = self.TemporaryCoordinates[1] + (pygame.mouse.get_pos()[1] - self.MovementOffset[1])
            else:
                self.MouseMovementState = True


    #Update the AI. Will only work when commanded to
    def AIUpdate(self):
        if self.AIState: #--> only activate when commanded to
            FrequencyTrue, FrequencyFalse = Battleships.BooleanFrequency(self.AIGrid) #Get the available coordinates

            #check whether the AI can make an explosion
            if self.AIExplosionAvailable:
                XValues, YValues = self.Log(zip(*FrequencyTrue)) #It will make an explosion at the average coordinates
                AverageCoordinateTrue = (int(sum(XValues)/len(XValues)),
                                         int(sum(YValues)/len(YValues)))
                Feedback = self.Log(self.Command("aiexplosion " + str(AverageCoordinateTrue[0]) + "," + str(AverageCoordinateTrue[1]) + " 6"))[0][1]
                self.AIExplosionAvailable = False #no longer allow the AI to make an explosion until reset

                #update the grid to make sure the random check runs faster
                for Coordinate in Feedback:
                    self.AIGrid[Coordinate[0]][Coordinate[1]] = False

            #If the game is registered as done, reset the game
            if self.Log(self.Command("update"))[0][1]:
                self.Log(self.Command("reset"))

            #if locations available for testing, test them
            if not len(FrequencyTrue) == 0:
                RandomCoordinates = FrequencyTrue[random.randrange(0, len(FrequencyTrue))]
                if Battleships.ExceedBoundaries(RandomCoordinates, self.GridDimensions):
                   return
            else:
                self.Log(self.Command("reset"))
                return #reset when determination complete

            #attempt to destroy segment
            if not self.Command("ebattleship " + str(RandomCoordinates[0]) + "," + str(RandomCoordinates[1]))[0][0]:
                self.AIGrid[RandomCoordinates[0]][RandomCoordinates[1]] = False
                return
            else: self.AIGrid[RandomCoordinates[0]][RandomCoordinates[1]] = False


    #Check whether mouse three has been pressed
    def MouseThreePressed(self, Admin):
        if Admin: #administrator overight
            self.CommandLineSavedText = self.CommandLineCurrentText
            self.CommandLineCurrentText = ""

        Text = self.Font.render("Enter", 1, (0, 100, 0))
        if Button3LayerRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]: #-->  change color when pressed
                ChangeBackgroundColour(Button3Layer, (0, 0, 0))
                self.CommandLineSavedText = self.CommandLineCurrentText
                self.CommandLineSavedPerm = self.CommandLineCurrentText
                self.CommandLineCurrentText = ""
            else: pygame.draw.rect(Button3Layer ,(0, 200, 0), [3, 3, Button3Layer.get_width()-6, Button3Layer.get_height()-6], 3)
        else: pygame.draw.rect(Button3Layer ,(0, 150, 0), [3, 3, Button3Layer.get_width()-6, Button3Layer.get_height()-6], 3)

        #place the enter button on the screen
        Button3Layer.blit(Text, ((Button3Layer.get_width()/2)-(Text.get_width()/2),
                                 (Button3Layer.get_height()/2)-(Text.get_height()/2)))


    #Place a ship on the grid at a given location with extension "size - 1" and direction
    def PlaceBattleship(self, Location, Size, Direction):
        #Setup a "data store" for the ships coordinates and direction
        TemporaryShipTemplate = Battleships.BattleShip()
        TemporaryShipTemplate.Segments = []

        try:
            if [self.CheckPlacement(Battleships.DirectionalOffset(Location, Offset, Direction))
                for Offset in range(Size)].count(self.ShipRepresentation) >= 1:
                if [self.CheckPlacement(Battleships.DirectionalOffset(Location, Offset, Direction))
                for Offset in range(Size)].count(self.ExplosionRepresentation) >= 1:
                    return False #---> Cant and shouldn't attempt to place a ship on an explosive location
                return False #---> Return false if there are any ships located in the requested space
            else:
                for Segment in range(Size):
                    NewLocation = Battleships.DirectionalOffset(Location, Segment, Direction) #---> Establish a new set of coordinates with offset
                    if not Battleships.ExceedBoundaries(NewLocation, self.GridDimensions):
                        self.SetPlacement(NewLocation, 1) #---> change state of "NewLocation"
                        TemporaryShipTemplate.Segments.append(NewLocation)
                    else:
                        self.DeleteBattleship(TemporaryShipTemplate)
                        return False #--> if it exceeded the boundary, delete and cancel
        except: return False #---> Sometimes occurs but only when passed parameters where wrong

        #Complete the data assignment for the Ship
        TemporaryShipTemplate.Direction = Direction
        TemporaryShipTemplate.Size = Size

        #Append the the current ActiveShips list
        self.ActiveShips.append(TemporaryShipTemplate)
        return True


    #function for logging to log box
    def Log(self, Text):
        if Text == "" or Text == None: return False
        LogLayer.fill((0, 0, 0))
        pygame.draw.rect(LogLayer, (102, 0, 204), [3, 3, LogLayer.get_width()-6, LogLayer.get_height()-6], 3)

        #Function for rendering text with Colour "Colour"
        def RenderText(Text, Colour):
            return self.LogFont.render(Text, 1, Colour) #Use self.Font

        #Determin what text will go on which line
        TempTextUnrendered = ""
        for Character in range(len(str(Text))):
            TempTextUnrendered = TempTextUnrendered + str(Text)[Character] #--> text gets longer by the iteration
            if RenderText(TempTextUnrendered, (153, 0, 153)).get_width() > 0.90 * LogLayer.get_width():
                self.UnrenderedText.append(TempTextUnrendered) #only when text exceeds boudaries
                TempTextUnrendered = "" #reset for futher determination

        #add whatever is left of the command
        self.UnrenderedText.append(TempTextUnrendered)

        #check if exceeding height boundary
        for line in range(15): #Doesnt seem to work just once
            if (RenderText(self.UnrenderedText[0], (0, 0, 0)).get_height()
                    * len(self.UnrenderedText)) > 0.90 * LogLayer.get_height():
                self.UnrenderedText = self.UnrenderedText[1:] #delete first item only

        #render the text and add to new list
        for UnrenderedText in self.UnrenderedText:
            self.RenderedText.append(RenderText(UnrenderedText, (76, 0, 153)))

        #blit the rendered text to the screen at different y positions and equal x position
        for RenderedText in range(len(self.RenderedText)):
            LogLayer.blit(self.RenderedText[RenderedText], ((0.05*LogLayer.get_width()),
                                                            (0.05*LogLayer.get_height())+(self.RenderedText[RenderedText].get_height()*RenderedText)))
        self.RenderedText = [] #--> reset the rendered text list
        return Text #return text for function run


    #Enter commands into the systems. Used for AI
    def Command(self, Command):
        if Command == "" or Command == None: return None #--> Command != None
        TempCommand = Command.split() #Split commands and arguments into list

        #append useless values for indexing unused values
        TempCommand += ["100, 100" for i in range(5)]

        def Explosion(Args): #function for breaking up > 1 arguments
            return self.CreateExplosion(tuple([int(x) for x in Args[0].split(",")]), int(Args[1]))

        def PBattleship(Args): #likewise, function for breaking up > 2 arguments
            return self.PlaceBattleship(tuple([int(x) for x in Args[0].split(",")]), int(Args[1]), int(Args[2]))

        def Set(Args): #function for breaking up > 1 arguments
            return self.SetPlacement(tuple([int(x) for x in Args[0].split(",")]), int(Args[1]))

        def AIState(): #change the aistate variable
            self.AIState = {False: True, True: False}[self.AIState]
            return self.AIState

        #Convert commands to functions and args
        FunctionArgs = {
            "ebattleship": (self.ExplodeBattleshipSegment, tuple([int(x) for x in TempCommand[1].split(",")])),
            "check": (self.CheckPlacement, tuple([int(x) for x in TempCommand[1].split(",")])),
            "set": (Set, (TempCommand[1], TempCommand[2])),
            "aiexplosion": (Explosion, (TempCommand[1], TempCommand[2])),
            "dbattleship": (self.DeleteBattleship, TempCommand[1]),
            "update": (self.UpdateBattleships, TempCommand[1]),
            "supdate": (self.SegmentedUpdate, TempCommand[1]),
            "rplace": (self.RandomPlacement, tuple([int(x) for x in TempCommand[1].split(",")])),
            "pbattleship": (PBattleship, (TempCommand[1], TempCommand[2], TempCommand[3])),
            "reset": (self.Reset, TempCommand[1]),
            "aiattempt": (self.AIAttempt, tuple([int(x) for x in TempCommand[1].split(",")])),
            "aistate": (AIState, TempCommand[1])
        }
        #get the function and args for the passed command
        try:
            FunctionArgs = FunctionArgs[str(TempCommand[0])]
        except:
            self.Log("Error: The Function Was Either Not Recognised Or Incorrectly Ran.")
            return

        #outputs to the log for analysis
        MessageOutput = {
            "ebattleship": "The Battleship Explode Function Has Been Called.",
            "check": "The Check Placement Function Has Been Called.",
            "set": "The Set Placement Function Has Been Called.",
            "aiexplosion": "The AI Has Made An Attempt.",
            "dbattleship": "The Destroy Battleship Function Has Been Called.",
            "update": "The Update Function Has Been Called.",
            "supdate": "The Segmented Update Function Has Been Called.",
            "rplace": "The Random Placement Function Has Been Called.",
            "pbattleship": "The Place Battleship Function Has Been Called.",
            "reset": "The Board Has Been Reset",
            "aiattempt": "The AI Has Made An Attempt.",
            "aistate": "Change The State Of The AI",
        }[str(TempCommand[0])]

        #return the output from running this function
        if FunctionArgs[1] == "100, 100":
            return FunctionArgs[0](), MessageOutput
        else: return FunctionArgs[0](FunctionArgs[1]), MessageOutput


    #Refresh the Display
    def RefreshDisplay(self):
        UpdateIOFeatures() #---> Update the IO features


    #update the screen with the IO board
    def UpdateDisplay(self):
        self.Screen.blit(self.InputOutputFeatureLayer, (0, 0)) #--> blit these features to the screen


    #one of few functions for the AI system
    def AIAttempt(self, Coordinates):
        CheckOutput = self.Log(self.Command("check " + str(Coordinates[0]) + "," + str(Coordinates[1])))
        FunctionOutput = self.Log(self.Command("set " + str(Coordinates[0]) + "," + str(Coordinates[1]) + " 2"))
        if CheckOutput[0] == self.ShipRepresentation:
            return True, Coordinates #return true if hit and the coordinates
        else:
            return False, Coordinates#return false if no hit detected with coordinates


    #Randomly determine where to put a passed set of ships
    def RandomPlacement(self, Specification):
        for Placement in Specification:
            while True:
                TemporaryLocation = ( #---> Pick a "Random" location on the board
                random.randrange(0, self.GridDimensions[0]),
                random.randrange(0, self.GridDimensions[1])
                )

                #cancel current placement as it exceed dimensions
                if Placement > self.GridDimensions[0] or\
                    Placement > self.GridDimensions[1]: break

                #place battleship on the board
                if self.PlaceBattleship(TemporaryLocation, Placement,
                random.randrange(0, 4)):
                    break


    #Create an explosion on the board with x radius
    def CreateExplosion(self, Location, Range):
        CoordinatesHitList = []
        CoordinatesList = []
        for OffsetX in range(-Range, Range + 1):
            for OffsetY in range(-Range, Range + 1):
                if abs(OffsetX) + abs(OffsetY) <= Range:
                    CoordinatesList.append((Location[0]+OffsetX, Location[1]+OffsetY))
                    if not Battleships.ExceedBoundaries((Location[0]+OffsetX, Location[1]+OffsetY), self.GridDimensions):
                        for Coordinate in self.ActiveShips:
                            if (Location[0]+OffsetX, Location[1]+OffsetY) in Coordinate.Segments:
                                Coordinate.Segments.remove((Location[0]+OffsetX, Location[1]+OffsetY))
                                CoordinatesHitList.append((Location[0]+OffsetX, Location[1]+OffsetY))
                        self.SetPlacement((Location[0]+OffsetX, Location[1]+OffsetY), 3)

        return CoordinatesHitList, CoordinatesList#---> return a list of the destroyed ship segments

    #Update the battleships that have been destroyed.
    def SegmentedUpdate(self):
        ExplodedShips = []
        GameCompleted = False
        for Battleship in self.ActiveShips:
            if len(Battleship.Segments) == 0: #--> if zero segments are active on the board
                ExplodedShips.append(Battleship)
                self.ActiveShips.remove(Battleship)
        if len(self.ActiveShips) == 0: GameCompleted = True
        return ExplodedShips, GameCompleted

    #Sometimes, a single update fails yet three updates succeeds
    def UpdateBattleships(self):
        SegmentedDeletion = []
        for segment in range(2): SegmentedDeletion.append(self.SegmentedUpdate()[0])
        FinalUpdate = self.SegmentedUpdate()
        return SegmentedDeletion + FinalUpdate[0], FinalUpdate[1]

    #delete an active battleship
    def DeleteBattleship(self, Battleship):
        for Segment in Battleship.Segments:
            self.SetPlacement(Segment, 0) #---> delete all presence on board
        if Battleship in self.ActiveShips:
            self.ActiveShips.remove(Battleship) #---> remove from active ships

    #Destroy ship segment and replace with self.ExplosionRepresentation
    def ExplodeBattleshipSegment(self, Coordinates):
        for Segments in self.ActiveShips:
            if Coordinates in Segments.Segments:
                Segments.Segments.remove(Coordinates)
                self.SetPlacement(Coordinates, 3)
                return True, Coordinates #comfirmed hit
            self.SetPlacement(Coordinates, 3)
        return False, Coordinates #uncomfirmed hit

    #Change the state of a given location
    def SetPlacement(self, Location, State):
        self.GridData[Location[1]][Location[0]] = {0: self.OceanRepresentation,
        1: self.ShipRepresentation, 2: self.ExplosionRepresentation, 3: self.DestroyedRepresentation}[State] #---> Toggle between ship and ocean


    #Check the placement at a given location
    def CheckPlacement(self, Location):
        return self.GridData[Location[1]][Location[0]]

    #This function resets the game instance
    def Reset(self):
        self.ActiveShips = [] #reset the Active ships lists
        self.AIExplosionAvailable = True #Reset AI variables
        self.GridData = [[self.OceanRepresentation for AspectX in range(self.GridDimensions[0])]
                         for AspectY in range(self.GridDimensions[1])] #Reset the Grid
        self.AIGrid = [[True for AspectX in range(self.GridDimensions[0])]
                         for AspectY in range(self.GridDimensions[1])] #Reset the AI Grid
        self.Command("rplace 4,5,6,7,8,9,10,4,5,6,7,8") #issue a random place command

        #return the output from an update command
        return self.Command("update")
