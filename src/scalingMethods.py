import scaling
from math import *  #for ceil function
import numpy.random as np   #for random number generation np.random.rand(1)
import random  # for shuffling array random.shuffle()
from queue import PriorityQueue
from random import seed
from random import randint



def checkFactor(factor):
    if (factor <= 0) or (factor > 1):
        print("Invalid input")
        exit()

def timeSpanScaling(inputFilename, factor):
    checkFactor(factor)

    scale = 1/factor

    ''' assumption about filename format???'''
    outputFilename = str.split(inputFilename, ".")[0] + "tspan.txt"

    reader = scaling.TraceReader(inputFilename)
    writer = scaling.TraceWriter(outputFilename) # only one writer in random

    nextReq = reader.readNextReq()
    while nextReq:
        ts = int(nextReq.timestamp)
        nextReq.timestamp = str(int(ts * scale))

        writer.writeNextReq(nextReq)
        nextReq = reader.readNextReq()

    '''Close files'''
    reader.finish()
    writer.finish()

    return

def randomSampling(inputFilename, factor):
    checkFactor(factor)

    probability = factor
    outputFilename = str.split(inputFilename, ".")[0] + "rand" + ".txt"

    reader = scaling.TraceReader(inputFilename)
    writer = scaling.TraceWriter(outputFilename) # only one writer in random

    nextReq = reader.readNextReq()
    while nextReq:
        if np.rand(1) <= probability:
            writer.writeNextReq(nextReq)
        nextReq = reader.readNextReq()


    '''Close files'''
    reader.finish()
    writer.finish()

    return


