# Imports
import PySimpleGUI as sg
from epfParser import character

character = character('testPlayer.epf')


def createLayout(c):
    def createGenericInfo():
        basic = sg.Column([
            [
                sg.Column([
                    [sg.T("Name:")],
                    [sg.T("Race:")],
                    [sg.T("Level:")],
                    [sg.T("Class:")]
                ]),
                sg.Column([
                    [sg.T(c.name)],
                    [sg.T(c.race + ', ' + c.subrace)],
                    [sg.T(c.level)],
                    [sg.T(c.job)]
                ])
            ]
        ])
        advanced = sg.Column([
            [
                sg.Column([
                    [sg.T("HP:")],
                    [sg.T("Proficiency Bonus:")],
                    [sg.T("Armor Class")],
                    [sg.T("Speed")]
                ]),
                sg.Column([
                    [sg.Spin(values=list(range(11)), initial_value=10, s=(3, 1)), sg.T("/10")],
                    [sg.T(c.profBon)],
                    [sg.T("13")],
                    [sg.T("30 f.t.")]
                ])
            ]
        ])
        generic = sg.Column([
            [basic, advanced]
        ])
        return generic

    def createAbilityScores():
        strScore = sg.Column([
            [sg.T(c.strNum, font=("Arial", 14))],
            [sg.T("STR")],
            [sg.T(c.strMod)]
        ], element_justification='c')
        dexScore = sg.Column([
            [sg.T(c.dexNum, font=("Arial", 14))],
            [sg.T("DEX")],
            [sg.T(c.dexMod)]
        ], element_justification='c')
        conScore = sg.Column([
            [sg.T(c.conNum, font=("Arial", 14))],
            [sg.T("CON")],
            [sg.T(c.conMod)]
        ], element_justification='c')
        inteScore = sg.Column([
            [sg.T(c.inteNum, font=("Arial", 14))],
            [sg.T("INT")],
            [sg.T(c.inteMod)]
        ], element_justification='c')
        wisScore = sg.Column([
            [sg.T(c.wisNum, font=("Arial", 14))],
            [sg.T("WIS")],
            [sg.T(c.wisMod)]
        ], element_justification='c')
        chaScore = sg.Column([
            [sg.T(c.chaNum, font=("Arial", 14))],
            [sg.T("CHA")],
            [sg.T(c.chaMod)]
        ], element_justification='c')
        scores = sg.Column([
            [strScore, dexScore, conScore, inteScore, wisScore, chaScore]
        ])
        return scores

    def createCombatInfo():
        initiative = sg.Column([
            [sg.T("\nInitiative")],
            [sg.T(c.dexMod, font=("Arial", 14))]
        ], element_justification='c')
        passPerception = sg.Column([
            [sg.T("Passive\nPerception", justification='c')],
            [sg.T(10 + c.percMod, font=("Arial", 14))]
        ], element_justification='c')
        numOfAttacks = sg.Column([
            [sg.T("Number of\nAttacks", justification='c')],
            [sg.T("1", font=("Arial", 14))]
        ], element_justification='c')
        hitDie = sg.Column([
            [sg.T("\nHit Die")],
            [sg.T("10d8", font=("Arial", 14))]
        ], element_justification='c')
        combatInfo = sg.Column([
            [initiative, passPerception, numOfAttacks, hitDie]
        ])
        return combatInfo

    def createSavingThrows():
        pass

    profColumn = sg.Column([
        [sg.T("")],
        [sg.T("[" + c.profs[1] + "]")],
        [sg.T("[" + c.profs[2] + "]")],
        [sg.T("[" + c.profs[3] + "]")],
        [sg.T("[" + c.profs[4] + "]")],
        [sg.T("[" + c.profs[5] + "]")],
        [sg.T("[" + c.profs[6] + "]")],
        [sg.T("[" + c.profs[7] + "]")],
        [sg.T("[" + c.profs[8] + "]")],
        [sg.T("[" + c.profs[9] + "]")],
        [sg.T("[" + c.profs[10] + "]")],
        [sg.T("[" + c.profs[11] + "]")],
        [sg.T("[" + c.profs[12] + "]")],
        [sg.T("[" + c.profs[13] + "]")],
        [sg.T("[" + c.profs[14] + "]")],
        [sg.T("[" + c.profs[15] + "]")],
        [sg.T("[" + c.profs[16] + "]")],
        [sg.T("[" + c.profs[17] + "]")],
        [sg.T("[" + c.profs[18] + "]")]
    ])
    skillColumn = sg.Column([
        [sg.T("Skill")],
        [sg.T("Athletics")],
        [sg.T("Acrobatics")],
        [sg.T("Sleight of Hand")],
        [sg.T("Stealth")],
        [sg.T("Arcana")],
        [sg.T("History")],
        [sg.T("Investigation")],
        [sg.T("Nature")],
        [sg.T("Religion")],
        [sg.T("Animal Handling")],
        [sg.T("Insight")],
        [sg.T("Medicine")],
        [sg.T("Perception")],
        [sg.T("Survival")],
        [sg.T("Deception")],
        [sg.T("Intimidation")],
        [sg.T("Performance")],
        [sg.T("Persuasion")]
    ])
    modColumn = sg.Column([
        [sg.T("Modifier")],
        [sg.T(c.athMod)],
        [sg.T(c.acrMod)],
        [sg.T(c.sohMod)],
        [sg.T(c.steMod)],
        [sg.T(c.arcMod)],
        [sg.T(c.hisMod)],
        [sg.T(c.invMod)],
        [sg.T(c.natMod)],
        [sg.T(c.relMod)],
        [sg.T(c.aniMod)],
        [sg.T(c.insMod)],
        [sg.T(c.medMod)],
        [sg.T(c.percMod)],
        [sg.T(c.surMod)],
        [sg.T(c.decMod)],
        [sg.T(c.intiMod)],
        [sg.T(c.perfMod)],
        [sg.T(c.persMod)]
    ], element_justification='c')
    skillProf = sg.Column([
        [profColumn, skillColumn, modColumn]
    ])
    asCombat = sg.Column([
        [createAbilityScores()],
        [createCombatInfo()]
    ])
    mainColumn = sg.Column([
        [createGenericInfo()],
        [asCombat]

    ])

    layout = [
        [skillProf, mainColumn]
    ]
    return layout


class frame:
    def __init__(self, windowName, layout):
        self.windowName = windowName
        self.layout = layout

    def createWindow(self):
        newWindow = sg.Window(self.windowName, self.layout)
        return newWindow


if __name__ == '__main__':
    window = frame("Character Viewer - {}".format(character.name), createLayout(character)).createWindow()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

window.close()
