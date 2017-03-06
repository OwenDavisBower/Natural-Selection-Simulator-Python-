'''
2016 CS-167 Final Project: 
natural_selection.py

This program runs a simulation on natural selection in a
graphical interface. Watch as the organisms move about
targeting prey (or plants) and attempting to avoid predators.
The largest fitter organisms will survive.

by Owen Davis-Bower
'''

import random
from graphics import *

# Simulation configuration
windowSize = 100
tickTime = .5
gameTicks = 200
eventLog = False
speedFactor = 1
loop = False

class organism:
	'''
	This class represents organism objects that all 
	have different traits and allows them to move about
	and consume each other every game tick.
	'''
	
	def __init__(self, window, x, y, size, speed, organismType):
		'''
		Initializes the organism by assigning it's traits
		and drawing the organism on the screen.

		Parameters:
			window: The graphical window to draw on.
			x, y: The x and y starting coordinates of the organism.
			size: The size of the organism. This effects the graphical
			      size of the organism as well as the strength of the
			      organism in combat.
			speed: The maximum speed at which an organism can move each
			       game tick.
			organismType: The type of an organism (Plant, omnivore, 
						  herbivore, or carnivore)

		Return Value: none
		'''
		self.pos = [x, y]
		self.size = size
		self.speed = speed
		self.type = organismType
		self.prey = self.preyList()
		self.hunger = 50

		self.organismGraphic = Circle(Point(self.pos[0], self.pos[1]), self.size)

		# assign a color based upon organism type
		if self.type == 'omnivore':
			self.organismGraphic.setFill('orange')
		elif self.type == 'herbivore':
			self.organismGraphic.setFill('blue')
		elif self.type == 'carnivore':
			self.organismGraphic.setFill('red')
		elif self.type ==  'plant':
			self.organismGraphic.setFill(color_rgb(10, 117, 31))
		self.organismGraphic.draw(window)

	def update(self, organismsList, window):
		'''
		Updates the organism's position and hunger every
		simulation tick.

		Parameters:
			organismsList: the list of organisms (including
						   the organism itself)
			window: The graphical window which the organism
					resides on.

		Return Value: none
		'''
		self.closestTarget = self.nearestTarget(organismsList)

		# move the organism
		if self.isPrey(self.closestTarget):
			self.moveToTarget(self.closestTarget)
		else:
			self.moveRandom()

		# keep the organisms from leaving the screen
		self.stayInScreen()

		self.draw(window)

		# checks for collisions and responds accordingly
		self.checkCollisions(organismsList)

		self.hunger += -0.5
		if self.hunger <= 0:
			if eventLog:
				print('Self starved')
			self.die(organismsList)

	def isPrey(self, target):
		'''
		Given a target organism, checks if the target is prey
		for the checking organism.

		Parameters:
			target: The target organism that is being checked.

		Return Value:
			True if the target organism is prey for the self;
			else False.
		'''
		if target.getType() == 'plant' and 'plant' in self.prey:
			return True
		elif target.getType() in self.prey and target.getSize() < self.size:
			return True
		return False

	def preyList(self):
		'''
		Taking in the self organism's type, returns a list of
		prey types. For example an herbivore will only return
		'plant'.

		Return Value:
			A tuple containing all of the acceptable prey types.
		'''
		if self.type == 'omnivore':
			return ('plant', 'omnivore', 'herbivore', 'carnivore')
		elif self.type == 'herbivore':
			return ('plant')
		elif self.type == 'carnivore':
			return ('omnivore', 'herbivore', 'carnivore')

	def getPos(self):
		'''
		Returns the position of the given organism as a list
		containing two points [x, y].
		'''
		return self.pos

	def getSize(self):
		'''
		Returns the size of the given organism as a float value.
		'''
		return self.size

	def getType(self):
		'''
		Returns the type of the given organism as a string value.
		'''
		return self.type

	def die(self, organismsList):
		'''
		"Kills" the given organism by undrawing it and then
		removing it from the list of organisms.

		Parameters:
			organismsList: The list to remove the given
						   organism from.

		Return Value: none
		'''
		self.organismGraphic.undraw()
		organismsList.remove(self)

	def distanceFromTarget(self, target):
		'''
		Calculates and returns the distance between the given
		organism and the target organism.

		Parameters:
			target: A target organism.

		Return Value: The distance between the given organism
					  and the target organism.
		'''
		return (abs(target.getPos()[0] - self.pos[0]) + abs(target.getPos()[1] - self.pos[1]))

	def nearestTarget(self, organismsList):
		'''
		Searches through the list of other organisms and
		returns the organism object of the nearest organism.

		Parameters:
			organismsList: The list of living organisms.

		Return Value: The organism object of the nearest
					  organism.
		'''
		self.selfIndex = organismsList.index(self)
		self.otherOrganisms = list(organismsList)
		self.otherOrganisms.pop(self.selfIndex)
		self.closestTarget = self.otherOrganisms[0]
		for organism in self.otherOrganisms[1:]:
			if self.distanceFromTarget(organism) < self.distanceFromTarget(self.closestTarget):
				self.closestTarget = organism
		return self.closestTarget

	def moveToTarget(self, target):
		'''
		Moves the given organism towards the target organism.

		Parameters:
			target: A target organism.

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
		Moves the given organism randomly in 2D space.
		'''
		self.velocity = (random.uniform(-self.speed, self.speed) * speedFactor, random.uniform(-self.speed, self.speed) * speedFactor)
		self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

	def stayInScreen(self):
		'''
		Prevents the organisms from leaving the screen.
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
		Creates a graphical object for the organism based
		upon it's size and type and then draws it onto the
		graphic window.

		Parameters:
			window: A graphical window.

		Return Value: none
		'''
		if self.type != 'plant':
			if self.organismGraphic:
				self.organismGraphic.undraw()
			self.organismGraphic = Circle(Point(self.pos[0], self.pos[1]), self.size)

			# assign a color based upon organism type
			if self.type == 'omnivore':
				self.organismGraphic.setFill('orange')
			elif self.type == 'herbivore':
				self.organismGraphic.setFill('blue')
			elif self.type == 'carnivore':
				self.organismGraphic.setFill('red')
			elif self.type ==  'plant':
				self.organismGraphic.setFill(color_rgb(10, 117, 31))
			self.organismGraphic.draw(window)

	def checkCollision(self, collidingOrganism):
		'''
		Checks if the given organism is colliding with the
		"collidingOrganism".

		Parameters:
			collidingOrganism: The organism to be tested against.

		Return Value:
			True if the given organism is colliding with the
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

	def checkCollisions(self, organismsList):
		'''
		Checks if the organism is colliding with any organisms
		and reacts appropriately by killing one of the
		organisms if it is prey of the other.

		Parameters:
			organismsList: The list of organisms.

		Return Value: none
		'''
		for organism in organismsList:
			if organism != self: # prevents organism from checking if it's colliding with itself
				if self.checkCollision(organism):
					if self.isPrey(organism):
						if eventLog:
							print('Self killed organism')
							self.hunger += 8
						organism.die(organismsList)
					elif organism.isPrey(self):
						if eventLog:
							print('Organism killed self')
						organism.hunger += 8
						self.die(organismsList)

class simInterface:

	def __init__(self):
		'''
		Initializes the simulation window.
		'''
		# initialize window
		self.win = GraphWin('Natural Selection Simulation', 700, 700)
		# transform coordinates
		self.win.setCoords(-100, -150, 100, 100)

		self.lowerInterface = self.createLowerInterface()
		self.lowerInterface.draw(self.win)

		self.organismCircle = None

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

		# destroy all remaining organisms
		for organism in self.organisms:
			organism.die(self.organisms)

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
		self.informativeText_1 = Text(Point(0, -105), 'Click anywhere inside the habitat to spawn a new organism.')
		self.informativeText_1.setSize(20)
		self.informativeText_1.draw(self.window)

		self.plantExample = Circle(Point(-90, -120), 3)
		self.plantExample.setFill(color_rgb(10, 117, 31))
		self.plantExample.draw(self.window)
		self.plantTitle = Text(Point(-75, -120), '= Plant')
		self.plantTitle.setSize(20)
		self.plantTitle.draw(self.window)

		self.herbivoreExample = Circle(Point(-90, -130), 3)
		self.herbivoreExample.setFill('blue')
		self.herbivoreExample.draw(self.window)
		self.herbivoreTitle = Text(Point(-69, -130), '= Herbivore')
		self.herbivoreTitle.setSize(20)
		self.herbivoreTitle.draw(self.window)

		self.omnivoreExample = Circle(Point(-90, -140), 3)
		self.omnivoreExample.setFill('orange')
		self.omnivoreExample.draw(self.window)
		self.omnivoreTitle = Text(Point(-69, -140), '= Omnivore')
		self.omnivoreTitle.setSize(20)
		self.omnivoreTitle.draw(self.window)

	def randomOrganism(self, organismType, position = None):
		'''
		Generates a random organism.

		Parameters:
			organismType: The type of the new organism (Plant,
						  herbivore, omnivore, carnivore)
			position (optional): The starting position of the
								 organism. Otherwise the start
								 position is randomly generated.

		Return Value: A randomly generated organism object.
		'''
		if position == None:
			x = random.uniform(-(windowSize * .9), windowSize * .9)
			y = random.uniform(-(windowSize * .9), windowSize * .9)
		else:
			x, y = position
		size = random.uniform(1, 7)
		speed = random.uniform(5, 10)
		return organism(self.window, x, y, size, speed, organismType)

	def spawnOrganisms(self):
		'''
		Spawns in randomly generated organisms by adding them
		to a list of organisms.
		'''
		self.organisms = []
		for i in range(7):
			self.organisms.append(self.randomOrganism('omnivore'))
		for i in range(5):
			self.organisms.append(self.randomOrganism('herbivore'))
		# BUG: Carnivores are not fully implemented yet.
		# for i in range(5):
		# 	self.organisms.append(self.randomOrganism('carnivore'))
		for i in range(15):
			self.organisms.append(self.randomOrganism('plant'))

	def spawnOrganismFromInput(self):
		'''
		Spawns in randomly generated organisms at the location
		of a mouse click. (Only works if the mouse click is in
		the simulation window.)
		'''
		self.mousePos = self.window.checkMouse()
		if self.mousePos != None:
			if abs(self.mousePos.getX()) < windowSize and abs(self.mousePos.getY()) < windowSize:
				self.organisms.append(self.randomOrganism(random.choice(('omnivore', 'herbivore', 'plant')), (self.mousePos.getX(), self.mousePos.getY())))

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

			self.spawnOrganismFromInput()

			for organism in self.organisms:
				if organism.getType() != 'plant':
					self.livingOrganisms += 1
					organism.update(self.organisms, self.window)

			# generates new plants to sustain the organisms.
			if random.randrange(10) > 2:
				self.organisms.append(self.randomOrganism('plant'))

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
