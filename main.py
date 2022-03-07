from colorama import Fore, Back, init
import PySimpleGUI as sg
import json, pyautogui
from search import searchItems
from random import randint

init(autoreset=True)
WIDTH, HEIGHT = pyautogui.size()

with open('settings.json', 'r+', encoding='utf-8') as settingsFile:
    settings = json.load(settingsFile)

try:
    with open('data/characters/exampleCharacter.json', 'r+', encoding='utf-8') as characterFile:
        characterFileJSON = json.load(characterFile)
except FileNotFoundError:
    print("FileNotFoundError: Opening exampleCharacter")
    with open('data/characters/exampleCharacter.json', 'r+', encoding='utf-8') as characterFile:
        characterFileJSON = json.load(characterFile)

class PlayerClass:
    def __init__(self, name, level, subclass):
        self.name = name
        self.classlevel = level
        self.subclass =  PlayerSubclass(subclass,self.classlevel)
        with open(f'data/classes/{self.name}.json', 'r+', encoding='utf-8') as self.classFile:
            classdata = json.load(self.classFile)
        self.savingThrows = classdata['proficiencies']['savingThrows']

class PlayerSubclass:
    def __init__(self, name, level):
        pass

class Character:
    def __init__(self, characterData=characterFileJSON):
        self.name = characterData['name']
        self.level = characterData['level']
        self.mainclass = PlayerClass(characterData['class'][0], characterData['class'][1], characterData['class'][2])
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

    def calculateBasics(self):
        # Proficiency modifier
        self.profMod = int(2 + (self.level-1)/4)
        # Ability scores
        self.str = self.scores['str']
        self.strMod = (self.str - 10) // 2
        self.dex = self.scores['dex']
        self.dexMod = (self.dex - 10) // 2
        self.con = self.scores['con']
        self.conMod = (self.con - 10) // 2
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
        self.dexSave = self.dexMod + (self.profMod * self.mainclass.savingThrows['dex'])
        self.conSave = self.conMod + (self.profMod * self.mainclass.savingThrows['con'])
        self.intSave = self.intMod + (self.profMod * self.mainclass.savingThrows['int'])
        self.wisSave = self.wisMod + (self.profMod * self.mainclass.savingThrows['wis'])
        self.chaSave = self.chaMod + (self.profMod * self.mainclass.savingThrows['cha'])

