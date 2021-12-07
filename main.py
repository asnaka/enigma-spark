# Imports
# import PySimpleGUI as sg

# .epf parser/opener
class character:
    def __init__(self, epfFile):
        self.epfFile = open("characters/" + epfFile, 'r')
        for line in self.epfFile:
            t = line.split(',')
            if t[0] == "Basic":
                self.basic = t
                self.basic.remove('\n')
                self.name = self.basic[1]
                self.race = self.basic[2]
                self.level = self.basic[3]
            elif t[0] == "Class":
                self.jobInf = t
                self.jobInf.remove('\n')
                if self.jobInf[1] == 'True':
                    job1 = self.jobInf[2] + ', ' + self.jobInf[3]
                    job2 = self.jobInf[4] + ', ' + self.jobInf[5]
                    self.job = job1 + '/' + job2
                else:
                    self.job = self.jobInf[2] + ', ' + self.jobInf[3]
            elif t[0] == "Info":
                self.info = t
                self.info.remove('\n')


if __name__ == '__main__':
    currentPlayer = character('nullLoad.epf')
    print(currentPlayer.level)
# Basic window test
#
# layout = [[sg.T("Text 1")],
#           [sg.T("Text 2"), sg.InputText()],
#           [sg.B("OK"), sg.B("CANCEL")]]
# window = sg.Window("Hello World", layout=layout)
#
# if __name__ == '__main__':
#     while True:
#         event, values = window.read()
#         if event == sg.WIN_CLOSED or event == "CANCEL":
#             break
#         print("You entered", values[0])
#
# window.close()
