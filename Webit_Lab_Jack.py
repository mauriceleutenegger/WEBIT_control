import tkinter as tk
from tkinter import ttk, Spinbox,Scrollbar
from labjack import ljm
from matplotlib import pyplot as plt
from matplotlib import style

class Webit_GUI(tk.Frame):

    def __init__(self, master):

        self.IsConnected = False # should make an indicator for this
        self.handle = None # placeholder

        # Initializes the frame
        tk.Frame.__init__(self, master)

        ConnectButton = tk.Button(
            self.master, text = 'Connect', command=self.Connect)
        ConnectButton.grid(row=0, column=0)

        disconnectButton = tk.Button(
            self.master, text = 'Disconnect', command=self.Disconnect)
        disconnectButton.grid(row=0, column=1)

        #Get_Info_Button = tk.Button(
        #    self.master, text = 'Get Info', command=self.Get_Info)
        #Get_Info_Button.grid(row=0, column=6)

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

        # make an indicator to show if we are connected
        canvas_y = 18
        self.ConnectedCanvas = tk.Canvas (self.master, width=300, height=30)
        self.ConnectedCanvas.create_text (50,canvas_y,text='Connected')
        self.ConnectedCanvas.grid (row=0, column=2)
        self.LEDcolor = 'red'
        button_r = 10
        button_y0 = canvas_y - button_r
        button_y1 = canvas_y + button_r
        button_x = 105
        button_x0 = button_x - button_r
        button_x1 = button_x + button_r
        self.ConnectedLED = self.ConnectedCanvas.create_oval(button_x0,button_y0,button_x1,button_y1, fill=self.LEDcolor)
        self.ConnectedCanvas.after (1000, self.UpdateStatus)

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

        self.AIN14 = 0.
        self.AIN14_Var = tk.StringVar ()
        #self.AIN14_Var.set ("AIN14:\t{:.2f}".format (0.))
        #
        self.UpdateAIN_Vars
        self.AIN14_Output = tk.Label(self.master, textvariable=self.AIN14_Var)
        self.AIN14_Output.grid(row=14, column=0)
        self.AIN14_Output.after (1000, self.UpdateAIN)

        
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

        # make fields for serial number etc. :

        # These are centered, but maybe left justified would be better...
        
        self.SerialNumber = 0
        self.SerialNumber_Var = tk.StringVar ()
        self.SerialNumber_Output = tk.Label(self.master, textvariable=self.SerialNumber_Var)
        self.SerialNumber_Output.grid (row=5, column=2)

        self.IPaddress = '0.0.0.0'
        self.IPaddress_Var = tk.StringVar ()
        self.IPaddress_Output = tk.Label(self.master, textvariable=self.IPaddress_Var)
        self.IPaddress_Output.grid (row=6, column=2)

        self.Port = 0
        self.Port_Var = tk.StringVar ()
        self.Port_Output = tk.Label(self.master, textvariable=self.Port_Var)
        self.Port_Output.grid (row=7, column=2)

        self.DeviceType = -1
        self.DeviceType_Var = tk.StringVar ()
        self.DeviceType_Output = tk.Label(self.master, textvariable=self.DeviceType_Var)
        self.DeviceType_Output.grid (row=8, column=2)

        self.ConnectionType = -1
        self.ConnectionType_Var = tk.StringVar ()
        self.ConnectionType_Output = tk.Label(self.master, textvariable=self.ConnectionType_Var)
        self.ConnectionType_Output.grid (row=9, column=2)

        self.UpdateInfo ()

        
    def Connect(self):
        self.handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier
        self.IsConnected = True
        info = ljm.getHandleInfo(self.handle)
        self.DeviceType = info[0]
        self.ConnectionType = info[1]
        self.SerialNumber = info[2]
        self.IPaddress = ljm.numberToIP(info[3])
        self.Port = info[4]
        self.UpdateInfo ()

    def UpdateAIN_Vars (self) :
        self.AIN14_Var.set ("AIN14:\t{:.2f}".format (self.AIN14))
        
    def UpdateInfo (self) :
        self.SerialNumber_Var.set ("Serial Number {}".format (self.SerialNumber))
        self.IPaddress_Var.set ("IP address {}".format (self.IPaddress))
        self.Port_Var.set ("Port {}".format (self.Port))
        self.DeviceType_Var.set ("DeviceType {}".format (self.DeviceType))
        self.ConnectionType_Var.set ("Connection Type {}".format (self.ConnectionType))
                           
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
        self.IsConnected = False
        
    #Prints to terminal
    #def Get_Info(self):
    #    info = ljm.getHandleInfo(self.handle)
    #    print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
    #        "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
    #        (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    def UpdateAIN (self):
        print ("Updating AIN")
        if self.IsConnected :
            print ("Reading")
            name = "AIN14"
            self.AIN14 = ljm.eReadName(self.handle, name)
            print (self.AIN14)
            #print (result)
            #self.AIN14_Var.set ("AIN14:\t{:.2f}".format (result))
            self.UpdateAIN_Vars ()
        self.AIN14_Output.after (1000, self.UpdateAIN)

    def UpdateStatus (self):
        print ("Updating Status")
        if self.IsConnected :
            self.LEDcolor = "green"
        else :
            self.LEDcolor = "red"
        self.ConnectedCanvas.itemconfig(self.ConnectedLED, fill=self.LEDcolor)
        self.ConnectedCanvas.after (1000, self.UpdateStatus)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("WEBIT LabJack T7 GUI")
    app = Webit_GUI(root)
    app.mainloop()

# TODO
# make connected indicator
# make updater for all AIN
# add error handling for connect (and disconnect?)
# add error handling for getinfo if not connected?


# connection types
#LJM_ctANY (0), LJM_ctUSB (1), LJM_ctTCP (2), LJM_ctETHERNET (3), LJM_ctWIFI (4)


# make formatting better

# change AIN variable storage to be a list instead of individually named/numbered variables
# see what else can be converted to a list instead of  numbered
