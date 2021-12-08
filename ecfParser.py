# Imports
# none

# .escf parser/opener
class subjob:
    def __init__(self, fileName, subclass):
        self.filePath = "subclasses/" + fileName
        self.escfFile = open(self.filePath, 'r')
        for line in self.escfFile:
            t = line.split(',')
            if t[0] == subclass:
                self.subjob = t
                self.subjob.remove('\n')


# .ecf parser/opener
class job:
    def __init__(self, jobType):
        self.jobType = jobType
        self.ecfFile = open("classes/" + jobType.lower() + ".ecf", 'r')
        for line in self.ecfFile:
            t = line.split(',')
            if t[0] == "subclassFile":
                self.subclassFile = t[1]


if __name__ == "__main__":
    _class = job("FiGhter")
    print(_class.subclassFile)
