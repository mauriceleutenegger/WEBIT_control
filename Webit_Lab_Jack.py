import tkinter as tk
from tkinter import ttk, Spinbox,Scrollbar
from labjack import ljm
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time

class Webit_GUI(tk.Frame):

    def __init__(self, master):

        self.IsConnected = False # should make an indicator for this
        self.handle = None # placeholder

        # Set the file name based on the start time. 
        # Currently using time since lest epoch. Other times might be neater.
        self.startTime = time.time()
        # self.AIN_FNAME = 'AIN_File{}.dat'.format(self.startTime)
        # self.AIN_REAL_FNAME = 'AIN_REAL_File{}.dat'.format(self.startTime)
        # While testing- use basic file name.
        self.AIN_FNAME = 'AIN_File.dat'
        self.AIN_REAL_FNAME = 'AIN_REAL_File.dat'


        # Initializes the frame
        tk.Frame.__init__(self, master)

        ConnectButton = tk.Button(
            self.master, text = 'Connect', command=self.Connect)
        ConnectButton.grid(row=0, column=0)

        disconnectButton = tk.Button(
            self.master, text = 'Disconnect', command=self.Disconnect)
        disconnectButton.grid(row=0, column=1)

        SetAnodeButton = tk.Button(
            self.master, text = 'Set Anode (kV)', command=self.Set_Anode)
        SetAnodeButton.grid(row=1, column=5)

        SetIBuckButton = tk.Button(
            self.master, text = 'Set I_Buck (A)', command=self.Set_IBuck)
        SetIBuckButton.grid(row=2, column=5)

        QuitButton = tk.Button(
            master,
            text = 'Quit',
            command=master.quit,
            width=15
        )
        QuitButton.grid(row=0, column=10)

        PlotButton = tk.Button(
            master,
            text = 'Plot',
            command=self.Plot,
            width=15
        )
        PlotButton.grid(row=0, column=9)
        # make an indicator to show if we are connected
        canvas_y = 18
        self.ConnectedCanvas = tk.Canvas (self.master, width=150, height=30)
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


        # add a ticker to indicate aliveness
        self.tick_value = 0
        self.TickerVar = tk.StringVar ()
        self.TickerVar.set (self.tick_value)
        self.TickerLabel = \
            tk.Label (self.master, textvariable=self.TickerVar)
        self.TickerLabel.grid (row=0,column=3,sticky=tk.W)
        self.UpdateTicker ()
        
        # make a list of AIN values, initialize to zero, and also corresponding real measured numbers
        self.AIN = []
        self.AIN_Real = []
        self.AIN_Update = []
        self.AIN_Real_Update = []
        for i in range (14) :
            self.AIN.append (0.)
            self.AIN_Real.append (0.)
            self.AIN_Update.append (0.)
            self.AIN_Real_Update.append (0.)

        # make a list of StringVars to feed to the label widgets 
        self.AIN_Var = []
        self.AIN_Real_Var = []
        for i in range (14) :
            self.AIN_Var.append (tk.StringVar ())
            self.AIN_Real_Var.append (tk.StringVar ())
        # initialize
        self.UpdateAIN_Vars ()
            
        # make output fields for AIN values using tk.Label
        self.AIN_Output_Label = [] # labels for AIN channels
        self.AIN_Output = [] # AIN values in V
        self.AIN_Real_Output_Label = [] # labels for "Real" values
        self.AIN_Real_Output = [] # corresponding "Real" parameter values
        self.AIN_Real_Names = ['Anode (kV)', 'Ibuck (A)',
                             'Pegun (torr)', 'Ptop (torr)', 'Pinj (torr)',
                             'Ianode (uA)', 'N/A', 'N/A',
                             'VMDT (kV)', 'N/A', 'N/A',
                             'N/A', 'N/A', 'N/A']
        for i in range (14) :
            row = i+1
            self.AIN_Output_Label.append (
                tk.Label (self.master, text='AIN{} (V):'.format (i)))
            self.AIN_Output.append (
                tk.Label (self.master, textvariable=self.AIN_Var[i]))
            self.AIN_Output_Label[i].grid (row=row, column=0, sticky=tk.W)
            self.AIN_Output[i].grid (row=row, column=1, sticky=tk.W)
            self.AIN_Real_Output_Label.append (
                tk.Label (self.master, text=self.AIN_Real_Names[i]+":"))
            self.AIN_Real_Output.append (
                tk.Label (self.master, textvariable=self.AIN_Real_Var[i]))
            self.AIN_Real_Output_Label[i].grid (row=row, column=2, sticky=tk.W)
            self.AIN_Real_Output[i].grid (row=row, column=3, sticky=tk.W)
            
        self.master.after (1000, self.UpdateAIN)


        # entries for DAC0 and DAC1
        self.DAC_volts = []
        for i in range (2) :
            self.DAC_volts.append (0.)
        # corresponding values for the actual numbers
        self.VAnode_setting = 0.
        self.IBuck_setting = 0.

        # stringvars for DACs and corresponding real numbers
        self.DAC0_Var = tk.StringVar ()
        self.DAC1_Var = tk.StringVar ()
        self.VAnode_Var = tk.StringVar ()
        self.IBuck_Var = tk.StringVar ()
        self.DAC0_Var.set (0.)
        self.DAC1_Var.set (0.)
        self.VAnode_Var.set (0.)
        self.IBuck_Var.set (0.)
        
        # set up the entry boxes and reporting
        self.DAC0_Entry = tk.Entry(self.master, width=5)
        self.DAC0_Entry.grid(row=1, column=4)
        self.DAC0_Entry.insert ('end', 0) # default value
        #self.DAC_volts[0] = float (self.DAC0_Entry.get ())
        self.DAC0_Limit_Label = tk.Label (self.master, text='Allowed range: 0-5 kV')
        self.DAC0_Limit_Label.grid (row=1, column=10, sticky=tk.W)
        # reporting
        self.VAnode_Value_Label = tk.Label (self.master, text='VAnode (kV):')
        self.VAnode_Value_Label.grid (row=1, column=6, sticky=tk.W)
        self.VAnode_Value = tk.Label (self.master, textvariable=self.VAnode_Var)
        self.VAnode_Value.grid (row=1, column=7, sticky=tk.W)
        self.DAC0_Value_Label = tk.Label (self.master, text='DAC0 (V):')
        self.DAC0_Value_Label.grid (row=1, column=8, sticky=tk.W)
        self.DAC0_Value = tk.Label (self.master, textvariable=self.DAC0_Var)
        self.DAC0_Value.grid (row=1, column=9, sticky=tk.W)

        
        self.DAC1_Entry = tk.Entry(self.master, width=5)
        self.DAC1_Entry.grid(row=2, column=4)
        self.DAC1_Entry.insert ('end', 0) # default value
        self.DAC_volts[1] = float (self.DAC1_Entry.get ())
        self.DAC1_Limit_Label = tk.Label (self.master, text='Allowed range: 0-10 A')
        self.DAC1_Limit_Label.grid (row=2, column=10, sticky=tk.W)
        # reporting
        self.IBuck_Value_Label = tk.Label (self.master, text='IBuck (A):')
        self.IBuck_Value_Label.grid (row=2, column=6, sticky=tk.W)
        self.IBuck_Value = tk.Label (self.master, textvariable=self.IBuck_Var)
        self.IBuck_Value.grid (row=2, column=7, sticky=tk.W)
        self.DAC1_Value_Label = tk.Label (self.master, text='DAC1 (V):')
        self.DAC1_Value_Label.grid (row=2, column=8, sticky=tk.W)
        self.DAC1_Value = tk.Label (self.master, textvariable=self.DAC1_Var)
        self.DAC1_Value.grid (row=2, column=9, sticky=tk.W)

        # heading for current settings
        self.CurrentSettingsLabel = tk.Label (self.master, text='Current settings:')
        self.CurrentSettingsLabel.grid (row=0, column=6, sticky=tk.W)

        # broaden some of the columns for formatting
        self.master.grid_columnconfigure(7, minsize=50)
        self.master.grid_columnconfigure(8, minsize=100)
        self.master.grid_columnconfigure(9, minsize=50)
        
        # make fields for serial number etc. :

        # These are centered, but maybe left justified would be better...
        
        self.SerialNumber = 0
        self.SerialNumber_Var = tk.StringVar ()
        self.SerialNumber_Label = tk.Label (self.master, text='Serial Number')
        self.SerialNumber_Label.grid (row=5, column=5, sticky=tk.W)
        self.SerialNumber_Output = tk.Label(self.master, textvariable=self.SerialNumber_Var, justify=tk.LEFT)
        self.SerialNumber_Output.grid (row=5, column=6, sticky=tk.W)

        self.IPaddress = '0.0.0.0'
        self.IPaddress_Var = tk.StringVar ()
        self.IPaddress_Label = tk.Label (self.master, text='IP address')
        self.IPaddress_Label.grid (row=6, column=5, sticky=tk.W)
        self.IPaddress_Output = tk.Label(self.master, textvariable=self.IPaddress_Var)
        self.IPaddress_Output.grid (row=6, column=6, sticky=tk.W)

        self.Port = 0
        #self.Port_Var = tk.StringVar ()
        #self.Port_Output = tk.Label(self.master, textvariable=self.Port_Var)
        #self.Port_Output.grid (row=7, column=2, sticky='w')

        self.DeviceType = -1
        self.DeviceType_Var = tk.StringVar ()
        self.DeviceType_Label = tk.Label (self.master, text='Device Type')
        self.DeviceType_Label.grid (row=7, column=5, sticky=tk.W)
        self.DeviceType_Output = tk.Label(self.master, textvariable=self.DeviceType_Var)
        self.DeviceType_Output.grid (row=7, column=6, sticky=tk.W)

        self.ConnectionType = -1
        self.ConnectionType_Var = tk.StringVar ()
        self.ConnectionType_Label = tk.Label (self.master, text='Connection Type')
        self.ConnectionType_Label.grid (row=8, column=5, sticky=tk.W)
        self.ConnectionType_Output = tk.Label(self.master, textvariable=self.ConnectionType_Var)
        self.ConnectionType_Output.grid (row=8, column=6, sticky=tk.W)

        self.MaxBytesPerMB = 0
        self.MaxBytesPerMB_Var = tk.StringVar ()
        self.MaxBytesPerMB_Label = tk.Label (self.master, text='Max bytes per MB')
        self.MaxBytesPerMB_Label.grid (row=9, column=5, sticky=tk.W)
        self.MaxBytesPerMB_Output = tk.Label (self.master, textvariable=self.MaxBytesPerMB_Var)
        self.MaxBytesPerMB_Output.grid (row=9, column=6, sticky=tk.W)

        # add a field for error handling
        self.ErrorText = "N/A"
        self.Error_Var = tk.StringVar ()
        self.Error_Var.set ("---")
        self.Error_Label = tk.Label (self.master, textvariable=self.Error_Var)
        self.Error_Label.grid (row=11, column=5, columnspan=4, rowspan=3,
                               sticky=tk.W)
        self.UpdateErrorText ()
        
        self.UpdateInfo ()

