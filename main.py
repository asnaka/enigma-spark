from colorama import Fore, Back, init
import PySimpleGUI as sg
import json
from search import searchItems
from random import randint

init(autoreset=True)

with open('settings.json', 'r+', encoding='utf-8') as settingsFile:
    settings = json.load(settingsFile)

try:
    with open('data/characters/exampleCharacter.json', 'r+', encoding='utf-8') as characterFile:
        characterFileJSON = json.load(characterFile)
except FileNotFoundError:
    print("FileNotFoundError: Opening exampleCharacter")
    with open('data/characters/exampleCharacter.json', 'r+', encoding='utf-8') as characterFile:
        characterFileJSON = json.load(characterFile)

class playerClass:
    def __init__(self, name, level, subclass):
        self.mainclass = name
        self.classlevel = level
        self.subclass =  subclass
        with open(f'data/classes/{self.mainclass}.json', 'r+', encoding='utf-8') as self.classFile:
            classdata = json.load(self.classFile)
        self.savingThrows = classdata['proficiencies']['savingThrows']

class playerSubclass:
    def __init__(self, name, level):
        pass

class character:
    def __init__(self, characterData=characterFileJSON):
        self.name = characterData['name']
        self.level = characterData['level']
        self.mainclass = playerClass(characterData['class'][0], characterData['class'][1], characterData['class'][2])
        self.race = characterData['race']
        self.description = characterData['description']
        self.hair = self.description['hair']
        self.eyes = self.description['eyes']
        self.skin = self.description['skin']
        self.height = self.description['height']
        self.weight = self.description['weight']
        self.sex = self.description['sex']
        self.age = self.description['age']
        self.traits = self.description['personalityTraits']
        self.ideals = self.description['ideals']
        self.bonds = self.description['bonds']
        self.flaws = self.description['flaws']
        self.background = self.description['background']
        self.inventory = characterData['inventory']
        self.scores = characterData['scores']
        self.skillProficiencies = characterData['proficiencies']['skills']
        self.languages = characterData['proficiencies']['languages']
        self.calculateBasics()

    def printInventory(self, value=None):
        inventory = []
        for item in self.inventory:
            itemdict = searchItems(item)
            inventory.append(itemdict)

        for index, i in enumerate(inventory):
            if value is not None and i is not None:
                try:
                    if value == 'cost':
                        coins = ["gold", "silver", "copper"]
                        cost = i[value]
                        pointer = 0
                        while int(cost) != cost:
                            cost *= 10
                            pointer += 1
                        print('{}[{}] {}{} {}{} {}'.format(Fore.MAGENTA, i['name'], Fore.GREEN, value, Fore.CYAN, int(cost), coins[pointer]))
                    else:
                        print('{}[{}] {}{} {}{}'.format(Fore.MAGENTA, i['name'], Fore.GREEN, value, Fore.CYAN, i[value]))
                except KeyError:
                    print("{}{}KeyError: Value {}[{}] {}not found in item {}[{}]{}.".format(Back.BLACK, Fore.RED,
                                                                                            Fore.CYAN, value, Fore.RED,
                                                                                            Fore.MAGENTA, i['name'],
                                                                                            Fore.RED))
            elif i is None:
                print("{}{}TypeError: Item {}[{}] {}not found.".format(Back.BLACK, Fore.RED, Fore.MAGENTA, self.inventory[index],
                                                                       Fore.RED))
            else:
                print(i)

    def printStats(self):
        print(f'''
SCORES:
STR: {self.str}, {self.strMod}
CON: {self.con}, {self.conMod}
DEX: {self.dex}, {self.dexMod}
INT: {self.int}, {self.intMod}
WIS: {self.wis}, {self.wisMod}
CHA: {self.cha}, {self.chaMod}
SKILLS:
acro: {self.acroMod}
anim: {self.animMod}
arca: {self.arcaMod}
athl: {self.athlMod}
dece: {self.deceMod}
hist: {self.histMod}
insi: {self.insiMod}
inti: {self.intiMod}
inve: {self.inveMod}
medi: {self.mediMod}
natu: {self.natuMod}
perc: {self.percMod}
perf: {self.perfMod}
pers: {self.persMod}
reli: {self.reliMod}
slei: {self.sleiMod}
stea: {self.steaMod}
surv: {self.survMod}
SAVING THROWS
STR: {self.strSave}
CON: {self.conSave}
DEX: {self.dexSave}
INT: {self.intSave}
WIS: {self.wisSave}
CHA: {self.chaSave}
            ''')

    def calculateBasics(self):
        # Proficiency modifier
        self.profMod = int(2 + (self.level-1)/4)
        # Ability scores
        self.str = self.scores['str']
        self.strMod = (self.str - 10) // 2
        self.con = self.scores['con']
        self.conMod = (self.con - 10) // 2
        self.dex = self.scores['dex']
        self.dexMod = (self.dex - 10) // 2
        self.int = self.scores['int']
        self.intMod = (self.int - 10) // 2
        self.wis = self.scores['wis']
        self.wisMod = (self.wis - 10) // 2
        self.cha = self.scores['cha']
        self.chaMod = (self.cha - 10) // 2

        # Skill proficiencies
        self.acroMod = self.dexMod + (self.profMod * self.skillProficiencies['acro'])
        self.animMod = self.wisMod + (self.profMod * self.skillProficiencies['anim'])
        self.arcaMod = self.intMod + (self.profMod * self.skillProficiencies['arca'])
        self.athlMod = self.strMod + (self.profMod * self.skillProficiencies['athl'])
        self.deceMod = self.chaMod + (self.profMod * self.skillProficiencies['dece'])
        self.histMod = self.intMod + (self.profMod * self.skillProficiencies['hist'])
        self.insiMod = self.wisMod + (self.profMod * self.skillProficiencies['insi'])
        self.intiMod = self.chaMod + (self.profMod * self.skillProficiencies['inti'])
        self.inveMod = self.intMod + (self.profMod * self.skillProficiencies['inve'])
        self.mediMod = self.wisMod + (self.profMod * self.skillProficiencies['medi'])
        self.natuMod = self.intMod + (self.profMod * self.skillProficiencies['natu'])
        self.percMod = self.wisMod + (self.profMod * self.skillProficiencies['perc'])
        self.perfMod = self.chaMod + (self.profMod * self.skillProficiencies['perf'])
        self.persMod = self.chaMod + (self.profMod * self.skillProficiencies['pers'])
        self.reliMod = self.intMod + (self.profMod * self.skillProficiencies['reli'])
        self.sleiMod = self.dexMod + (self.profMod * self.skillProficiencies['slei'])
        self.steaMod = self.dexMod + (self.profMod * self.skillProficiencies['stea'])
        self.survMod = self.wisMod + (self.profMod * self.skillProficiencies['surv'])
        # Saving throws
        self.strSave = self.strMod + (self.profMod * self.mainclass.savingThrows['str'])
        self.conSave = self.conMod + (self.profMod * self.mainclass.savingThrows['con'])
        self.dexSave = self.dexMod + (self.profMod * self.mainclass.savingThrows['dex'])
        self.intSave = self.intMod + (self.profMod * self.mainclass.savingThrows['int'])
        self.wisSave = self.wisMod + (self.profMod * self.mainclass.savingThrows['wis'])
        self.chaSave = self.chaMod + (self.profMod * self.mainclass.savingThrows['cha'])


class frame:
    def __init__(self, character):
        self.character = character
        self.window = sg.Window("Test", self.createLayout(), finalize=True)

    def createLayout(self):
        testText = self.createScoreBlock(self.character.str, self.character.strMod)
        testButton = sg.B("testB")
        layout = [
            [testText],
            [testButton]
        ]
        return layout

    @staticmethod
    def createScoreBlock(score, mod):
        block = sg.Column([
            [sg.T(f'[{score}]', font=('Arial', 15))],
            [sg.T(f'+{mod}' if str(mod)[0] != '-' else f'{mod}', font=('Arial', 12))]
            ], element_justification='center')
        return block

character = character()
windowFrame = frame(character)
window = windowFrame.window

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'testB':
        character.printStats()

window.close()
characterFile.close()
character.mainclass.classFile.close()
