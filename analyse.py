import numpy as np
import matplotlib.pyplot as plt

figure = None
plot = None

def plotValues(Organisms):
    '''This function plots the interesting values of the organisms
    '''
    global figure
    global plot
    speeds = []
    sizes = []
    
    if figure != None:
        
        for Organism in Organisms:
            speeds.append(Organism.speed)
            sizes.append(Organism.size)
        
        plot.set_ydata(sizes)
        plot.set_xdata(speeds)
        

    else:
        
        plt.ion()
        figure = plt.figure()
        
        for Organism in Organisms:
            speeds.append(Organism.speed)
            sizes.append(Organism.size)
            
        plot, = figure.add_subplot(1, 1, 1).plot(speeds, sizes, 'b*')
        plt.title("Living organisms attributes")
        plt.xlabel("Speed")
        plt.ylabel("Size")