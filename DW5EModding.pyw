import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil

# iso file, template, reference, mod file, backups folder, template storage, and offset
dw5e = ["DW5E.iso", "DW5E.5edata", "DW5E.5eref", ".dw5emod",
           "Backups_For_Mod_Disabling", "DW5E(unit)", "DW5E_Ico_Files"]

class TheCheck:
    @staticmethod
    def validate_numeric_input(new_value):
        return new_value == "" or (new_value.replace(".", "", 1).isdigit() and '.' not in new_value and float(new_value) >= 0)
def rem():
    fpath1 = os.path.join(dw5e[5], dw5e[1])
    if os.path.isfile(fpath1):
        os.remove(fpath1)
    fpath2 = os.path.join(dw5e[5], dw5e[2])
    if os.path.isfile(fpath2):
        os.remove(fpath2)

class MainEditor(TheCheck): # For the unit editor
    def __init__(self, root):
        self.root = root
        self.root.title("Dynasty Warriors 5 Empires Unit Editor")
        self.root.iconbitmap(os.path.join(dw5e[6], "icon2.ico"))
        self.root.minsize(800, 900)
        self.root.resizable(False, False)
        self.cred = tk.Label(self.root, text="Credit goes to Michael for documentation of DW5E unit data.")
        self.cred.place(x=0, y=800)
        self.editor_button = tk.Button(self.root, text="Mod Manager", command = self.open_mod_manager, width = 20, height = 5)
        self.editor_button.place(x=600, y=800)

        self.dw5e_path = os.path.join(dw5e[5], dw5e[1]) # template
        self.odw5e_path = os.path.join(dw5e[4], dw5e[1]) # backup file
        self.dw5e_ref = os.path.join(dw5e[5], dw5e[2]) # ref file
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.place(x=480, y=200)  # For displaying success or errors
        self.name = tk.IntVar() # Unit Name
        self.unknown1 = tk.IntVar() # Unknown value but still needed for data reading and writing
        self.voice = tk.IntVar() # Unit Voice
        self.model = tk.IntVar() # Unit Model
        self.color = tk.IntVar() # Unit Color
        self.moveset = tk.IntVar() # Unit Moveset
        self.horse = tk.IntVar() # Horse Unit uses
        self.life = tk.IntVar() # Health value
        self.attack = tk.IntVar() # Attack value
        self.defense = tk.IntVar() # Defense value
        self.bow = tk.IntVar() # Unit Bow value
        self.mounted = tk.IntVar() # Mounted value
        self.speed = tk.IntVar() # Unit Speed
        self.strafespeed = tk.IntVar() # Unit Strafespeed
        self.jump = tk.IntVar() # Unit jump height
        self.ailevel = tk.IntVar() # Unit ai level
        self.aitype = tk.IntVar() # Unit ai type
        self.unknown2 = tk.IntVar() # Unknown value but still needed for data reading and writing
        self.weapon = tk.IntVar() # Weapon model
        self.weaponlevel = tk.IntVar() # Level for the weapon
        self.orb = tk.IntVar() # Related to the orb item
        self.modname = tk.StringVar() # User mod name
        hex_values = [hex(i) for i in range(896)] # Size of the combobox while using hex values
        
        # Labels for Unit data
        self.labels = ["Name", "Voice", "Model", "Color", "Moveset", "Horse", "Life",
                       "Attack Stat", "Defense Stat", "Bow", "Mounted", "Speed", "Strafe Speed",
                       "Jump", "AI Level", "AI Type", "Weapon", "Weapon Level", "Orb"]
        

        # Entries for Unit data
        self.entry_vars = [self.name, self.voice, self.model, self.color, self.moveset, self.horse,
                           self.life, self.attack, self.defense, self.bow, self.mounted, self.speed,
                           self.strafespeed, self.jump, self.ailevel, self.aitype, self.weapon, self.weaponlevel,
                           self.orb]

        # loop for placing the labels and entries
        for i, (label_text, entry_var) in enumerate(zip(self.labels, self.entry_vars)):
            y_position = i * 40

            tk.Label(self.root, text=label_text).place(x=160, y=y_position)
            tk.Entry(self.root, textvariable=entry_var, validate="key",
                     validatecommand=(self.root.register(self.validate_numeric_input), "%P")
                    ).place(x=0, y=y_position)
        self.selected_slot = tk.IntVar(self.root) # using integer variables
        self.selected_slot.set(0)  # Default value
        slot_combobox = ttk.Combobox(self.root, textvariable=self.selected_slot, values=hex_values) # creating the combobox
        slot_combobox.bind("<<ComboboxSelected>>", self.slot_selected)
        slot_combobox.place(x=600, y=10)
        tk.Label(self.root, text="Character slot:").place(x=510, y=10) # creating label
        tk.Button(self.root, text="Submit values to .5edata file", command= self.submit_unit, height=5).place(x=600, y=250) # button for submitting values
        tk.Button(self.root, text = "Create Unit Mod", command = self.create_unit_mod, height=5, width=20).place(x=600,y=450) # button to create mod file
        mm1 = tk.Entry(self.root, textvariable = self.modname).place(x=600,y=400) # entry for accepting a mod name
        mm2 = tk.Label(self.root, text = f"Enter a mod name").place(x=490,y=400) # label
        self.unit_reading()
        self.unit_ref()
    def create_unit_mod(self): # for creating a mod file with custom extension
        sep = "." # to be used for correcting possible user filenames that have their own extension
        try:
            usermodname = self.modname.get().split(sep, 1)[0] + dw5e[3] # Create modname with the user entered name and custom extension
            with open(self.dw5e_path, "rb") as r1: # open the template file that was modded
                data = r1.read() # read the data
                with open(usermodname, "wb") as w1: # open and create the user's mod file
                    w1.write(data) # write the data
            self.status_label.config(text=f"Mod file '{usermodname}' created successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error creating mod file '{usermodname}': {str(e)}", fg="red")
    def slot_selected(self, event=None): # update display data
        self.selected_slot_value = self.selected_slot.get()
        self.unit_display(self.selected_slot_value)
    def submit_unit(self): # Submitting values to the template file
        try: # get all data for the unit slot that was modded
            col = [self.name.get().to_bytes(2, "little"), self.unknown1.get().to_bytes(1, "little"), self.voice.get().to_bytes(1, "little"),
                         self.model.get().to_bytes(1, "little"), self.color.get().to_bytes(1, "little"), self.moveset.get().to_bytes(1, "little"),
                         self.horse.get().to_bytes(1, "little"), self.life.get().to_bytes(1, "little"), self.attack.get().to_bytes(1, "little"),
                         self.defense.get().to_bytes(1, "little"), self.bow.get().to_bytes(1, "little"), self.mounted.get().to_bytes(1, "little"),
                         self.speed.get().to_bytes(1, "little"), self.strafespeed.get().to_bytes(1, "little"), self.jump.get().to_bytes(1, "little"),
                         self.ailevel.get().to_bytes(1, "little"), self.aitype.get().to_bytes(1, "little"), self.unknown2.get().to_bytes(1, "little"),
                         self.weapon.get().to_bytes(1, "little"), self.weaponlevel.get().to_bytes(1, "little"), self.orb.get().to_bytes(1, "little")]
            unit_slot = self.selected_slot.get()
            with open(self.dw5e_ref, "rb") as r1: # for obtaining the offset for a unit slot from the .ref file
                uservalue = unit_slot * 8 # get the user's selected slot and multiply by 8
                r1.seek(uservalue) # seek the offset
                getoffset = int.from_bytes(r1.read(8), "little") # convert the bytes to integer to get the offset needed to be used with the template file
                with open(self.dw5e_path, "r+b") as f1: # for updating the unit slot in the template file with the current values from col list
                    f1.seek(getoffset) # go to the offset
                    for b in col:
                        f1.write(b)
            self.status_label.config(text=f"Values submitted successfully.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
    def unit_reading(self): # Used for reading data from the iso file and creating the template file for unit data
        global getoffset # needed for other functions to access the updated value
        # search for this pattern, the reason is because different regions of this file may have different offsets
        aob_pattern = b'\x14\x14\x14\x80\x14\x14\x14\x80\x14\x14\x14\x80\x14\x14\x14\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        chunk_size = 8000  # chunk size for reading
        with open(dw5e[0], "rb") as f1: # open iso file for reading
            offset = 0
            found = False
            while not found:
                chunk = f1.read(chunk_size)
                if not chunk:
                    break
                pattern_offset = chunk.find(aob_pattern)
                if pattern_offset != -1:
                    getoffset = offset + pattern_offset + 0x3D0 # add 3D0 so that it seeks the correct offset for unit data
                    with open(self.dw5e_path, "ab") as f2: # open and create the template file
                        f1.seek(getoffset) # seek the offset for unit data
                        for i in range(0, 0x37F): # loop through all unit slots
                            unitdata1 = f1.read(22) # read the unit data
                            f2.write(unitdata1) # write the unit data
                offset += chunk_size
        if not os.path.exists(self.odw5e_path): # backup file if it doesn't exist
            shutil.copy(self.dw5e_path, self.odw5e_path)
    def unit_ref(self): # for creating the reference file
        with open(self.dw5e_path, "rb") as r1:  # Open the unit data file
            with open(self.dw5e_ref, "ab") as r2: # open and create the ref file
                offset = 0  # Initialize offset counter
                while True:
                    data_chunk = r1.read(22)  # Read a 22-byte chunk from the unit data file
                    if not data_chunk:  # Break loop if end of file is reached
                        break
                    r2.write(offset.to_bytes(8, "little"))  # Write the offset to the ref file
                    offset += 22  # Move offset to the next chunk
    def unit_display(self, selected_slot_value): # for displaying unit data in the entries
        with open(self.dw5e_ref, "rb") as r1: # open and read from the ref file
            useroffset = self.selected_slot_value # get the current selected unit slot
            uservalue = self.selected_slot_value * 8 # get the selected unit slot value and multiply by 8
            r1.seek(uservalue) # seek the offset
            getoffset = int.from_bytes(r1.read(8), "little") # convert the bytes to integer to get the offset to use for unit data file
            with open(self.dw5e_path, "r+b") as r2: # open the unit data file for reading and writing
                r2.seek(getoffset) # seek offset of the selected unit slot
                # this section is for reading the unit data(unit data is 22 bytes long for each unit)
                unitname = int.from_bytes(r2.read(2), "little")
                unk1 = int.from_bytes(r2.read(1), "little")
                unitvoice = int.from_bytes(r2.read(1), "little")
                unitmodel = int.from_bytes(r2.read(1), "little")
                unitcolor = int.from_bytes(r2.read(1), "little")
                unitmoveset = int.from_bytes(r2.read(1), "little")
                unithorse = int.from_bytes(r2.read(1), "little")
                unitlife = int.from_bytes(r2.read(1), "little")
                unitattack = int.from_bytes(r2.read(1), "little")
                unitdefense = int.from_bytes(r2.read(1), "little")
                unitbow = int.from_bytes(r2.read(1), "little")
                unitmounted = int.from_bytes(r2.read(1), "little")
                unitspeed = int.from_bytes(r2.read(1), "little")
                unitstrafespeed = int.from_bytes(r2.read(1), "little")
                unitjump = int.from_bytes(r2.read(1), "little")
                unitailevel = int.from_bytes(r2.read(1), "little")
                unitaitype = int.from_bytes(r2.read(1), "little")
                unk2 = int.from_bytes(r2.read(1), "little")
                unitweapon = int.from_bytes(r2.read(1), "little")
                unitweaponlevel = int.from_bytes(r2.read(1), "little")
                unitorb = int.from_bytes(r2.read(1), "little")
                # this section is used for setting the values read
                self.name.set(unitname)
                self.unknown1.set(unk1)
                self.voice.set(unitvoice)
                self.model.set(unitmodel)
                self.color.set(unitcolor)
                self.moveset.set(unitmoveset)
                self.horse.set(unithorse)
                self.life.set(unitlife)
                self.attack.set(unitattack)
                self.defense.set(unitdefense)
                self.bow.set(unitbow)
                self.mounted.set(unitmounted)
                self.speed.set(unitspeed)
                self.strafespeed.set(unitstrafespeed)
                self.jump.set(unitjump)
                self.ailevel.set(unitailevel)
                self.aitype.set(unitaitype)
                self.unknown2.set(unk2)
                self.weapon.set(unitweapon)
                self.weaponlevel.set(unitweaponlevel)
                self.orb.set(unitorb)
    
    def open_mod_manager(self): # open mod manager
        manager = ModManager(self.root)
        
class ModManager: # mod manager for unit mods
    def __init__(self, root):
        self.root = tk.Toplevel()
        self.root.title("DW5E Mod Manager")
        self.root.iconbitmap(os.path.join(dw5e[6], "icon3.ico"))
        self.root.minsize(400, 400)
        self.root.resizable(False, False)
        self.mod_status = tk.Label(self.root, text="", fg="green")
        self.mod_status.place(x=10, y=170)
        tk.Button(self.root, text="Enable Mod", command=self.ask_open_file, height=10, width=50).place(x=10, y=10) # button for enabling mods
        tk.Button(self.root, text="Disable Mod", command=self.ask_open_ofile, height=10, width=50).place(x=10, y=210) # button for disabling mods
    def ask_open_file(self): # This is for enabling the user selected mod
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.dw5emod;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # Apply the mod to the iso file
                with open(dw5e[0], "r+b") as f1: # open iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod file for reading
                        f1.seek(offset) # seek the offset in the iso file
                        sdata = f2.read(19690) # read the mod file's data
                        f1.write(sdata) # write the mod file's data to the iso file
                self.mod_status.config(text=f"Mod file '{os.path.basename(file_path)}' enabled successfully.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")
    def ask_open_ofile(self): # For disabling mods
        global getoffset
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select mod file",
            filetypes=(
                ("Supported Files", "*.5edata;"),
            ))
        try:
            if file_path:
                offset = getoffset # offset for unit data in the iso file
                # apply the mod disabling file to the iso file
                with open(dw5e[0], "r+b") as f1: # open the iso file for reading and writing
                    with open(file_path, "rb") as f2: # open the mod disabling file
                        f1.seek(offset) # seek offset for unit data in the iso file
                        sdata = f2.read(19690) # read the data for disabling unit mods
                        f1.write(sdata) # write the data
                self.mod_status.config(text=f"The mod that used the '{os.path.basename(file_path)}' template was disabled.", fg="green")
        except Exception as e:
            self.mod_status.config(text=f"Error: {str(e)}", fg="red")

def main():
    root = tk.Tk()
    dw5eu = MainEditor(root)
    root.mainloop()
if __name__ == "__main__":
    os.makedirs(dw5e[4], exist_ok = True) # create backups folder
    os.makedirs(dw5e[5], exist_ok = True) # create the unit folder
    os.makedirs(dw5e[6], exist_ok = True) # create the icon files folder
    rem() # clean old files
    main()