# PLOTTING #####################################################################
        # Here we set up the plot, in the animate function we update the plot. 
        # Currently updating every 1 s.
        # Update interval set in MAIN when GUI is created. 
        # animation is created in main. 

        self.Ain_fig = plt.figure("WEBIT Parameters")
        animation.FuncAnimation(self.Ain_fig, self.animate_init, interval=1000, blit=False)


# PLOTTING #####################################################################
        
    def Connect(self):
        self.animate()     #plot once connected. 

        try:
            self.handle = ljm.openS("T7", "ANY", "ANY")
            # T7 device, Any connection, Any identifier
        except ljm.LJMError :
            self.ErrorText =\
                "LJM error while connecting - check if device is connected"
            self.UpdateErrorText ()
            return
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
            self.AIN_Var[i].set ("{:.3f}".format (self.AIN[i]))
        for i in range (14):
            self.AIN_Real_Var[i].set ("{:.3f}".format(self.AIN_Real[i]))
            # self.AIN_Real[0] = self.startTime-time.time()
        
            
    def UpdateInfo (self) :
        # connection types
        #LJM_ctANY (0), LJM_ctUSB (1), LJM_ctTCP (2), LJM_ctETHERNET (3), LJM_ctWIFI (4)
        CT_string_list = ['ANY', 'USB', 'TCP', 'ETHERNET', 'WIFI']
        CT_string = 'NONE'
        if self.ConnectionType > -1 :
            CT_string = CT_string_list[self.ConnectionType]
        self.SerialNumber_Var.set (self.SerialNumber)
        self.IPaddress_Var.set ("{}:{}".format (self.IPaddress, self.Port))
        self.DeviceType_Var.set (self.DeviceType)
        self.ConnectionType_Var.set ("{} ({})".format (self.ConnectionType, CT_string))
        self.MaxBytesPerMB_Var.set (self.MaxBytesPerMB)
        

    def Set_Anode(self) :
        if not self.IsConnected :
            self.ErrorText = "Not connected, not setting Anode."
            self.UpdateErrorText ()
            return
        DAC0_Entry_String = self.DAC0_Entry.get () # read value from entry field
        self.VAnode_setting = 0. # placeholder
        # check if it is a number
        try :
            self.VAnode_setting = float (DAC0_Entry_String)
        except ValueError :
            self.ErrorText = "Error getting entry for DAC0, value was {}".format (DAC0_Entry_String)
            self.UpdateErrorText ()
            return
        # enforce limits on VAnode
        if self.VAnode_setting > 5. :
            self.ErrorText = "Can't set Anode voltage {} > 5. kV".format (self.VAnode_setting) # limit of 5 kV based on Bertan supply
            self.UpdateErrorText ()
            return
        if self.VAnode_setting < 0. :
            self.ErrorText = "Can't set Anode volts {} < 0. kV".format (self.VAnode_setting)
            self.UpdateErrorText ()
            return
        self.DAC_volts[0] = self.VAnode_setting # conversion is 1 V remote per 1 kV on anode
        ljm.eWriteName(self.handle, "DAC0", self.DAC_volts[0])
        # update reporting
        self.DAC0_Var.set ("{:.3f}".format (self.DAC_volts[0]))
        self.VAnode_Var.set ("{:.3f}".format (self.VAnode_setting))
        return

    # need to set limit once we have the conversion for Ibuck
    # the conversion is that 1 V corresponds to the maximum value of I which is 10 A
    # we may want to have a more stringent limit on current
    # typical actual value for WEBIT is 5-6 A
    def Set_IBuck(self):
        if not self.IsConnected :
            self.ErrorText = "Not connected, not setting IBuck."
            self.UpdateErrorText ()
            return
        DAC1_Entry_String = self.DAC1_Entry.get () # read value from entry field
        self.IBuck_setting = 0. # placeholder
        # check if it is a number
        try :
            self.IBuck_setting = float (DAC1_Entry_String)
        except ValueError :
            self.ErrorText = "Error getting entry for DAC1, value was {}".format (DAC1_Entry_String)
            self.UpdateErrorText ()
            return
        # enforce limits on Ibuck
        if self.IBuck_setting > 10. :
            self.ErrorText = "Can't set IBuck current {} > 10. A".format (self.IBuck_setting)
            self.UpdateErrorText ()
            return
        if self.IBuck_setting < 0. :
            self.ErrorText = "Can't set IBuck current {} < 0. A".format (self.IBuck_setting)
            self.UpdateErrorText ()
            return
        self.DAC_volts[1] = 0.1 * self.IBuck_setting # conversion is 1 V = 10 A (max)        
        ljm.eWriteName(self.handle, "DAC1", self.DAC_volts[1])
        # update reporting
        self.DAC1_Var.set ("{:.3f}".format(self.DAC_volts[1]))
        self.IBuck_Var.set ("{:.3f}".format (self.IBuck_setting))
        return

    def Disconnect(self):
        if self.IsConnected :
            ljm.close(self.handle)
        self.IsConnected = False

    def UpdateAIN (self):
        #print ("Updating AIN")
        if self.IsConnected :
            #print ("Reading")
            numFrames = 14
            names = ['AIN0', 'AIN1', 'AIN2', 'AIN3', 'AIN4', 'AIN5', 'AIN6',
                     'AIN7', 'AIN8', 'AIN9', 'AIN10', 'AIN11', 'AIN12', 'AIN13']
            self.AIN = ljm.eReadNames (self.handle, numFrames, names)
            #print (self.AIN)
            self.UpdateMonitorValues ()
            self.UpdateAIN_Vars ()
        self.Update_Data_File()     
        self.master.after (1000, self.UpdateAIN)
        

    def UpdateStatus (self):
        #print ("Updating Status")
        if self.IsConnected :
            self.LEDcolor = "green"
        else :
            self.LEDcolor = "red"
        self.ConnectedCanvas.itemconfig(self.ConnectedLED, fill=self.LEDcolor)
        self.ConnectedCanvas.after (1000, self.UpdateStatus)


    #The Bertan HV supplies use the following conversions:
    #current monitor: 1 V = 100 microAmp
    #Voltage monitor: 1V = 1 kV
    # Terranova 921 conversion, V in Volts
    #P = 10^-10 * 10**(2V) Torr
    # kepco supply (bucking coil) is 1 V at full current (10A)
    def UpdateMonitorValues (self):
        self.AIN_Real[0] = self.AIN[0]         # AIN0: Vanode monitor
        self.AIN_Real[1] = self.AIN[1] * 10.0   # AIN1: Ibuck monitor
        self.AIN_Real[2] = self.ConvertPressure (self.AIN[2]) # Pegun (torr)
        self.AIN_Real[3] = self.ConvertPressure (self.AIN[3]) # Ptop (torr)
        self.AIN_Real[4] = self.ConvertPressure (self.AIN[4]) # Pinj (torr)
        self.AIN_Real[5] = self.AIN[5] * 100. # Ianode (microamp)
        # need to add conversions to these
        #self.Icath = self.AIN[6]
        #self.Icoll = self.AIN[7]
        self.AIN_Real[8] = self.AIN[8] # VMDT (kV)


    # Append time to Ain_Real and AIN in new list, and save as string. 
    # Call "write_AIN_Data" fucntion to write to file. 
    # New list is sent to "animate" function for plotting.
    def Update_Data_File(self):
        Current_time = time.time()
        self.AIN_Update = self.AIN.copy()
        self.AIN_Update.insert(0, Current_time)

        self.AIN_Real_Update = self.AIN_Real.copy()
        self.AIN_Real_Update.insert(0, Current_time)
        self.Write_AIN_Data()

    def Write_AIN_Data(self):
        AIN_Update_str = ','.join(str(i) for i in self.AIN_Update)
        AIN_Real_Update_str = ','.join(str(i) for i in self.AIN_Real_Update)

        with open(self.AIN_FNAME, "a") as self.Ain_File:
            self.Ain_File.write(AIN_Update_str + "\n")

        with open(self.AIN_REAL_FNAME, "a") as self.Real_Ain_File:
            self.Real_Ain_File.write(AIN_Real_Update_str + "\n")

