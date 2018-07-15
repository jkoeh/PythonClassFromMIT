# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 08:33:32 2018

@author: Johann
"""
import pylab
import random
class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def move(self, deltax, deltay):
        return Location(self.x + deltax, self.y + deltay)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x -ox
        yDist = self.y -oy
        return (xDist**2 + yDist **2)**0.5
    def __str__(self):
        return '<{}, {}>'.format(self.x, self.y)
class Field(object): 
    def __init__(self):
        self.drunks = {}
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc
    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not found')
        else:
            return self.drunks[drunk]
    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()        
        currentLocation = self.drunks[drunk]
        self.drunks[drunk] = currentLocation.move(xDist, yDist)
class Drunk(object):
    def __init__(self, name=None):
        self.name = name
    def __str__(self):
        return 'This drunk is named {}.'.format(self.name)
class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices=[(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)
    
class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices=[(0.0, 0.9),(0.0, -1.1), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)
    
def walk(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):        
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))

def simWalks(numSteps, numTrials, dClass):
    Homer = dClass(numSteps)
    origin = Location(0,0)
    distances = []
    for t in range(numTrials):
        f=Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances
def drunkTest(walkLengths, numTrials, dClass):
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print('{} random walk of {} steps'.format(dClass.__name__, numSteps))
        print('Mean = ', round(sum(distances)/len(distances), 4))
        print('Max =', max(distances), 'Min = ', min(distances))
        
class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles
    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles)-1:
            self.index = 0
        else: 
            self.index +=1
        return result
class OddField(Field):
    def __init__(self, numHoles = 1000, 
                 xRange = 100, yRange = 100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x,y)]= newLoc
    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if(x,y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x,y)]
def simDrunk(numTrials, dClass, walkLengths):
    meanDistances=[]
    for numSteps in walkLengths:
        print('Starting simulation of', numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials)/len(trials)
        meanDistances.append(mean)
    return meanDistances
def simAll(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulattion of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle, label=dClass.__name__)
    pylab.title('Mean Distance from Origin (' + str(numTrials) + 'trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance fromq Origin')
    pylab.legend(loc = 'best')
def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0,0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals))/len(xVals)
        meanY = sum(abs(yVals))/len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, label = dClass.__name__ +\
                   'mean abs dist =<{}, {}>'.format(str(meanX), str(meanY)))
    pylab.title('Location at End of Walks ({}) steps'.format(str(numSteps)))
    pylab.ylim(-1000, 1000)
    pylab.xlim(-1000, 1000)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Orign')
    pylab.legend(loc = 'uppder left')
def traceWalk(fieldKinds, numSteps):
    styleChoice = styleIterator(('b+', 'r^', 'ko'))
    for fClass in fieldKinds:
        d = UsualDrunk()
        f = fClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle, label = fClass.__name__)
    pylab.title('Spots Visited on walks')
    pylab.xlable('Step East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc = 'best')
    