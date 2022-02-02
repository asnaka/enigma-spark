# Imports
# none

# .escf parser/opener
class subjob:
    def __init__(self, fileName, subclass):
        self.filePath = "subclasses/" + fileName
        self.escfFile = open(self.filePath, 'r')
        self.spellcaster = False
        self.spellList = None
        for line in self.escfFile:
            t = line.split(',')
            if t[0] == subclass:
                self.subjob = t
                self.subjob.remove('\n')
                print('subj', self.subjob)
                for i in self.subjob:
                    features = i.split('-')
                    print('feat', features)
                    for j in features:
                        subitem = j.split('/')
                        print('sub', subitem)
                        for k in subitem:
                            if k == "Spellcasting":
                                self.spellcaster = True
                                self.spellList = subitem[subitem.index(k)+1] + ".esl"


# .ecf parser/opener
class job:
    def __init__(self, jobType, subjobType):
        self.jobType = jobType
        self.subjobType = subjobType
        self.ecfFile = open("classes/" + jobType.lower() + ".ecf", 'r')
        for line in self.ecfFile:
            t = line.split(',')
            if t[0] == "subclassFile":
                self.subclassFile = t[1]
                self.subjob = subjob(self.subclassFile, self.subjobType)


if __name__ == "__main__":
    _class = job("Fighter", "Eldritch Knight")
    print(_class.subjob.spellList)
