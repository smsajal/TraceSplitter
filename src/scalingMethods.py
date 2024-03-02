import scaling
import math  # for ceil function
import numpy.random as np  # for random number generation np.random.rand(1)
import random  # for shuffling array random.shuffle()
from queue import PriorityQueue
from random import seed
from random import randint
import argparse


def checkFactor(factor):
    if (factor <= 0) or (factor > 1):
        print("Invalid input")
        exit()


def timeSpanScaling(inputFilename, factor):
    checkFactor(factor)

    scale = 1/factor

    outputFilename = str.split(inputFilename, ".")[0] + "tspan.txt"

    reader = scaling.TraceReader(inputFilename)
    writer = scaling.TraceWriter(outputFilename)

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
    writer = scaling.TraceWriter(outputFilename)

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

    numberOfnServers = int(math.floor(1.0 / factor))
    numberOfxServers = 1
    if (factor-numberOfnServers)<=0:
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
    for i in range(0, numberOfnServers):
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

    numberOfnServers = int(math.floor(1.0 / factor))
    numberOfxServers = 1
    if (factor-numberOfnServers)<=0:
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
    for i in range(0, numberOfnServers):
        outputFilename = str.split(inputFilename, ".")[
            0] + str(i + 1) + "randrr.txt"
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

    numberOfnServers = int(math.floor(1.0 / factor))
    numberOfxServers = 1
    if (factor-numberOfnServers)<=0:
        numberOfxServers = 0

    p_x = 0
    p_resampling = 0
    p_n = 1

    if numberOfxServers == 1:
        p_x = 1 - factor * numberOfnServers
        p_n = factor
        p_resampling = (p_n - p_x)/(1-p_x)

    writer = [0] * numberOfnServers

    '''serverPriority queue has the tuple (totalReqSizeInThisQueue, queueIndex). It keeps track of amount of work in each queue and puts queue with least work left in the front'''
    serverPriority = PriorityQueue()
    for i in range(0, (numberOfnServers + numberOfxServers)):
        serverPriority.put((0, i))

    reader = scaling.TraceReader(inputFilename)
    for i in range(0, numberOfnServers):
        outputFilename = str.split(inputFilename, ".")[
            0] + str(i+1) + "lwl.txt"
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


def avgRateScaling(inputFilename, factor, bucketSize):
    checkFactor(factor)
    nanoSecInSec = 1000000000

    # in nanoseconds, same unit as timestamp in file
    bucketSize = bucketSize * nanoSecInSec

    outputFilename = str.split(inputFilename, ".")[0] + "avgRateScaling.txt"

    reader = scaling.TraceReader(inputFilename)
    writer = scaling.TraceWriter(outputFilename)

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

        for i in range(0, numberOfNewReq):
            timestamps.append(randint(timeStamp1, timeStamp2))
        timestamps = sorted(timestamps)

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


def scalingFactorLimit(arg):
    max = 1
    min = 0
    """ Type function for argparse - a float within some predefined bounds """
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f <= min or f > max:
        raise argparse.ArgumentTypeError(
            "Argument must be <= " + str(max) + "and > " + str(min))
    return f


def main():

    my_parser = argparse.ArgumentParser(
        allow_abbrev=False, description='downscale the trace using TraceSplitter')
    my_parser.add_argument("--traceFile", action='store',
                           type=str, required=True, metavar='path of the trace to be scaled')
    my_parser.add_argument("--downscalingScheme",
                           action='store', type=str, default="LWL", choices=["avgRateScaling", "tspan", "randomSampling", "RRR", "RR", "LWL"], metavar='downscaling technique to be used, default is LWL')
    my_parser.add_argument("--bucket", action='store', type=float, default=1.0,
                           metavar='duration of time bucket size (seconds) for AvgRateScaling, default is 1.0')
    my_parser.add_argument("--scalingFactor", action='store',
                           type=scalingFactorLimit, default=0.5, metavar='scaling factor for downscaling, 0 < scalingFactor <= 1, default is 0.5')

    args = my_parser.parse_args()

    traceFile = args.traceFile
    downscalingScheme = args.downscalingScheme
    bucketSize = args.bucket
    scalingFactor = args.scalingFactor
    if downscalingScheme == "avgRateScaling":
        avgRateScaling(traceFile, scalingFactor, bucketSize)
    elif downscalingScheme == "tspan":
        timeSpanScaling(traceFile, scalingFactor)
    elif downscalingScheme == "randomSampling":
        randomSampling(traceFile, scalingFactor)
    elif downscalingScheme == "RRR":
        randomRoundRobinSamplingAll(traceFile, scalingFactor)
    elif downscalingScheme == "RR":
        roundRobinSamplingAll(traceFile, scalingFactor)
    elif downscalingScheme == "LWL":
        leastWorkLeftAll(traceFile, scalingFactor)


if __name__ == "__main__":
    main()