class CharacterViewer:
    def __init__(self, character):
        self.character = character
        self.window = sg.Window(f'{self.character.name} | {self.character.mainclass.name.capitalize()}, {self.character.mainclass.classlevel}', self.createLayout(), finalize=True, resizable=True,margins=(0,0))

    def createLayout(self):
        self.scoreCol = self.createScoreCol()
        self.basicInfo = self.createBasicInfo()
        self.skillBlock = self.createSkillBlock()
        self.buttons = self.createButtons()
        self.descBar = self.createDescriptorBar()
        self.leftCol = sg.Column([
                self.scoreCol,[sg.HorizontalSeparator()],
                self.basicInfo,[sg.HorizontalSeparator()],
                self.skillBlock], element_justification='center', scrollable=True, vertical_scroll_only=True, expand_y=True)
        self.midCol = sg.Column([
            self.buttons, [sg.HorizontalSeparator()]], vertical_alignment='top')
        layout = [
            [sg.HorizontalSeparator()],
            self.descBar,
            [sg.HorizontalSeparator()],
            [sg.Column([[self.leftCol, self.midCol]], expand_y=True)]
        ]
        return layout

    def createScoreCol(self):
        strBlock = self.createScoreBlock(self.character.str, self.character.strMod, 'STR')
        dexBlock = self.createScoreBlock(self.character.dex, self.character.dexMod, 'DEX')
        conBlock = self.createScoreBlock(self.character.con, self.character.conMod, 'CON')
        intBlock = self.createScoreBlock(self.character.int, self.character.intMod, 'INT')
        wisBlock = self.createScoreBlock(self.character.wis, self.character.wisMod, 'WIS')
        chaBlock = self.createScoreBlock(self.character.cha, self.character.chaMod, 'CHA')
        return [sg.Column([[strBlock,dexBlock,conBlock,intBlock,wisBlock,chaBlock]])]

    def createBasicInfo(self):
        leftBlock = sg.Column([
            [sg.T('Proficiency Bonus', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'+{self.character.profMod}', font=('Arial', 13, 'bold'), pad=(3,0))],
            [sg.T('Passive Perception', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{10+self.character.percMod}', font=('Arial', 13, 'bold'), pad=(3,0))],
            [sg.T('Speed', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{30} ft.', font=('Arial', 13, 'bold'), pad=(3,0))],
            ], element_justification='center', pad=(3,0))

        rightBlock = sg.Column([
            [sg.T('Armour Class', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{self.character.percMod}', font=('Arial', 13, 'bold'), pad=(3,0))],
            [sg.T('Max Hit Points', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{self.character.percMod}', font=('Arial', 13, 'bold'), pad=(3,0))],
            [sg.T('Darkvision', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{0} ft.', font=('Arial', 13, 'bold'), pad=(3,0))],
            ], element_justification='center', pad=(3,0))

        return [leftBlock,sg.T(size=(3,0)), rightBlock]

    def createSkillBlock(self):
        profs = sg.Column([
            [sg.T('[P]' if self.character.skillProficiencies[i] == 1 else '[E]' if self.character.skillProficiencies[i] == 2 else '[N]')] for i in self.character.skillProficiencies.keys()
            ])
        names = sg.Column([
            [sg.T('Acrobatics')],
            [sg.T('Animal Handling')],
            [sg.T('Arcana')],
            [sg.T('Athletics')],
            [sg.T('Deception')],
            [sg.T('History')],
            [sg.T('Insight')],
            [sg.T('Intimidation')],
            [sg.T('Investigation')],
            [sg.T('Medicine')],
            [sg.T('Nature')],
            [sg.T('Perception')],
            [sg.T('Performance')],
            [sg.T('Persuasion')],
            [sg.T('Religion')],
            [sg.T('Sleight of Hand')],
            [sg.T('Stealth')],
            [sg.T('Survival')]])

        mods = sg.Column([
            [sg.T(f'+{self.character.acroMod}' if self.character.acroMod > 0 else f'{self.character.acroMod}' if self.character.acroMod < 0 else f' {self.character.acroMod}')],
            [sg.T(f'+{self.character.animMod}' if self.character.animMod > 0 else f'{self.character.animMod}' if self.character.animMod < 0 else f' {self.character.animMod}')],
            [sg.T(f'+{self.character.arcaMod}' if self.character.arcaMod > 0 else f'{self.character.arcaMod}' if self.character.arcaMod < 0 else f' {self.character.arcaMod}')],
            [sg.T(f'+{self.character.athlMod}' if self.character.athlMod > 0 else f'{self.character.athlMod}' if self.character.athlMod < 0 else f' {self.character.athlMod}')],
            [sg.T(f'+{self.character.deceMod}' if self.character.deceMod > 0 else f'{self.character.deceMod}' if self.character.deceMod < 0 else f' {self.character.deceMod}')],
            [sg.T(f'+{self.character.histMod}' if self.character.histMod > 0 else f'{self.character.histMod}' if self.character.histMod < 0 else f' {self.character.histMod}')],
            [sg.T(f'+{self.character.insiMod}' if self.character.insiMod > 0 else f'{self.character.insiMod}' if self.character.insiMod < 0 else f' {self.character.insiMod}')],
            [sg.T(f'+{self.character.intiMod}' if self.character.intiMod > 0 else f'{self.character.intiMod}' if self.character.intiMod < 0 else f' {self.character.intiMod}')],
            [sg.T(f'+{self.character.inveMod}' if self.character.inveMod > 0 else f'{self.character.inveMod}' if self.character.inveMod < 0 else f' {self.character.inveMod}')],
            [sg.T(f'+{self.character.mediMod}' if self.character.mediMod > 0 else f'{self.character.mediMod}' if self.character.mediMod < 0 else f' {self.character.mediMod}')],
            [sg.T(f'+{self.character.natuMod}' if self.character.natuMod > 0 else f'{self.character.natuMod}' if self.character.natuMod < 0 else f' {self.character.natuMod}')],
            [sg.T(f'+{self.character.percMod}' if self.character.percMod > 0 else f'{self.character.percMod}' if self.character.percMod < 0 else f' {self.character.percMod}')],
            [sg.T(f'+{self.character.perfMod}' if self.character.perfMod > 0 else f'{self.character.perfMod}' if self.character.perfMod < 0 else f' {self.character.perfMod}')],
            [sg.T(f'+{self.character.persMod}' if self.character.persMod > 0 else f'{self.character.persMod}' if self.character.persMod < 0 else f' {self.character.persMod}')],
            [sg.T(f'+{self.character.reliMod}' if self.character.reliMod > 0 else f'{self.character.reliMod}' if self.character.reliMod < 0 else f' {self.character.reliMod}')],
            [sg.T(f'+{self.character.sleiMod}' if self.character.sleiMod > 0 else f'{self.character.sleiMod}' if self.character.sleiMod < 0 else f' {self.character.sleiMod}')],
            [sg.T(f'+{self.character.steaMod}' if self.character.steaMod > 0 else f'{self.character.steaMod}' if self.character.steaMod < 0 else f' {self.character.steaMod}')],
            [sg.T(f'+{self.character.survMod}' if self.character.survMod > 0 else f'{self.character.survMod}' if self.character.survMod < 0 else f' {self.character.survMod}')]], 
            element_justification='center', 
            pad=(3,0))

        block = sg.Column([
            [sg.T('Skills', font=('Arial', 11, 'bold'))], [sg.HorizontalSeparator()],[profs, names, mods]], element_justification='center')
        return [block]

    # WHY DOES THIS NOT WORK
    # def createSavingBlock(self):
    #     block = sg.Column([[sg.T('Strength')]])
    #     return block

    def createButtons(self):
        buttons = sg.Column([
            [sg.B('Combat'),sg.B('Proficiencies'),sg.B('Spells'),sg.B('Features'),sg.B('Equipment')]
            ])
        return [buttons]

    def createDescriptorBar(self):
        col1 = [sg.Column([[sg.T('Name:', font=('Arial', 10, 'bold'), size=(5,1)), sg.T(f'{self.character.name}')],[sg.T('Class:', font=('Arial', 10, 'bold'), size=(5,1)), sg.T(f'{self.character.mainclass.name.capitalize()}')]])]
        return col1

    @staticmethod
    def createScoreBlock(score, mod, name):
        block = sg.Column([
            [sg.T(f'{name}', font=('Arial', 12, 'bold'), pad=(3,0))],
            [sg.T(f'[{score}]', font=('Arial', 15), pad=(3,0))],
            [sg.T(f'+{mod}' if str(mod)[0] != '-' else f'{mod}', font=('Arial', 12), pad=(3,0))]
            ], element_justification='center', pad=(3,0))
        return block

character = Character()
characterWindow = CharacterViewer(character)
window = characterWindow.window

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'testB':
        character.printStats()

window.close()
characterFile.close()
character.mainclass.classFile.close()
