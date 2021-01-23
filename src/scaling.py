from abc import ABC
import userDefinedMethods


class Request(ABC):
    def __init__(self, timestamp, size, details):
        self.timestamp = int(timestamp)
        self.reqSize = float(size)
        self.details = details

    def getTimestamp(self):
        return self.timestamp

    def getSize(self):
        return self.reqSize

    def getRelativeSize(self):
        return userDefinedMethods.reqSizeEstimation(self.reqSize, self.details)

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setReqSize(self, size):
        self.reqSize = size

    def getOutputString(self):
        return str(self.timestamp) + "," + str(self.reqSize) + "," + str(self.details)


class TraceReader(ABC):

    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, "r")
        self.i = 0
        return

    def readNextReq(self):
        nextLine = self.file.readline().strip()
        if nextLine == None:
            return nextLine
        line = str.split(nextLine, ",")
        if len(line) < 2:
            return None
        r = Request(line[0], line[1], line[2])
        return r

    def finish(self):
        self.file.close()


class TraceWriter(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, "w")
        return

    def writeNextReq(self, req):
        self.file.write(req.getOutputString() + "\n")

    def finish(self):
        self.file.close()
