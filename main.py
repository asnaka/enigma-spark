from colorama import Fore, Back, init
import PySimpleGUI as sg
import json, pyautogui
import roller
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
        self.hitdie = classdata['hitDie']

class PlayerSubclass:
    def __init__(self, name, level):
        pass

class Character:
    def __init__(self, characterData=characterFileJSON):
        self.name = characterData['name']
        self.level = characterData['level']
        self.mainclass = PlayerClass(characterData['class'][0], characterData['class'][1], characterData['class'][2])
        self.hitDice = f'{self.mainclass.classlevel}d{self.mainclass.hitdie}'
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
        self.equipped = characterData['equipped']
        self.calculateBasics()

    def printInventory(self, value=None):
        inventory = []
        for item in self.inventory:
            itemdict = searchItems(item)
            inventory.append(itemdict)

        for index, item in enumerate(inventory):
            if value is not None and item is not None:
                try:
                    if value == 'cost':
                        coins = ["gold", "silver", "copper"]
                        cost = item[value]
                        pointer = 0
                        while int(cost) != cost:
                            cost *= 10
                            pointer += 1
                        print('{}[{}] {}{} {}{} {}'.format(Fore.MAGENTA, item['name'], Fore.GREEN, value, Fore.CYAN, int(cost), coins[pointer]))
                    else:
                        print('{}[{}] {}{} {}{}'.format(Fore.MAGENTA, item['name'], Fore.GREEN, value, Fore.CYAN, item[value]))
                except KeyError:
                    print("{}{}KeyError: Value {}[{}] {}not found in item {}[{}]{}.".format(Back.BLACK, Fore.RED,
                                                                                            Fore.CYAN, value, Fore.RED,
                                                                                            Fore.MAGENTA, item['name'],
                                                                                            Fore.RED))
            elif item is None:
                print("{}{}TypeError: Item {}[{}] {}not found.".format(Back.BLACK, Fore.RED, Fore.MAGENTA, self.inventory[index],
                                                                       Fore.RED))
            else:
                print(item)

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
        # Main left column
        self.scoreCol = self.createScoreCol()
        self.basicInfo = self.createBasicInfo()
        self.skillBlock = self.createSkillBlock()
        self.buttons = self.createButtons()
        self.descBar = self.createDescriptorBar()
        self.savesBlock = self.createSavingBlock()
        self.skillsaves = [sg.Column([[self.skillBlock,sg.VerticalSeparator(),self.savesBlock]])]
        self.leftCol = sg.Column([
                self.scoreCol,[sg.HorizontalSeparator()],
                self.basicInfo,[sg.HorizontalSeparator()],
                self.skillsaves], element_justification='center', scrollable=True, vertical_scroll_only=True, expand_y=True)
        
        # Combat block
        self.combatBlock = self.createCombatBlock()

        # Assemble middle/right column
        self.midCol = sg.Column([
            self.buttons,[self.combatBlock]], vertical_alignment='top')

        layout = [
            [sg.HorizontalSeparator()],
            self.descBar,
            [sg.HorizontalSeparator()],
            [sg.Column([[self.leftCol, self.midCol]], expand_y=True)]
        ]
        return layout

    def createCombatBlock(self):
        # Basic combat info
        self.combatArmourBlock = sg.Column([
            [sg.T('Armour Class', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{self.character.percMod}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatHPBlock = sg.Column([
            [sg.T('Max Hit Points', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{self.character.percMod}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatSpeedBlock = sg.Column([
            [sg.T('Speed', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{30} ft.', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatInitiativeBlock = sg.Column([
            [sg.T('Initiative', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'+{self.character.dexMod}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatCriticalBlock = sg.Column([
            [sg.T('Critical Hits', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{20}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatHitDice = sg.Column([
            [sg.T('Hit Dice', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{self.character.hitDice}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        self.combatAttackNumber = sg.Column([
            [sg.T('Number of Attacks', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.T(f'{2}', font=('Arial', 13, 'bold'), pad=(3,0))]], element_justification='center')
        
        self.combatInfo = sg.Column([[sg.Column([[self.combatArmourBlock],[self.combatCriticalBlock]], element_justification='center'),sg.Column([[self.combatHPBlock], [self.combatHitDice]], element_justification='center'), sg.Column([[self.combatSpeedBlock, self.combatInitiativeBlock], [self.combatAttackNumber]], element_justification='center')]])
        
        # Equipped items
        self.combatWornArmour = sg.Column([
            [sg.T('Worn Armour', font=('Arial', 9, 'bold'), pad=(3,0))],
            [sg.T(f"{self.character.equipped['armour']}")]], element_justification='center')
        self.combatWieldedShield = sg.Column([
            [sg.T('Wielded Shield', font=('Arial', 9, 'bold'), pad=(3,0))],
            [sg.T(f"{self.character.equipped['shield']}")]], element_justification='center')
        self.combatMainHand = sg.Column([
            [sg.T('Main Hand Weapon', font=('Arial', 9, 'bold'), pad=(3,0))],
            [sg.T(f"{self.character.equipped['mainHand']}")]], element_justification='center')
        self.combatOffHand = sg.Column([
            [sg.T('Off Hand Weapon', font=('Arial', 9, 'bold'), pad=(3,0))],
            [sg.T(f"{self.character.equipped['offHand']}")]], element_justification='center', visible=False)
        self.combatItems = sg.Column([
            [sg.T('Equipped Items', font=('Arial', 10, 'bold'), pad=(3,0))],
            [sg.HorizontalSeparator()],
            [self.combatWornArmour, self.combatWieldedShield],
            [self.combatMainHand, self.combatOffHand]])
        
        return sg.Column([
            [sg.HorizontalSeparator()],
            [self.combatInfo],
            [sg.HorizontalSeparator()],
            [self.combatItems]])

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
            [sg.T(f'+{self.character.acroMod}' if self.character.acroMod > 0 else f'{self.character.acroMod}' if self.character.acroMod < 0 else f' {self.character.acroMod}', right_click_menu = ['acroMod', ['acro | Advantage','acro | Flat','acro | Disadvantage']])],
            [sg.T(f'+{self.character.animMod}' if self.character.animMod > 0 else f'{self.character.animMod}' if self.character.animMod < 0 else f' {self.character.animMod}', right_click_menu = ['animMod', ['anim | Advantage','anim | Flat','anim | Disadvantage']])],
            [sg.T(f'+{self.character.arcaMod}' if self.character.arcaMod > 0 else f'{self.character.arcaMod}' if self.character.arcaMod < 0 else f' {self.character.arcaMod}', right_click_menu = ['arcaMod', ['arca | Advantage','arca | Flat','arca | Disadvantage']])],
            [sg.T(f'+{self.character.athlMod}' if self.character.athlMod > 0 else f'{self.character.athlMod}' if self.character.athlMod < 0 else f' {self.character.athlMod}', right_click_menu = ['athlMod', ['athl | Advantage','athl | Flat','athl | Disadvantage']])],
            [sg.T(f'+{self.character.deceMod}' if self.character.deceMod > 0 else f'{self.character.deceMod}' if self.character.deceMod < 0 else f' {self.character.deceMod}', right_click_menu = ['deceMod', ['dece | Advantage','dece | Flat','dece | Disadvantage']])],
            [sg.T(f'+{self.character.histMod}' if self.character.histMod > 0 else f'{self.character.histMod}' if self.character.histMod < 0 else f' {self.character.histMod}', right_click_menu = ['histMod', ['hist | Advantage','hist | Flat','hist | Disadvantage']])],
            [sg.T(f'+{self.character.insiMod}' if self.character.insiMod > 0 else f'{self.character.insiMod}' if self.character.insiMod < 0 else f' {self.character.insiMod}', right_click_menu = ['insiMod', ['insi | Advantage','insi | Flat','insi | Disadvantage']])],
            [sg.T(f'+{self.character.intiMod}' if self.character.intiMod > 0 else f'{self.character.intiMod}' if self.character.intiMod < 0 else f' {self.character.intiMod}', right_click_menu = ['intiMod', ['inti | Advantage','inti | Flat','inti | Disadvantage']])],
            [sg.T(f'+{self.character.inveMod}' if self.character.inveMod > 0 else f'{self.character.inveMod}' if self.character.inveMod < 0 else f' {self.character.inveMod}', right_click_menu = ['inveMod', ['inve | Advantage','inve | Flat','inve | Disadvantage']])],
            [sg.T(f'+{self.character.mediMod}' if self.character.mediMod > 0 else f'{self.character.mediMod}' if self.character.mediMod < 0 else f' {self.character.mediMod}', right_click_menu = ['mediMod', ['medi | Advantage','medi | Flat','medi | Disadvantage']])],
            [sg.T(f'+{self.character.natuMod}' if self.character.natuMod > 0 else f'{self.character.natuMod}' if self.character.natuMod < 0 else f' {self.character.natuMod}', right_click_menu = ['natuMod', ['natu | Advantage','natu | Flat','natu | Disadvantage']])],
            [sg.T(f'+{self.character.percMod}' if self.character.percMod > 0 else f'{self.character.percMod}' if self.character.percMod < 0 else f' {self.character.percMod}', right_click_menu = ['percMod', ['perc | Advantage','perc | Flat','perc | Disadvantage']])],
            [sg.T(f'+{self.character.perfMod}' if self.character.perfMod > 0 else f'{self.character.perfMod}' if self.character.perfMod < 0 else f' {self.character.perfMod}', right_click_menu = ['perfMod', ['perf | Advantage','perf | Flat','perf | Disadvantage']])],
            [sg.T(f'+{self.character.persMod}' if self.character.persMod > 0 else f'{self.character.persMod}' if self.character.persMod < 0 else f' {self.character.persMod}', right_click_menu = ['persMod', ['pers | Advantage','pers | Flat','pers | Disadvantage']])],
            [sg.T(f'+{self.character.reliMod}' if self.character.reliMod > 0 else f'{self.character.reliMod}' if self.character.reliMod < 0 else f' {self.character.reliMod}', right_click_menu = ['reliMod', ['reli | Advantage','reli | Flat','reli | Disadvantage']])],
            [sg.T(f'+{self.character.sleiMod}' if self.character.sleiMod > 0 else f'{self.character.sleiMod}' if self.character.sleiMod < 0 else f' {self.character.sleiMod}', right_click_menu = ['sleiMod', ['slei | Advantage','slei | Flat','slei | Disadvantage']])],
            [sg.T(f'+{self.character.steaMod}' if self.character.steaMod > 0 else f'{self.character.steaMod}' if self.character.steaMod < 0 else f' {self.character.steaMod}', right_click_menu = ['steaMod', ['stea | Advantage','stea | Flat','stea | Disadvantage']])],
            [sg.T(f'+{self.character.survMod}' if self.character.survMod > 0 else f'{self.character.survMod}' if self.character.survMod < 0 else f' {self.character.survMod}', right_click_menu = ['survMod', ['surv | Advantage','surv | Flat','surv | Disadvantage']])]], 
            element_justification='center', 
            pad=(3,0))

        block = sg.Column([
            [sg.T('Skills', font=('Arial', 11, 'bold'))], [sg.HorizontalSeparator()],[profs, names, mods]], element_justification='center')
        return block

    def createSavingBlock(self):
        names = sg.Column([
            [sg.T('Strength')],
            [sg.T('Dexterity')],
            [sg.T('Constitution')],
            [sg.T('Intelligence')],
            [sg.T('Wisdom')],
            [sg.T('Charisma')]])
        mods = sg.Column([
            [sg.T(f'+{self.character.strSave}' if self.character.strSave > 0 else f'{self.character.strSave}')],
            [sg.T(f'+{self.character.dexSave}' if self.character.dexSave > 0 else f'{self.character.dexSave}')],
            [sg.T(f'+{self.character.conSave}' if self.character.conSave > 0 else f'{self.character.conSave}')],
            [sg.T(f'+{self.character.intSave}' if self.character.intSave > 0 else f'{self.character.intSave}')],
            [sg.T(f'+{self.character.wisSave}' if self.character.wisSave > 0 else f'{self.character.wisSave}')],
            [sg.T(f'+{self.character.chaSave}' if self.character.chaSave > 0 else f'{self.character.chaSave}')]
            ])
        block = sg.Column([
            [sg.T('Saving Throws', font=('Arial', 11, 'bold'))],
            [sg.HorizontalSeparator()],
            [names,mods]], vertical_alignment='top')
        return block

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
    if 'Flat' in event:
        sg.popup(roller.rollFlat(event, character), title='')
    if 'Advantage' in event:
        sg.popup(roller.rollAdv(event, character), title='')
    if 'Disadvantage' in event:
        sg.popup(roller.rollDis(event, character), title='')


window.close()
characterFile.close()
character.mainclass.classFile.close()
