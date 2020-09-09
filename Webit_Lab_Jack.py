import tkinter as tk
from tkinter import ttk, Spinbox,Scrollbar
from labjack import ljm
from matplotlib import pyplot as plt
from matplotlib import style

class Webit_GUI(tk.Frame):

    def __init__(self, master):
        # Initializes the frame
        tk.Frame.__init__(self, master)

        ConnectButton = tk.Button(
            self.master, text = 'Connect', command=self.Connect)
        ConnectButton.grid(row=0, column=0)

        disconnectButton = tk.Button(
            self.master, text = 'Disconnect', command=self.Disconnect)
        disconnectButton.grid(row=0, column=1)

        Get_Info_Button = tk.Button(
            self.master, text = 'Get Info', command=self.Get_Info)
        Get_Info_Button.grid(row=0, column=6)

        SetAnodeButton = tk.Button(
            self.master, text = 'Set', command=self.Set_Anode)
        SetAnodeButton.grid(row=2, column=4)

        SetDTButton = tk.Button(
            self.master, text = 'Set', command=self.Set_DT)
        SetDTButton.grid(row=1, column=4)

        QuitButton = tk.Button(
            master,
            text = 'Quit',
            command=master.quit,
            width=15
        )
        QuitButton.grid(row=0, column=4)

# I need to verify that Connect and Disconnect works before I can verify that 
# all of the entry boxes are really working properly.
# Lets make Get_Ain0 working properly first.
# Each of these will have to have a Get_Ain#, which would be included in a time 
# loop for constant read-ins. Lets start with the first one.  
        Get_AIN0_Button = tk.Button(
            self.master, text = 'Get Ain0', command=self.Get_Ain0)
        Get_AIN0_Button.grid(row=3, column=2)
        self.Get_AIN0_Entry = tk.Entry(self.master)
        self.Get_AIN0_Entry.grid(row=3, column=3)

# These are the entry boxes for the "Analog input" 
        self.Entry_1_Label = tk.Label(self.master, text="Input 1: ")
        self.Entry_1_Label.grid(row=1, column=0)
        self.Entry_1_Entry = tk.Entry(self.master)
        self.Entry_1_Entry.grid(row=1, column=1)

        self.Entry_2_Label = tk.Label(self.master, text="Input 2: ")
        self.Entry_2_Label.grid(row=2, column=0)
        self.Entry_2_Entry = tk.Entry(self.master)
        self.Entry_2_Entry.grid(row=2, column=1)

        self.Entry_3_Label = tk.Label(self.master, text="Input 3: ")
        self.Entry_3_Label.grid(row=3, column=0)
        self.Entry_3_Entry = tk.Entry(self.master)
        self.Entry_3_Entry.grid(row=3, column=1)

        self.Entry_4_Label = tk.Label(self.master, text="Input 4: ")
        self.Entry_4_Label.grid(row=4, column=0)
        self.Entry_4_Entry = tk.Entry(self.master)
        self.Entry_4_Entry.grid(row=4, column=1)

        self.Entry_5_Label = tk.Label(self.master, text="Input 5: ")
        self.Entry_5_Label.grid(row=5, column=0)
        self.Entry_5_Entry = tk.Entry(self.master)
        self.Entry_5_Entry.grid(row=5, column=1)		

        self.Entry_6_Label = tk.Label(self.master, text="Input 6: ")
        self.Entry_6_Label.grid(row=6, column=0)
        self.Entry_6_Entry = tk.Entry(self.master)
        self.Entry_6_Entry.grid(row=6, column=1)	

        self.Entry_7_Label = tk.Label(self.master, text="Input 7: ")
        self.Entry_7_Label.grid(row=7, column=0)
        self.Entry_7_Entry = tk.Entry(self.master)
        self.Entry_7_Entry.grid(row=7, column=1)

        self.Entry_8_Label = tk.Label(self.master, text="Input 8: ")
        self.Entry_8_Label.grid(row=8, column=0)
        self.Entry_8_Entry = tk.Entry(self.master)
        self.Entry_8_Entry.grid(row=8, column=1)

        self.Entry_9_Label = tk.Label(self.master, text="Input 9: ")
        self.Entry_9_Label.grid(row=9, column=0)
        self.Entry_9_Entry = tk.Entry(self.master)
        self.Entry_9_Entry.grid(row=9, column=1)

        self.Entry_10_Label = tk.Label(self.master, text="Input 10: ")
        self.Entry_10_Label.grid(row=10, column=0)
        self.Entry_10_Entry = tk.Entry(self.master)
        self.Entry_10_Entry.grid(row=10, column=1)

        self.Entry_11_Label = tk.Label(self.master, text="Input 11: ")
        self.Entry_11_Label.grid(row=11, column=0)
        self.Entry_11_Entry = tk.Entry(self.master)
        self.Entry_11_Entry.grid(row=11, column=1)

        self.Entry_12_Label = tk.Label(self.master, text="Input 12: ")
        self.Entry_12_Label.grid(row=12, column=0)
        self.Entry_12_Entry = tk.Entry(self.master)
        self.Entry_12_Entry.grid(row=12, column=1)

        self.Entry_13_Label = tk.Label(self.master, text="Input 13: ")
        self.Entry_13_Label.grid(row=13, column=0)
        self.Entry_13_Entry = tk.Entry(self.master)
        self.Entry_13_Entry.grid(row=13, column=1)

        self.Entry_14_Label = tk.Label(self.master, text="Input 14: ")
        self.Entry_14_Label.grid(row=14, column=0)
        self.Entry_14_Entry = tk.Entry(self.master)
        self.Entry_14_Entry.grid(row=14, column=1)

# Place holder. The plan is to read in the Anode and Bucking Coil above, and we
# set the values as input here. 
        self.Entry_DAC0_Label = tk.Label(self.master, text="Anode: ")
        self.Entry_DAC0_Label.grid(row=1, column=2)
        self.Entry_DAC0_Entry = tk.Entry(self.master)
        self.Entry_DAC0_Entry.grid(row=1, column=3)

        self.Entry_DAC1_Label = tk.Label(self.master, text="Bucking Coil: ")
        self.Entry_DAC1_Label.grid(row=2, column=2)
        self.Entry_DAC1_Entry = tk.Entry(self.master)
        self.Entry_DAC1_Entry.grid(row=2, column=3)

    def Connect(self):
        self.handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier

# This is a test to verify that the GUI is able to get the first Analog input 
# The other outputs can easily be added if this works. 
# This should print to the entry box next to AINO and to the terminal. 
    def Get_Ain0(self):
        # TEST# It appears that the naming is as follows from the examples, but 
        # the examples on the website look more like hte second name (AIN0)
        # name = "FIO0"
        name = "AIN0"
        result = ljm.eReadName(self.handle, name)
        print("\n%s state : %f" % (name, result))
        self.Get_AIN0_Entry.insert(0, result)

# Lets verify that reading in works. 
    def Set_Anode(self):
        print('Not Configured')
    def Set_DT(self):
        print('Not Configured')

# this should work if connect works I think
    def Disconnect(self):
        ljm.close(self.handle)
    #Prints to terminal
    def Get_Info(self):
        info = ljm.getHandleInfo(self.handle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
            "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
            (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))




if __name__ == "__main__":
    root = tk.Tk()
    root.title("WEBIT LabJack GUI")
    app = Webit_GUI(root)
    app.mainloop()
