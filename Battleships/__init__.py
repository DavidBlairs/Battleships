#calculate the offset direction of a given location and numeric direction (given as coordinates)
def DirectionalOffset(Location, Offset, Direction):
    return {
        0: (Location[0], Location[1] - Offset),
        1: (Location[0] + Offset, Location[1]),
        2: (Location[0], Location[1] + Offset),
        3: (Location[0] - Offset, Location[1])
    }[Direction]


#Adjust for the unbalance direction chosen during random selection (given as a numeric direction)
def DirectionalAdjustment(Location, Size, GridDimensions):
    return {
        Location[0] < Size: 1,
        Location[0] > GridDimensions[0] - Size: 3,
        Location[1] < Size: 2,
        Location[1] > GridDimensions[1] - Size: 2,
        True: False
    }[True]


#check whether the given coordinates exceed the boundaries of the grid
def ExceedBoundaries(Location, GridDimensions):
    if Location[0] < 0: return True
    elif Location[1] < 0: return True
    elif Location[0] >= GridDimensions[0]: return True
    elif Location[1] >= GridDimensions[1]: return True
    else: return False


#How different aspects are presented and saved
AspectRepresentation = {
    0: "X", #0 ---> Ocean
    1: "O", #1 ---> Boat
    2: "E", #2 ---> Explosion
    3: "D"  #3 ---> Destroyed
}

#Used to store data for a given ship
class BattleShip:
    Segments = None
    Direction = None
    Size = None

#determin the frequency of True and False in 2d list
def BooleanFrequency(List):
    TrueFrequency = [] #Location of True
    FalseFrequency = [] #Location of False
    for x in range(len(List)):
        for y in range(len(List[x])):
            if List[x][y] == True:
                TrueFrequency.append((x, y))
            else: FalseFrequency.append((x, y))
    return TrueFrequency, FalseFrequency

