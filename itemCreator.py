import PySimpleGUI as sg
import sqlite3 as sql

class WeaponCreator:
    def __init__(self):
        sg.SetOptions(background_color='#333333',
       text_element_background_color='#333333',
       element_background_color='#333333',
       scrollbar_color='#BBD8B3',
       input_elements_background_color='#504B4B',
       progress_meter_color = ('green', 'blue'),
       button_color=('#1F1F1F','#7D5BA6'))
        self.db = sql.connect('data/items.db')
        self.cur = self.db.cursor()
        self.table_contents = []

        for row in self.cur.execute('SELECT * FROM weapons ORDER BY name'):
            self.table_contents.append(list(row))

        die_types = [100,20,12,10,8,6,4]
        damage_types = ["Acid", "Bludgeoning", "Cold", "Fire", "Force", "Lightning", "Necrotic", "Piercing", "Poison", "Psychic", "Radiant", "Slashing", "Thunder"]
        spin_range = [i for i in range(1,11)]
        self.range_area = sg.Column([[sg.T("Range")],[sg.T("Min:"),sg.In(60,size=(12,1),key='RANGE_MIN'),sg.T("Max:"),sg.In(300,size=(12,1),key='RANGE_MAX')]],visible=True)
        self.range_visible = True
        self.name_input = sg.In(size=(12,1),key='ITEM_NAME')
        self.cost_input = sg.In(size=(12,1),key='ITEM_COST')
        self.ranged_check = sg.Checkbox("Ranged",key='RANGED_ITEM',change_submits=True,enable_events=True,default=True)
        self.magic_check = sg.Checkbox("Magic",key='MAGIC_ITEM',change_submits=True,enable_events=True)
        self.die_type_input = sg.Combo(die_types,readonly=True,default_value=8,key='DIE_TYPE')
        self.die_amount_input = sg.Spin(spin_range,key='DIE_AMOUNT')
        self.damage_type_input = sg.Combo(damage_types,readonly=True,default_value="Slashing",key='DAMAGE_TYPE')
        self.weapon_type_input = sg.Combo(("Simple","Martial"),readonly=True,default_value="Simple",key='ITEM_TYPE')
        input_area = [
        [sg.Column([[sg.T("Name")],[self.name_input]]),sg.Column([[sg.T("Cost")],[self.cost_input]]),sg.Column([[self.ranged_check],[self.magic_check]])],
        [sg.Column([[sg.T("Damage")],[self.die_amount_input,sg.T("d"),self.die_type_input,self.damage_type_input]]),sg.Column([[sg.T("Type")],[self.weapon_type_input]])],
        [self.range_area]
        ]
        self.buttons = sg.Column([
            [sg.B('Create',size=(10,1))],
            [sg.B('Reset',size=(10,1))],
            [sg.B('Update',size=(10,1))],
            [sg.HorizontalSeparator()],
            [sg.B('Refresh',size=(10,1)),sg.B('Load',size=(10,1))],
            [sg.B('Save',size=(10,1))]
            ])
        self.weaponTable = sg.Table(self.table_contents,headings=['Name','Cost','Damage','Ranged','Type','Magic','Max Range','Min Range'],key='DATA_TABLE')
        self.layout = [
        [sg.Frame("Input Area", input_area),self.buttons],
        [self.weaponTable]
        ]
        self.window = sg.Window('Item Editor', self.layout, finalize=True, resizable=True,margins=(0,0))

    def updateTable(self):
        self.table_contents = []

        for row in self.cur.execute('SELECT * FROM weapons ORDER BY name'):
            self.table_contents.append(list(row))

        self.weaponTable.update(values=self.table_contents)

    def resetAll(self):
        self.name_input.update(value="")
        self.cost_input.update(value="")
        self.ranged_check.update(value=1)
        self.range_visible = True
        self.range_area.update(visible=True)
        self.magic_check.update(value=0)
        self.die_type_input.update(value=8)
        self.die_amount_input.update(value=1)
        self.damage_type_input.update(value='Slashing')
        self.weapon_type_input.update(value='Simple')

weaponCreator = WeaponCreator()
window = weaponCreator.window

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: break
    if event == 'RANGED_ITEM':
        weaponCreator.range_visible = not weaponCreator.range_visible
        weaponCreator.range_area.update(visible=weaponCreator.range_visible)
    if event == 'Create':
        try: cost = float(values['ITEM_COST']) 
        except: cost = ""
        if values['ITEM_NAME'] != "" and cost != "":
            weaponCreator.cur.execute('''
                SELECT name FROM weapons;
                ''')
            rows = weaponCreator.cur.fetchall()
            current_items = []
            for row in rows:
                current_items.append(row[0])
            if values["ITEM_NAME"] in current_items:
                sg.popup(f'Item {values["ITEM_NAME"]} already exists!')
            else:
                # damage = f"{values["DIE_AMOUNT"]}d{values["DIE_TYPE"]} {values["DAMAGE_TYPE"]}"
                weaponCreator.cur.execute('''
                    INSERT INTO weapons('name','cost','damage','ranged','type','magic','maxRange','minRange') VALUES(?,?,?,?,?,?,?,?);
                    ''', (values["ITEM_NAME"],values["ITEM_COST"],f'{values["DIE_AMOUNT"]}d{values["DIE_TYPE"]} {values["DAMAGE_TYPE"]}',values["RANGED_ITEM"],values["ITEM_TYPE"],values["MAGIC_ITEM"],values["RANGE_MAX"] if values["RANGED_ITEM"] else 0,values["RANGE_MIN"] if values["RANGED_ITEM"] else 0))
                # print(f'''
                #     INSERT INTO items VALUES({values["ITEM_NAME"]},{values["ITEM_COST"]},{damage},{values["RANGED_ITEM"]},{values["ITEM_TYPE"]},{values["MAGIC_ITEM"]},{values["RANGE_MAX"] if values["RANGED_ITEM"] else 0},{values["RANGE_MIN"] if values["RANGED_ITEM"] else 0})
                #     ''')
                weaponCreator.db.commit()
                weaponCreator.updateTable()
                sg.popup(f'Created new item {values["ITEM_NAME"]}')
                weaponCreator.resetAll()
        else:
            sg.PopupError(f'Error creating new item {values["ITEM_NAME"]}')
    if event == 'Reset':
        weaponCreator.resetAll()
    if event == 'Refresh':
        weaponCreator.updateTable()
        sg.popup("Table updated")
    if event == 'Save':
        weaponCreator.db.commit()
        sg.popup('Table saved')
    if event == 'Load':
        item_load = weaponCreator.table_contents[values['DATA_TABLE'][0]]
        weaponCreator.name_input.update(value=item_load[0])
        weaponCreator.cost_input.update(value=item_load[1])
        weaponCreator.ranged_check.update(value=item_load[3])
        weaponCreator.range_visible = True if item_load[3] == 1 else False
        weaponCreator.range_area.update(visible=weaponCreator.range_visible)
        weaponCreator.magic_check.update(value=item_load[5])
        weaponCreator.die_type_input.update(value=8) # DO
        weaponCreator.die_amount_input.update(value=1) # DO
        weaponCreator.damage_type_input.update(value='Slashing') # DO
        weaponCreator.weapon_type_input.update(value=item_load[4])


weaponCreator.db.close()
window.close()