#   Animate the GUI Anode Volatage. 
    # def animate(self,i):
    #     xar.append(self.AIN_Real_Update[0])
    #     yarAnode.append(self.AIN_Real_Update[1])
    #     yarIbuck.append(self.AIN_Real_Update[2])

    #     self.line.set_data(xar, yarAnode)
    #     self.ax.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

    def Plot(self):
        # self.Ain_fig = plt.figure("WEBIT Parameters")
        # animation.FuncAnimation(self.Ain_fig, self.animate_init, interval=1000, blit=False)
        self.animate()

#   Animate the Fig window including Ain0-6.
#   The X-axis limit is updated here in set_xlim
#   The data is updated in set_data.
#   The (x and y) data is first appended to arrays.
#   These arrays are initialated in MAIN- required for the animation. 
#   Note that the first element in the Ain_Real_Updatee is Time, so each Ain 
#   index # is increased by 1. 
    def animate_init(self,i):
        xarrTime.append(self.AIN_Real_Update[0])

        yarrAnode.append(self.AIN_Real_Update[1])
        yarrIbuck.append(self.AIN_Real_Update[2])
        yarrpegun.append(self.AIN_Real_Update[3])
        yarrptop.append(self.AIN_Real_Update[4])
        yarrpinj.append(self.AIN_Real_Update[5])
        yarrianode.append(self.AIN_Real_Update[6])

        self.line1.set_data(xarrTime, yarrAnode)
        self.ax1.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.line2.set_data(xarrTime, yarrIbuck)
        self.ax2.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.line3.set_data(xarrTime, yarrpegun)
        self.ax3.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.line4.set_data(xarrTime, yarrptop)
        self.ax4.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.line5.set_data(xarrTime, yarrpinj)
        self.ax5.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.line6.set_data(xarrTime, yarrianode)
        self.ax6.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)
    
