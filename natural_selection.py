'''
2016 CS-167 Final Project: 
natural_selection.py
This program runs a simulation on natural selection in a
graphical interface. Watch as the Organisms move about
targeting prey (or plants) and attempting to avoid predators.
The largest fitter Organisms will survive.
by Owen Davis-Bower
'''

import random
from graphics import *
from organisms import *
from configuration import *
from analyse import *

class simInterface:

    def __init__(self):
        '''
        Initializes the simulation window.
        '''
        # initialize window
        self.win = GraphWin('Natural Selection Simulation', 700, 600)
        # transform coordinates
        self.win.setCoords(-100, -150, 100, 100)

        self.lowerInterface = self.createLowerInterface()
        self.lowerInterface.draw(self.win)

        self.OrganismCircle = None

    def getWin(self):
        '''
        Returns the simulation window.
        '''
        return self.win

    def createLowerInterface(self):
        '''
        Draws the interface at the bottom of the screen.
        '''
        interfaceRectangle = Rectangle(Point(-100, -100), Point(100, -150))
        interfaceRectangle.setFill("gray")
        return interfaceRectangle

    def close(self):
        '''
        Closes the graphical window.
        '''
        self.win.close()

class naturalSelectionSim:

    def __init__(self):
        '''
        Initializes the simulation window and interface.
        '''
        self.interface = simInterface()
        self.window = self.interface.getWin()

    def runSim(self):
        '''
        Runs the simulation from start to finish.
        '''
        self.displayInformation()

        self.waitForClick()

        self.spawnOrganisms()

        self.keepRunning = True
        for i in range(gameTicks):
            self.update()

        time.sleep(2)

        # destroy all remaining Organisms
        for Organism in self.Organisms:
            Organism.die(self.Organisms)

    def waitForClick(self):
        '''
        Displays a message on the screen and waits for user
        input in order to continue.
        '''
        self.startText = Text(Point(0, 0), 'Click anywhere to begin the simulation.')
        self.startText.setSize(20)
        self.startText.draw(self.window)
        self.window.getMouse()
        self.startText.undraw()

    def displayInformation(self):
        '''
        Displays information in the lower interface of simulation
        window.
        '''
        self.informativeText_1 = Text(Point(0, -105), 'Click anywhere inside the habitat to spawn a new Organism.')
        self.informativeText_1.setSize(20)
        self.informativeText_1.draw(self.window)

        self.plantExample = Circle(Point(-90, -120), 3)
        self.plantExample.setFill(color_rgb(10, 117, 31))
        self.plantExample.draw(self.window)
        self.plantTitle = Text(Point(-67, -120), '= Plant')
        self.plantTitle.setSize(20)
        self.plantTitle.draw(self.window)

        self.herbivoreExample = Circle(Point(-90, -130), 3)
        self.herbivoreExample.setFill('blue')
        self.herbivoreExample.draw(self.window)
        self.herbivoreTitle = Text(Point(-59, -130), '= Herbivore')
        self.herbivoreTitle.setSize(20)
        self.herbivoreTitle.draw(self.window)

        self.omnivoreExample = Circle(Point(-90, -140), 3)
        self.omnivoreExample.setFill('orange')
        self.omnivoreExample.draw(self.window)
        self.omnivoreTitle = Text(Point(-59, -140), '= Omnivore')
        self.omnivoreTitle.setSize(20)
        self.omnivoreTitle.draw(self.window)

    def spawnOrganisms(self):
        '''
        Spawns in randomly generated Organisms by adding them
        to a list of Organisms.
        '''
        self.Organisms = []
        for i in range(3):
            self.Organisms.append(Omnivore(self.window))
        for i in range(5):
            self.Organisms.append(Herbivore(self.window))
        # BUG: Carnivores are not fully implemented yet.
        # for i in range(5):
        #   self.Organisms.append(self.randomOrganism('carnivore'))
        for i in range(15):
            self.Organisms.append(Plant(self.window))

    def close(self):
        '''
        Closes the simulation.
        '''
        self.interface.close()

    def update(self):
        '''
        Updates everything in the simulation every time
        the function is called.
        '''
        while self.keepRunning:
            self.livingOrganisms = 0
            
            #show the evolution data
            plotValues(self.Organisms)

            for Organism in self.Organisms:
                self.livingOrganisms += 1
                Organism.update(self.Organisms, self.window)

            if self.livingOrganisms <= 1:
                self.keepRunning = False
                break

            time.sleep(tickTime)

def main():
    '''
    Calls the simulation. If loop = True then loops the simulation
    otherwise the simulation only runs once.
    '''
    if loop:
        for i in range(100):
            simulation = naturalSelectionSim()
            simulation.runSim()
            simulation.close()
            time.sleep(1)
    else:
        simulation = naturalSelectionSim()
        simulation.runSim()
        simulation.close()

if __name__ == '__main__':
    main()
