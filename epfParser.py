# Imports
# none

# Function to calculate ability score modifiers
def modCalc(score):
    t = score - 10
    modifier = t // 2
    return modifier


# Function to calculate modifiers for skills
def skillModCalc(abiScr, prof, pBon):
    eBon = pBon * 2
    if prof == 'n':
        mod = abiScr
    elif prof == 'p':
        mod = abiScr + pBon
    elif prof == 'e':
        mod = abiScr + eBon
    return mod


# .epf parser/opener
class character:

    def __init__(self, epfFile):
        # Open given .epf file
        self.epfFile = open("characters/" + epfFile, 'r')
        # Look at each line in the file
        for line in self.epfFile:
            t = line.split(',')
            # Check what information we are being given from the .epf file
            # Get basic information about the character
            if t[0] == "Basic":
                self.basic = t
                self.basic.remove('\n')
                self.name = self.basic[1]
                self.race = self.basic[2]
                self.level = int(self.basic[3])
                self.subrace = self.basic[4]
                if self.level in (1, 2, 3, 4):
                    self.profBon = 2
                elif self.level in (5, 6, 7, 8):
                    self.profBon = 3
                elif self.level in (9, 10, 11, 12):
                    self.profBon = 4
                elif self.level in (13, 14, 15, 16):
                    self.profBon = 5
                elif self.level in (17, 18, 19, 20):
                    self.profBon = 6
                self.expBon = 2 * self.profBon
            # Get information about the character's class(es)
            elif t[0] == "Class":
                self.jobInf = t
                self.jobInf.remove('\n')
                if self.jobInf[1] == 'True':
                    job1 = self.jobInf[2] + ', ' + self.jobInf[3]
                    job2 = self.jobInf[4] + ', ' + self.jobInf[5]
                    self.job = job1 + '/' + job2
                else:
                    self.job = self.jobInf[2] + ', ' + self.jobInf[3]
            # Get the character's ability scores and calculate the ability modifiers
            elif t[0] == "Scores":
                self.abiScores = t
                self.abiScores.remove('\n')
                self.strNum = int(self.abiScores[1])
                self.dexNum = int(self.abiScores[2])
                self.conNum = int(self.abiScores[3])
                self.inteNum = int(self.abiScores[4])
                self.wisNum = int(self.abiScores[5])
                self.chaNum = int(self.abiScores[6])
                self.strMod = modCalc(self.strNum)
                self.dexMod = modCalc(self.dexNum)
                self.conMod = modCalc(self.conNum)
                self.inteMod = modCalc(self.inteNum)
                self.wisMod = modCalc(self.wisNum)
                self.chaMod = modCalc(self.chaNum)
            # Calculate skill modifiers
            elif t[0] == "SklProficiencies":
                self.profs = t
                self.profs.remove('\n')
                self.athMod = skillModCalc(self.strMod, self.profs[1], self.profBon)
                self.acrMod = skillModCalc(self.dexMod, self.profs[2], self.profBon)
                self.sohMod = skillModCalc(self.dexMod, self.profs[3], self.profBon)
                self.steMod = skillModCalc(self.dexMod, self.profs[4], self.profBon)
                self.arcMod = skillModCalc(self.inteMod, self.profs[5], self.profBon)
                self.hisMod = skillModCalc(self.inteMod, self.profs[6], self.profBon)
                self.invMod = skillModCalc(self.inteMod, self.profs[7], self.profBon)
                self.natMod = skillModCalc(self.inteMod, self.profs[8], self.profBon)
                self.relMod = skillModCalc(self.inteMod, self.profs[9], self.profBon)
                self.aniMod = skillModCalc(self.wisMod, self.profs[10], self.profBon)
                self.insMod = skillModCalc(self.wisMod, self.profs[11], self.profBon)
                self.medMod = skillModCalc(self.wisMod, self.profs[12], self.profBon)
                self.percMod = skillModCalc(self.wisMod, self.profs[13], self.profBon)
                self.surMod = skillModCalc(self.wisMod, self.profs[14], self.profBon)
                self.decMod = skillModCalc(self.chaMod, self.profs[15], self.profBon)
                self.intiMod = skillModCalc(self.chaMod, self.profs[16], self.profBon)
                self.perfMod = skillModCalc(self.chaMod, self.profs[17], self.profBon)
                self.persMod = skillModCalc(self.chaMod, self.profs[18], self.profBon)
            # Get other, more in-depth, information about the character
            elif t[0] == "Info":
                self.info = t
                self.info.remove('\n')