#   Here, the Figure window is initialated.  Right now this is called in "Connected"
#   The Y- limits need to be updated here. They could possibly be animated in
#   "animate_init"
    def animate(self):
        # self.ax1.set_xlim(self.startTime, self.AIN_Real_Update[0]+1)

        self.ax1 = self.Ain_fig.add_subplot(3,2,1)
        self.ax1.set_ylim(-1, 10) # Note: Modify for correct limits. 
        # self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Anode Voltage (kV)')
        self.line1, = self.ax1.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[1])

        self.ax2 = self.Ain_fig.add_subplot(3,2,2)
        self.ax2.set_ylim(-1, 10) # Note: Modify for correct limits. 
        # self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Bucking Coil (A)')
        self.line2, = self.ax2.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[2])

        self.ax3 = self.Ain_fig.add_subplot(3,2,3)
        # self.ax3.set_ylim(0.0e-10, 0.0e-4) # Note: Modify for correct limits. 
        # self.ax3.set_xlabel('Time (s)')
        # self.ax3.set_yscale('log')
        self.ax3.set_ylabel('Pegun (torr')
        self.line3, = self.ax3.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[3])
        self.line3.set_label('Pegun')

        # self.line4, = self.ax3.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[4])
        # self.line4.set_label('Ptop')

        # self.line6, = self.ax3.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[6])
        # self.line6.set_label('Pinj')

        self.ax4 = self.Ain_fig.add_subplot(3,2,4)
        # self.ax4.set_ylim(-1, 10) # Note: Modify for correct limits. 
        self.ax4.set_xlabel('Time (s)')
        self.ax4.set_ylabel('Pinj (torr)')
        self.line4, = self.ax4.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[4])

        self.ax5 = self.Ain_fig.add_subplot(3,2,5)
        self.ax5.set_ylim(-1, 10) # Note: Modify for correct limits. 
        
        self.ax5.set_xlabel('Time (s)')
        self.ax5.set_ylabel('I Anode(uA)')
        self.line5, = self.ax5.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[5])

        self.ax6 = self.Ain_fig.add_subplot(3,2,6)
        # self.ax6.set_ylim(-1, 10) # Note: Modify for correct limits. 
        self.ax6.set_xlabel('Time (s)')
        self.ax6.set_ylabel('Ptop (torr)')
        self.line6, = self.ax6.plot(self.AIN_Real_Update[0], self.AIN_Real_Update[6])


        self.Ain_fig.subplots_adjust(hspace=.5,wspace = 0.3)
        plt.legend()
        self.Ain_fig.show()

    def ConvertPressure (self, v) : 
        return 1.e-10 * 10.**(2. * v) # torr
        
        
    def UpdateTicker (self) :
        self.tick_value += 1
        self.TickerVar.set ("Tick:\t{}".format (self.tick_value))
        self.master.after (1000, self.UpdateTicker)
        return

    def UpdateErrorText (self) :
        print (self.ErrorText) # print to command line, serves as a log
        self.Error_Var.set ("Most recent error: {}".format(self.ErrorText))
    
