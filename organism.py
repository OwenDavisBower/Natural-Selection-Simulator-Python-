import random
from graphics import *
from configuration import *  
from abc import ABC, abstractmethod 

class Organism (ABC):
    '''
    This class represents Organism objects that all 
    have different traits and allows them to move about
    and consume each other every game tick.
    '''
    
    def __init__(self, window, x, y, size, speed):
        '''
        Initializes the Organism by assigning it's traits
        and drawing the Organism on the screen.
        Parameters:
            window: The graphical window to draw on.
            x, y: The x and y starting coordinates of the Organism.
            size: The size of the Organism. This effects the graphical
                  size of the Organism as well as the strength of the
                  Organism in combat.
            speed: The maximum speed at which an Organism can move each
                   game tick.
        Return Value: none
        '''
        self.pos = [x, y]
        self.speed = speed
        self.size = size
        self.prey = None
        self.energy = 25
        self.age = 0
        self.type = self.getType()

        self.OrganismGraphic = Circle(Point(self.pos[0], self.pos[1]), self.size)

    def update(self, OrganismsList, window):
        '''
        Updates the Organism's position and energy every
        simulation tick.
        Parameters:
            OrganismsList: the list of Organisms (including
                           the Organism itself)
            window: The graphical window which the Organism
                    resides on.
        Return Value: none
        '''
        self.closestTarget = self.nearestTarget(OrganismsList)
        
        # move the Organism
        if self.isPrey(self.closestTarget):
            self.moveToTarget(self.closestTarget)
        else:
            self.moveRandom()

        # keep the Organisms from leaving the screen
        self.stayInScreen()

        self.draw(window)

        # checks for collisions and responds accordingly
        self.checkCollisions(OrganismsList)
        
        self.updateEnergy()
        self.age += 1
        
        if self.energy <= 0:
            if eventLog:
                print('Self starved')
            self.die(OrganismsList)
            
        #reproduces if he has enough energy
        if self.energy >= 30:
            self.energy -= 25
            self.reproduce(window, OrganismsList)
    
    def updateEnergy(self):
        self.energy -= self.energyEfficiency(energyFactor/20, 10)*(self.size**3)*(self.speed)**2
    
    def energyEfficiency(self, factor=1, offsetx=0, offsety=0):
        #Calculate the enegy efficiency with the age
        return (self.age - offsetx)**2*factor + offsety
    
    def reproduce (self, window, OrganismsList):
        '''
        It teproduces the organism at the parent location
        the mutation variable helps to create some genetic variations
        they should be coded in the child functions
        '''
        OrganismsList.append(self.__class__(window, self.pos[0], self.pos[1], self.size, self.speed))

    def isPrey(self, target):
        '''
        Given a target Organism, checks if the target is prey
        for the checking Organism.
        Parameters:
            target: The target Organism that is being checked.
        Return Value:
            True if the target Organism is prey for the self;
            else False.
        '''
        if self.prey == None:
            return False
            
        if target.getType() in self.prey:
            if target.getType() == self.getType():
                if target.getSize() < self.size:
                    return True
            else:
                return True
        return False

    def getPos(self):
        '''
        Returns the position of the given Organism as a list
        containing two points [x, y].
        '''
        return self.pos

    def getSize(self):
        '''
        Returns the size of the given Organism as a float value.
        '''
        return self.size

    def getType(self):
        '''
        Returns the type of the given Organism as a string value.
        '''
        return self.__class__.__name__

    def die(self, OrganismsList):
        '''
        "Kills" the given Organism by undrawing it and then
        removing it from the list of Organisms.
        Parameters:
            OrganismsList: The list to remove the given
                           Organism from.
        Return Value: none
        '''
        #This is to avoid dying from hunger and eaten at the same time
        if self in OrganismsList:
            self.OrganismGraphic.undraw()
            OrganismsList.remove(self)

    def distanceFromTarget(self, target):
        '''
        Calculates and returns the distance between the given
        Organism and the target Organism.
        Parameters:
            target: A target Organism.
        Return Value: The distance between the given Organism
                      and the target Organism.
        '''
        return (abs(target.getPos()[0] - self.pos[0]) + abs(target.getPos()[1] - self.pos[1]))

    def nearestTarget(self, OrganismsList):
        '''
        Searches through the list of other Organisms and
        returns the Organism object of the nearest Organism.
        Parameters:
            OrganismsList: The list of living Organisms.
        Return Value: The Organism object of the nearest
                      Organism.
        '''
        self.selfIndex = OrganismsList.index(self)
        self.otherOrganisms = list(OrganismsList)
        self.otherOrganisms.pop(self.selfIndex)
        self.closestTarget = self.otherOrganisms[0]
        for Organism in self.otherOrganisms[1:]:
            if self.distanceFromTarget(Organism) < self.distanceFromTarget(self.closestTarget):
                self.closestTarget = Organism
        return self.closestTarget

    def moveToTarget(self, target):
        '''
        Moves the given Organism towards the target Organism.
        Parameters:
            target: A target Organism.
        Return Value: none
        '''
        self.targetPosX, self.targetPosY = target.getPos()
        self.distanceX, self.distanceY = (self.targetPosX - self.pos[0], self.targetPosY - self.pos[1])

        if self.distanceX >= 0:
            self.velocityX = self.speed * speedFactor
            if abs(self.distanceX) < abs(self.velocityX):
                self.velocityX = self.distanceX
        else:
            self.velocityX = -self.speed * speedFactor
            if abs(self.distanceX) < abs(self.velocityX):
                self.velocityX = self.distanceX
        self.pos[0] += self.velocityX

        if self.distanceY >= 0:
            self.velocityY = self.speed * speedFactor
            if abs(self.distanceY) < abs(self.velocityY):
                self.velocityX = self.distanceX
        else:
            self.velocityY = -self.speed * speedFactor
            if abs(self.distanceY) < abs(self.velocityY):
                self.velocityY = self.distanceY
        self.pos[1] += self.velocityY

    def moveRandom(self):
        '''
        Moves the given Organism randomly in 2D space.
        '''
        self.velocity = (random.uniform(-self.speed, self.speed) * speedFactor, random.uniform(-self.speed, self.speed) * speedFactor)
        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

    def stayInScreen(self):
        '''
        Prevents the Organisms from leaving the screen.
        '''
        if self.pos[0] + self.size >= windowSize:
            self.pos[0] = windowSize - self.size
        elif self.pos[0] - self.size <= -windowSize:
            self.pos[0] = -windowSize + self.size
        elif self.pos[1] + self.size >= windowSize:
            self.pos[1] = windowSize - self.size
        elif self.pos[1] - self.size <= -windowSize:
            self.pos[1] = -windowSize + self.size

    def draw(self, window):
        '''
        Creates a graphical object for the Organism based
        upon it's size and type and then draws it onto the
        graphic window.
        Parameters:
            window: A graphical window.
        Return Value: none
        '''
        if self.OrganismGraphic:
            self.OrganismGraphic.undraw()
        self.OrganismGraphic = Circle(Point(self.pos[0], self.pos[1]), self.size)

    def checkCollision(self, collidingOrganism):
        '''
        Checks if the given Organism is colliding with the
        "collidingOrganism".
        Parameters:
            collidingOrganism: The Organism to be tested against.
        Return Value:
            True if the given Organism is colliding with the
            "collidingOrganism"; else returns False.
        '''
        self.collidingOrganismPos = collidingOrganism.getPos()
        self.collidingOrganismsize = collidingOrganism.getSize()

        if (self.pos[0] - self.size) <= self.collidingOrganismPos[0] <= (self.pos[0] + self.size):
            if (self.pos[1] - self.size) <= self.collidingOrganismPos[1] <= (self.pos[1] + self.size):
                return True
        elif (self.collidingOrganismPos[0] - self.collidingOrganismsize) <= self.pos[0] <= (self.collidingOrganismPos[0] + self.collidingOrganismsize):
            if (self.collidingOrganismPos[1] - self.collidingOrganismsize) <= self.pos[1] <= (self.collidingOrganismPos[1] + self.collidingOrganismsize):
                return True
        return False

    def checkCollisions(self, OrganismsList):
        '''
        Checks if the Organism is colliding with any Organisms
        and reacts appropriately by killing one of the
        Organisms if it is prey of the other.
        Parameters:
            OrganismsList: The list of Organisms.
        Return Value: none
        '''
        for Organism in OrganismsList:
            if Organism != self: # prevents Organism from checking if it's colliding with itself
                if self.checkCollision(Organism):
                    if self.isPrey(Organism):
                        if eventLog:
                            print('Self killed Organism')
                        
                        self.energy += Organism.energy
                        Organism.die(OrganismsList)
                    elif Organism.isPrey(self):
                        if eventLog:
                            print('Organism killed self')
                        self.die(OrganismsList)