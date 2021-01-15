import random
from graphics import *
from organism import Organism
from configuration import *  

class Herbivore(Organism):
    def __init__(self, window, x = None, y = None, size = None, speed = None):
        '''
        Can generate a random Herbivore.
        Return Value: A randomly generated Organism object.
        '''
        if(x == None):
            x = random.uniform(-(windowSize * .9), windowSize * .9)
        if(y == None):
            y = random.uniform(-(windowSize * .9), windowSize * .9)
        if(size == None):
            size = random.uniform(1, 7)
        if(speed == None):
            speed = random.uniform(5, 10)
        
        Organism.__init__(self, window, x, y, size, speed)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('blue')
        self.OrganismGraphic.draw(window)
        self.prey = ['Plant']
        
    def draw(self,window):
        super().draw(window)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('blue')
        self.OrganismGraphic.draw(window)
        
class Omnivore(Organism):
    def __init__(self, window, x = None, y = None, size = None, speed = None):
        '''
        Can generate a random Omnivore.
        Return Value: A randomly generated Organism object.
        '''
        if(x == None):
            x = random.uniform(-(windowSize * .9), windowSize * .9)
        if(y == None):
            y = random.uniform(-(windowSize * .9), windowSize * .9)
        if(size == None):
            size = random.uniform(1, 7)
        if(speed == None):
            speed = random.uniform(5, 10)
        
        Organism.__init__(self, window, x, y, size, speed)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('orange')
        self.OrganismGraphic.draw(window)
        self.prey = ['Plant', 'Omnivore', 'Herbivore', 'Carnivore']
        
    def draw(self,window):
        super().draw(window)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('orange')
        self.OrganismGraphic.draw(window)

class Carnivore(Organism):
    def __init__(self, window, x = None, y = None, size = None, speed = None):
        '''
        Can generate a random Carnivore.
        Return Value: A randomly generated Organism object.
        '''
        if(x == None):
            x = random.uniform(-(windowSize * .9), windowSize * .9)
        if(y == None):
            y = random.uniform(-(windowSize * .9), windowSize * .9)
        if(size == None):
            size = random.uniform(1, 7)
        if(speed == None):
            speed = random.uniform(5, 10)
            
        Organism.__init__(self, window, x, y, size, speed)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('red')
        self.OrganismGraphic.draw(window)
        self.prey = ['Omnivore', 'Herbivore', 'Carnivore']
        
    def draw(self,window):
        super().draw(window)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill('red')
        self.OrganismGraphic.draw(window)
        
class Plant(Organism):
    def __init__(self, window, x = None, y = None, size = None, speed = None):
        '''
        Can generate a random Plant.
        Return Value: A randomly generated Organism object.
        '''
        if(x == None):
            x = random.uniform(-(windowSize * .9), windowSize * .9)
        if(y == None):
            y = random.uniform(-(windowSize * .9), windowSize * .9)
        if(size == None):
            size = random.uniform(1, 7)
        if(speed == None):
            speed = random.uniform(5, 10)
            
        Organism.__init__(self, window, x, y, size, speed)
        # assign a color based upon Organism type
        self.OrganismGraphic.setFill(color_rgb(10, 117, 31))
        self.OrganismGraphic.draw(window)
        
    def draw(self,window):
        pass
        
    #Plants gather energy from sun
    def updateEnergy(self):
        self.energy += self.energyEfficiency(energyFactor, 10, 100*energyFactor)*(self.size**2)
        
    def reproduce (self, window, OrganismsList):
        '''
        It teproduces the organism at the parent location
        the mutation variable helps to create some genetic variations
        they should be coded in the child functions
        '''
        x_offset = random.randint(-15, 15)
        y_offset = random.randint(-15, 15)
        random.seed(time)
        
        if self.pos[0] + self.size + x_offset >= windowSize or self.pos[0] - self.size + x_offset <= -windowSize:
            x_offset *= -1
        elif self.pos[1] + self.size + y_offset >= windowSize or self.pos[1] - self.size + y_offset <= -windowSize:
            x_offset *= -1
            
        newpos = [self.pos[0] + x_offset, self.pos[1] + y_offset]
        OrganismsList.append(self.__class__(window, newpos[0], newpos[1], self.size, self.speed))