if __name__ == "__main__":
    
    yarAnode = []
    yarIbuck = []  

    xar = []   
    yar = []
    xarrTime = []
    yarrAnode = []
    yarrIbuck = []
    yarrpegun = []
    yarrptop = []
    yarrpinj = []
    yarrianode = []
    root = tk.Tk()
    root.title("WEBIT LabJack T7 GUI")
    app = Webit_GUI(root)
    # GUI Plot
    # ani = animation.FuncAnimation(app.fig, app.animate, interval=1000, blit=False)
    # Separate Plot Window
    ani_AIN = animation.FuncAnimation(app.Ain_fig, app.animate_init, interval=1000, blit=False)

    app.mainloop()

# TODO

# Renata: add logging (need to record time - figure out best scheme)
        #Time since last epoch works, but might not be clean. 


# change "UpdateStatus" to only update on connect or disconnect instead of every second

# zero out device info on disconnect and also AIN values

# assign the rest of the AIN channels and add conversions

# make a "clear error" button

# Renata: Plotting: 
    # Allow modifyication of axes.
        # Possibly plot for a specific range, and allow the x-axis to be modified.
        # update y-axes for apprpriate values
    # Only allows opening the figure window first time it is connected- possibly 
        # an easy fix.
    # Need appropriate y- range, or alllow the y-axis to vary based on current values.
    # Do we want 12 plots? 
    # Can we save the zoomed X-axis? 









