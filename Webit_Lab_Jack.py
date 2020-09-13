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

        SetIBuckButton = tk.Button(
            self.master, text = 'Set', command=self.Set_IBuck)
        SetIBuckButton.grid(row=1, column=4)

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

        # make a list of AIN values, initialize to zero
        self.AIN = []
        for i in range (14) :
            self.AIN.append (0.)

        # make a list of StringVars to feed to the label widgets 
        self.AIN_Var = []
        for i in range (14) :
            self.AIN_Var.append (tk.StringVar ())
            #self.AIN_Var[i].set (self.AIN[i])
            
        # initialize
        self.UpdateAIN_Vars ()
            
        #Get_AIN0_Button = tk.Button(
        #    self.master, text = 'Get Ain0', command=self.Get_Ain0)
        #Get_AIN0_Button.grid(row=3, column=2)
        #self.Get_AIN0_Entry = tk.Entry(self.master)
        #self.Get_AIN0_Entry.grid(row=3, column=3)

        # make output fields for AIN values using tk.Label
        self.AIN_Output = []
        for i in range (14) :
            self.AIN_Output.append (tk.Label (self.master, textvariable=self.AIN_Var[i]))
            self.AIN_Output[i].grid (row=[i+1], column=0)

        self.master.after (1000, self.UpdateAIN)
        
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

        self.MaxBytesPerMB = 0
        self.MaxBytesPerMB_Var = tk.StringVar ()
        self.MaxBytesPerMB_Output = tk.Label (self.master, textvariable=self.MaxBytesPerMB_Var)
        self.MaxBytesPerMB_Output.grid (row=10, column=2)
        
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
        self.MaxBytesPerMB = info[5]
        self.UpdateInfo ()

    def UpdateAIN_Vars (self) :
        for i in range (14) :
            self.AIN_Var[i].set ("AIN{}:\t{:.2f}".format (i, self.AIN[i]))
        
    def UpdateInfo (self) :
        self.SerialNumber_Var.set ("Serial Number {}".format (self.SerialNumber))
        self.IPaddress_Var.set ("IP address {}".format (self.IPaddress))
        self.Port_Var.set ("Port {}".format (self.Port))
        self.DeviceType_Var.set ("DeviceType {}".format (self.DeviceType))
        self.ConnectionType_Var.set ("Connection Type {}".format (self.ConnectionType))
        self.MaxBytesPerMB_Var.set ("Max Bytes Per MB {}".format (self.MaxBytesPerMB))
        
    # This is a test to verify that the GUI is able to get the first Analog input 
    # The other outputs can easily be added if this works. 
    # This should print to the entry box next to AINO and to the terminal. 
    #def Get_Ain0(self):
        # TEST# It appears that the naming is as follows from the examples, but 
        # the examples on the website look more like hte second name (AIN0)
        # name = "FIO0"
        #name = "AIN0"
        #result = ljm.eReadName(self.handle, name)
        #print("\n%s state : %f" % (name, result))
        #self.Get_AIN0_Entry.insert(0, result)

    # Lets verify that reading in works. 
    def Set_Anode(self):
        print('Not Configured')
    def Set_IBuck(self):
        print('Not Configured')

    def Disconnect(self):
        if self.IsConnected :
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
            #print ("Reading")
            numFrames = 14
            names = ['AIN0', 'AIN1', 'AIN2', 'AIN3', 'AIN4', 'AIN5', 'AIN6',
                     'AIN7', 'AIN8', 'AIN9', 'AIN10', 'AIN11', 'AIN12', 'AIN13']
            self.AIN = ljm.eReadNames (self.handle, numFrames, names)
            #print (self.AIN)
            self.UpdateAIN_Vars ()
        self.master.after (1000, self.UpdateAIN)

    def UpdateStatus (self):
        #print ("Updating Status")
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
# assign channels and add conversions
# print converted values
# add setting DAC
# test DAC by tying to AIN0 with a wire
# add error handling for connect (and disconnect?)
# add logging (need to record time - figure out best scheme)
# add plotting
# print info on connection type

# connection types
#LJM_ctANY (0), LJM_ctUSB (1), LJM_ctTCP (2), LJM_ctETHERNET (3), LJM_ctWIFI (4)


# make formatting better