def roundRobinSamplingAll(inputFilename, factor):
    checkFactor(factor)

    numberOfnServers = int(1 // factor)
    numberOfxServers = 1
    if ceil(1 / factor) == 1 // factor:
        numberOfxServers = 0

    p_x = 0
    p_resampling = 0

    if numberOfxServers == 1:
        p_x = 1 - factor * numberOfnServers
        p_n = factor
        p_resampling = (p_n - p_x) / (1-p_x)


    writer = [0] * numberOfnServers
    currentServerIdx = 0

    reader = scaling.TraceReader(inputFilename)
    for i in range(0, numberOfnServers):       # range does [start, end)
        outputFilename = str.split(inputFilename, ".")[0] + str(i+1) + "rr.txt"
        writer[i] = scaling.TraceWriter(outputFilename)
    if numberOfxServers == 1:
        outputFilename = str.split(inputFilename, ".")[0] + "Xrr.txt"
        writerX = scaling.TraceWriter(outputFilename)

    nextReq = reader.readNextReq()
    while nextReq:
        if random.random() < p_x:
            writerX.writeNextReq(nextReq)
        else:
            if random.random() < p_resampling:
                writerX.writeNextReq(nextReq)
            writer[currentServerIdx].writeNextReq(nextReq)
            currentServerIdx = (currentServerIdx + 1) % numberOfnServers
        nextReq = reader.readNextReq()

    '''Close files'''
    reader.finish()
    for i in range(0, numberOfnServers):
        writer[i].finish()
    if numberOfxServers == 1:
        writerX.finish()
    return


def randomRoundRobinSamplingAll(inputFilename, factor):
    checkFactor(factor)

    numberOfnServers = int(1 // factor)
    numberOfxServers = 1
    if ceil(1 / factor) == 1 // factor:
        numberOfxServers = 0

    p_x = 0
    p_resampling = 0
    p_n = 1

    if numberOfxServers == 1:
        p_x = 1 - factor * numberOfnServers
        p_n = factor
        p_resampling = (p_n - p_x) / (1-p_x)

    writer = [0] * numberOfnServers


    serverPriority = []
    for i in range(0, numberOfnServers):
        serverPriority.append(i)
    random.shuffle(serverPriority)
    currentServerIdx = 0

    reader = scaling.TraceReader(inputFilename)
    for i in range(0, numberOfnServers):  # range does [start, end)
        outputFilename = str.split(inputFilename, ".")[0] + str(i + 1) + "randrr.txt"
        writer[i] = scaling.TraceWriter(outputFilename)
    if numberOfxServers == 1:
        outputFilename = str.split(inputFilename, ".")[0] + "Xrandrr.txt"
        writerX = scaling.TraceWriter(outputFilename)

    nextReq = reader.readNextReq()
    while nextReq:
        if random.random() < p_x:
            writerX.writeNextReq(nextReq)
        else:
            if random.random() < p_resampling:
                writerX.writeNextReq(nextReq)
            writer[serverPriority[currentServerIdx]].writeNextReq(nextReq)
            currentServerIdx = (currentServerIdx + 1) % numberOfnServers
            if currentServerIdx == 0:
                random.shuffle(serverPriority)
        nextReq = reader.readNextReq()

    '''Close files'''
    reader.finish()
    for i in range(0, numberOfnServers):
        writer[i].finish()
    if numberOfxServers == 1:
        writerX.finish()

    return


def leastWorkLeftAll(inputFilename, factor):
    checkFactor(factor)

    numberOfnServers = int(1 // factor)
    numberOfxServers = 1
    if ceil(1 / factor) == 1 // factor:
        numberOfxServers = 0

    p_x = 0
    p_resampling = 0
    p_n = 1

    if numberOfxServers == 1:
        p_x = 1 - factor * numberOfnServers
        p_n = factor
        p_resampling = (p_n - p_x)/(1-p_x)

    writer = [0] * numberOfnServers


    serverPriority = PriorityQueue()            #serverPriority queue has the tuple (totalReqSizeInThisQueue, queueIndex). It keeps track of amount of work in each queue and puts queue with least work left in the front
    for i in range(0, (numberOfnServers + numberOfxServers)):
        serverPriority.put((0, i))


    reader = scaling.TraceReader(inputFilename)
    for i in range(0, numberOfnServers):
        outputFilename = str.split(inputFilename, ".")[0] + str(i+1) + "lwl.txt"
        writer[i] = scaling.TraceWriter(outputFilename)
    if numberOfxServers == 1:
        outputFilename = str.split(inputFilename, ".")[0] + "Xlwl.txt"
        writerX = scaling.TraceWriter(outputFilename)

    nextReq = reader.readNextReq()
    while nextReq:
        smallestq = serverPriority.get()
        if smallestq is None:
            print("Queue empty")
        if smallestq[1] == numberOfnServers:
            writerX.writeNextReq(nextReq)
            newSize = smallestq[0] + (1 / p_x * nextReq.getRelativeSize())
        else:
            writer[smallestq[1]].writeNextReq(nextReq)
            newSize = smallestq[0] + (1 / p_n * nextReq.getRelativeSize())
            if random.random() < p_resampling:
                writerX.writeNextReq(nextReq)
        serverPriority.put((newSize, smallestq[1]))
        nextReq = reader.readNextReq()

    '''Close files'''
    reader.finish()
    for i in range(0, numberOfnServers):
        writer[i].finish()
    if numberOfxServers == 1:
        writerX.finish()

    return

def modelBasedSimple(inputFilename, factor, bucketSize):
    checkFactor(factor)
    nanoSecInSec = 1000000000

    bucketSize = bucketSize * nanoSecInSec # in nanoseconds, same unit as timestamp in file

    outputFilename = str.split(inputFilename, ".")[0] + "model.txt"

    reader = scaling.TraceReader(inputFilename)
    writer = scaling.TraceWriter(outputFilename)  # only one writer in model Based

    nextReq = reader.readNextReq()

    '''Update timestamp and bucket initially'''
    timeStamp1 = float(nextReq.timestamp)
    timeStamp2 = timeStamp1 + bucketSize

    while nextReq:
        requestList = []
        while nextReq:
            requestList.append(nextReq)
            nextReq = reader.readNextReq()
            if nextReq is None:
                break
            if float(nextReq.timestamp) > timeStamp2:
                break

        numberOfNewReq = round(len(requestList)*factor)
        timestamps = []
        seed(1)
        for i in range(0, numberOfNewReq):
            timestamps.append(randint(timeStamp1, timeStamp2))
        timestamps = sorted(timestamps)

        seed(1)
        for i in range(0, numberOfNewReq):
            randReqIdx = randint(0, len(requestList)-1)
            newReq = requestList[randReqIdx]
            newReq.setTimestamp(str(timestamps[i]))
            writer.writeNextReq(newReq)

        '''Update timestamp and bucket'''
        timeStamp1 = timeStamp2
        timeStamp2 = timeStamp1 + bucketSize

    '''Close files'''
    reader.finish()
    writer.finish()


    return

def main():
    inputFile = "/Users/rxh655/OneDrive - The Pennsylvania State University/Research/Code/ScalingTrace/ScalingTrace/traceScaling/input/generic_trace_file.txt"
    scalingFactor = 1
    bucket = 20

    modelBasedSimple(inputFile, scalingFactor, bucketSize=bucket)
    timeSpanScaling(inputFile, scalingFactor)
    randomSampling(inputFile, scalingFactor)
    randomRoundRobinSamplingAll(inputFile, scalingFactor)
    roundRobinSamplingAll(inputFile, scalingFactor)
    leastWorkLeftAll(inputFile, scalingFactor)


if __name__ == "__main__":
    main()
